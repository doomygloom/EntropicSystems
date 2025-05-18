from PIL import Image, ImageEnhance, ImageFilter
import random
import numpy as np

# X: @owldecoy

def pixel_sort(input_path, output_path, row_step=20, sort_height=10, angle=0, contrast=False):

        image = Image.open(input_path)
        if image.mode != 'RGB':
                image = image.convert('RGB')
        width, height = image.size

        original_width, original_height = image.size

        rotated_image = image.rotate(angle, expand=True)
        img_array = np.array(rotated_image)
        rows, cols, _ = img_array.shape

        glitch_array = np.copy(img_array)

        for i in range(0, rows, row_step):
                if random.random() > 0.8:
                        end_row = min(i + sort_height, rows)
                        glitch_array[i:end_row] = np.sort(glitch_array[i:end_row], axis=1)

        glitched_image = Image.fromarray(glitch_array)
        final_image = glitched_image.rotate(-angle, expand=True)

        left = (final_image.width - original_width) // 2
        top = (final_image.height - original_height) // 2
        right = left + original_width
        bottom = top + original_height
        final_image = final_image.crop((left, top, right, bottom))

        if contrast:
                final_image = ImageEnhance.Contrast(final_image).enhance(1.3)
                #final_image = final_image.filter(ImageFilter.EDGE_ENHANCE)

        if final_image.mode == 'RGBA':
                final_image = final_image.convert('RGB')

        final_image.save(output_path, 'JPEG')
