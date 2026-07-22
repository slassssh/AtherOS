import sys
from PyQt6.QtWidgets import QApplication
from backend.app.core.engine import Engine
from backend.app.gui.main_window import AtherOSMainWindow


def run_desktop():
    """Entry point for launching AtherOS Desktop Operating Environment."""
    app = QApplication(sys.argv)
    engine = Engine()
    window = AtherOSMainWindow(engine)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run_desktop()
