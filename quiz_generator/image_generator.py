import textwrap
from PIL import Image, ImageDraw
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter
import io



def add_code_to_console(code_text, padding_top, padding_sides, font_path, font_size):
    processed_lines = []

    # Обрабатываем каждую строку текста
    for line in code_text.splitlines():
        stripped_line = line.strip()

        # Если строка пустая, добавляем её без изменений
        if not stripped_line:
            processed_lines.append(line)
            continue

        # Обработка существующих комментариев, оставляем как есть
        if stripped_line.startswith('#'):
            wrapped_line = textwrap.fill(line, width=60)
            processed_lines.extend(wrapped_line.splitlines())
            continue

        # Обработка строк кода (начинаются с ключевых слов или имеют отступы)
        if (line.lstrip().startswith(('def', 'class', 'print', 'return', 'import')) or
                '=' in line or '**' in line or line[0].isspace()):
            wrapped_code_line = textwrap.fill(line, width=60)
            processed_lines.extend(wrapped_code_line.splitlines())
            continue

        # Для остальных строк добавляем символ # и переносим длинные строки
        wrapped_description = textwrap.fill(line.strip(), width=60)
        for wrapped_line in wrapped_description.splitlines():
            processed_lines.append(f"# {wrapped_line}")

    # Соединяем строки обратно
    wrapped_code = "\n".join(processed_lines)

    # Подсветка синтаксиса с помощью Pygments
    lexer = PythonLexer()
    formatter = ImageFormatter(font_name=font_path, font_size=font_size, line_numbers=False, style="monokai",
                               image_pad=10, background="dark")

    # Сгенерировать изображение с подсветкой кода
    code_image_data = highlight(wrapped_code, lexer, formatter)

    # Открытие изображения с подсвеченным кодом
    code_image = Image.open(io.BytesIO(code_image_data)).convert("RGBA")

    # Прозрачность для темных областей
    datas = code_image.getdata()
    new_data = [(255, 255, 255, 0) if item[0] < 50 and item[1] < 50 and item[2] < 50 else item for item in datas]
    code_image.putdata(new_data)

    # Вычисляем размеры текста
    code_image_width, code_image_height = code_image.size

    # Динамическое изменение размеров консоли
    console_width = code_image_width + 2 * padding_sides
    console_height = code_image_height + padding_top + padding_sides

    # Создаем пустое изображение для консоли (с прозрачностью)
    console_image = Image.new("RGBA", (console_width, console_height), (0, 0, 0, 0))

    # Создаем объект для рисования на консоли
    draw_console = ImageDraw.Draw(console_image)

    # Рисуем чёрный прямоугольник для консоли
    draw_console.rounded_rectangle([(0, 0), (console_width, console_height)], radius=30, fill=(30, 30, 30))

    # Центрирование текста внутри консоли
    paste_x = (console_width - code_image_width) // 2
    paste_y = padding_top

    # Вставляем изображение с кодом в консоль
    console_image.paste(code_image, (paste_x, paste_y), code_image)

    return console_image, console_width, console_height




def create_console_image_with_code(code_text: str, output_image_path: str, logo_path: str):
    width, height = 1000, 700  # Размер фона
    padding_top = 50  # Увеличенный отступ сверху
    padding_sides = 50  # Увеличенные отступы по бокам
    font_path = "/Library/Fonts/Arial Unicode.ttf"
    font_size = 26  # Увеличенный размер шрифта

    # Создаем фон изображения с фоновым цветом
    background_color = (173, 216, 230)  # Светло-синий фон
    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # Генерация консоли с текстом
    console_image, console_width, console_height = add_code_to_console(code_text, padding_top, padding_sides, font_path, font_size)

    # Центрирование консоли по фону
    console_x0 = (width - console_width) // 2
    console_y0 = (height - console_height) // 2

    # Вставляем консоль на фон
    image.paste(console_image, (console_x0, console_y0), console_image)

    # Рисуем кнопки управления (красную, жёлтую и зелёную точки)
    circle_radius = 16  # Увеличиваем размер кнопок
    circle_spacing = 25  # Увеличиваем отступы между кнопками
    circle_y = console_y0 + 20  # Позиция кнопок

    # Красная точка
    draw.ellipse((console_x0 + circle_spacing, circle_y, console_x0 + circle_spacing + 2 * circle_radius,
                  circle_y + 2 * circle_radius), fill=(255, 59, 48))
    # Жёлтая точка
    draw.ellipse((console_x0 + 3 * circle_spacing, circle_y, console_x0 + 3 * circle_spacing + 2 * circle_radius,
                  circle_y + 2 * circle_radius), fill=(255, 204, 0))
    # Зелёная точка
    draw.ellipse((console_x0 + 5 * circle_spacing, circle_y, console_x0 + 5 * circle_spacing + 2 * circle_radius,
                  circle_y + 2 * circle_radius), fill=(40, 205, 65))

    # Добавляем логотип в правый верхний угол
    add_logo(image, logo_path)

    # Сохранить изображение
    image.save(output_image_path)


def add_logo(image: Image, logo_path: str):
    """
    Добавляет логотип в правый верхний угол изображения.
    :param image: Изображение, на которое нужно добавить логотип.
    :param logo_path: Путь к файлу логотипа.
    """
    logo = Image.open("media/administration/logo_no_back.png")

    # Конвертируем логотип в формат RGBA (чтобы поддерживалась прозрачность)
    if logo.mode != 'RGBA':
        logo = logo.convert('RGBA')

    # Изменяем размер логотипа под картинку (например, 10% от ширины изображения)
    logo_width = int(image.width * 0.1)
    logo_height = int(logo_width * logo.height / logo.width)
    logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)

    # Определяем позицию для логотипа в правом верхнем углу
    position = (image.width - logo_width - 10, 10)  # 10 пикселей отступ от правого верхнего угла

    # Добавляем логотип на изображение
    image.paste(logo, position, logo)
