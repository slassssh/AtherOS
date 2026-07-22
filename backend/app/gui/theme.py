class AtherOSTheme:
    """
    Futuristic AI OS Dark Glass Theme Engine for PyQt6.
    Uses curated dark color palette, neon cyan highlights, clean font hierarchy,
    and rounded borders.
    """

    DARK_STYLESHEET = """
    QMainWindow {
        background-color: #0b0f19;
        color: #e2e8f0;
        font-family: 'Segoe UI', 'Roboto', sans-serif;
    }

    QWidget {
        background-color: #0b0f19;
        color: #e2e8f0;
        font-family: 'Segoe UI', 'Roboto', sans-serif;
        font-size: 13px;
    }

    /* Left Navigation Bar */
    QListWidget#nav_bar {
        background-color: #111827;
        border: 1px solid #1f2937;
        border-radius: 8px;
        outline: none;
        padding: 6px;
    }

    QListWidget#nav_bar::item {
        color: #94a3b8;
        padding: 12px 16px;
        border-radius: 6px;
        margin-bottom: 4px;
        font-weight: 600;
    }

    QListWidget#nav_bar::item:hover {
        background-color: #1e293b;
        color: #38bdf8;
    }

    QListWidget#nav_bar::item:selected {
        background-color: #0369a1;
        color: #ffffff;
    }

    /* Cards & Containers */
    QFrame.card {
        background-color: #111827;
        border: 1px solid #1f2937;
        border-radius: 10px;
        padding: 16px;
    }

    QGroupBox {
        border: 1px solid #334155;
        border-radius: 8px;
        margin-top: 12px;
        font-weight: bold;
        color: #38bdf8;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px;
    }

    /* Buttons */
    QPushButton {
        background-color: #0284c7;
        color: #ffffff;
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: 600;
    }

    QPushButton:hover {
        background-color: #0369a1;
    }

    QPushButton:pressed {
        background-color: #075985;
    }

    QPushButton#secondary_btn {
        background-color: #334155;
        color: #e2e8f0;
    }

    QPushButton#secondary_btn:hover {
        background-color: #475569;
    }

    /* Inputs & Edits */
    QLineEdit, QTextEdit, QPlainTextEdit {
        background-color: #0f172a;
        color: #f8fafc;
        border: 1px solid #334155;
        border-radius: 6px;
        padding: 8px;
        selection-background-color: #0284c7;
    }

    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
        border: 1px solid #38bdf8;
    }

    /* Tables & Trees */
    QTableWidget, QTreeWidget, QListWidget {
        background-color: #0f172a;
        border: 1px solid #1f2937;
        border-radius: 6px;
        gridline-color: #1e293b;
        color: #e2e8f0;
    }

    QHeaderView::section {
        background-color: #1e293b;
        color: #38bdf8;
        padding: 6px;
        font-weight: bold;
        border: none;
    }

    /* Status Bar */
    QStatusBar {
        background-color: #0f172a;
        color: #94a3b8;
        border-top: 1px solid #1f2937;
    }
    """
