from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import random
import numpy as np

# X: @owldecoy

def shift_flux(input_path, output_path, shift_range=(-10, 333), row_step=1, max_flux=1000):
    """
    Applies a horizontal flux effect by randomly shifting rows of pixels within a specified range, creating a glitch effect.

    Args:
        input_path (str): The file path to the input image.
        output_path (str): The file path where the modified image will be saved in JPEG format.
        shift_range (tuple, optional): The range of pixel shifts to apply, as a tuple of (min_shift, max_shift). Default is (-10, 333).
        row_step (int, optional): The step size for selecting rows to apply the flux effect. Default is 1 pixel.
        max_flux (int, optional): The maximum amount of flux applied to the image (currently unused). Default is 1000.
    """

        image = Image.open(input_path)
        if image.mode != 'RGB':
                image = image.convert('RGB')
        width, height = image.size

        img_array = np.array(image)
        rows, cols, _ = img_array.shape

        for i in range(0, rows, row_step):
                shift_value = random.randint(*shift_range)
                img_array[i] = np.roll(img_array[i], shift_value, axis=0)

        glitched_image = Image.fromarray(img_array)

        glitched_image = ImageEnhance.Contrast(glitched_image).enhance(1.0)
        #glitched_image = glitched_image.filter(ImageFilter.GaussianBlur(radius=0.5))

        if glitched_image.mode == 'RGBA':
                glitched_image = glitched_image.convert('RGB')

        glitched_image.save(output_path, 'JPEG')


def shift_flux_area(input_path, output_path, shift_range=(-10, 333), row_step=1, max_flux=1000, size=200):
    """
    Applies a localized horizontal flux effect to a randomly selected area of the image by shifting rows of pixels within a specified range.

    Args:
        input_path (str): The file path to the input image.
        output_path (str): The file path where the modified image will be saved in JPEG format.
        shift_range (tuple, optional): The range of pixel shifts to apply, as a tuple of (min_shift, max_shift). Default is (-10, 333).
        row_step (int, optional): The step size for selecting rows to apply the flux effect. Default is 1 pixel.
        max_flux (int, optional): The maximum amount of flux applied to the selected area (currently unused). Default is 1000.
        size (int, optional): The size of the square area to be processed. Default is 200 pixels.
    """

        image = Image.open(input_path)
        if image.mode != 'RGB':
                image = image.convert('RGB')
        width, height = image.size

        result_image = image.copy()

        area_x = random.randint(0, width - 1)
        area_y = random.randint(0, height - 1)

        left = max(0, area_x)
        top = max(0, area_y)
        right = min(width, area_x + size)
        bottom = min(height, area_y + size)

        area_width = right - left
        area_height = bottom - top

        area = image.crop((left, top, right, bottom))

        img_array = np.array(area)
        rows, cols, _ = img_array.shape

        for i in range(0, rows, row_step):
                shift_value = random.randint(*shift_range)
                img_array[i] = np.roll(img_array[i], shift_value, axis=0)

        glitched_area = Image.fromarray(img_array)

        glitched_area = ImageEnhance.Contrast(glitched_area).enhance(1.0)
        # uncomment for blur
        # glitched_area = glitched_area.filter(ImageFilter.GaussianBlur(radius=0.5))

        result_image.paste(glitched_area, (left, top))

        if result_image.mode == 'RGBA':
                result_image = result_image.convert('RGB')

        result_image.save(output_path, 'JPEG')
