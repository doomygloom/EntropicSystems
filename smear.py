import random
import numpy as np
from PIL import Image

# X: @owldecoy

def smear(input_path, output_path, area_size=200, max_steps=300):
        """
        Selects a 200x200px area from an image and smears it over a random length without blending.

        Args:
                input_path (str): Path to the input image
                output_path (str): Path where the result will be saved
                area_size (int): Size of the square area to smear (default: 200)
                max_steps (int): Maximum length of the smear in pixels (default: 300)
        """
        image = Image.open(input_path).convert('RGBA')
        width, height = image.size

        area_size = min(area_size, width, height)

        try:
                start_x = random.randint(0, width - area_size)
                start_y = random.randint(0, height - area_size)
        except ValueError:
                start_x, start_y = 0, 0

        smear_area = image.crop((start_x, start_y, start_x + area_size, start_y + area_size))

        angle = random.uniform(0, 2 * np.pi)
        step_length = random.randint(50, max_steps)

        end_x = start_x + int(step_length * np.cos(angle))
        end_y = start_y + int(step_length * np.sin(angle))

        end_x = max(0, min(end_x, width - area_size))
        end_y = max(0, min(end_y, height - area_size))

        steps = max(abs(end_x - start_x), abs(end_y - start_y)) // 10 + 1

        output_image = image.copy()

        for i in range(steps + 1):
                t = i / steps
                current_x = int(start_x + (end_x - start_x) * t)
                current_y = int(start_y + (end_y - start_y) * t)

                output_image.paste(smear_area, (current_x, current_y), smear_area)

        if output_image.mode == 'RGBA':
                output_image = output_image.convert('RGB')

        output_image.save(output_path, 'JPEG')
