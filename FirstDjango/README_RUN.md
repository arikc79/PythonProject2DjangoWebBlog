Запуск серверу (Windows)

Інструкції:

1) Відкрийте CMD або PowerShell.
2) Перейдіть у папку проекту:
   cd /d D:\Step\StepPyton2409\PythonProject2Django3\FirstDjango

3) Запустіть:
   - Для cmd: run_server.bat
   - Для PowerShell: .\run_server.ps1

Сценарій створить (якщо потрібно) віртуальне оточення `env`, встановить залежності з requirements.txt (або django + python-dotenv), застосує міграції і запустить dev-server на 127.0.0.1:8000.

Якщо виникнуть помилки, пришліть вивід терміналу сюди.
