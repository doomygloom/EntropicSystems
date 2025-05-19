from PIL import Image, ImageDraw, ImageFilter
import random

# X: @owldecoy

def lineator(input_path, output_path, num_lines=None):
    """
    Reorganizes the image by slicing it into horizontal lines and randomly shuffling the lines.

    Args:
        input_path (str): The file path to the input image.
        output_path (str): The file path where the modified image will be saved in JPEG format.
        num_lines (int, optional): The number of horizontal lines to divide the image into. Default is the entire image height in pixels.
    """

        image = Image.open(input_path)
        if image.mode != 'RGB':
                image = image.convert('RGB')
        width, height = image.size

        line_height = max(1, height // num_lines)
        lines = [image.crop((0, i * line_height, width, (i + 1) * line_height)) for i in range(num_lines)]

        random.shuffle(lines)
        lineated_image = Image.new("RGB", (width, height))

        for i, line in enumerate(lines):
                lineated_image.paste(line, (0, i * line_height))

        if lineated_image.mode == 'RGBA':
                lineated_image = lineated_image.convert('RGB')

        lineated_image.save(output_path, 'JPEG')


def lineator_area(input_path, output_path, num_lines=None, area_width=200, area_height=200):
    """
    Applies the lineator effect to a randomly selected rectangular area of the image by slicing it into horizontal lines and shuffling them.

    Args:
        input_path (str): The file path to the input image.
        output_path (str): The file path where the modified image will be saved in JPEG format.
        num_lines (int, optional): The number of horizontal lines to divide the selected area into. Default is 20.
        area_width (int, optional): The width of the rectangular area to be processed. Default is 200 pixels.
        area_height (int, optional): The height of the rectangular area to be processed. Default is 200 pixels.
    """


        image = Image.open(input_path)
        if image.mode != 'RGB':
                image = image.convert('RGB')
        width, height = image.size

        if num_lines is None:
                num_lines = 20

        area_x = random.randint(0, width - 1)
        area_y = random.randint(0, height - 1)

        area_width = min(area_width, width - area_x)
        area_height = min(area_height, height - area_y)

        result_image = image.copy()

        area = image.crop((area_x, area_y, area_x + area_width, area_y + area_height))

        line_height = max(1, area_height // num_lines)
        actual_num_lines = area_height // line_height
        lines = [area.crop((0, i * line_height, area_width, (i + 1) * line_height))
                         for i in range(actual_num_lines)]

        random.shuffle(lines)

        glitched_area = Image.new("RGB", (area_width, area_height))
        for i, line in enumerate(lines):
                glitched_area.paste(line, (0, i * line_height))

        result_image.paste(glitched_area, (area_x, area_y))

        if result_image.mode == 'RGBA':
                result_image = result_image.convert('RGB')

        result_image.save(output_path, 'JPEG')
