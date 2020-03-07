from argparse import ArgumentParser
from PIL import Image
from os.path import join
import os
import configparser

# Make a new directory for all the incoming cropped images
def make_target_directory(inputDir):
    new_foldr_path = inputDir+"/cropped_images"
    # Create target directory & all intermediate directories if don't exists
    if not os.path.exists(new_foldr_path):
        os.makedirs(new_foldr_path)
        print("Directory " , new_foldr_path, " Created.")
    else:    
        print("Directory " , new_foldr_path, " already exists.")
    return new_foldr_path

# https://note.nkmk.me/en/python-pillow-image-crop-trimming/
def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

# https://note.nkmk.me/en/python-pillow-image-crop-trimming/
def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))

# Main cropping function
def cropImage(fileNames, imagePaths, currentDir):
    foldr_path = make_target_directory(currentDir)

    for i in range(len(imagePaths)):
        print("Processing image: " + fileNames[i])
        img = Image.open(imagePaths[i])

        try:

            # Crop image into a square given the image's min(length || width)
            new_img = crop_max_square(img)
            
            # Crop out image's excess outer perimeter (unit pixels)
            #pixl_diff = min(new_img.size)-10
            #new_img = crop_center(new_img, pixl_diff, pixl_diff)

            # Proceed to wrap up by saving into optimal discord resolution, then save.
            new_img = new_img.resize((128,128))
            new_img.save(foldr_path+ '/' + fileNames[i])
            print("Image saved.")
        except AttributeError:
            print("Couldn't save image {}".format(imagePaths[i]))

# Main function
def main():
    parser = ArgumentParser(description="Resize images to optimal discord emoji resolution [128x128].")
    parser.add_argument('-d', '--input_dir', type=str, required=True, help="Directory containing the images")
    args = parser.parse_args()
    if not os.path.exists(args.input_dir):
        print("Error with directory path")
        return
    
    # Get all images' path into a list
    imagePaths = []
    fileNames = []
    currentDir = args.input_dir
    for root, dirs, files in os.walk(currentDir):
        for file in files:
            imagePaths.append(args.input_dir + '/' + file)
            fileNames.append(file)
    
    # Crop all the images
    cropImage(fileNames, imagePaths, currentDir)

# Finally call the fuction
if __name__ == '__main__':
    main()