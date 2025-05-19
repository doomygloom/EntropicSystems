from PIL import Image, ImageEnhance

# X: @owldecoy

def decolorize(input_path, output_path, contrast_factor=2.0, threshold=128):                                                                   
        """                                                                                                                                    
        Convert an image to a high-contrast black-and-white version.                                                                           
                                                                                                                                               
        Args:                                                                                                                                  
                input_path (str): Path to input image                                                                                          
                output_path (str): Path to save output image                                                                                   
                contrast_factor (float): Factor to enhance contrast (default 2.0)                                                              
                threshold (int): Threshold value for binarization (0-255, default 128)                                                         
        """                                                                                                                                    
        image = Image.open(input_path)                                                                                                         
        if image.mode != 'RGB':                                                                                                                
                image = image.convert('RGB')                                                                                                   
        width, height = image.size                                                                                                             
                                                                                                                                               
        gray_image = image.convert('L')                                                                                                        
                                                                                                                                               
        enhancer = ImageEnhance.Contrast(gray_image)                                                                                           
        high_contrast = enhancer.enhance(contrast_factor)                                                                                      
                                                                                                                                               
        bw_image = high_contrast.point(lambda p: 255 if p > threshold else 0)                                                                  
                                                                                                                                               
        final_image = bw_image.convert('RGB')                                                                                                  
                                                                                                                                               
        if final_image.mode == 'RGBA':                                                                                                         
                final_image = final_image.convert('RGB')                                                                                       
                                                                                                                                               
        final_image.save(output_path, 'JPEG')
