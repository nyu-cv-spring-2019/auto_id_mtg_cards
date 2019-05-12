import os
import cv2
from util import Util


class PreprocessorImg:

    def __init__(self, img_path):
        self.mtg_img = cv2.imread(img_path)
        self.mtg_just_card = None
        self.mtg_just_card_grayscale = None
        self.mtg_just_card_thres = self._get_just_card_thres()
        self.mtg_greyscale_set_image = None
        self.mtg_thres_set_image = self._find_set_image_alternative()

    def _get_just_card_thres(self):
        """
        https://stackoverflow.com/questions/51656362/how-do-i-crop-the-black-background-of-the-image-using-opencv-in-python
        :return:
        """
        grayscale = cv2.cvtColor(self.mtg_img, cv2.COLOR_BGR2GRAY)
        thes, thresholded = cv2.threshold(grayscale, 20, 255, cv2.THRESH_BINARY)
        thresholded = Util.flip_threshold_values(thresholded)
        bbox = cv2.boundingRect(thresholded)
        x, y, w, h = bbox
        self.mtg_just_card = self.mtg_img[y:y + h, x:x + w]
        self.mtg_just_card_grayscale = grayscale[y:y + h, x:x + w]
        foreground = thresholded[y:y + h, x:x + w]
        return foreground

    def _find_thresh_set_image(self):
        """
        Finding the set image is not that hard because it will always be in the middle of the image. So we just
        find it and crop it out.
        We could use edges to find the set image(?)
        :return:
        """
        height, width = self.mtg_just_card_thres.shape
        height_into_parts_for_cropping = 20
        width_into_parts_for_cropping = 20
        set_image_width = round(width/height_into_parts_for_cropping)
        set_image_height = round(height/width_into_parts_for_cropping)
        start_height = round(set_image_height * 11.4)
        start_width = set_image_width * 16
        crop_set_img = self.mtg_just_card_thres[start_height:start_height + round(set_image_height/1.2),
                       start_width+ round((set_image_width *.3)):start_width + round((set_image_width *1.8))]
        crop_set_img = Util.flip_threshold_values(crop_set_img)
        return crop_set_img

    def _find_set_image_alternative(self):
        """
        We resize to 672x936 because that's what mtg provides as large resolution
        https://scryfall.com/docs/api/images
        :return:
        """
        resized_mtg_card = cv2.resize(self.mtg_just_card_grayscale, (2000, 1500))
        crop_set_img = resized_mtg_card[860:910, 1640:1820]
        thes, thresh_crop_set_img = cv2.threshold(crop_set_img, 20, 255, cv2.THRESH_OTSU)
        new_thresh_crop_set_img = Util.flip_threshold_values(thresh_crop_set_img)
        bbox = cv2.boundingRect(new_thresh_crop_set_img)
        x, y, w, h = bbox
        self.mtg_greyscale_set_image = crop_set_img[y:y + h, x:x + w]
        adjusted_thresh_crop_set_img = thresh_crop_set_img[y:y + h, x:x + w]
        finished_thresh_crop_set_img = Util.flip_threshold_values(adjusted_thresh_crop_set_img)
        return finished_thresh_crop_set_img