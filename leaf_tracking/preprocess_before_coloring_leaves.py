from PIL import Image
import os

INPUT_DIR = r"masks_edges"
OUTPUT_DIR = r"mask_edges_black_white"
images_path = [f for f in os.listdir(INPUT_DIR)]

def process_image(original_img: Image, image_name):
    '''
    Converting RGB image with 3 color channels into 1 color channel black and white image
    :param original_img: images that needs to be converted to black and white
    :param image_name: name of the image file
    '''
    new_image = Image.new(mode="L", size=(224, 224))
    i = 0
    j = 0
    for x in range(original_img.width):
        for y in range(original_img.height):
            if original_img.getpixel((x, y)) == (68, 1, 84):
                new_image.putpixel((x, y), 0)
                i += 1
            else:
                j += 1
                new_image.putpixel((x, y), 255)

    print("black: i = " + str(i) + ", white: j = " + str(j))
    new_image.save(OUTPUT_DIR + "/" + image_name.replace(".png", "_modi.png"))

for image_path in images_path:
    print(image_path)
    img = Image.open(INPUT_DIR + "/" + image_path).convert('RGB')
    process_image(img, image_path)

