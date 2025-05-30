# BottleWebProject_C224_3_FYSP

## Описание проекта

**GRAFSYS** — это веб-приложение, реализующее базовые алгоритмы из теории графов. Приложение позволяет выполнять обход неориентированных графов, строить остовные деревья и производить раскраску графа с минимальным числом цветов. Пользователь может задать граф с помощью матрицы смежности или/и матрицы весов и получить результат в виде новых матриц и визуализации.

Проект разработан в учебных целях, для закрепления знаний по теме "Элементы теории графов".

## Участники проекта

* Фокин Денис
* Якимович Андрей
* Петров Артём
* Стрельников Максим

## Платформа и технологии

* **Язык программирования:** Python 3.9 и выше
* **Веб-фреймворк:** Bottle
* **Среда разработки:** Visual Studio 2022

## Возможности

* Задание графа с помощью матрицы смежности или матрицы весов
* Построение остовных деревьев:

  * Поиск в ширину (BFS)
  * Поиск в глубину (DFS)
  * Поиск по лучу (Beam Search)
* Раскраска графа минимальным числом цветов (жадный алгоритм)
* Визуализация результата и вывод итоговых матриц

## Системные требования

* Python 3.9 или выше
* Операционная система Windows 10/11, Linux, MacOS
* Современный веб-браузер (Chrome, Firefox, Edge и т.д.)

## Установка и настройка
1. Склонировать репозиторий проекта
   ```bash
   git clone https://github.com/art2535/BottleWebProject_C224_3_FYSP.git
   ```

2. Открыть проект в Visual Studio 2022

3. После открытия проекта Visual Studio предложит установить виртуальную среду окружения с дополнительными библиотеками для работы

4. Запустить проект
   ```bash
   python app.py
   ```

5. Перейти по адресу в браузере
   [http://localhost:8080](http://localhost:8080)

## Инструкции по управлению
* Введите количество вершин и матрицу смежности или весов
* Выберите нужный алгоритм:
  * BFS – построение остовного дерева в ширину
  * DFS – построение остовного дерева в глубину
  * Beam Search – построение остовного дерева по лучу
  * Coloring – раскраска графа
* Нажмите "Построить граф"
* Результат появится на экране: матрица смежности дерева/раскраска и визуализация

Для остановки сервера используйте `Ctrl+C` в терминале.

## Примеры использования

### Ввод:

* Количество вершин: `5`

* Матрица смежности:

  ```
  0 1 1 0 0
  1 0 1 1 0
  1 1 0 0 1
  0 1 0 0 1
  0 0 1 1 0
  ```

* Выбран алгоритм: `DFS`

### Вывод:

* Матрица смежности остовного дерева (DFS):

  ```
  0 1 0 0 0
  1 0 1 0 0
  0 1 0 1 0
  0 0 1 0 1
  0 0 0 1 0
  ```

* Совместимость: OK

* Визуализация графа: ✓

## Текущая версия

* Стабильная версия: **1.0.0** (по состоянию на 14.05.2025)
* Тесты: ручное тестирование
* Поддержка автоматических тестов планируется в будущем

## Лицензия

**Нет**

## Контактная информация

Если у вас есть вопросы или предложения, свяжитесь с нами:

**Email:** 
* [fokindenlelush2006@gmail.com](mailto:fokindenlelush2006@gmail.com)
* [artem010606@yandex.ru](mailto:artem010606@yandex.ru)

## Инструкции по обновлению

1. Скачайте новую версию из репозитория
2. Замените старые файлы новыми
3. Перезапустите приложение:

   ```bash
   python app.py
   ```
