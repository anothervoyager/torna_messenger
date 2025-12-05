import socket
import json
import threading
from PySide6.QtCore import QObject, Signal, QThread
from .protocol import PacketType


class ServerThread(QThread):
    """Поток, слушающий входящие соединения. Не блокирует UI."""
    new_packet_received = Signal(dict, str)  # пакет, ip_отправителя
    log_message = Signal(str)

    def __init__(self, port):
        super().__init__()
        self.port = port
        self.running = True

    def run(self):
        server = None
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Исправляет ошибку "Address already in use" при перезапуске
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(('0.0.0.0', self.port))
            server.listen(5)

            # Исправляет зависание UI: сокет проверяет соединения раз в 1 сек
            server.settimeout(1.0)

            self.log_message.emit(f"Server started on port {self.port}")

            while self.running:
                try:
                    client, addr = server.accept()
                    # Обработка клиента в отдельном потоке
                    threading.Thread(target=self._handle_client, args=(client, addr)).start()
                except socket.timeout:
                    # Таймаут вышел, проверяем self.running и слушаем дальше
                    continue
                except OSError:
                    break

        except Exception as e:
            self.log_message.emit(f"Server Error: {e}")
        finally:
            if server:
                server.close()
            self.log_message.emit("Server stopped")

    def _handle_client(self, client_socket, addr):
        try:
            client_socket.settimeout(5.0)
            data = client_socket.recv(1024 * 64)  # 64KB буфер
            if data:
                packet = json.loads(data.decode('utf-8'))
                self.new_packet_received.emit(packet, addr[0])
        except Exception:
            pass
        finally:
            client_socket.close()

    def stop(self):
        self.running = False
        # wait() вызывается в NetworkManager, чтобы не морозить тут


class NetworkManager(QObject):
    msg_received = Signal(str, str, str)  # timestamp, sender, text
    log_signal = Signal(str)

    def __init__(self, security_manager):
        super().__init__()
        self.sec_man = security_manager
        self.server_thread = None
        self.known_peers = {}  # {ip: public_key_pem}
        self.my_listening_port = 5000

    def start_server(self, port):
        self.my_listening_port = port

        if self.server_thread and self.server_thread.isRunning():
            self.server_thread.stop()
            self.server_thread.wait()  # Ждем безопасного закрытия

        self.server_thread = ServerThread(port)
        self.server_thread.new_packet_received.connect(self.process_packet)
        self.server_thread.log_message.connect(self.log_signal.emit)
        self.server_thread.start()

    def send_handshake(self, target_ip, target_port, is_reply=False):
        """Отправляем свой ключ и СВОЙ ПОРТ"""
        packet = {
            "type": PacketType.HANDSHAKE,
            "pub_key": self.sec_man.get_public_key_pem(),
            "sender_listening_port": self.my_listening_port,
            "is_reply": is_reply
        }

        def _send_thread():
            try:
                self._send_raw(target_ip, target_port, packet)
                direction = "reply" if is_reply else "request"
                self.log_signal.emit(f"Handshake ({direction}) sent to {target_ip}:{target_port}")
            except Exception as e:
                self.log_signal.emit(f"Handshake failed: {e}")

        threading.Thread(target=_send_thread).start()

    def send_message(self, target_ip, target_port, text):
        """Прямая отправка"""
        if target_ip not in self.known_peers:
            self.log_signal.emit(f"Key for {target_ip} missing. Sending Handshake...")
            self.send_handshake(target_ip, target_port, is_reply=False)
            return False

        recipient_key = self.known_peers[target_ip]
        encrypted_payload = self.sec_man.encrypt_hybrid(text, recipient_key)

        packet = {
            "type": PacketType.DIRECT_MSG,
            "payload": encrypted_payload
        }

        threading.Thread(target=self._send_safe, args=(target_ip, target_port, packet)).start()
        return True

    def send_via_relay(self, target_ip, target_port, relay_ip, relay_port, text):
        """Отправка через посредника"""
        if target_ip not in self.known_peers:
            self.log_signal.emit(f"Key for Target {target_ip} missing. Need direct handshake first.")
            return False

        # 1. Шифруем для конечного получателя
        recipient_key = self.known_peers[target_ip]
        encrypted_payload = self.sec_man.encrypt_hybrid(text, recipient_key)

        # 2. Внутренний пакет (как будто прямой)
        inner_packet = {
            "type": PacketType.DIRECT_MSG,
            "payload": encrypted_payload
        }

        # 3. Пакет для посредника
        relay_packet = {
            "type": PacketType.RELAY_MSG,
            "target_addr": [target_ip, int(target_port)],
            "inner_packet": inner_packet
        }

        self.log_signal.emit(f"Sending via Relay {relay_ip} -> {target_ip}")
        threading.Thread(target=self._send_safe, args=(relay_ip, relay_port, relay_packet)).start()
        return True

    def _send_safe(self, ip, port, packet):
        try:
            self._send_raw(ip, port, packet)
        except Exception as e:
            self.log_signal.emit(f"Send Error: {e}")

    def _send_raw(self, ip, port, data_dict):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((ip, int(port)))
        sock.send(json.dumps(data_dict).encode('utf-8'))
        sock.close()

    def process_packet(self, packet, sender_ip):
        p_type = packet.get("type")

        # === HANDSHAKE ===
        if p_type == PacketType.HANDSHAKE:
            self.known_peers[sender_ip] = packet["pub_key"]
            peer_listening_port = packet.get("sender_listening_port", 5000)
            is_reply = packet.get("is_reply", False)

            if is_reply:
                self.log_signal.emit(f"✅ Secure connection established with {sender_ip}")
            else:
                self.log_signal.emit(f"Handshake from {sender_ip}. Auto-replying...")
                self.send_handshake(sender_ip, peer_listening_port, is_reply=True)

        # === DIRECT MSG ===
        elif p_type == PacketType.DIRECT_MSG:
            try:
                decrypted_text = self.sec_man.decrypt_hybrid(packet["payload"])
                import datetime
                timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                self.msg_received.emit(timestamp, sender_ip, decrypted_text)
            except Exception as e:
                self.log_signal.emit(f"Decryption error (Wrong Key?): {e}")

        # === RELAY MSG ===
        elif p_type == PacketType.RELAY_MSG:
            target_info = packet.get("target_addr")
            inner = packet.get("inner_packet")
            if target_info and inner:
                t_ip, t_port = target_info
                self.log_signal.emit(f"🔄 Relaying packet from {sender_ip} to {t_ip}:{t_port}")
                threading.Thread(target=self._send_safe, args=(t_ip, t_port, inner)).start()