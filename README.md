# pomidorik
timer for timemanagement

## pyqt версия
- python3.12
- PyQt6
### рекурсивная установка зависимостей для pyqt версии приложения
- python3.12 -m venv .venv
- source .venv/Scripts/activate
- pip install -r requirements.txt
### Для создания исполнимого файла .exe под Windows:
- выключить антивирусы
- pip install Pyinstaller
- pyinstaller --onefile -w pomodorik.py
