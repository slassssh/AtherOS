"""
AtherOS v1.0.0-rc1 — Desktop Crash Dialog (PyQt6)

Shown when the AtherOS desktop application encounters an unhandled exception.
Provides exception details, stack trace, copy-to-clipboard, and restart/exit actions.
"""
from __future__ import annotations

import json
import traceback
from pathlib import Path
from typing import Optional


def show_crash_dialog(exc: BaseException, crash_dump_path: Optional[Path] = None) -> None:
    """
    Display a PyQt6 crash dialog. Safe to call even if PyQt6 is unavailable
    (falls back to printing to stderr).
    """
    try:
        _show_qt_dialog(exc, crash_dump_path)
    except ImportError:
        import sys
        print(f"[AtherOS CRASH] {type(exc).__name__}: {exc}", file=sys.stderr)
        if crash_dump_path:
            print(f"[AtherOS CRASH] Dump: {crash_dump_path}", file=sys.stderr)


def _show_qt_dialog(exc: BaseException, crash_dump_path: Optional[Path]) -> None:
    from PyQt6.QtWidgets import (
        QApplication,
        QDialog,
        QDialogButtonBox,
        QLabel,
        QPlainTextEdit,
        QPushButton,
        QVBoxLayout,
        QHBoxLayout,
    )
    from PyQt6.QtCore import Qt
    from PyQt6.QtGui import QFont

    import sys

    app = QApplication.instance() or QApplication(sys.argv)

    dialog = QDialog()
    dialog.setWindowTitle("AtherOS — Unexpected Error")
    dialog.setMinimumSize(680, 420)
    dialog.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowStaysOnTopHint)

    layout = QVBoxLayout(dialog)
    layout.setSpacing(12)
    layout.setContentsMargins(20, 20, 20, 20)

    # ── Header ──────────────────────────────────────────────────────────
    header = QLabel(f"💥  AtherOS has encountered an unexpected error")
    header.setStyleSheet("font-size: 15px; font-weight: bold; color: #e74c3c;")
    layout.addWidget(header)

    exc_label = QLabel(f"<b>{type(exc).__name__}</b>: {exc}")
    exc_label.setWordWrap(True)
    exc_label.setStyleSheet("font-size: 12px; color: #ecf0f1;")
    layout.addWidget(exc_label)

    # ── Traceback ───────────────────────────────────────────────────────
    tb_text = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    tb_view = QPlainTextEdit(tb_text)
    tb_view.setReadOnly(True)
    font = QFont("Courier New", 9)
    tb_view.setFont(font)
    tb_view.setStyleSheet(
        "background-color: #1a1a2e; color: #a8d8ea; border: 1px solid #444; border-radius: 4px;"
    )
    layout.addWidget(tb_view)

    # ── Crash dump path ─────────────────────────────────────────────────
    if crash_dump_path and crash_dump_path.exists():
        dump_label = QLabel(f"📄 Crash dump saved: <code>{crash_dump_path}</code>")
        dump_label.setStyleSheet("font-size: 10px; color: #95a5a6;")
        layout.addWidget(dump_label)

    # ── Buttons ─────────────────────────────────────────────────────────
    btn_layout = QHBoxLayout()

    copy_btn = QPushButton("📋 Copy Report")
    copy_btn.setFixedWidth(130)

    def _copy_report():
        content = tb_text
        if crash_dump_path and crash_dump_path.exists():
            try:
                content = crash_dump_path.read_text(encoding="utf-8")
            except OSError:
                pass
        app.clipboard().setText(content)
        copy_btn.setText("✅ Copied!")

    copy_btn.clicked.connect(_copy_report)
    btn_layout.addWidget(copy_btn)
    btn_layout.addStretch()

    exit_btn = QPushButton("Exit AtherOS")
    exit_btn.setFixedWidth(120)
    exit_btn.setStyleSheet("background-color: #c0392b; color: white;")
    exit_btn.clicked.connect(lambda: sys.exit(1))
    btn_layout.addWidget(exit_btn)

    restart_btn = QPushButton("🔄 Restart")
    restart_btn.setFixedWidth(120)
    restart_btn.setStyleSheet("background-color: #2980b9; color: white;")

    def _restart():
        dialog.accept()
        import os, subprocess
        subprocess.Popen([sys.executable] + sys.argv)
        sys.exit(0)

    restart_btn.clicked.connect(_restart)
    btn_layout.addWidget(restart_btn)

    layout.addLayout(btn_layout)

    dialog.setStyleSheet("""
        QDialog { background-color: #2c2c3e; color: #ecf0f1; }
        QPushButton { padding: 6px 12px; border-radius: 4px; font-weight: bold; }
        QPushButton:hover { opacity: 0.9; }
    """)

    dialog.exec()
