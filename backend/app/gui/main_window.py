import sys
from typing import Optional
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QStackedWidget,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from backend.app.core.engine import Engine
from backend.app.gui.theme import AtherOSTheme
from backend.app.gui.views import (
    AgentMonitorView,
    AIConsoleView,
    DashboardView,
    KnowledgeGraphView,
    LiveEventsView,
    MemoryExplorerView,
    PluginManagerView,
    SystemMonitorView,
)
from backend.app.gui.worker import GoalExecutionWorker


class AtherOSMainWindow(QMainWindow):
    """
    Master Flagship Desktop Operating Environment for AtherOS.
    Communicates ONLY through EventBus, CapabilityRegistry, and public Engine APIs.
    Features Left Navigation, Header Telemetry Bar, Stacked View Workspace, and QThread worker integration.
    """

    def __init__(self, engine: Optional[Engine] = None):
        super().__init__()
        self.engine = engine or Engine()
        self.worker: Optional[GoalExecutionWorker] = None

        self.setWindowTitle("AtherOS - AI Operating System Desktop Environment")
        self.resize(1280, 800)
        self.setStyleSheet(AtherOSTheme.DARK_STYLESHEET)

        self.init_ui()

        # Telemetry Timer (updates dashboard/monitor every 2 seconds)
        self.telemetry_timer = QTimer(self)
        self.telemetry_timer.timeout.connect(self.on_telemetry_tick)
        self.telemetry_timer.start(2000)

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # 1. Left Navigation Bar
        self.nav_bar = QListWidget()
        self.nav_bar.setObjectName("nav_bar")
        self.nav_bar.setFixedWidth(220)

        nav_items = [
            "Dashboard",
            "AI Console",
            "Multi-Agent Monitor",
            "Memory Explorer",
            "Knowledge Graph",
            "Live Event Feed",
            "Plugin Manager",
            "System Monitor"
        ]

        for item_name in nav_items:
            self.nav_bar.addItem(item_name)

        self.nav_bar.currentRowChanged.connect(self.switch_view)
        main_layout.addWidget(self.nav_bar)

        # 2. Main Workspace & Views Stack
        workspace_layout = QVBoxLayout()

        # Top Telemetry Header
        header_layout = QHBoxLayout()
        header_title = QLabel("AtherOS v0.1.0-Enterprise")
        header_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #38bdf8;")

        self.status_label = QLabel("System Status: OPERATIONAL | LLM: Provider Agnostic")
        self.status_label.setStyleSheet("color: #94a3b8;")

        header_layout.addWidget(header_title)
        header_layout.addStretch()
        header_layout.addWidget(self.status_label)
        workspace_layout.addLayout(header_layout)

        # Stacked Views Widget
        self.stacked_widget = QStackedWidget()

        self.dashboard_view = DashboardView(self.engine)
        self.console_view = AIConsoleView(self.engine, self.execute_goal)
        self.agent_view = AgentMonitorView(self.engine)
        self.memory_view = MemoryExplorerView(self.engine)
        self.graph_view = KnowledgeGraphView(self.engine)
        self.events_view = LiveEventsView(self.engine)
        self.plugin_view = PluginManagerView(self.engine)
        self.monitor_view = SystemMonitorView(self.engine)

        self.stacked_widget.addWidget(self.dashboard_view)
        self.stacked_widget.addWidget(self.console_view)
        self.stacked_widget.addWidget(self.agent_view)
        self.stacked_widget.addWidget(self.memory_view)
        self.stacked_widget.addWidget(self.graph_view)
        self.stacked_widget.addWidget(self.events_view)
        self.stacked_widget.addWidget(self.plugin_view)
        self.stacked_widget.addWidget(self.monitor_view)

        workspace_layout.addWidget(self.stacked_widget)
        main_layout.addLayout(workspace_layout)

        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready. AtherOS AI Operating System running.")

        # Default to Dashboard view
        self.nav_bar.setCurrentRow(0)

    def switch_view(self, index: int):
        self.stacked_widget.setCurrentIndex(index)
        # Refresh active view
        widget = self.stacked_widget.widget(index)
        if hasattr(widget, "refresh_metrics"):
            widget.refresh_metrics()
        elif hasattr(widget, "refresh_agents"):
            widget.refresh_agents()
        elif hasattr(widget, "refresh_memory"):
            widget.refresh_memory()
        elif hasattr(widget, "refresh_graph"):
            widget.refresh_graph()
        elif hasattr(widget, "refresh_plugins"):
            widget.refresh_plugins()
        elif hasattr(widget, "refresh_monitor"):
            widget.refresh_monitor()

    def execute_goal(self, goal_text: str):
        self.status_bar.showMessage(f"Executing goal: '{goal_text}'...")
        self.worker = GoalExecutionWorker(self.engine, goal_text)
        self.worker.finished_signal.connect(self.on_goal_finished)
        self.worker.error_signal.connect(self.on_goal_error)
        self.worker.start()

    def on_goal_finished(self, result: dict):
        self.status_bar.showMessage(f"Goal execution completed: {result.get('status', 'SUCCESS')}")
        self.console_view.append_output(f"\n[GOAL SUCCESS] Status: {result.get('status')}")
        if "final_response" in result:
            self.console_view.append_output(f"Result Summary:\n{result['final_response']}\n")

    def on_goal_error(self, err_msg: str):
        self.status_bar.showMessage("Goal execution failed!")
        self.console_view.append_output(f"\n[GOAL FAILURE] Error: {err_msg}\n")

    def on_telemetry_tick(self):
        self.dashboard_view.refresh_metrics()
        self.monitor_view.refresh_monitor()
