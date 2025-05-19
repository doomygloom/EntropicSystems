import random
from PIL import Image

# X: @owldecoy

def chaos_brush(input_path, output_path, brush_size=100, brush_strokes=42, second_image=None):
    """
    Creates a chaotic brush stroke effect using a brush_size x brush_size area as a transparent brush tip.
    Optionally uses a second image as the source for the brush tip.

    Args:
        input_path (str): Path to the input image
        output_path (str): Path where the result will be saved
        brush_size (int): Size of the brush tip (default: 100)
        brush_strokes (int): Number of brush strokes to apply (default: 42)
        second_image (str, optional): Path to a second image to use for the brush tip
    """
    image = Image.open(input_path).convert('RGBA')
    width, height = image.size

    if second_image:
        brush_source = Image.open(second_image).convert('RGBA')
        brush_width, brush_height = brush_source.size
    else:
        brush_source = image
        brush_width, brush_height = width, height

    try:
        brush_x = random.randint(0, brush_width - brush_size)
        brush_y = random.randint(0, brush_height - brush_size)
    except ValueError:
        print("[!] brush size exceeded brush source dimensions, trying with smaller size...")
        brush_size = min(brush_width, brush_height)
        brush_x = random.randint(0, brush_width - brush_size)
        brush_y = random.randint(0, brush_height - brush_size)

    brush_tip = brush_source.crop((brush_x, brush_y, brush_x + brush_size, brush_y + brush_size))

    mask = Image.new('L', (brush_size, brush_size), 255)

    output_image = image.copy()

    try:
        current_x = random.randint(0, width - brush_size)
        current_y = random.randint(0, height - brush_size)
    except ValueError:
        current_x = 0
        current_y = 0

    for _ in range(brush_strokes):
        rotation = random.randint(-45, 45)
        rotated_brush = brush_tip.rotate(rotation, expand=False)
        rotated_mask = mask.rotate(rotation, expand=False)

        output_image.paste(rotated_brush, (current_x, current_y), rotated_mask)

        angle = random.uniform(0, 2 * 3.14159)
        step_size = random.randint(11, 142)

        next_x = current_x + int(step_size * random.uniform(-1, 1))
        next_y = current_y + int(step_size * random.uniform(-1, 1))

        current_x = max(0, min(next_x, width - brush_size))
        current_y = max(0, min(next_y, height - brush_size))

    if output_image.mode == 'RGBA':
        output_image = output_image.convert('RGB')

    output_image.save(output_path, 'JPEG')
