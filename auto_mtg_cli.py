import os
import operator
from collections import OrderedDict

import cv2
import fire

from core.background_subtract import find_card
from core.confusion_matrix import get_confusion_matrix
from core.cross_correlate import cross_correlate_all_set_images, thresh_all_set_templates
from core.mtg_api import get_all_cards_in_set, make_set_image_each_set, get_card_by_multiverse_id, \
    get_first_card_image_from_set
from core.preprocess import PreprocessorImg


def run_set_compare(path_to_original_image, remake_set_images=True, use_cv2_cross_corr=False):
    if remake_set_images:
        make_set_image_each_set()
    pre_process = PreprocessorImg(path_to_original_image)
    crop_set_image = pre_process.mtg_thres_set_image
    thresh_all_set_templates(crop_set_image.shape)
    cross_correlate_dict = cross_correlate_all_set_images(crop_set_image, use_cv2_cross_corr=use_cv2_cross_corr)
    max_tuple = max(cross_correlate_dict.items(), key=operator.itemgetter(1))
    print(sorted(cross_correlate_dict.items(), key=lambda x: x[1], reverse=True))
    print("The matching set is {} and the score was {}".format(max_tuple[0], max_tuple[1]))
    return max_tuple[0].split('.')[0]

# def run_set_compare_2(path_to_original_image, remake_set_images=True, use_cv2_cross_corr=False):
#     if remake_set_images:
#         make_set_image_each_set()
#     pre_process = PreprocessorImg(path_to_original_image)
#     crop_set_image = pre_process.mtg_thres_set_image
#     thresh_all_set_templates(crop_set_image.shape)
#     cross_correlate_dict = cross_correlate_all_set_images(crop_set_image, use_cv2_cross_corr=use_cv2_cross_corr)
#     max_tuple = max(cross_correlate_dict.items(), key=operator.itemgetter(1))
#     if max_tuple[1] < 0:
#
#     print(sorted(cross_correlate_dict.items(), key=lambda x: x[1], reverse=True))
#     print("The matching set is {} and the score was {}".format(max_tuple[0], max_tuple[1]))
#     return max_tuple[0].split('.')[0]


def run_card_compare(path_to_original_image, use_cv2_cross_corr=False, set_code=None):
    if not set_code:
        set_code = run_set_compare(path_to_original_image)
    pre_process = PreprocessorImg(path_to_original_image)
    cross_correlate_dict = find_card(pre_process.mtg_just_card, set_code, use_cv2_cross_corr=use_cv2_cross_corr)
    max_tuple = max(cross_correlate_dict.items(), key=operator.itemgetter(1))
    print(max_tuple)
    card = get_card_by_multiverse_id(max_tuple[0])
    card_info = (card['name'], card['image_uris']['large'], card['prices'])
    print(card_info)


def run_confusion_matrix(remake_set_images=True):
    if remake_set_images:
        make_set_image_each_set()
    thresh_all_set_templates((60,40))
    confusion_matrix = get_confusion_matrix()
    print(confusion_matrix)





if __name__ == '__main__':
    fire.Fire({
        'run_set_compare': run_set_compare,
        'run_card_compare': run_card_compare,
        'run_confusion_matrix': run_confusion_matrix
    })


