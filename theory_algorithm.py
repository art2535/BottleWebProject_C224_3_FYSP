import markdown  # Импортируем модуль для преобразования Markdown в HTML

def get_theory(pathToFile):
    """
    Читает содержимое Markdown-файла по указанному пути и возвращает его в виде HTML.

    Вход:
        pathToFile (str): Путь к .md файлу с теорией.

    Выход:
        str: HTML-версия текста, если успешно.
             Сообщение об ошибке, если произошёл сбой при чтении или парсинге.
    """
    try:
        # Открываем файл в режиме чтения
        with open(pathToFile) as file:
            theory_md = file.read()  # Считываем весь текст из файла

        # Преобразуем Markdown-текст в HTML
        theory_html = markdown.markdown(theory_md)

        return theory_html  # Возвращаем HTML-версию теории

    except Exception as e:
        # В случае любой ошибки возвращаем её описание
        return f"Error loading theory: {e}"
