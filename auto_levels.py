from PIL import Image, ImageEnhance

# X: @owldecoy

def auto_levels(input_path, output_path):

        """
            Adjusts the levels of an image by enhancing contrast for each RGB channel independently.

            Args:
                input_path (str): The file path to the input image.
                output_path (str): The file path where the adjusted image will be saved in JPEG format.
        """

        image = Image.open(input_path)
        if image.mode != 'RGB':
                image = image.convert('RGB')
        width, height = image.size

        r, g, b = image.split()

        def adjust_channel(channel):
                hist = channel.histogram()

                total_pixels = channel.size[0] * channel.size[1]
                threshold = total_pixels * 0.005 # 0.5%

                min_val = 0
                pixel_count = 0
                for i, count in enumerate(hist):
                        pixel_count += count
                        if pixel_count > threshold:
                                min_val = i
                                break

                max_val = 255
                pixel_count = 0
                for i, count in enumerate(hist[::-1]):
                        pixel_count += count
                        if pixel_count > threshold:
                                max_val = 255 - i
                                break

                if max_val > min_val:
                        channel = ImageEnhance.Contrast(channel).enhance(255.0 / (max_val - min_val))
                        channel = Image.eval(channel, lambda x: (x - min_val) * (255.0 / (max_val - min_val)))

                return channel

        r_adjusted = adjust_channel(r)
        g_adjusted = adjust_channel(g)
        b_adjusted = adjust_channel(b)

        adjusted_image = Image.merge('RGB', (r_adjusted, g_adjusted, b_adjusted))

        if adjusted_image.mode == 'RGBA':
                adjusted_image = adjusted_image.convert('RGB')

        adjusted_image.save(output_path, 'JPEG')
