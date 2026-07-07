import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from desktop.app.core.desktop_app import DesktopApp
from desktop.app.core.window_manager import WindowManager
from desktop.app.ui.app_shell import AppShell
from desktop.app.ui.navigation import Navigation
from desktop.app.ui.theme import ThemeEngine



def test_desktop_foundation():


    app = DesktopApp()

    assert app.start()["running"]



    windows = WindowManager()

    assert windows.create_window(
        "main"
    )["created"]



    shell = AppShell()

    assert shell.load()["shell"] == "loaded"



    nav = Navigation()

    nav.add_route(
        "/dashboard"
    )

    assert "/dashboard" in nav.get_routes()



    theme = ThemeEngine()

    theme.set_theme(
        "dark"
    )

    assert theme.current() == "dark"



if __name__ == "__main__":

    test_desktop_foundation()


    print(
        "✅ v1.3 Desktop UI Block 1 (Features 1-5) Tests Passed"
    )