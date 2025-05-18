import numpy as np
from PIL import Image, ImageFilter, ImageDraw
import random

# X: @owldecoy

def shannon_entropy(input_path, output_path, target_entropy_increase=2.0, num_pieces=10, 
                         max_piece_size=100, noise_factor=0.1, blur_edges=False, disable_cut_shuffle=False):
    
    image = Image.open(input_path).convert('RGB')
    width, height = image.size
    img_array = np.array(image, dtype=np.float32)

    def calc_entropy(arr):
        entropy = 0
        for channel in range(3):
            hist, _ = np.histogram(arr[:, :, channel].flatten(), bins=256, range=(0, 256))
            probs = hist / hist.sum()
            nonzero_probs = probs[probs > 0]
            entropy += -np.sum(nonzero_probs * np.log2(nonzero_probs))
        return entropy / 3

    original_entropy = calc_entropy(img_array)
    print(f"Original Entropy: {original_entropy:.4f} bits")

    if disable_cut_shuffle:
        chaotic_array = img_array.copy()
        noise = np.random.normal(0, noise_factor * 255, chaotic_array.shape)
        chaotic_array += noise
        chaotic_array = np.clip(chaotic_array, 0, 255).astype(np.uint8)
        chaotic_image = Image.fromarray(chaotic_array)
    else:
        pieces = []
        min_piece_size = 11
        for _ in range(num_pieces):
            x1, y1 = random.randint(0, width - 1), random.randint(0, height - 1)
            x2 = min(x1 + random.randint(min_piece_size, max_piece_size), width)
            y2 = min(y1 + random.randint(min_piece_size, max_piece_size), height)
            
            x2 = max(x2, x1 + min_piece_size) if x2 <= x1 else x2
            y2 = max(y2, y1 + min_piece_size) if y2 <= y1 else y2
            x2, y2 = min(x2, width), min(y2, height)
            
            region = image.crop((x1, y1, x2, y2))
            region_array = np.array(region, dtype=np.float32)
            noise = np.random.normal(0, noise_factor * 255, region_array.shape)
            noisy_region = np.clip(region_array + noise, 0, 255).astype(np.uint8)
            pieces.append(Image.fromarray(noisy_region))

        random.shuffle(pieces)
        chaotic_image = image.copy()
        chaotic_array = img_array.copy()

        for piece in pieces:
            piece_width, piece_height = piece.size
            x1, y1 = random.randint(0, width - piece_width), random.randint(0, height - piece_height)
            
            if blur_edges:
                mask = Image.new('L', (piece_width, piece_height), 0)
                draw = ImageDraw.Draw(mask)
                edge_thickness = 10
                if piece_width > 2 * edge_thickness and piece_height > 2 * edge_thickness:
                    draw.rectangle([(0, 0), (piece_width - 1, edge_thickness - 1)], fill=255)
                    draw.rectangle([(0, piece_height - edge_thickness), (piece_width - 1, piece_height - 1)], fill=255)
                    draw.rectangle([(0, 0), (edge_thickness - 1, piece_height - 1)], fill=255)
                    draw.rectangle([(piece_width - edge_thickness, 0), (piece_width - 1, piece_height - 1)], fill=255)
                
                blurred_mask = mask.filter(ImageFilter.GaussianBlur(radius=3))
                blurred_piece = piece.filter(ImageFilter.GaussianBlur(radius=5))
                edge_blurred_piece = Image.composite(blurred_piece, piece, blurred_mask)
                chaotic_image.paste(edge_blurred_piece, (x1, y1))
            else:
                chaotic_image.paste(piece, (x1, y1))
            
            piece_array = np.array(piece)
            chaotic_array[y1:y1+piece_height, x1:x1+piece_width] = piece_array

    final_array = np.array(chaotic_image)
    new_entropy = calc_entropy(final_array)
    print(f"New Entropy: {new_entropy:.4f} bits")
    print(f"Entropy Increase: {new_entropy - original_entropy:.4f} bits")

    if new_entropy - original_entropy < target_entropy_increase:
        print("Entropy target not met; consider increasing noise_factor.")

    chaotic_image.save(output_path, 'JPEG')
