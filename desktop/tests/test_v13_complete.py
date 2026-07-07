import sys
import os


sys.path.append(
    os.path.abspath(".")
)


from desktop.app.core.final_integration import FinalDesktopIntegration
from desktop.app.core.desktop_app import DesktopApp
from desktop.app.ui.command_center import CommandCenter
from desktop.app.ui.chat_interface import ChatInterface
from desktop.app.ui.system_monitor import SystemMonitorUI



def test_v13_desktop_complete():


    app = DesktopApp()

    assert app.start()["running"]



    command = CommandCenter()

    assert command.execute(
        "boot"
    )["executed"]



    chat = ChatInterface()

    assert chat.send(
        "hello"
    )["sent"]



    monitor = SystemMonitorUI()

    monitor.update(
        "status",
        "online"
    )

    assert monitor.status()["status"] == "online"



    desktop = FinalDesktopIntegration()

    result = desktop.launch()


    assert result["running"]

    assert result["optimized"]




if __name__ == "__main__":

    test_v13_desktop_complete()


    print(
        "🎉 AtherOS v1.3 Desktop UI Complete"
    )