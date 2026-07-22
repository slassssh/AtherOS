import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

# Set offscreen QPA platform for headless testing
os.environ["QT_QPA_PLATFORM"] = "offscreen"

import pytest
from PyQt6.QtWidgets import QApplication
from backend.app.core.engine import Engine
from backend.app.gui.main_window import AtherOSMainWindow


def get_app():
    return QApplication.instance() or QApplication(sys.argv)


def test_desktop_main_window_init():
    app = get_app()
    engine = Engine()
    window = AtherOSMainWindow(engine)
    assert window is not None
    assert window.windowTitle().startswith("AtherOS")
    assert window.stacked_widget.count() == 8


def test_desktop_navigation_switching():
    app = get_app()
    engine = Engine()
    window = AtherOSMainWindow(engine)

    # Test switching across all 8 navigation items
    for index in range(8):
        window.nav_bar.setCurrentRow(index)
        assert window.stacked_widget.currentIndex() == index


def test_desktop_memory_explorer_and_graph_views():
    app = get_app()
    engine = Engine()
    session = engine.create_session("Test Session", "GUI verification")
    window = AtherOSMainWindow(engine)

    # Refresh memory view
    window.memory_view.refresh_memory()
    assert window.memory_view.mem_table.rowCount() >= 1

    # Refresh graph view
    window.graph_view.refresh_graph()
    assert window.graph_view.node_tree.topLevelItemCount() >= 1


def test_desktop_plugin_manager_controls():
    app = get_app()
    engine = Engine()
    window = AtherOSMainWindow(engine)

    # Verify plugins loaded in plugin manager table
    window.plugin_view.refresh_plugins()
    assert window.plugin_view.plugin_table.rowCount() >= 4
