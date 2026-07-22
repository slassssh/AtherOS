import psutil
from typing import Any, Dict, List, Optional
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import (
    QComboBox,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPlainTextEdit,
    QPushButton,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from backend.app.core.engine import Engine
from backend.app.events.types import SystemEvent


# ----------------------------------------------------
# 1. Dashboard View
# ----------------------------------------------------
class DashboardView(QWidget):
    def __init__(self, engine: Engine):
        super().__init__()
        self.engine = engine
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("AtherOS System Dashboard")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #38bdf8;")
        layout.addWidget(title)

        # Telemetry Card Grid
        grid_layout = QHBoxLayout()

        self.cpu_card = self._create_card("CPU Load", "0.0 %")
        self.ram_card = self._create_card("RAM Usage", "0.0 GB")
        self.agents_card = self._create_card("Active Agents", "8 Agents")
        self.memory_card = self._create_card("Memory Items", "0 Items")
        self.graph_card = self._create_card("Knowledge Nodes", "0 Nodes")

        grid_layout.addWidget(self.cpu_card)
        grid_layout.addWidget(self.ram_card)
        grid_layout.addWidget(self.agents_card)
        grid_layout.addWidget(self.memory_card)
        grid_layout.addWidget(self.graph_card)

        layout.addLayout(grid_layout)

        # Overview Table
        box = QGroupBox("System Subsystems Status")
        box_layout = QVBoxLayout(box)

        self.status_table = QTableWidget(6, 3)
        self.status_table.setHorizontalHeaderLabels(["Subsystem", "Provider / Interface", "Status"])
        self.status_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        subsystems = [
            ("Core Engine", "AtherOS Engine (Stateless)", "OPERATIONAL"),
            ("Autonomous Multi-Agent Runtime", "8 Specialized Production Agents", "ACTIVE"),
            ("Enterprise Memory Manager", "7-Layer Memory Manager", "ONLINE"),
            ("Context Engine", "Native Knowledge Graph", "ONLINE"),
            ("Security Hardening", "ToolSandbox & PermissionManager", "ENFORCED"),
            ("System Event Bus", "Pub/Sub Nervous System", "ACTIVE"),
        ]

        for i, (name, prov, st) in enumerate(subsystems):
            self.status_table.setItem(i, 0, QTableWidgetItem(name))
            self.status_table.setItem(i, 1, QTableWidgetItem(prov))
            item = QTableWidgetItem(st)
            item.setForeground(Qt.GlobalColor.green)
            self.status_table.setItem(i, 2, item)

        box_layout.addWidget(self.status_table)
        layout.addWidget(box)

        self.refresh_metrics()

    def _create_card(self, title_text: str, default_val: str) -> QFrame:
        card = QFrame()
        card.setProperty("class", "card")
        card.setStyleSheet("background-color: #111827; border: 1px solid #1f2937; border-radius: 8px; padding: 12px;")
        l = QVBoxLayout(card)
        t = QLabel(title_text)
        t.setStyleSheet("color: #94a3b8; font-size: 12px;")
        v = QLabel(default_val)
        v.setStyleSheet("color: #38bdf8; font-size: 18px; font-weight: bold;")
        l.addWidget(t)
        l.addWidget(v)
        card.val_label = v
        return card

    def refresh_metrics(self):
        try:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().used / (1024 ** 3)
            mem_count = len(self.engine.memory_manager.search(""))
            nodes = len(self.engine.context_manager._nodes)

            self.cpu_card.val_label.setText(f"{cpu:.1f} %")
            self.ram_card.val_label.setText(f"{ram:.2f} GB")
            self.memory_card.val_label.setText(f"{mem_count} Items")
            self.graph_card.val_label.setText(f"{nodes} Nodes")
        except Exception:
            pass


# ----------------------------------------------------
# 2. AI Console View
# ----------------------------------------------------
class AIConsoleView(QWidget):
    def __init__(self, engine: Engine, on_execute_goal):
        super().__init__()
        self.engine = engine
        self.on_execute_goal = on_execute_goal
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("AI Goal Console")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #38bdf8;")
        layout.addWidget(title)

        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        self.console_output.setPlaceholderText("Enter natural language goals below (e.g., 'Build my portfolio', 'Run security audit')...")
        layout.addWidget(self.console_output)

        input_layout = QHBoxLayout()
        self.prompt_input = QLineEdit()
        self.prompt_input.setPlaceholderText("Type goal here...")
        self.prompt_input.returnPressed.connect(self.submit_goal)

        self.exec_btn = QPushButton("Execute Goal")
        self.exec_btn.clicked.connect(self.submit_goal)

        input_layout.addWidget(self.prompt_input)
        input_layout.addWidget(self.exec_btn)
        layout.addLayout(input_layout)

    def submit_goal(self):
        text = self.prompt_input.text().strip()
        if not text:
            return
        self.prompt_input.clear()
        self.console_output.append(f"\n> USER GOAL: {text}")
        self.console_output.append(">>> Autonomous Multi-Agent Runtime orchestrating solution...\n")
        self.on_execute_goal(text)

    def append_output(self, msg: str):
        self.console_output.append(msg)


# ----------------------------------------------------
# 3. Multi-Agent Monitor View
# ----------------------------------------------------
class AgentMonitorView(QWidget):
    def __init__(self, engine: Engine):
        super().__init__()
        self.engine = engine
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Autonomous Multi-Agent Monitor")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #38bdf8;")
        layout.addWidget(title)

        self.agent_table = QTableWidget(8, 4)
        self.agent_table.setHorizontalHeaderLabels(["Agent Name", "Role", "Status", "Current Task"])
        self.agent_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.agent_table)
        self.refresh_agents()

    def refresh_agents(self):
        agents = self.engine.agent_manager.list_agents()
        self.agent_table.setRowCount(len(agents))
        for i, a in enumerate(agents):
            self.agent_table.setItem(i, 0, QTableWidgetItem(a["name"]))
            self.agent_table.setItem(i, 1, QTableWidgetItem(a["role"]))
            st_item = QTableWidgetItem(a["status"])
            st_item.setForeground(Qt.GlobalColor.cyan if a["status"] == "IDLE" else Qt.GlobalColor.green)
            self.agent_table.setItem(i, 2, st_item)
            self.agent_table.setItem(i, 3, QTableWidgetItem(a.get("task", "None")))


# ----------------------------------------------------
# 4. Memory Explorer View
# ----------------------------------------------------
class MemoryExplorerView(QWidget):
    def __init__(self, engine: Engine):
        super().__init__()
        self.engine = engine
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Enterprise Memory Explorer (7 Layers)")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #38bdf8;")
        layout.addWidget(title)

        top_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search memory items...")
        self.search_input.textChanged.connect(self.refresh_memory)

        self.layer_combo = QComboBox()
        self.layer_combo.addItems(["ALL", "session", "working", "project", "long_term", "episodic", "semantic", "tool"])
        self.layer_combo.currentTextChanged.connect(self.refresh_memory)

        top_layout.addWidget(self.search_input)
        top_layout.addWidget(self.layer_combo)
        layout.addLayout(top_layout)

        self.mem_table = QTableWidget(0, 5)
        self.mem_table.setHorizontalHeaderLabels(["ID", "Layer", "Content", "Importance", "Timestamp"])
        self.mem_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.mem_table)

        self.refresh_memory()

    def refresh_memory(self):
        query = self.search_input.text().strip()
        layer_filter = self.layer_combo.currentText()
        layer = None if layer_filter == "ALL" else layer_filter

        items = self.engine.memory_manager.search(query=query, layer=layer)
        self.mem_table.setRowCount(len(items))

        for i, item in enumerate(items):
            self.mem_table.setItem(i, 0, QTableWidgetItem(item.memory_id[:8]))
            self.mem_table.setItem(i, 1, QTableWidgetItem(item.layer))
            self.mem_table.setItem(i, 2, QTableWidgetItem(item.content))
            self.mem_table.setItem(i, 3, QTableWidgetItem(str(item.importance)))
            self.mem_table.setItem(i, 4, QTableWidgetItem(str(item.timestamp)[:19]))


# ----------------------------------------------------
# 5. Knowledge Graph Viewer
# ----------------------------------------------------
class KnowledgeGraphView(QWidget):
    def __init__(self, engine: Engine):
        super().__init__()
        self.engine = engine
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Context Engine Knowledge Graph")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #38bdf8;")
        layout.addWidget(title)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Node Tree
        self.node_tree = QTreeWidget()
        self.node_tree.setHeaderLabels(["Node ID", "Type", "Label"])
        self.node_tree.itemClicked.connect(self.on_node_clicked)

        # Detail Box
        self.detail_text = QPlainTextEdit()
        self.detail_text.setReadOnly(True)

        splitter.addWidget(self.node_tree)
        splitter.addWidget(self.detail_text)
        layout.addWidget(splitter)

        self.refresh_graph()

    def refresh_graph(self):
        self.node_tree.clear()
        nodes = self.engine.context_manager._nodes.values()
        for n in nodes:
            type_str = n.node_type.value if hasattr(n.node_type, "value") else str(n.node_type)
            item = QTreeWidgetItem([n.node_id[:8], type_str, n.label])
            item.setData(0, Qt.ItemDataRole.UserRole, n)
            self.node_tree.addTopLevelItem(item)

    def on_node_clicked(self, item: QTreeWidgetItem, col: int):
        node = item.data(0, Qt.ItemDataRole.UserRole)
        if node:
            type_str = node.node_type.value if hasattr(node.node_type, "value") else str(node.node_type)
            details = f"Node ID: {node.node_id}\nType: {type_str}\nLabel: {node.label}\n\nProperties:\n{node.properties}"
            self.detail_text.setPlainText(details)


# ----------------------------------------------------
# 6. Live Event Feed
# ----------------------------------------------------
class LiveEventsView(QWidget):
    def __init__(self, engine: Engine):
        super().__init__()
        self.engine = engine
        self.init_ui()

        # Subscribe directly to EventBus wildcard events
        self.engine.event_bus.subscribe("*", self.on_system_event)

    def init_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Live System Event Stream (EventBus)")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #38bdf8;")
        layout.addWidget(title)

        self.event_list = QListWidget()
        layout.addWidget(self.event_list)

    def on_system_event(self, event: SystemEvent):
        text = f"[{str(event.timestamp)[11:19]}] [{event.source}] {event.type.value} | Payload: {event.payload}"
        item = QListWidgetItem(text)
        item.setForeground(Qt.GlobalColor.cyan)
        self.event_list.insertItem(0, item)


# ----------------------------------------------------
# 7. Plugin Manager View
# ----------------------------------------------------
class PluginManagerView(QWidget):
    def __init__(self, engine: Engine):
        super().__init__()
        self.engine = engine
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Enterprise Plugin Manager")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #38bdf8;")
        layout.addWidget(title)

        self.plugin_table = QTableWidget(0, 5)
        self.plugin_table.setHorizontalHeaderLabels(["Plugin ID", "Name", "Version", "Permissions", "Enabled"])
        self.plugin_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.plugin_table)

        btn_layout = QHBoxLayout()
        self.toggle_btn = QPushButton("Toggle Enable/Disable")
        self.toggle_btn.clicked.connect(self.toggle_plugin)

        self.reload_btn = QPushButton("Hot Reload")
        self.reload_btn.clicked.connect(self.reload_plugin)

        btn_layout.addWidget(self.toggle_btn)
        btn_layout.addWidget(self.reload_btn)
        layout.addLayout(btn_layout)

        self.refresh_plugins()

    def refresh_plugins(self):
        plugins = self.engine.plugin_manager.list_plugins()
        self.plugin_table.setRowCount(len(plugins))
        for i, p in enumerate(plugins):
            self.plugin_table.setItem(i, 0, QTableWidgetItem(p["plugin_id"]))
            self.plugin_table.setItem(i, 1, QTableWidgetItem(p["name"]))
            self.plugin_table.setItem(i, 2, QTableWidgetItem(p["version"]))
            self.plugin_table.setItem(i, 3, QTableWidgetItem(", ".join(p["permissions"])))
            st = "YES" if p["is_enabled"] else "NO"
            item = QTableWidgetItem(st)
            item.setForeground(Qt.GlobalColor.green if p["is_enabled"] else Qt.GlobalColor.red)
            self.plugin_table.setItem(i, 4, item)

    def toggle_plugin(self):
        row = self.plugin_table.currentRow()
        if row >= 0:
            pid = self.plugin_table.item(row, 0).text()
            current_en = self.plugin_table.item(row, 4).text() == "YES"
            if current_en:
                self.engine.plugin_manager.disable_plugin(pid)
            else:
                self.engine.plugin_manager.enable_plugin(pid)
            self.refresh_plugins()

    def reload_plugin(self):
        row = self.plugin_table.currentRow()
        if row >= 0:
            pid = self.plugin_table.item(row, 0).text()
            self.engine.plugin_manager.reload_plugin(pid)
            self.refresh_plugins()


# ----------------------------------------------------
# 8. System Monitor View
# ----------------------------------------------------
class SystemMonitorView(QWidget):
    def __init__(self, engine: Engine):
        super().__init__()
        self.engine = engine
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("System Monitor Telemetry")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #38bdf8;")
        layout.addWidget(title)

        self.info_edit = QPlainTextEdit()
        self.info_edit.setReadOnly(True)
        layout.addWidget(self.info_edit)

        self.refresh_monitor()

    def refresh_monitor(self):
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage("/")

        info = f"""
=====================================================
            AtherOS System Telemetry
=====================================================
CPU Utilization   : {cpu:.1f} %
Memory Used       : {mem.used / (1024**3):.2f} GB / {mem.total / (1024**3):.2f} GB ({mem.percent}%)
Disk Utilization  : {disk.used / (1024**3):.2f} GB / {disk.total / (1024**3):.2f} GB ({disk.percent}%)

Subsystem Telemetry:
-----------------------------------------------------
Database Engine   : Connected (SQLite UnitOfWork)
EventBus Status   : Active (Subscribers: {len(self.engine.event_bus._subscribers)})
Capability Registry: Registered Subsystems ({len(self.engine.capability_registry.discover())})
Plugins Installed : {len(self.engine.plugin_manager.list_plugins())}
Agents Registered : {len(self.engine.agent_manager.list_agents())}
=====================================================
"""
        self.info_edit.setPlainText(info)
