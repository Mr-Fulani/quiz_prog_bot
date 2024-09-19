from PIL import Image, ImageDraw, ImageFont
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter
import io


def add_code_to_console(code_text, font_path, min_font_size=12, max_font_size=24):
    console_width, console_height = 700, 250
    padding_top = 40
    padding_bottom = 20
    padding_sides = 20
    dot_area = 50  # Area reserved for control dots

    lexer = PythonLexer()

    while True:
        formatter = ImageFormatter(font_name=font_path, font_size=max_font_size, line_numbers=False,
                                   style="monokai", background="dark")  # Устанавливаем тёмный фон


        code_image_data = highlight(code_text, lexer, formatter)
        code_image = Image.open(io.BytesIO(code_image_data)).convert("RGBA")



        # Удаляем фон (чёрные пиксели)
        data = code_image.getdata()
        new_data = []
        for item in data:
            # Если цвет пикселя близок к чёрному, делаем его прозрачным
            if item[:3] == (0, 0, 0):
                new_data.append((0, 0, 0, 0))  # Прозрачный цвет
            else:
                new_data.append(item)
        code_image.putdata(new_data)


        if (code_image.width <= console_width - 2 * padding_sides - dot_area and
                code_image.height <= console_height - padding_top - padding_bottom):
            break

        max_font_size -= 1
        if max_font_size < min_font_size:
            max_font_size = min_font_size
            break

    code_x = padding_sides + dot_area
    code_y = padding_top + (console_height - padding_top - padding_bottom - code_image.height) // 2

    return code_image, (code_x, code_y)


def create_console_image_with_code(code_text: str, output_image_path: str, logo_path: str):
    width, height = 800, 500
    font_path = "/Library/Fonts/Arial Unicode.ttf"
    background_color = (173, 216, 230)
    console_color = (0, 0, 0, 255)

    # Create background
    image = Image.new("RGBA", (width, height), background_color + (255,))
    draw = ImageDraw.Draw(image)

    # Create console
    console_width, console_height = 700, 250
    console_x = (width - console_width) // 2
    console_y = (height - console_height) // 2

    # Draw rounded rectangle for console
    corner_radius = 20
    console = Image.new("RGBA", (console_width, console_height), (0, 0, 0, 0))
    console_draw = ImageDraw.Draw(console)
    console_draw.rounded_rectangle([(0, 0), (console_width, console_height)],
                                   radius=corner_radius, fill=console_color)

    # Add code to console
    code_image, (code_x, code_y) = add_code_to_console(code_text, font_path)
    console.paste(code_image, (code_x, code_y), code_image)

    # Add control dots
    circle_radius = 8
    circle_spacing = 25
    circle_y = 15
    for color in [(255, 59, 48), (255, 204, 0), (40, 205, 65)]:
        console_draw.ellipse((circle_spacing, circle_y,
                              circle_spacing + 2 * circle_radius,
                              circle_y + 2 * circle_radius), fill=color)
        circle_spacing += 30

    # Paste console onto background
    image.paste(console, (console_x, console_y), console)

    # Add logo
    add_logo(image, logo_path)

    # Save image
    image.save(output_image_path)


def add_logo(image: Image, logo_path: str):
    logo = Image.open(logo_path)
    if logo.mode != 'RGBA':
        logo = logo.convert('RGBA')
    logo_width = int(image.width * 0.1)
    logo_height = int(logo_width * logo.height / logo.width)
    logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
    position = (image.width - logo_width - 10, 10)
    image.paste(logo, position, logo)