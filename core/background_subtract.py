import cv2
import numpy as np
import requests

from core.mtg_api import get_all_cards_in_set


def find_card(input_image, set_id, use_cv2_cross_corr=False):
    cards = get_all_cards_in_set(set_id)
    card_results = {}
    len_cards = len(cards)
    processing = 0
    for card in cards:
        card_url = card[0]
        card_id = card[1][0]
        card_name = card[2]
        card_image = requests.get(card_url).content
        img_array = np.array(bytearray(card_image), dtype=np.uint8)
        template_card_img = cv2.imdecode(img_array, -1)
        height, width, colors = template_card_img.shape
        resized_input_image = cv2.resize(input_image, (width, height))
        full_result = 0
        greyscale_resized_input_image = cv2.cvtColor(resized_input_image, cv2.COLOR_BGR2GRAY)
        greyscale_template_card_img = cv2.cvtColor(template_card_img, cv2.COLOR_BGR2GRAY)
        if use_cv2_cross_corr:
            full_result = cv2.matchTemplate(greyscale_resized_input_image, greyscale_template_card_img, cv2.TM_CCORR_NORMED)
        else:
            for row in range(len(resized_input_image)):
                for column in range(len(resized_input_image[row])):
                    intensity_result = greyscale_resized_input_image[row][column] - greyscale_template_card_img[row][column]
                    full_result += intensity_result
        processing += 1
        card_results[card_id] = full_result
        print("processing {} out of {}, card name: {}".format(processing, len_cards, card_name))
    return card_results

