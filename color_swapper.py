from PIL import Image
import numpy as np

# X:@owldecoy

def color_swapper(input_path, output_path, blur_radius=0.0):
        image = Image.open(input_path)
        if image.mode != 'RGB':
                image = image.convert('RGB')
        width, height = image.size

        img_array = np.array(image)

        black_pixels = np.sum(np.all(img_array == [0, 0, 0], axis=2))
        white_pixels = np.sum(np.all(img_array == [255, 255, 255], axis=2))

        result_array = img_array.copy()

        if black_pixels > white_pixels:
                black_mask = np.all(img_array == [0, 0, 0], axis=2)
                result_array[black_mask] = [255, 255, 255]
        else:
                white_mask = np.all(img_array == [255, 255, 255], axis=2)
                result_array[white_mask] = [0, 0, 0]

        result_image = Image.fromarray(result_array)

        if blur_radius > 0:
                result_image = result_image.filter(ImageFilter.GaussianBlur(radius=blur_radius))

        if result_image.mode == 'RGBA':
                result_image = result_image.convert('RGB')

        result_image.save(output_path, 'JPEG')

input_path = ""
output_path = ""
blur_radius = 0.2
color_swapper(input_path, output_path, blur_radius)
