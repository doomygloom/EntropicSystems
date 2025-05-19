import random
import numpy as np
from PIL import Image

def fractal_generator(input_path, output_path, tile_size=10, max_iter=20, blend_factor=0.7):
       
        image = Image.open(input_path)
        if image.mode != 'RGB':
                image = image.convert('RGB')
        width, height = image.size

        result_image = image.copy()

        grid_size = min(9, width // tile_size, height // tile_size)

        area_size = grid_size * tile_size

        area_x = random.randint(0, width - area_size) if width > area_size else 0
        area_y = random.randint(0, height - area_size) if height > area_size else 0

        left = area_x
        top = area_y
        right = min(width, area_x + area_size)
        bottom = min(height, area_y + area_size)

        area_width = right - left
        area_height = bottom - top

        original_area = image.crop((left, top, right, bottom))
        original_array = np.array(original_area, dtype=np.float32) / 255.0

        def get_random_color(img):
                while True:
                        x = random.randint(0, width - 1)
                        y = random.randint(0, height - 1)
                        r, g, b = img.getpixel((x, y))
                        if (r, g, b) != (0, 0, 0) and (r, g, b) != (255, 255, 255):
                                return (r, g, b)

        background_color = get_random_color(image)

        generative_area = Image.new('RGB', (area_width, area_height), background_color)

        def sample_tile():
                x = random.randint(0, width - tile_size)
                y = random.randint(0, height - tile_size)
                return image.crop((x, y, x + tile_size, y + tile_size))

        x = np.linspace(-2, 1, grid_size)
        y = np.linspace(-1.5, 1.5, grid_size)
        X, Y = np.meshgrid(x, y)
        C = X + 1j * Y # complex plane
        Z = np.zeros_like(C, dtype=complex)
        mask = np.ones_like(C, dtype=bool)

        for _ in range(max_iter):
                Z[mask] = Z[mask] * Z[mask] + C[mask]
                mask = np.abs(Z) < 4

        for i in range(grid_size):
                for j in range(grid_size):
                        if mask[i, j]:
                                tile = sample_tile()
                                generative_area.paste(tile, (j * tile_size, i * tile_size))

        generative_array = np.array(generative_area, dtype=np.float32) / 255.0

        blended_array = (blend_factor * generative_array) + ((1 - blend_factor) * original_array)
        blended_array = np.clip(blended_array, 0, 1) * 255
        blended_image = Image.fromarray(blended_array.astype(np.uint8))

        result_image.paste(blended_image, (left, top))

        if result_image.mode == 'RGBA':
                result_image = result_image.convert('RGB')

        result_image.save(output_path, 'JPEG')
