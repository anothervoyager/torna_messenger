# core/network.py
import socket
import json
import threading
from PySide6.QtCore import QObject, Signal, QThread
from .protocol import PacketType


class ServerThread(QThread):
    """Поток, который слушает входящие соединения"""
    new_packet_received = Signal(dict, str)  # пакет, ip_отправителя
    log_message = Signal(str)

    def __init__(self, port):
        super().__init__()
        self.port = port
        self.running = True

    def run(self):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 0.0.0.0 позволяет принимать соединения с других компьютеров
            server.bind(('0.0.0.0', self.port))
            server.listen(5)
            self.log_message.emit(f"Server started on port {self.port}")

            while self.running:
                client, addr = server.accept()
                threading.Thread(target=self._handle_client, args=(client, addr)).start()
        except Exception as e:
            self.log_message.emit(f"Server Error: {e}")

    def _handle_client(self, client_socket, addr):
        try:
            data = client_socket.recv(1024 * 16)  # 16KB буфер
            if data:
                packet = json.loads(data.decode('utf-8'))
                self.new_packet_received.emit(packet, addr[0])
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            client_socket.close()

    def stop(self):
        self.running = False
        self.quit()


class NetworkManager(QObject):
    msg_received = Signal(str, str, str)  # timestamp, sender, text
    log_signal = Signal(str)

    def __init__(self, security_manager):
        super().__init__()
        self.sec_man = security_manager
        self.server_thread = None
        self.known_peers = {}  # {ip: public_key_pem}

    def start_server(self, port):
        if self.server_thread and self.server_thread.isRunning():
            self.server_thread.stop()

        self.server_thread = ServerThread(port)
        self.server_thread.new_packet_received.connect(self.process_packet)
        self.server_thread.log_message.connect(self.log_signal.emit)
        self.server_thread.start()

    def send_handshake(self, target_ip, target_port):
        """Отправка своего публичного ключа"""
        packet = {
            "type": PacketType.HANDSHAKE,
            "pub_key": self.sec_man.get_public_key_pem()
        }
        self._send_raw(target_ip, target_port, packet)

    def send_message(self, target_ip, target_port, text, use_relay=False):
        """Отправка сообщения. Если ключа нет - сначала HANDSHAKE"""

        # Если мы не знаем ключ получателя, нужно сначала обменяться
        if target_ip not in self.known_peers:
            self.log_signal.emit(f"Key for {target_ip} not found. Sending Handshake...")
            self.send_handshake(target_ip, target_port)
            return False  # Сообщение не отправлено, попробуйте позже

        recipient_key = self.known_peers[target_ip]
        encrypted_payload = self.sec_man.encrypt_hybrid(text, recipient_key)

        packet = {
            "type": PacketType.DIRECT_MSG,
            "payload": encrypted_payload
        }

        # Здесь можно добавить логику RELAY (как в предыдущем примере)
        # if use_relay: ...

        try:
            self._send_raw(target_ip, target_port, packet)
            return True
        except Exception as e:
            self.log_signal.emit(f"Send failed: {e}")
            return False

    def _send_raw(self, ip, port, data_dict):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((ip, int(port)))
        sock.send(json.dumps(data_dict).encode('utf-8'))
        sock.close()

    def process_packet(self, packet, sender_ip):
        p_type = packet.get("type")

        if p_type == PacketType.HANDSHAKE:
            # Сохраняем ключ собеседника
            self.known_peers[sender_ip] = packet["pub_key"]
            self.log_signal.emit(f"Handshake received from {sender_ip}")

        elif p_type == PacketType.DIRECT_MSG:
            try:
                decrypted_text = self.sec_man.decrypt_hybrid(packet["payload"])
                import datetime
                timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                # Эмитим сигнал, чтобы UI обновился
                self.msg_received.emit(timestamp, sender_ip, decrypted_text)
            except Exception as e:
                self.log_signal.emit(f"Decryption error: {e}")