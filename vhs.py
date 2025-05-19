from PIL import Image, ImageEnhance
import numpy as np
import random

# X: @owldecoy

def vhs(input_path, output_path, noise_level=25, line_freq=0.05, jitter_strength=5, tracking_lines=True):
    """
    Applies a VHS-style effect to an image by adding noise, color channel shifts, and optional tracking lines.

    Args:
        input_path (str): The file path to the input image.
        output_path (str): The file path where the modified image will be saved in JPEG format.
        noise_level (int, optional): The standard deviation of the Gaussian noise to be added. Default is 25.
        line_freq (float, optional): The frequency of tracking lines (0.0 to 1.0). Default is 0.05.
        jitter_strength (int, optional): The maximum pixel shift for horizontal jitter effect. Default is 5 pixels.
        tracking_lines (bool, optional): Whether to add random horizontal tracking lines. Default is True.
    """

    image = Image.open(input_path)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    img_array = np.array(image, dtype=np.float32)
    height, width, _ = img_array.shape

    noise = np.random.normal(0, noise_level, (height, width, 3))
    noisy_img = img_array + noise
    noisy_img = np.clip(noisy_img, 0, 255)

    shift = random.randint(-3, 3)
    shifted_img = noisy_img.copy()
    shifted_img[:, :-shift, 0] = noisy_img[:, shift:, 0]
    shifted_img[:, shift:, 2] = noisy_img[:, :-shift, 2]

    if tracking_lines:
        for y in range(0, height, 1):
            if random.random() < line_freq:
                line_thickness = random.randint(1, 3)
                shifted_img[y:y+line_thickness, :, :] = random.uniform(150, 255)

    jittered_img = shifted_img.copy()
    for y in range(height):
        jitter = random.randint(-jitter_strength, jitter_strength)
        if jitter > 0:
            jittered_img[y, jitter:, :] = shifted_img[y, :-jitter, :]
        elif jitter < 0:
            jittered_img[y, :jitter, :] = shifted_img[y, -jitter:, :]

    vhs_image = Image.fromarray(np.uint8(jittered_img))

    #enhancer = ImageEnhance.Brightness(vhs_image)
    #vhs_image = enhancer.enhance(0.9) # slightly darken
    #enhancer = ImageEnhance.Contrast(vhs_image)
    #vhs_image = enhancer.enhance(0.85) # reduce contrast

    vhs_image.save(output_path, 'JPEG')
