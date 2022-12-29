from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import string

# colors that are used to color leaves
# colors are picked so that they are as much different between each other, and that they are not similar to the black
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


class Leaf:
    '''
    Class for representing individual leaves.
    Leaf has a unique id, list of pixels, color, area (which is calculated as the number of pixels),
    bool variable indicating if the leaf has been paired, and mark.
    '''
    def __init__(self, id, pixels, color):
        self.id = id
        self.pixels = pixels
        self.color = color
        self.area = len(pixels)
        self.paired = False
        self.mark = None

    def cal_position_for_text(self):
        '''
        Finding a position for mark to be written on the image
        '''
        x_s = [pixel[0] for pixel in self.pixels]
        y_s = [pixel[1] for pixel in self.pixels]

        x_min = min(x_s)
        x_max = max(x_s)

        y_min = min(y_s)
        y_max = max(y_s)

        x_start = x_min + 0.15 * (x_max - x_min)
        y_start = y_min + 0.15 * (y_max - y_min)

        return (x_start, y_start)


def find_all_pixels_in_color(image, color):
    '''
    Finding all pixels in an image with specified color.
    :param image: Image that will be searched
    :param color: color that the function is searching for in an image
    :return:
    '''
    pixels = []
    for x in range(image.width):
        for y in range(image.height):
            if image.getpixel((x, y)) == color or image.getpixel((x, y)) == (color[0], color[1], color[2], 255):
                pixels.append([x, y])

    return pixels


def analyze_image(input_path):
    '''
    Finding all leaves in the image
    :param input_path: input path to the image
    :return: array of instances of class Leaf
    '''
    leaves = []
    image = Image.open(input_path)

    i = 1
    for color in colors:
        pixels = find_all_pixels_in_color(image, color)
        if len(pixels) >= 5:
            leaves.append(Leaf(i, pixels, color))
            i += 1

    return leaves


def check_overlapping_percentage(leaf_1, leaf_2):
    '''
    Checking how much leaf_1 and leaf_2 overlap.
    :param leaf_1: first leaf
    :param leaf_2: second leaf
    :return: If overlapp is more than 60% return true.
    '''
    matched = 0
    for pixel in leaf_1.pixels:
        if pixel in leaf_2.pixels:
            matched += 1

    return matched >= 0.65 * leaf_1.area


def pair_leaves(leaves_1, leaves_2):
    '''
    Trying to pair appropriate leaves from two lists.
    :param leaves_1: first list
    :param leaves_2: second list
    :return: list of pairs of ids of leaves that were paired
    '''
    ids_of_pairs = []
    leaves_1.sort(key=lambda x: x.area)
    leaves_2.sort(key=lambda x: x.area)

    for i in range(min(len(leaves_1), len(leaves_2))):
        if check_overlapping_percentage(leaves_1[i], leaves_2[i]):
            ids_of_pairs.append([leaves_1[i].id, leaves_2[i].id])
            leaves_1[i].paired = True
            leaves_2[i].paired = True

    unpaired_ids_1 = [leaf.id for leaf in leaves_1 if not leaf.paired]
    unpaired_ids_2 = [leaf.id for leaf in leaves_2 if not leaf.paired]

    if len(unpaired_ids_1) > 0 and len(unpaired_ids_2) > 0:
        for id_1 in unpaired_ids_1:
            index_1 = next(i for i, x in enumerate(leaves_1) if x.id == id_1)
            for id_2 in unpaired_ids_2:
                index_2 = next(i for i, x in enumerate(leaves_2) if x.id == id_2)
                if not leaves_1[index_1].paired and not leaves_2[index_2].paired:
                    if check_overlapping_percentage(leaves_1[index_1], leaves_2[index_2]):
                        ids_of_pairs.append([leaves_1[index_1].id, leaves_2[index_2].id])
                        leaves_1[index_1].paired = True
                        leaves_2[index_2].paired = True

    return ids_of_pairs


def get_different_color(used_colors):
    '''
    Function that ensures that same color will not be used for two different leaves.
    :param used_colors: list of used colors
    :return: color that is in the list of colors, but not in the used colors
    '''
    for color in colors:
        if color not in used_colors:
            return color


def color_leaves(leaves_1, leaves_2, ids_of_pairs):
    '''
    Coloring leaves accordingly to the pairing.
    :param leaves_1: list of leaves in one image
    :param leaves_2: list of leaves in second image
    :param ids_of_pairs: list of ids of paired leaves
    '''
    i = 0
    used_colors = []
    for id_pair in ids_of_pairs:
        id_1 = id_pair[0]
        id_2 = id_pair[1]

        index_1 = next(i for i, x in enumerate(leaves_1) if x.id == id_1)
        index_2 = next(i for i, x in enumerate(leaves_2) if x.id == id_2)

        leaves_2[index_2].color = leaves_1[index_1].color
        used_colors.append(leaves_1[index_1].color)

        leaves_1[index_1].mark = string.ascii_uppercase[i]
        leaves_2[index_2].mark = string.ascii_uppercase[i]
        i += 1

    # color unpaired leaves
    unpaired_ids_1 = [leaf.id for leaf in leaves_1 if not leaf.paired]
    unpaired_ids_2 = [leaf.id for leaf in leaves_2 if not leaf.paired]

    for id_1 in unpaired_ids_1:
        index_1 = next(i for i, x in enumerate(leaves_1) if x.id == id_1)
        leaves_1[index_1].color = get_different_color(used_colors)
        used_colors.append(leaves_1[index_1].color)
        leaves_1[index_1].mark = string.ascii_uppercase[i] + '#'
        i += 1

    for id_2 in unpaired_ids_2:
        index_2 = next(i for i, x in enumerate(leaves_2) if x.id == id_2)
        leaves_2[index_2].color = get_different_color(used_colors)
        used_colors.append(leaves_2[index_2].color)
        leaves_2[index_2].mark = string.ascii_uppercase[i] + '#'
        i += 1


def output_images(leaves_1, leaves_2, input_path_1, input_path_2):
    '''
    Saving images with appropriate leaf marks.
    :param leaves_1: list of leaves of the first image
    :param leaves_2: list of leaves of the second image
    :param input_path_1: input path of the first image
    :param input_path_2: input path of the second image
    '''
    output_image_1 = Image.new(mode="RGB", size=(224, 224))

    for leaf in leaves_1:
        for pixel in leaf.pixels:
            output_image_1.putpixel(pixel, leaf.color)

    output_image_2 = Image.new(mode="RGB", size=(224, 224))

    for leaf in leaves_2:
        for pixel in leaf.pixels:
            output_image_2.putpixel(pixel, leaf.color)

    output_image_1.save(input_path_1.replace("_labels", "_leaves"))
    output_image_2.save(input_path_2.replace("_labels", "_leaves"))


def process_images(input_path_1, input_path_2):
    '''
    Finding pairs of leaves in two consecutive images
    :param input_path_1: input path of the first image
    :param input_path_2: input path of the second image
    :return: two lists, one is list of leaves in first image, and second is list of leaves in the second image
    '''
    leaves_1 = analyze_image(input_path_1)
    leaves_2 = analyze_image(input_path_2)

    ids_of_pairs = pair_leaves(leaves_1, leaves_2)
    color_leaves(leaves_1, leaves_2, ids_of_pairs)
    output_images(leaves_1, leaves_2, input_path_1, input_path_2)

    return leaves_1, leaves_2


def write_on_original_images(original_image_path_1, leaves_1, original_image_path_2, leaves_2):
    '''
    Writing marks on the images and saving them.
    :param original_image_path_1: path to the first original image
    :param leaves_1: list of leaves in the first image
    :param original_image_path_2: path to the second original image
    :param leaves_2: list of leaves in the second image
    '''
    myFont = ImageFont.truetype('arial.ttf', 10)

    original_image_1 = Image.open(original_image_path_1)
    original_image_1 = original_image_1.resize((224, 224))
    original_image_2 = Image.open(original_image_path_2)
    original_image_2 = original_image_2.resize((224, 224))

    original_image_1_draw = ImageDraw.Draw(original_image_1)
    for leaf in leaves_1:
        start_point = leaf.cal_position_for_text()
        if leaf.paired:
            original_image_1_draw.text(start_point, leaf.mark, font=myFont, fill=(255, 20, 147))
        else:
            original_image_1_draw.text(start_point, leaf.mark, font=myFont, fill=(255, 255, 255))

    original_image_2_draw = ImageDraw.Draw(original_image_2)
    for leaf in leaves_2:
        start_point = leaf.cal_position_for_text()
        if leaf.paired:
            original_image_2_draw.text(start_point, leaf.mark, font=myFont, fill=(255, 20, 147))
        else:
            original_image_2_draw.text(start_point, leaf.mark, font=myFont, fill=(255, 255, 255))

    original_image_1.save(original_image_path_1.replace(".png", "leaves.png"))
    original_image_2.save(original_image_path_2.replace(".png", "leaves.png"))


input_1 = r"example_1_top_2_labels.png"
input_2 = r"example_2_top_2_labels.png"

leaves_1, leaves_2 = process_images(input_1, input_2)

original_image_path_1 = r"example_1_top_2.png"
original_image_path_2 = r"example_2_top_2.png"

write_on_original_images(original_image_path_1, leaves_1, original_image_path_2, leaves_2)
