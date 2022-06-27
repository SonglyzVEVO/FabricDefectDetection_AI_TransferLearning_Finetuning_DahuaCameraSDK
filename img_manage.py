import matplotlib.pyplot as plt 
import cv2

class ImageHandle:
    
    def crop_upperleft(img_rgb):
        #cropped_region_upperleft = img_rgb[0:768, 0:1024]
        cropped_region_upperleft = img_rgb[0:300, 0:450]
        plt.imshow(cropped_region_upperleft)
        return cropped_region_upperleft
    
    def crop_upperright(img_rgb):
        #cropped_region_upperright = img_rgb[0:768, 0:2048]
        cropped_region_upperright = img_rgb[0:300, 450:903]
        plt.imshow(cropped_region_upperright)
        return cropped_region_upperright
           
    def crop_lowerleft(img_rgb):
        #cropped_region_lowerleft = img_rgb[768:1536, 0:1024]
        cropped_region_lowerleft = img_rgb[300:600, 0:450]
        plt.imshow(cropped_region_lowerleft)
        return cropped_region_lowerleft
        
    def crop_lowerright(img_rgb):
        #cropped_region_lowerright = img_rgb[768:1536, 1024:2048]
        cropped_region_lowerright = img_rgb[300:600, 450:903]
        plt.imshow(cropped_region_lowerright)
        return cropped_region_lowerright
   
    def resizing_img(img_rgb):
        desired_width = 224
        desired_height = 224
        dim = (desired_width, desired_height)
        resized_cropped_region = cv2.resize(img_rgb, dsize=dim, interpolation=cv2.INTER_AREA)
        plt.imshow(resized_cropped_region)
        return resized_cropped_region
