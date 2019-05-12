import collections
import os

import cv2
import numpy as np

from core.preprocess import PreprocessorImg


def prepare_image(matrix, template=True):
    """
    :param template:
    :param matrix:
    :return:
    """
    if not template:
        background = -1
    else:
        background = 0
    len_row = len(matrix)
    len_column = len(matrix[0])
    new_matrix = np.zeros((len_row, len_column))
    for row in range(len_row):
        for column in range(len_column):
            val = matrix[row][column]
            if val == 255:
                new_matrix[row][column] = background
            else:
                new_matrix[row][column] = 1
    return new_matrix


def cross_correlate_change_to_binary_and_score(origin_image, set_image):
    full_result = 0
    prepared_set = prepare_image(set_image, template=True)
    prepared_original = prepare_image(origin_image, template=False)
    for row in range(len(prepared_original)):
        for column in range(len(prepared_original[row])):
            intensity_result = prepared_original[row][column] * prepared_set[row][column]
            full_result += intensity_result
    return full_result


def thresh_all_set_templates(shape):
    height, width = shape
    set_images_path = os.path.join('png_set_images')
    for set_image_path in os.listdir(set_images_path):
        set_image_memory = cv2.imread(os.path.join(set_images_path, set_image_path))
        set_image_memory = cv2.cvtColor(set_image_memory, cv2.COLOR_BGR2GRAY)
        set_image_resized = cv2.resize(set_image_memory, (width, height))
        thes, set_image_thresholded = cv2.threshold(set_image_resized, 50, 255, cv2.THRESH_BINARY)
        cv2.imwrite(os.path.join('thresh_resize_images', set_image_path), set_image_thresholded)


def cross_correlate_all_set_images(crop_set_image_original, use_cv2_cross_corr=False):
    all_image_name_score = {}
    set_images_path = os.path.join('thresh_resize_images')
    for set_image_path in os.listdir(set_images_path):
        set_image_thresholded = cv2.imread(os.path.join(set_images_path, set_image_path), cv2.IMREAD_GRAYSCALE)
        if use_cv2_cross_corr:
            cc_result = cv2.matchTemplate(crop_set_image_original, set_image_thresholded, cv2.TM_CCORR_NORMED)
        else:
            cc_result = cross_correlate_change_to_binary_and_score(crop_set_image_original, set_image_thresholded)
        all_image_name_score[set_image_path] = cc_result
    return all_image_name_score

