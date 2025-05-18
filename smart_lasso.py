from PIL import Image, ImageDraw, ImageFilter
import random
import cv2
import numpy as np

# X: @owldecoy

def smart_lasso(input_path, second_image_path, output_path):
        """
        Select a random object from second_image and paste it into input_image with sharp edges.

        Parameters:
        - input_path: Path to destination image (image1)
        - second_image_path: Path to source image containing objects (image2)
        - output_path: Path to save the resulting image
        """
        base_image = Image.open(input_path)
        if base_image.mode != 'RGB':
                base_image = base_image.convert('RGB')
        base_width, base_height = base_image.size

        second_image = Image.open(second_image_path)
        if second_image.mode != 'RGB':
                second_image = second_image.convert('RGB')
        second_width, second_height = second_image.size

        second_cv = cv2.cvtColor(np.array(second_image), cv2.COLOR_RGB2BGR)

        second_cv = cv2.GaussianBlur(second_cv, (5, 5), 0)

        gray = cv2.cvtColor(second_cv, cv2.COLOR_BGR2GRAY)

        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                                                cv2.THRESH_BINARY_INV, 11, 2)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        min_area = 1111
        max_area = second_width * second_height * 0.5
        valid_contours = []
        for c in contours:
                area = cv2.contourArea(c)
                if min_area < area < max_area:
                        x, y, w, h = cv2.boundingRect(c)
                        aspect_ratio = w / h if h != 0 else 1
                        if 0.2 < aspect_ratio < 5:
                                valid_contours.append(c)

        if not valid_contours:
                raise ValueError("No suitable objects found in second image")

        random_contour = random.choice(valid_contours)

        x, y, w, h = cv2.boundingRect(random_contour)

        object_section = second_image.crop((x, y, x + w, y + h))

        mask = Image.new('L', (w, h), 0)
        draw = ImageDraw.Draw(mask)

        contour_points = [(pt[0][0] - x, pt[0][1] - y) for pt in random_contour]
        draw.polygon(contour_points, fill=255)


        object_with_mask = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        object_with_mask.paste(object_section, (0, 0), mask)

        grid_cell_width = max(w // 2, base_width // 20)
        grid_cell_height = max(h // 2, base_height // 20)

        num_x_junctions = (base_width - w) // grid_cell_width + 1
        num_y_junctions = (base_height - h) // grid_cell_height + 1

        num_x_junctions = max(1, num_x_junctions)
        num_y_junctions = max(1, num_y_junctions)

        grid_x = random.randint(0, num_x_junctions - 1)
        grid_y = random.randint(0, num_y_junctions - 1)

        paste_x = grid_x * grid_cell_width
        paste_y = grid_y * grid_cell_height

        paste_x = min(paste_x, base_width - w)
        paste_y = min(paste_y, base_height - h)

        base_image.paste(object_with_mask, (paste_x, paste_y), object_with_mask)

        if base_image.mode == 'RGBA':
                base_image = base_image.convert('RGB')

        base_image.save(output_path, 'JPEG')
