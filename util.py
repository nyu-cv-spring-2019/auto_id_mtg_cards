import os

import cv2

from core.mtg_api import get_first_card_image_from_set


class Util:

    @staticmethod
    def flip_threshold_values(threshold_img):
        threshold_img[threshold_img == 0] = 254
        threshold_img[threshold_img == 255] = 0
        threshold_img[threshold_img == 254] = 255
        return threshold_img

    @staticmethod
    def process_set_images():
        process_from_cards = 'thresh_from_card_images'
        set_names = [name.split('.')[0] for name in os.listdir('png_set_images')]
        for set_name in set_names:
            card_image = get_first_card_image_from_set(set_name)
            crop_set_img = card_image[530:568, 560:618]
            greyscale_crop_set_img = cv2.cvtColor(crop_set_img, cv2.COLOR_BGR2GRAY)
            thes, thresh_crop_set_img = cv2.threshold(greyscale_crop_set_img, 20, 255, cv2.THRESH_OTSU)
            cv2.imwrite(os.path.join(process_from_cards, '{}.png'.format(set_name)), thresh_crop_set_img)