# Torna messenger

<img width="658" height="529" alt="изображение" src="https://github.com/user-attachments/assets/cc02cc1a-f7bf-4940-8a6b-f0e3d25543da" />

# Usage:
## Установите зависимости:
```bash
pip install PySide6 cryptography
```

## Запуск
Запустите `main.py` на **Компьютере А** и **Компьютере Б**.

## Настройка Компьютера А
- **Your Name**: Alice  
- **Own Port**: 5000 (нажмите **Apply**)  
- **Target IP**: `<IP Компьютера Б>`  
- **Target Port**: 5000  

## Настройка Компьютера Б
- **Your Name**: Bob  
- **Own Port**: 5000 (нажмите **Apply**)  
- **Target IP**: `<IP Компьютера А>`  
- **Target Port**: 5000  

## Обмен сообщениями
- При первой попытке отправить сообщение система обнаружит, что у неё нет публичного ключа получателя.  
- Она автоматически отправит **HANDSHAKE**-пакет.  
- В логе получателя появится: `Handshake received.`  
- Нажмите **«Отправить»** второй раз — сообщение будет зашифровано и отправлено.
```
