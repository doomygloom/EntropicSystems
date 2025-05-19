import random
from PIL import Image, ImageDraw, ImageFilter

def gooey_overlay(input_path, second_image_path, output_path, goo_width=100, goo_height=100):
        base_image = Image.open(input_path)
        if base_image.mode != 'RGB':
                base_image = base_image.convert('RGB')
        base_width, base_height = base_image.size

        second_image = Image.open(second_image_path)
        if second_image.mode != 'RGB':
                second_image = second_image.convert('RGB')
        second_width, second_height = second_image.size

        if second_width < goo_width or second_height < goo_height:
                scale = max(goo_width / second_width, goo_height / second_height)
                new_width = int(second_width * scale)
                new_height = int(second_height * scale)
                second_image = second_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                second_width, second_height = second_image.size

        x_start = random.randint(0, second_width - goo_width)
        y_start = random.randint(0, second_height - goo_height)
        section = second_image.crop((x_start, y_start, x_start + goo_width, y_start + goo_height))

        mask = Image.new('L', (goo_width, goo_height), 0)
        draw = ImageDraw.Draw(mask)

        points = [
                (random.randint(int(goo_width/5), int(goo_width/2.5)), random.randint(int(goo_height/5), int(goo_height/2.5))),
                (random.randint(int(goo_width/1.7), int(goo_width/1.25)), random.randint(int(goo_height/5), int(goo_height/2.5))),
                (random.randint(int(goo_width/1.25), int(goo_width/1.1)), random.randint(int(goo_height/2.5), int(goo_height/1.7))),
                (random.randint(int(goo_width/1.7), int(goo_width/1.25)), random.randint(int(goo_height/1.7), int(goo_height/1.25))),
                (random.randint(int(goo_width/5), int(goo_width/2.5)), random.randint(int(goo_height/1.7), int(goo_height/1.25))),
                (random.randint(int(goo_width/10), int(goo_width/5)), random.randint(int(goo_height/2.5), int(goo_height/1.7)))
        ]
        draw.polygon(points, fill=255)

        #drip_size = min(goo_width, goo_height) // 20
        #for _ in range(3):
        #    drip_x = random.randint(0, goo_width)
        #    drip_y = random.randint(0, goo_height)
        #    draw.ellipse([drip_x - drip_size, drip_y - drip_size, drip_x + drip_size, drip_y + drip_size], fill=255)

        mask = mask.filter(ImageFilter.GaussianBlur(radius=0))

        gooey_section = Image.new('RGBA', (goo_width, goo_height), (0, 0, 0, 0))
        gooey_section.paste(section, (0, 0), mask)

        grid_cell_width = max(goo_width // 2, base_width // 20)
        grid_cell_height = max(goo_height // 2, base_height // 20)

        num_x_junctions = (base_width - goo_width) // grid_cell_width + 1
        num_y_junctions = (base_height - goo_height) // grid_cell_height + 1

        num_x_junctions = max(1, num_x_junctions)
        num_y_junctions = max(1, num_y_junctions)

        grid_x = random.randint(0, num_x_junctions - 1)
        grid_y = random.randint(0, num_y_junctions - 1)

        paste_x = grid_x * grid_cell_width
        paste_y = grid_y * grid_cell_height

        paste_x = min(paste_x, base_width - goo_width)
        paste_y = min(paste_y, base_height - goo_height)

        print(f"Pasting at: ({paste_x}, {paste_y})")

        base_image.paste(gooey_section, (paste_x, paste_y), gooey_section)

        if base_image.mode == 'RGBA':
                base_image = base_image.convert('RGB')

        base_image.save(output_path, 'JPEG')
