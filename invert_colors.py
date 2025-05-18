from PIL import Image

def invert_colors(input_path, output_path):

        image = Image.open(input_path)

        if image.mode != 'RGB':
                image = image.convert('RGB')

        inverted_image = Image.eval(image, lambda x: 255 - x)

        inverted_image.save(output_path, 'JPEG')
