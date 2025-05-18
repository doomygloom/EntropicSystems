from PIL import Image, ImageDraw
import random
import math

def generate_line_drawing(input_path, output_path, num_lines=50, line_thickness=1, line_length=100, anti_alias=True):
  
        base_image = Image.open(input_path)
        if base_image.mode != 'RGBA':
                base_image = base_image.convert('RGBA')
        width, height = base_image.size

        rgb_image = base_image.convert('RGB')
        x_sample = random.randint(0, width - 1)
        y_sample = random.randint(0, height - 1)
        line_color_rgb = rgb_image.getpixel((x_sample, y_sample))
        line_color = (line_color_rgb[0], line_color_rgb[1], line_color_rgb[2], 255)

        scale = 4 if anti_alias else 1
        draw_width, draw_height = width * scale, height * scale
        #draw_thickness = line_thickness * scale
        draw_thickness = max(1, int(line_thickness * scale + 0.5))

        drawing_layer = Image.new('RGBA', (draw_width, draw_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(drawing_layer)

        for i in range(num_lines):
                x1 = random.randint(0, draw_width)
                y1 = random.randint(0, draw_height)

                line_type = random.choice(['single', 'parallel', 'single_angle', 'parallel_angle'])

                adjusted_length = line_length * scale * random.uniform(0.8, 1.2)

                if line_type == 'single':
                        direction = random.choice([0, math.pi / 2, math.pi, 3 * math.pi / 2])
                        x2 = x1 + adjusted_length * math.cos(direction)
                        y2 = y1 + adjusted_length * math.sin(direction)
                        x2 = max(0, min(x2, draw_width - 1))
                        y2 = max(0, min(y2, draw_height - 1))
                        draw.line([(x1, y1), (x2, y2)], fill=line_color, width=draw_thickness)

                elif line_type == 'single_angle':
                        angle = random.uniform(0, 2 * math.pi)
                        x2 = x1 + adjusted_length * math.cos(angle)
                        y2 = y1 + adjusted_length * math.sin(angle)
                        x2 = max(0, min(x2, draw_width - 1))
                        y2 = max(0, min(y2, draw_height - 1))
                        draw.line([(x1, y1), (x2, y2)], fill=line_color, width=draw_thickness)

                if line_type == 'parallel':
                        direction = random.choice([0, math.pi / 2])
                        spacing = random.uniform(5, 15) * scale
                        num_parallel = random.randint(2, 5)
                        for j in range(num_parallel):
                                offset_x = j * spacing * math.sin(direction)
                                offset_y = j * spacing * math.cos(direction)
                                x2 = x1 + adjusted_length * math.cos(direction)
                                y2 = y1 + adjusted_length * math.sin(direction)
                                draw.line([(x1 + offset_x, y1 - offset_y), (x2 + offset_x, y2 - offset_y)], 
                                                  fill=line_color, width=draw_thickness)
                                if random.random() < 0.5:
                                        perp_direction = direction + math.pi / 2
                                        x3 = x2 + adjusted_length * math.cos(perp_direction)
                                        y3 = y2 + adjusted_length * math.sin(perp_direction)
                                        x3 = max(0, min(x3, draw_width - 1))
                                        y3 = max(0, min(y3, draw_height - 1))
                                        draw.line([(x2 + offset_x, y2 - offset_y), (x3 + offset_x, y3 - offset_y)], 
                                                          fill=line_color, width=draw_thickness)

                elif line_type == 'parallel_angle':
                        angle = random.uniform(0, 2 * math.pi)
                        spacing = random.uniform(5, 15) * scale
                        num_parallel = random.randint(2, 5)
                        for j in range(num_parallel):
                                offset_x = j * spacing * math.sin(angle)
                                offset_y = j * spacing * math.cos(angle)
                                x2 = x1 + adjusted_length * math.cos(angle)
                                y2 = y1 + adjusted_length * math.sin(angle)
                                draw.line([(x1 + offset_x, y1 - offset_y), (x2 + offset_x, y2 - offset_y)], 
                                                  fill=line_color, width=draw_thickness)

        if anti_alias:
                drawing_layer = drawing_layer.resize((width, height), Image.Resampling.LANCZOS)

        final_image = Image.alpha_composite(base_image, drawing_layer)

        if final_image.mode == 'RGBA':
                final_image = final_image.convert('RGB')

        final_image.save(output_path, 'JPEG')
