import random

# X: @owldecoy

def glitch_image(input_path, output_path, intensity=5, mode='bit_flip', preserve_header=True):
    """
    Applies a glitch effect to an image by manipulating its binary data using various glitch modes.

    Args:
        input_path (str): The file path to the input image.
        output_path (str): The file path where the glitched image will be saved.
        intensity (int, optional): The intensity level of the glitch effect. Higher values increase the severity of the glitch. Default is 5.
        mode (str, optional): The glitch mode to apply. Options are 'bit_flip' (alters individual bits) or 'byte_shift' (reverses chunks of bytes). Default is 'bit_flip'.
        preserve_header (bool, optional): Whether to preserve the header of the image to maintain basic image structure. Default is True.
    """

        with open(input_path, 'rb') as f:
                data = bytearray(f.read())

                header_size = 50 if preserve_header else 0
                if len(data) <= header_size:
                        raise ValueError("Image file too small to glitch")

        glitched_data = data.copy()

        if mode == 'bit_flip':
                        iterations = intensity * 200
                        for _ in range(iterations):
                                index = random.randint(header_size, len(glitched_data) - 1)
                                bit = 1 << random.randint(0, 7)
                                glitched_data[index] ^= bit

        elif mode == 'byte_shift':
                chunk_size = max(1, intensity // 2)
                iterations = intensity * 20
                for _ in range(iterations):
                        start = random.randint(header_size, len(glitched_data) - chunk_size - 1)
                        end = start + chunk_size
                        glitched_data[start:end] = glitched_data[start:end][::-1]

        else:
                raise ValueError(f"Unknown glitch mode: {mode}")

        try:
                with Image.open(io.BytesIO(glitched_data)) as img:
                        img.verify()
        except Exception:
                for _ in range(intensity * 10):
                        index = random.randint(header_size, len(glitched_data) - 1)
                        glitched_data[index] = random.randint(0, 255)

        with open(output_path, 'wb') as f:
                f.write(glitched_data)
