import sys
import datetime
import socket
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import Slot

# Импорт вашего UI
from ui_main import Ui_MainWindow

# Импорт ядра
from core.crypto import SecurityManager
from core.database import StorageManager
from core.network import NetworkManager


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.db = StorageManager()
        self.crypto = SecurityManager()
        self.network = NetworkManager(self.crypto)

        self.load_settings()

        self.ui.button_apply.clicked.connect(self.on_apply_settings)
        self.ui.button_send_message.clicked.connect(self.on_send_message)

        self.network.log_signal.connect(self.log_system_message)
        self.network.msg_received.connect(self.on_incoming_message)

        my_ip = self.get_local_ip()
        self.ui.text_browser.append(f"<b>My Local IP: {my_ip}</b>")

    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"

    def load_settings(self):
        self.ui.line_your_name.setText(self.db.get_setting("username"))
        self.ui.line_own_port.setText(self.db.get_setting("own_port"))
        self.ui.line_ip_address.setText(self.db.get_setting("target_ip"))
        self.ui.line_port.setText(self.db.get_setting("target_port"))

        # Загрузка настроек релея (если есть такие поля в UI)
        if hasattr(self.ui, 'line_relay_ip'):
            self.ui.line_relay_ip.setText(self.db.get_setting("relay_ip"))
            self.ui.line_relay_port.setText(self.db.get_setting("relay_port"))

        own_port = self.ui.line_own_port.text()
        if own_port and own_port.isdigit():
            self.network.start_server(int(own_port))

    @Slot()
    def on_apply_settings(self):
        name = self.ui.line_your_name.text()
        own_port = self.ui.line_own_port.text()
        target_ip = self.ui.line_ip_address.text()
        target_port = self.ui.line_port.text()

        self.db.save_setting("username", name)
        self.db.save_setting("own_port", own_port)
        self.db.save_setting("target_ip", target_ip)
        self.db.save_setting("target_port", target_port)

        # Сохранение релея
        if hasattr(self.ui, 'line_relay_ip'):
            self.db.save_setting("relay_ip", self.ui.line_relay_ip.text())
            self.db.save_setting("relay_port", self.ui.line_relay_port.text())

        if own_port.isdigit():
            self.network.start_server(int(own_port))
            QMessageBox.information(self, "Success", f"Server restarted on port {own_port}")
        else:
            QMessageBox.warning(self, "Error", "Port must be a number")

    @Slot()
    def on_send_message(self):
        text = self.ui.text_edit_message.toPlainText()
        if not text: return

        target_ip = self.ui.line_ip_address.text()
        target_port = self.ui.line_port.text()
        username = self.ui.line_your_name.text() or "Me"

        if not target_ip or not target_port:
            QMessageBox.warning(self, "Error", "Target IP/Port required")
            return

        # Проверка на использование Relay
        use_relay = False
        relay_ip = ""
        relay_port = ""

        # Безопасная проверка наличия элементов UI (чтобы не упало, если вы их не добавили)
        if hasattr(self.ui, 'check_box_relay') and self.ui.check_box_relay.isChecked():
            use_relay = True
            relay_ip = self.ui.line_relay_ip.text()
            relay_port = self.ui.line_relay_port.text()
            if not relay_ip or not relay_port:
                QMessageBox.warning(self, "Error", "Relay IP/Port required")
                return

        success = False
        if use_relay:
            success = self.network.send_via_relay(target_ip, int(target_port),
                                                  relay_ip, int(relay_port), text)
        else:
            success = self.network.send_message(target_ip, int(target_port), text)

        timestamp = datetime.datetime.now().strftime("%H:%M:%S")

        if success:
            mode = " (via Relay)" if use_relay else ""
            formatted_msg = f"<span style='color:blue'>[{timestamp}] {username}: {text} ✅{mode}</span>"
            self.ui.text_browser.append(formatted_msg)
            self.ui.text_edit_message.clear()
            self.db.add_message(timestamp, username, text, "sent")
        else:
            self.ui.text_browser.append(
                f"<span style='color:gray'>[{timestamp}] ⏳ Establishing connection... Try again.</span>")

    @Slot(str, str, str)
    def on_incoming_message(self, timestamp, sender_ip, text):
        formatted_msg = f"<span style='color:green'>[{timestamp}] {sender_ip}: {text} 📩</span>"
        self.ui.text_browser.append(formatted_msg)
        self.db.add_message(timestamp, sender_ip, text, "received")

    @Slot(str)
    def log_system_message(self, msg):
        self.ui.text_browser.append(f"<i>[System]: {msg}</i>")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())