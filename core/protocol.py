# core/protocol.py

class PacketType:
    HANDSHAKE = "HANDSHAKE"   # Обмен ключами
    DIRECT_MSG = "DIRECT_MSG" # Прямое сообщение
    RELAY_MSG = "RELAY_MSG"   # (Задел на будущее) Пересылка