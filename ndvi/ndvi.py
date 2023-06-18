# Written following Astro Pi's guide on NDVI calculation
# https://projects.raspberrypi.org/en/projects/astropi-ndvi/

import os
import cv2
import numpy as np
from fastiecm import fastiecm


class NDVI:
    DISPLAY_DEFAULT = 0
    DISPLAY_CONTRASTED = 1
    DISPLAY_NDVI = 2
    DISPLAY_NDVI_CONTRASTED = 3
    DISPLAY_COLOR = 4

    def __init__(self, image_path, resize_factor=1) -> None:
        self.data = cv2.imread(image_path)
        self.resize_factor = resize_factor

        self.contrasted = self.__contrast_stretch(self.data)
        self.ndvi = self.__calc_ndvi()
        self.ndvi_contrasted = self.__contrast_stretch(self.ndvi)

        color_mapped_prep = self.ndvi_contrasted.astype(np.uint8)
        self.colored = cv2.applyColorMap(color_mapped_prep, fastiecm)

    def display(self, option=DISPLAY_DEFAULT, image_name="Image"):
        image = None
        image_name = "Image"
        match option:
            case 0:
                image = np.array(self.data, dtype=float) / float(255)
                image_name = "Default"
            case 1:
                image = np.array(self.contrasted, dtype=float) / float(255)
                image_name = "Contrasted"
            case 2:
                image = np.array(self.ndvi, dtype=float) / float(255)
                image_name = "NDVI"
            case 3:
                image = np.array(self.ndvi_contrasted, dtype=float) / float(255)
                image_name = "NDVI contrasted"
            case 4:
                image = np.array(self.colored, dtype=float) / float(255)
                image_name = "NDVI colored"

        shape = image.shape
        height = int(shape[0] * self.resize_factor)
        width = int(shape[1] * self.resize_factor)
        image = cv2.resize(image, (width, height))
        cv2.namedWindow(image_name)
        cv2.imshow(image_name, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def __contrast_stretch(self, im):
        in_min = np.percentile(im, 5)
        in_max = np.percentile(im, 95)

        out_min = 0.0
        out_max = 255.0

        out = im - in_min
        out *= (out_min - out_max) / (in_min - in_max)
        out += in_min

        return out

    def __calc_ndvi(self):
        b, g, r = cv2.split(self.data)
        bottom = r.astype(float) + b.astype(float)
        bottom[bottom == 0] = 0.01
        ndvi = (b.astype(float) - r) / bottom
        return ndvi

    def calc_pixel_ndvi(self, x, y):
        b, g, r = cv2.split(self.data)
        bottom = r.astype(float)[x, y] + b.astype(float)[x, y]
        bottom = bottom if bottom != 0 else 0.01
        ndvi = (b.astype(float)[x, y] - r[x, y]) / bottom
        return ndvi

    def save_contrasted(self, directory, filename, extension):
        cv2.imwrite(
            os.path.join(directory, f"{filename}_contrasted.{extension}"),
            self.contrasted,
        )

    def save_ndvi(self, directory, filename, extension):
        cv2.imwrite(
            os.path.join(directory, f"{filename}_ndvi.{extension}"),
            self.ndvi,
        )

    def save_ndvi_contrasted(self, directory, filename, extension):
        cv2.imwrite(
            os.path.join(directory, f"{filename}_ndvi_contrasted.{extension}"),
            self.ndvi_contrasted,
        )

    def save_colored(self, directory, filename, extension):
        cv2.imwrite(
            os.path.join(directory, f"{filename}_colored.{extension}"),
            self.colored,
        )
