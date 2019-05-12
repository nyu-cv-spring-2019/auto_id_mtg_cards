import os

import cv2
import requests
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
import numpy as np

def make_set_image_each_set():
    """
    Gets the svg for all sets from the api and converts it to png then saves both to disk.
    :param
    :return:
    """
    sets = requests.get('https://api.scryfall.com/sets').json()['data']
    small_sets = []
    for set in sets:
        if set['released_at'] > '2015-01-01' and set['released_at'] < '2019-05-01' and set['set_type'] in ['core', 'expansion']:
            small_sets.append(set)
    for set in small_sets:
        icon_uri = set['icon_svg_uri']
        set_name_svg = '{}.svg'.format(set['code'])
        svg_location = 'svg_set_images'
        response_svg_image = requests.get(icon_uri)
        with open(os.path.join(svg_location, set_name_svg), "wb") as f:
            f.write(response_svg_image.content)
        drawing = svg2rlg(os.path.join(svg_location, set_name_svg))
        renderPM.drawToFile(drawing, os.path.join('png_set_images', "{}.png".format(set['code'])), fmt="PNG")


def get_all_cards_in_set(set_code):
    """
    Only extract photo and multiverse_id. Each card object will be a tuple of img_url and multiverse
    We need the multiverse_id to do the full look up after.
    :param set_code:
    :return:
    """
    response_set = requests.get('https://api.scryfall.com/sets/{}'.format(set_code))
    set_card_uri = response_set.json()['search_uri']
    card_tuples = []
    has_more = True
    page = 1
    while has_more:
        set_card_uri = '{}&page={}'.format(set_card_uri, page)
        response_all_cards = requests.get(set_card_uri)
        has_more = response_all_cards.json()['has_more']
        page += 1
        for card in response_all_cards.json()['data']:
            # be careful the multiverse_id is a list? not sure why.
            card_tuple = (card['image_uris']['large'], card['multiverse_ids'], card['name'])
            card_tuples.append(card_tuple)
    return card_tuples


def get_card_by_multiverse_id(univeral_id):
    card = requests.get('https://api.scryfall.com/cards/multiverse/{}'.format(univeral_id)).json()
    return card


def get_first_card_image_from_set(set_code):
    response_set = requests.get('https://api.scryfall.com/sets/{}'.format(set_code))
    set_card_uri = response_set.json()['search_uri']
    response_cards = requests.get(set_card_uri).json()
    large_img_uri = response_cards['data'][0]['image_uris']['large']
    card_image = requests.get(large_img_uri).content
    img_array = np.array(bytearray(card_image), dtype=np.uint8)
    large_img = cv2.imdecode(img_array, -1)
    return large_img