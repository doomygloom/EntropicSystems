from PIL import Image, ImageDraw, ImageFilter
import random

# X:@owldecoy

def data_burn(input_path, output_path, num_burns=None, burn_length=None, dark_burn=False, light_burn=False):

        image = Image.open(input_path)
        if image.mode != 'RGB':
                image = image.convert('RGB')
        width, height = image.size

        glitched_image = image.copy()

        for _ in range(num_burns):
                x_start = random.randint(0, width - 1)
                y_start = random.randint(0, height - burn_length - 1)
                bleed_width = random.randint(5, 200)

                seed_region = glitched_image.crop((x_start, y_start,
                                                                                 min(x_start + bleed_width, width),
                                                                                 y_start + 1))

                for y_offset in range(1, burn_length):
                        y_pos = y_start + y_offset
                        if y_pos >= height:
                                break
                        glitched_image.paste(seed_region, (x_start, y_pos))

                        if dark_burn:
                                seed_region = seed_region.point(lambda p: p * 0.82)  # dark - Uncomment for fade effect

                        elif light_burn:
                                seed_region = seed_region.point(lambda p: p * 1.1)  # light - Uncomment for fade effect

        if glitched_image.mode == 'RGBA':
                glitched_image = glitched_image.convert('RGB')

        glitched_image.save(output_path, 'JPEG')
