#! /usr/bin/python3

import argparse
from PIL import Image
from random import seed, randint


ITERATION_COUNT = 10000
DELTA = 3


def get_next_random_point(x_limit, y_limit):
    return randint(0, x_limit - 1), randint(0, y_limit - 1)


def increase_brightness(pixel):
    return _change_brightness(pixel, 1)


def decrease_brightness(pixel):
    return _change_brightness(pixel, -1)


def _change_brightness(pixel, sign):
    new_components = []
    for component in pixel:
        component += sign * DELTA
        if component < 0:
            component = 0
        elif component > 255:
            component = 255

        new_components.append(component)

    return tuple(new_components)


def point_supplier(x, y):
    for _ in range(ITERATION_COUNT):
        yield get_next_random_point(x, y), get_next_random_point(x, y)


def check_diff(args):
    image = Image.open(args.image)
    pixels = image.load()
    seed(args.key)
    sum_of_diffs = 0

    for (i_1, j_1), (i_2, j_2) in point_supplier(*image.size):
        sum_of_diffs += sum(pixels[i_1, j_1]) - sum(pixels[i_2, j_2])

    print(sum_of_diffs)
    if sum_of_diffs > 1.5 * DELTA * ITERATION_COUNT:
        print('Image may contain watermark')


def add_watermark(args):
    image = Image.open(args.image)
    pixels = image.load()
    seed(args.key)
    for (i_1, j_1), (i_2, j_2) in point_supplier(*image.size):
        pixels[i_1, j_1] = increase_brightness(pixels[i_1, j_1])
        pixels[i_2, j_2] = decrease_brightness(pixels[i_2, j_2])

    image.save(out_file)


def _parse_args():
    parser = argparse.ArgumentParser(description='Patchwork watermark algorithm.')
    parser.add_argument('image', type=str, help='Your image')
    parser.add_argument('key', type=int, help='Generator key')
    parser.add_argument('--out', type=str, help='Output image. Perform checking if not provided')

    return parser.parse_args()


def main():
    args = _parse_args()

    if args.out:
        add_watermark(args)
    else:
        check_diff(args)


if __name__ == "__main__":
    main()
