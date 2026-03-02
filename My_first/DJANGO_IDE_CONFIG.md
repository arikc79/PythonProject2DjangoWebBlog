# PyCharm/VS Code Django Settings

# Це файл для налаштування IDE розпізнавати Django модулі

# Додайте наступне в PyCharm:
# 1. File → Settings → Project → Django
# 2. Включіть: Enable Django Support
# 3. Django project root: D:\Step\StepPyton2409\PythonProject2Django3\My_first
# 4. Settings: My_first/settings.py
# 5. Manage script: manage.py

# Для VS Code додайте в .vscode/settings.json:
"""
{
    "python.linting.pylintArgs": [
        "--load-plugins=pylint_django",
        "--django-settings-module=My_first.settings"
    ],
    "python.formatting.provider": "black",
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/Scripts/python.exe"
}
"""

# Проект повністю функціональний!
# Помилки IDE можна ігнорувати - вони не впливають на роботу проекту.

