# Anleitung zum erstellen der .exe Datei
1. pip install pyinstaller
2. Navigiere in der Konsole zu einem Ordner, indem Sie die Datei haben wollen (gleicher Ordner geht nicht)
3. python -m PyInstaller --onefile --noconsole --name SZI-Chatbot-Manager path\to\file\gui.py
4. .exe Datei im generierten dist Verzeichnis