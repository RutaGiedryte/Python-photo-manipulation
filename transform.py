# this file is the one I actually filled in using the tutorial

from image import Image
import numpy as np

def brighten(image, factor):
    # when we brighten, we make each channel higher
    # factor is >0 (<1 = darken, >1 = brighten)
    
    x_pixels, y_pixels, num_channels = image.array.shape
    new_image = Image(x_pixels, y_pixels, num_channels)
    new_image.array = image.array * factor 
    
    return new_image

def adjust_contrast(image, factor, mid):
    # increase the difference from the user-defined midpoint by factor
    
    x_pixels, y_pixels, num_channels = image.array.shape
    new_image = Image(x_pixels, y_pixels, num_channels)
    new_image.array = (image.array - mid) * factor + mid
    
    return new_image

def blur(image, kernel_size):
    # kernel size is the number of pixels to use when blurring (always an odd number)
    # (kernel_size = 3 would be neighbors to the left/right, top/bottom, and diagonals)
    
    x_pixels, y_pixels, num_channels = image.array.shape
    new_image = Image(x_pixels, y_pixels, num_channels)
    neighbor_range = kernel_size // 2
    
    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                total = 0

                for x_i in range(max(0, x - neighbor_range), min(x_pixels, x + neighbor_range + 1)):
                    for y_i in range(max(0, y - neighbor_range), min(y_pixels, y + neighbor_range + 1)):
                        total += image.array[x_i, y_i, c]    
                new_image.array[x, y, c] = total / (kernel_size**2)
    
    return new_image

def apply_kernel(image, kernel):
    # the kernel should be a 2D array that represents the kernel we'll use!
    # let's assume that the kernel is SQUARE

    x_pixels, y_pixels, num_channels = image.array.shape
    new_image = Image(x_pixels, y_pixels, num_channels)
    kernel_size = kernel.shape[0]
    neighbor_range = kernel_size // 2
    
    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                total = 0

                for x_i in range(max(0, x - neighbor_range), min(x_pixels, x + neighbor_range + 1)):
                    for y_i in range(max(0, y - neighbor_range), min(y_pixels, y + neighbor_range + 1)):
                        x_k = x_i - (x - neighbor_range)
                        y_k = y_i - (y - neighbor_range)
                        
                        kernel_value = kernel[x_k, y_k]
                        total += image.array[x_i, y_i, c] * kernel_value   
                new_image.array[x, y, c] = total
                
    return new_image

def combine_images(image1, image2):
    # let's combine two images using the squared sum of squares: value = sqrt(value_1**2, value_2**2)
    # size of image1 and image2 MUST be the same
    
    x_pixels, y_pixels, num_channels = image1.array.shape
    new_image = Image(x_pixels, y_pixels, num_channels)
    
    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                new_image.array[x, y, c] = (image1.array[x, y, c]**2 + image2.array[x, y, c]**2) ** 0.5
    
    return new_image
    
if __name__ == '__main__':
    lake = Image(filename='lake.png')
    city = Image(filename='city.png')
    
    sobel_x_kernel = np.array([
        [1, 0, -1],
        [2, 0, -2],
        [1, 0, -1]
    ])
    sobel_y_kernel = np.array([
        [1, 2, 1],
        [0, 0, 0],
        [-1, -2, -1]
    ])
    
    sobel_x_image = apply_kernel(city, sobel_x_kernel)
    sobel_y_image = apply_kernel(city, sobel_y_kernel)
    
    sobel_xy_image = combine_images(sobel_x_image, sobel_y_image)
    sobel_xy_image.write_image('sobel_xy_image.png')
    
    
    
    
    
    
