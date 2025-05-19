import random
import numpy as np
from PIL import Image, ImageEnhance

# X: @owldecoy

def geo3d(input_path, output_path, area_size=300, contrast_factor=1.5, shadow_alpha=200):
        """
        Takes a 300x300px area from an image, creates a faux-3D geometric object from its parts with contrast,
        and overlays it onto a random area of the input image.

        Args:
                input_path (str): Path to the input image
                output_path (str): Path where the result will be saved
                area_size (int): Size of the square area to use (default: 300)
                contrast_factor (float): Contrast adjustment for the shape (1.0 = no change, >1.0 = more, <1.0 = less)
        """
        image = Image.open(input_path).convert('RGBA')
        width, height = image.size

        area_size = min(area_size, width, height)

        try:
                source_x = random.randint(0, width - area_size)
                source_y = random.randint(0, height - area_size)
        except ValueError:
                source_x, source_y = 0, 0

        source_area = image.crop((source_x, source_y, source_x + area_size, source_y + area_size))

        object_size = int(area_size * 1.5)
        object_canvas = Image.new('RGBA', (object_size, object_size), (0, 0, 0, 0))

        source_pixels = source_area.load()
        rand_x = random.randint(0, area_size - 1)
        rand_y = random.randint(0, area_size - 1)
        shadow_color = source_pixels[rand_x, rand_y][:3]
        shadow_color_with_alpha = shadow_color + (shadow_alpha,)

        parts = [
                source_area.crop((0, 0, area_size, area_size // 2)),
                source_area.crop((0, area_size // 2, area_size // 2, area_size)),
                source_area.crop((area_size // 2, area_size // 2, area_size, area_size)),
        ]

        shape_type = random.choice(['prism', 'pyramid', 'cube', 'cylinder', 'tetrahedron'])

        if shape_type == 'prism':
                faces = []
                for i, part in enumerate(parts):
                        part_enhanced = ImageEnhance.Contrast(part).enhance(contrast_factor)
                        shear = random.uniform(-0.3, 0.3)
                        distorted = part_enhanced.transform(
                                (area_size, area_size),
                                Image.AFFINE,
                                (1, shear, 0, 0, 1, 0),
                                resample=Image.BILINEAR
                        )
                        offset_x, offset_y = i * 20, i * 10
                        faces.append((distorted, (offset_x, offset_y)))

                shadow = Image.new('RGBA', (area_size, area_size), shadow_color_with_alpha)
                shadow = shadow.transform(
                        (area_size, area_size),
                        Image.AFFINE,
                        (1, 0.5, 0, 0, 1, 0),
                        resample=Image.BILINEAR
                )
                object_canvas.paste(shadow, (30, 30), shadow)
                for face, (dx, dy) in faces:
                        object_canvas.paste(face, (dx, dy), face)

        elif shape_type == 'pyramid':
                base = ImageEnhance.Contrast(parts[0]).enhance(contrast_factor).resize((area_size, area_size), Image.LANCZOS)
                side1 = ImageEnhance.Contrast(parts[1]).enhance(contrast_factor).transform(
                        (area_size // 2, area_size),
                        Image.PERSPECTIVE,
                        (1, 0, 0, 0, 1, 0, -0.002, 0),
                        resample=Image.BILINEAR
                )
                side2 = ImageEnhance.Contrast(parts[2]).enhance(contrast_factor).transform(
                        (area_size // 2, area_size),
                        Image.PERSPECTIVE,
                        (1, 0, 0, 0, 1, 0, 0.002, 0),
                        resample=Image.BILINEAR
                )
                shadow = Image.new('RGBA', (area_size, area_size), shadow_color_with_alpha)
                object_canvas.paste(shadow, (30, 30), shadow)
                object_canvas.paste(base, (0, 0), base)
                object_canvas.paste(side1, (0, 0), side1)
                object_canvas.paste(side2, (area_size // 2, 0), side2)

        elif shape_type == 'cube':
                front = ImageEnhance.Contrast(parts[0]).enhance(contrast_factor).resize((area_size, area_size), Image.LANCZOS)
                top = ImageEnhance.Contrast(parts[1]).enhance(contrast_factor).transform(
                        (area_size, area_size // 2),
                        Image.AFFINE,
                        (1, 0.5, 0, 0, 1, 0),
                        resample=Image.BILINEAR
                )
                right = ImageEnhance.Contrast(parts[2]).enhance(contrast_factor).transform(
                        (area_size // 2, area_size),
                        Image.AFFINE,
                        (1, 0, 0, -0.5, 1, 0),
                        resample=Image.BILINEAR
                )
                shadow = Image.new('RGBA', (area_size, area_size), shadow_color_with_alpha)
                object_canvas.paste(shadow, (30, 30), shadow)
                object_canvas.paste(front, (20, 20), front)
                object_canvas.paste(top, (20, 0), top)
                object_canvas.paste(right, (area_size // 2 + 20, 20), right)

        elif shape_type == 'cylinder':
                top = ImageEnhance.Contrast(parts[0]).enhance(contrast_factor).resize((area_size, area_size), Image.LANCZOS)
                side = ImageEnhance.Contrast(parts[1]).enhance(contrast_factor).transform(
                        (area_size, area_size),
                        Image.PERSPECTIVE,
                        (1, 0, 0, 0, 1, 0, 0.002, 0.002),
                        resample=Image.BILINEAR
                )
                shadow = Image.new('RGBA', (area_size, area_size), shadow_color_with_alpha)
                object_canvas.paste(shadow, (30, 30), shadow)
                object_canvas.paste(side, (0, 0), side)
                object_canvas.paste(top, (0, -area_size // 4), top)

        elif shape_type == 'tetrahedron':
                base = ImageEnhance.Contrast(parts[0]).enhance(contrast_factor).transform(
                        (area_size, area_size),
                        Image.PERSPECTIVE,
                        (1, 0, 0, 0, 1, 0, 0.001, 0.001),
                        resample=Image.BILINEAR
                )
                side1 = ImageEnhance.Contrast(parts[1]).enhance(contrast_factor).transform(
                        (area_size // 2, area_size),
                        Image.PERSPECTIVE,
                        (1, 0, 0, 0, 1, 0, -0.003, 0),
                        resample=Image.BILINEAR
                )
                side2 = ImageEnhance.Contrast(parts[2]).enhance(contrast_factor).transform(
                        (area_size // 2, area_size),
                        Image.PERSPECTIVE,
                        (1, 0, 0, 0, 1, 0, 0.003, 0),
                        resample=Image.BILINEAR
                )
                shadow = Image.new('RGBA', (area_size, area_size), shadow_color_with_alpha)
                object_canvas.paste(shadow, (30, 30), shadow)
                object_canvas.paste(base, (0, 0), base)
                object_canvas.paste(side1, (0, 0), side1)
                object_canvas.paste(side2, (area_size // 2, 0), side2)

        max_x = max(0, width - object_size)
        max_y = max(0, height - object_size)
        overlay_x = random.randint(0, max_x)
        overlay_y = random.randint(0, max_y)

        output_image = image.copy()
        output_image.paste(object_canvas, (overlay_x, overlay_y), object_canvas)

        if output_image.mode == 'RGBA':
                output_image = output_image.convert('RGB')

        output_image.save(output_path, 'JPEG')
