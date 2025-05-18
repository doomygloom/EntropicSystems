from PIL import Image, ImageDraw, ImageFilter
import random

# X:@owldecoy

def cut_and_shuffle(input_path, output_path, num_pieces=None, edge_thickness=10, max_piece_size=100, blur_edges=False):
    image = Image.open(input_path)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    width, height = image.size

    pieces = []
    for _ in range(num_pieces):
        x1, y1 = random.randint(0, width - 1), random.randint(0, height - 1)
        
        min_piece_size = 11
        
        x2 = min(x1 + random.randint(min_piece_size, max_piece_size), width)
        y2 = min(y1 + random.randint(min_piece_size, max_piece_size), height)
        
        if x2 <= x1:
            x2 = x1 + min_piece_size
        if y2 <= y1:
            y2 = y1 + min_piece_size
        if x2 > width:
            x2 = width
        if y2 > height:
            y2 = height
            
        region = image.crop((x1, y1, x2, y2))
        pieces.append(region)

    random.shuffle(pieces)
    glitched_image = image.copy()

    for piece in pieces:
        piece_width, piece_height = piece.size
        
        if blur_edges:
            mask = Image.new('L', (piece_width, piece_height), 0)
            draw = ImageDraw.Draw(mask)
            
            if piece_width > 2 * edge_thickness and piece_height > 2 * edge_thickness:
                draw.rectangle([(0, 0), (piece_width - 1, edge_thickness - 1)], fill=255)
                draw.rectangle([(0, piece_height - edge_thickness), (piece_width - 1, piece_height - 1)], fill=255)
                draw.rectangle([(0, 0), (edge_thickness - 1, piece_height - 1)], fill=255)
                draw.rectangle([(piece_width - edge_thickness, 0), (piece_width - 1, piece_height - 1)], fill=255)
            
            blurred_mask = mask.filter(ImageFilter.GaussianBlur(radius=3))
            
            blurred_piece = piece.filter(ImageFilter.GaussianBlur(radius=5))
            
            edge_blurred_piece = Image.composite(blurred_piece, piece, blurred_mask)
            
            x1, y1 = random.randint(0, width - piece_width), random.randint(0, height - piece_height)
            glitched_image.paste(edge_blurred_piece, (x1, y1))
        else:
            x1, y1 = random.randint(0, width - piece_width), random.randint(0, height - piece_height)
            glitched_image.paste(piece, (x1, y1))

    if glitched_image.mode == 'RGBA':
        glitched_image = glitched_image.convert('RGB')

    glitched_image.save(output_path, 'JPEG')


def cut_and_shuffle_region(input_path, output_path, num_pieces=None, region_size=500):
        image = Image.open(input_path)
        if image.mode != 'RGB':
                image = image.convert('RGB')
        width, height = image.size

        left = random.randint(0, max(0, width - region_size))
        top = random.randint(0, max(0, height - region_size))
        right = min(left + region_size, width)
        bottom = min(top + region_size, height)

        if right - left < region_size:
                left = max(0, width - region_size)
                right = min(width, left + region_size)
        if bottom - top < region_size:
                top = max(0, height - region_size)
                bottom = min(height, top + region_size)

        working_region = image.crop((left, top, right, bottom))
        region_width, region_height = working_region.size

        pieces = []
        for _ in range(num_pieces):
                x1 = random.randint(0, region_width - 1)
                y1 = random.randint(0, region_height - 1)
                x2 = min(x1 + random.randint(9, 142), region_width)
                y2 = min(y1 + random.randint(9, 142), region_height)
                region = working_region.crop((x1, y1, x2, y2))
                pieces.append(region)

        random.shuffle(pieces)
        glitched_region = working_region.copy()

        for piece in pieces:
                x1 = random.randint(0, region_width - piece.width)
                y1 = random.randint(0, region_height - piece.height)
                glitched_region.paste(piece, (x1, y1))

        output_image = image.copy()
        output_image.paste(glitched_region, (left, top))

        if output_image.mode == 'RGBA':
                output_image = output_image.convert('RGB')

        output_image.save(output_path, 'JPEG')
