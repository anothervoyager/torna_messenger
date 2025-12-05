import sys
import datetime
import socket
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import Slot

# Импорт UI (убедитесь, что ui_main.py лежит рядом)
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

        # 1. Инициализация систем
        self.db = StorageManager()
        self.crypto = SecurityManager()  # Ключи загружаются или создаются
        self.network = NetworkManager(self.crypto)

        # 2. Восстановление настроек из БД
        self.load_settings()

        # 3. Подключение сигналов UI
        self.ui.button_apply.clicked.connect(self.on_apply_settings)
        self.ui.button_send_message.clicked.connect(self.on_send_message)

        # 4. Подключение сетевых сигналов
        self.network.log_signal.connect(self.log_system_message)
        self.network.msg_received.connect(self.on_incoming_message)

        # Показываем свой IP для удобства
        my_ip = self.get_local_ip()
        self.ui.text_browser.append(f"<i>My Local IP: {my_ip}</i>")

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
        """Загрузка сохраненных данных в поля ввода"""
        self.ui.line_your_name.setText(self.db.get_setting("username"))
        self.ui.line_own_port.setText(self.db.get_setting("own_port"))
        self.ui.line_ip_address.setText(self.db.get_setting("target_ip"))
        self.ui.line_port.setText(self.db.get_setting("target_port"))

        # Если порт задан, сразу запускаем сервер
        own_port = self.ui.line_own_port.text()
        if own_port:
            self.network.start_server(int(own_port))

    @Slot()
    def on_apply_settings(self):
        """Сохранение настроек и перезапуск сервера"""
        name = self.ui.line_your_name.text()
        own_port = self.ui.line_own_port.text()
        target_ip = self.ui.line_ip_address.text()
        target_port = self.ui.line_port.text()

        self.db.save_setting("username", name)
        self.db.save_setting("own_port", own_port)
        self.db.save_setting("target_ip", target_ip)
        self.db.save_setting("target_port", target_port)

        # Перезапуск сервера
        if own_port.isdigit():
            self.network.start_server(int(own_port))
            QMessageBox.information(self, "Success", f"Settings saved. Listening on port {own_port}")
        else:
            QMessageBox.warning(self, "Error", "Port must be a number")

    @Slot()
    def on_send_message(self):
        """Обработка кнопки отправки"""
        text = self.ui.text_edit_message.toPlainText()
        if not text:
            return

        target_ip = self.ui.line_ip_address.text()
        target_port = self.ui.line_port.text()
        username = self.ui.line_your_name.text() or "Me"

        if not target_ip or not target_port:
            QMessageBox.warning(self, "Error", "Target IP/Port required")
            return

        # Попытка отправки через сеть
        success = self.network.send_message(target_ip, int(target_port), text)

        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        status_emoji = "✅" if success else "❌ (Key Error/Fail)"

        if not success:
            self.ui.text_browser.append(
                f"<span style='color:orange'>[{timestamp}] System: Handshake sent. Try again in a second.</span>")
            return

        # Отображение в своем чате
        formatted_msg = f"<span style='color:blue'>[{timestamp}] {username}: {text} {status_emoji}</span>"
        self.ui.text_browser.append(formatted_msg)
        self.ui.text_edit_message.clear()

        # Сохранение в историю
        self.db.add_message(timestamp, username, text, "sent")

    @Slot(str, str, str)
    def on_incoming_message(self, timestamp, sender_ip, text):
        """Слот, вызываемый при получении сообщения из сети"""
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