from PIL import Image

# X: @owldecoy

def invert_colors(input_path, output_path):
    """
    Inverts the colors of an image by subtracting each pixel value from 255.

    Args:
        input_path (str): The file path to the input image.
        output_path (str): The file path where the inverted image will be saved in JPEG format.
    """


        image = Image.open(input_path)

        if image.mode != 'RGB':
                image = image.convert('RGB')

        inverted_image = Image.eval(image, lambda x: 255 - x)

        inverted_image.save(output_path, 'JPEG')
