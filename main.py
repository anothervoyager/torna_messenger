# main.py
import sys
import datetime
import socket
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import Slot

# Импорт сгенерированного Qt Designer файла
# Убедитесь, что файл ui_main.py лежит рядом
from ui_main import Ui_MainWindow

# Импорт наших модулей
from core.crypto import SecurityManager
from core.database import StorageManager
from core.network import NetworkManager


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Инициализация ядра
        self.db = StorageManager()
        self.crypto = SecurityManager()
        self.network = NetworkManager(self.crypto)

        # Восстановление настроек
        self.load_settings()

        # Сигналы UI
        self.ui.button_apply.clicked.connect(self.on_apply_settings)
        self.ui.button_send_message.clicked.connect(self.on_send_message)

        # Сигналы Сети
        self.network.log_signal.connect(self.log_system_message)
        self.network.msg_received.connect(self.on_incoming_message)

        # Показать свой IP
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

        # Автозапуск сервера, если порт был сохранен
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

        if own_port.isdigit():
            self.network.start_server(int(own_port))
            QMessageBox.information(self, "OK", f"Server restarted on port {own_port}")
        else:
            QMessageBox.warning(self, "Error", "Port must be a number")

    @Slot()
    def on_send_message(self):
        text = self.ui.text_edit_message.toPlainText()
        if not text:
            return

        target_ip = self.ui.line_ip_address.text()
        target_port = self.ui.line_port.text()
        username = self.ui.line_your_name.text() or "Me"

        if not target_ip or not target_port:
            QMessageBox.warning(self, "Error", "Enter Target IP and Port")
            return

        # Попытка отправки
        success = self.network.send_message(target_ip, int(target_port), text)

        timestamp = datetime.datetime.now().strftime("%H:%M:%S")

        if not success:
            self.ui.text_browser.append(
                f"<span style='color:gray'>[{timestamp}] ⚠️ Handshaking with {target_ip}... Click send again in a moment.</span>")
            return

        # Если успешно
        formatted_msg = f"<span style='color:blue'>[{timestamp}] {username}: {text} ✅</span>"
        self.ui.text_browser.append(formatted_msg)
        self.ui.text_edit_message.clear()
        self.db.add_message(timestamp, username, text, "sent")

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