import socket
import json
import threading
from PySide6.QtCore import QObject, Signal, QThread
from .protocol import PacketType


class ServerThread(QThread):
    """Поток, слушающий входящие соединения"""
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
            # ВАЖНО: Разрешаем повторное использование адреса (чтобы не было ошибки при перезапуске)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(('0.0.0.0', self.port))
            server.listen(5)

            # ВАЖНО: Устанавливаем таймаут, чтобы accept не блокировал поток навечно
            server.settimeout(1.0)

            self.log_message.emit(f"Server started on port {self.port}")

            while self.running:
                try:
                    # Теперь accept будет ждать 1 секунду и выбрасывать исключение timeout
                    client, addr = server.accept()
                    threading.Thread(target=self._handle_client, args=(client, addr)).start()
                except socket.timeout:
                    # Таймаут вышел, просто продолжаем цикл и проверяем self.running
                    continue
                except OSError:
                    # Сокет был закрыт принудительно
                    break

        except Exception as e:
            self.log_message.emit(f"Server Error: {e}")
        finally:
            if server:
                server.close()
            self.log_message.emit("Server stopped")

    def _handle_client(self, client_socket, addr):
        try:
            # Клиентский сокет тоже должен иметь таймаут или быть блокирующим,
            # но здесь ставим таймаут на всякий случай
            client_socket.settimeout(5.0)
            data = client_socket.recv(1024 * 32)
            if data:
                packet = json.loads(data.decode('utf-8'))
                self.new_packet_received.emit(packet, addr[0])
        except Exception:
            pass  # Игнорируем ошибки чтения/таймауты от клиентов
        finally:
            client_socket.close()

    def stop(self):
        self.running = False
        # Мы не вызываем здесь wait(), чтобы не блокировать UI.
        # Поток завершится сам через макс. 1 секунду (из-за таймаута).


class NetworkManager(QObject):
    msg_received = Signal(str, str, str)  # timestamp, sender, text
    log_signal = Signal(str)

    def __init__(self, security_manager):
        super().__init__()
        self.sec_man = security_manager
        self.server_thread = None
        self.known_peers = {}
        self.my_listening_port = 5000

    def start_server(self, port):
        self.my_listening_port = port

        # Если сервер уже запущен
        if self.server_thread and self.server_thread.isRunning():
            # Говорим ему остановиться
            self.server_thread.stop()
            # Ждем завершения (максимум 1 сек + небольшая дельта),
            # чтобы освободить порт перед новым запуском.
            # wait() здесь безопасен, так как мы добавили timeout в run()
            self.server_thread.wait()

        self.server_thread = ServerThread(port)
        self.server_thread.new_packet_received.connect(self.process_packet)
        self.server_thread.log_message.connect(self.log_signal.emit)
        self.server_thread.start()

    def send_handshake(self, target_ip, target_port, is_reply=False):
        packet = {
            "type": PacketType.HANDSHAKE,
            "pub_key": self.sec_man.get_public_key_pem(),
            "sender_listening_port": self.my_listening_port,
            "is_reply": is_reply
        }

        def _send_thread():
            try:
                self._send_raw(target_ip, target_port, packet)
                if is_reply:
                    self.log_signal.emit(f"Sent reply handshake to {target_ip}:{target_port}")
                else:
                    self.log_signal.emit(f"Sent handshake request to {target_ip}:{target_port}")
            except Exception as e:
                self.log_signal.emit(f"Handshake failed: {e}")

        threading.Thread(target=_send_thread).start()

    def send_message(self, target_ip, target_port, text):
        if target_ip not in self.known_peers:
            self.log_signal.emit(f"Key for {target_ip} missing. Initiating handshake...")
            self.send_handshake(target_ip, target_port, is_reply=False)
            return False

        recipient_key = self.known_peers[target_ip]
        encrypted_payload = self.sec_man.encrypt_hybrid(text, recipient_key)

        packet = {
            "type": PacketType.DIRECT_MSG,
            "payload": encrypted_payload
        }

        try:
            self._send_raw(target_ip, target_port, packet)
            return True
        except Exception as e:
            self.log_signal.emit(f"Send Error: {e}")
            return False

    def _send_raw(self, ip, port, data_dict):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((ip, int(port)))
        sock.send(json.dumps(data_dict).encode('utf-8'))
        sock.close()

    def process_packet(self, packet, sender_ip):
        p_type = packet.get("type")

        if p_type == PacketType.HANDSHAKE:
            self.known_peers[sender_ip] = packet["pub_key"]
            peer_listening_port = packet.get("sender_listening_port", 5000)
            is_reply = packet.get("is_reply", False)

            if is_reply:
                self.log_signal.emit(f"✅ Connection established with {sender_ip}")
            else:
                self.log_signal.emit(f"Handshake from {sender_ip}. Auto-replying...")
                self.send_handshake(sender_ip, peer_listening_port, is_reply=True)

        elif p_type == PacketType.DIRECT_MSG:
            try:
                decrypted_text = self.sec_man.decrypt_hybrid(packet["payload"])
                import datetime
                timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                self.msg_received.emit(timestamp, sender_ip, decrypted_text)
            except Exception as e:
                self.log_signal.emit(f"Decryption error: {e}")