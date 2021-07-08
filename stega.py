from PIL import Image
import numpy as np

MAX_COLOUR_VALUE = 255
MAX_BIT_VALUE = 8

def make_image(data, resolution):
    image=Image.new("RGB", resolution)
    image.putdata(data)

    return image


def remove_n_least_significant_bits(value, n):
    value = value >> n
    return value << n


def get_n_least_significant_bits(value, n):
    value = value << MAX_BIT_VALUE - n
    value = value % MAX_COLOUR_VALUE + 1
    return value >> MAX_BIT_VALUE - n


def get_n_most_significant_bits(value, n):
    return value >> MAX_BIT_VALUE - n


def shift_n_bits_to_8(value, n):
    return value << MAX_BIT_VALUE - n


def encode(image_to_hide, image_to_hide_in, n_bits):
    width, height = image_to_hide.shape[:2]

    hide_image = image_to_hide
    hide_in_image = image_to_hide_in

    data = []

    for y in range(height):
        for x in range(width):

            r_hide, g_hide, b_hide = hide_image[x, y]

            r_hide = get_n_most_significant_bits(r_hide, n_bits)
            g_hide = get_n_most_significant_bits(g_hide, n_bits)
            b_hide = get_n_most_significant_bits(b_hide, n_bits)

            r_hide_in, g_hide_in, b_hide_in = hide_in_image[x,y]

            r_hide_in = remove_n_least_significant_bits(r_hide_in, n_bits)
            g_hide_in = remove_n_least_significant_bits(g_hide_in, n_bits)
            b_hide_in = remove_n_least_significant_bits(b_hide_in, n_bits)

            data.append((r_hide + r_hide_in, 
                         g_hide + g_hide_in,
                         b_hide + b_hide_in))

    return make_image(data, (image_to_hide.shape[:2]))

def decode(image_to_decode, n_bits):
    width, height = image_to_decode.shape[:2]
    encoded_image = image_to_decode

    data = []

    for y in range(height):
        for x in range(width):

            r_encoded, g_encoded, b_encoded = encoded_image[x,y]
            
            r_encoded = get_n_least_significant_bits(r_encoded, n_bits)
            g_encoded = get_n_least_significant_bits(g_encoded, n_bits)
            b_encoded = get_n_least_significant_bits(b_encoded, n_bits)

            r_encoded = shift_n_bits_to_8(r_encoded, n_bits)
            g_encoded = shift_n_bits_to_8(g_encoded, n_bits)
            b_encoded = shift_n_bits_to_8(b_encoded, n_bits)

            data.append((r_encoded, g_encoded, b_encoded))

    return make_image(data, (image_to_decode.shape[:2]))
    