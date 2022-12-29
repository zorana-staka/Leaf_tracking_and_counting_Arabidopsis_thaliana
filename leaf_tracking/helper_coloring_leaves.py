from PIL import Image
import cv2
import numpy as np
import time
import datetime

start_time = time.time()
print("Start: " + str(datetime.datetime.now()))

edges_image_path = r"C:\Users\User\Desktop\plant021_edges.png"
mask_image_path = r"C:\Users\User\Desktop\plant021_fg.png"


colors = [(240, 128, 128, 255), (255, 215, 0, 255), (124, 252, 0, 255), (0, 128, 0, 255), (0, 139, 139, 255),
          (0, 255, 255, 255), (0, 0, 128, 255), (138, 43, 226, 255), (139, 0, 139, 255), (255, 0, 255, 255),
          (255, 20, 147, 255), (255, 192, 203, 255), (255, 235, 205, 255), (210, 105, 30, 255), (139, 69, 19, 255),
          (112, 128, 144, 255), (176, 196, 222, 255), (0, 0, 255, 255), (255, 0, 0, 255), (0, 255, 0, 255),
          (221, 160, 221, 255), (135, 206, 235, 255), (227, 119, 6, 255)]

edges_image = Image.open(edges_image_path)
mask_image = Image.open(mask_image_path)

width = edges_image.width
height = edges_image.height

thresh = 200
fn = lambda x: 255 if x > thresh else 0
edges_image = edges_image.convert('L').point(fn, mode='1')
mask_image = mask_image.convert('L').point(fn, mode='1')

edges_image.show()
mask_image.show()

output_image = Image.new(mode="RGB", size=(width, height))

leaves = []

print("Pixel example: " + str(mask_image.getpixel((34, 123))))
print("Pixel example: " + str(edges_image.getpixel((34, 123))))
print("Pixel example: " + str(mask_image.getpixel((34, 29))))
print("Pixel example: " + str(edges_image.getpixel((34, 29))))

white = 255
black = 0


def check_pixel(x_2, y_2):
    if width > x_2 >= 0 and width > y_2 >= 0:
        if [x_2, y_2] in copy_pixel_list:
            if mask_image.getpixel((x_2, y_2)) == white and \
                    edges_image.getpixel((x_2, y_2)) == black:
                return True
    return False


def find_leaf(x, y):
    leaf.append([x, y])
    copy_pixel_list.remove([x, y])

    if check_pixel(x+1, y):
        find_leaf(x + 1, y)
    elif x + 1 < width and edges_image.getpixel((x + 1, y)) == white:
        leaf.append([x + 1, y])
        return

    if check_pixel(x, y+1):
        find_leaf(x, y + 1)
    elif y + 1 < height and edges_image.getpixel((x, y + 1)) == white:
        leaf.append([x, y + 1])
        return

    if check_pixel(x-1, y):
        find_leaf(x - 1, y)
    elif x - 1 >= 0 and edges_image.getpixel((x - 1, y)) == white:
        leaf.append([x - 1, y])
        return

    if check_pixel(x, y-1):
        find_leaf(x, y - 1)
    elif y - 1 >= 0 and edges_image.getpixel((x, y - 1)) == white:
        leaf.append([x, y - 1])
        return


pixel_list = []

for x in range(width):
    for y in range(height):
        pixel_list.append([x, y])

copy_pixel_list = pixel_list.copy()

for [x1, y1] in pixel_list:
    if [x1, y1] in copy_pixel_list:
        if mask_image.getpixel((x1, y1)) == white and \
                edges_image.getpixel((x1, y1)) == black:
            leaf = []
            find_leaf(x1, y1)
            print(len(copy_pixel_list))

            leaves.append(leaf)

i = 0
for leaf in leaves:
    if len(leaf) >= 7:
        for [x, y] in leaf:
            output_image.putpixel((x, y), colors[i])

        i += 1


output_image.save(r"C:\Users\User\Desktop\plant021_leaves.png")

print("--- %s seconds ---" % (time.time() - start_time))
print("End: " + str(datetime.datetime.now()))

output_image.show()
