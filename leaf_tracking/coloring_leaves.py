import os
from PIL import Image
import time
import datetime

# colors that are used to color leaves
# colors are picked so that they are as much different between each other, and that they are not simmilar to the black
colors = [(240, 128, 128), (255, 215, 0), (124, 252, 0), (0, 128, 0), (0, 139, 139), (0, 255, 255), (0, 0, 128),
          (138, 43, 226), (139, 0, 139), (255, 0, 255), (255, 20, 147), (255, 192, 203), (255, 235, 205),
          (210, 105, 30), (139, 69, 19), (112, 128, 144), (176, 196, 222), (0, 0, 255), (255, 0, 0), (0, 255, 0),
          (221, 160, 221), (135, 206, 235), (227, 119, 6), (255, 182, 193), (105, 102, 200), (50, 35, 255),
          (90, 3, 134), (115, 235, 82), (134, 37, 104), (149, 130, 108), (125, 156, 46), (210, 105, 30),
          (173, 188, 237), (216, 240, 248), (255, 140, 0), (189, 183, 107), (185, 228, 201), (146, 105, 184),
          (34, 97, 126), (95, 197, 243), (62, 185, 184), (238, 130, 238), (184, 245, 194), (198, 123, 191),
          (127, 125, 179), (158, 126, 146), (164, 5, 112), (249, 82, 16), (255, 0, 255), (255, 255, 204), (43, 158, 2),
          (251, 196, 49), (187, 170, 230), (81, 138, 157), (119, 83, 190), (38, 137, 16), (230, 99, 90),
          (232, 195, 149), (194, 46, 99), (38, 80, 48), (175, 70, 77), (139, 69, 19), (235, 246, 24), (129, 206, 54),
          (96, 121, 156)]

thresh = 200
fn = lambda x: 255 if x > thresh else 0

white = 255
black = 0


class Leaf_pixel:
    '''
    Class that holds information about pixel, including coordinates x and y, and whether the leaf is inner or not (edge)
    '''
    def __init__(self, x, y, inner=True):
        self.x = x
        self.y = y
        self.inner = inner


def color_leaves(edges_image_path, mask_image_path, input_folder, output_folder):
    '''
    Main method for coloring leaves in all the pairs of edges and mask images.
    :param edges_image_path: array of paths to edges images
    :param mask_image_path: array of paths to edges images
    :param input_folder: input folder where edges images and mask images are
    :param output_folder: output folder where results should be saved
    '''
    edges_image = Image.open(input_folder + "/" + edges_image_path)
    mask_image = Image.open(input_folder + "/" + mask_image_path)

    width = edges_image.width
    height = edges_image.height

    edges_image = edges_image.convert('L').point(fn, mode='1')
    mask_image = mask_image.convert('L').point(fn, mode='1')

    output_image = Image.new(mode="RGB", size=(width, height))

    leaves = []

    def check_pixel(x_2, y_2):
        '''
        Checking if pixel with provided coordinates is inner pixel of a leaf
        :param x_2: x coordinate
        :param y_2: y coordinate
        :return:
        '''
        if width > x_2 >= 0 and width > y_2 >= 0:
            if [x_2, y_2] in copy_pixel_list:
                if mask_image.getpixel((x_2, y_2)) == white and \
                        edges_image.getpixel((x_2, y_2)) == black:
                    return True
        return False

    def check_leaf(leaf):
        '''
        Checking wheater the leaf is composed of pixels that are edged.
        :param leaf: list of pixels representing leaf
        :return: true if the leaf has more than 80% of edged pixels
        '''
        num_pixel_edged = 0

        inner_pixels = [pixel for pixel in leaf if pixel.inner]
        edge_pixels = [pixel for pixel in leaf if not pixel.inner]
        for pixel in inner_pixels:
            x = pixel.x
            y = pixel.y

            y_s = [pixel.y for pixel in edge_pixels if pixel.x == x]
            x_s = [pixel.x for pixel in edge_pixels if pixel.y == y]

            if len(x_s) >= 2 and len(y_s) >= 2:
                if min(y_s) < y < max(y_s) and min(x_s) < x < max(x_s):
                    num_pixel_edged += 1

        return num_pixel_edged >= 0.8 * len(inner_pixels)


    def find_leaf(x, y):
        '''
        Using greedy approach to find whole leaf, based on the inner pixel with coordinates x and y.
        :param x: coordinate x
        :param y: coordinate y
        '''
        leaf.append(Leaf_pixel(x, y))
        copy_pixel_list.remove([x, y])

        if check_pixel(x + 1, y):
            find_leaf(x + 1, y)
        elif x + 1 < width and edges_image.getpixel((x + 1, y)) == white:
            leaf.append(Leaf_pixel(x + 1, y, False))
            # return

        if check_pixel(x, y + 1):
            find_leaf(x, y + 1)
        elif y + 1 < height and edges_image.getpixel((x, y + 1)) == white:
            leaf.append(Leaf_pixel(x, y + 1, False))
            # return

        if check_pixel(x - 1, y):
            find_leaf(x - 1, y)
        elif x - 1 >= 0 and edges_image.getpixel((x - 1, y)) == white:
            leaf.append(Leaf_pixel(x - 1, y, False))
            # return

        if check_pixel(x, y - 1):
            find_leaf(x, y - 1)
        elif y - 1 >= 0 and edges_image.getpixel((x, y - 1)) == white:
            leaf.append(Leaf_pixel(x, y - 1, False))
            # return

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
                try:
                    find_leaf(x1, y1)
                except:
                    print("Too much recurssion: " + edges_image_path)
                if check_leaf(leaf):
                    leaves.append(leaf)

    i = 0
    for leaf in leaves:
        if len(leaf) > 8:
            for leaf_pixel in leaf:
                output_image.putpixel((leaf_pixel.x, leaf_pixel.y), colors[i])

            i += 1

    output_image.save(output_folder + "/" + edges_image_path.replace("edges_modi", "labels"))


start_time = time.time()
print("Start: " + str(datetime.datetime.now()))

input_folder = r"mask_edges_black_white"
output_folder = r"colored_leaves"

files = os.listdir(input_folder)
edges_images_paths = [f for f in files if f.endswith("edges_modi.png")]
masks_images_paths = [f for f in files if f.endswith("mask_modi.png")]

for edges_image_path, mask_image_path in zip(edges_images_paths, masks_images_paths):
    color_leaves(edges_image_path, mask_image_path, input_folder, output_folder)

print("--- %s seconds ---" % (time.time() - start_time))
print("End: " + str(datetime.datetime.now()))
