from PIL import Image

# X: @owldecoy

def rotate(input_path, output_path):                                                                                                           
        """                                                                                                                                    
        Rotates an image 90 degrees clockwise and saves it to the output path.                                                                 
                                                                                                                                               
        Args:                                                                                                                                  
                input_path (str): Path to the input image                                                                                      
                output_path (str): Path where the rotated image will be saved                                                                  
        """                                                                                                                                    
        image = Image.open(input_path)                                                                                                         
        if image.mode != 'RGB':                                                                                                                
                image = image.convert('RGB')                                                                                                   
        width, height = image.size                                                                                                             
                                                                                                                                               
        rotated_image = image.rotate(-90, expand=True)                                                                                         
                                                                                                                                               
        if rotated_image.mode == 'RGBA':                                                                                                       
                rotated_image = rotated_image.convert('RGB')                                                                                   
                                                                                                                                               
        rotated_image.save(output_path, 'JPEG')
