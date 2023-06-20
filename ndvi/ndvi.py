# Written following Astro Pi's guide on NDVI calculations
# https://projects.raspberrypi.org/en/projects/astropi-ndvi/

import os
import cv2
import numpy as np
from fastiecm import fastiecm


class NDVI:
    """
    Class for performing NDVI (Normalized Difference Vegetation Index) calculations on an image.
    """

    # Display options for the image
    DISPLAY_DEFAULT = 0
    DISPLAY_CONTRASTED = 1
    DISPLAY_NDVI = 2
    DISPLAY_NDVI_CONTRASTED = 3
    DISPLAY_NDVI_CONTRASTED_REVERSED = 4
    DISPLAY_COLOR = 5

    def __init__(self, image_path) -> None:
        """
        Initializes the NDVI calculator with the provided image path and optional resize factor.

        Args:
            image_path (str): The path to the input image file.
        """

        self.data = cv2.imread(image_path)

        self.contrasted = self.__contrast_stretch(self.data)
        self.ndvi = self.__calc_ndvi()
        self.ndvi_contrasted = self.__contrast_stretch(self.ndvi)
        self.ndvi_contrasted_reversed = np.vectorize(lambda val: 255 - val)(
            self.ndvi_contrasted
        )

        color_mapped_prep = self.ndvi_contrasted.astype(np.uint8)
        self.colored = cv2.applyColorMap(color_mapped_prep, fastiecm)

    def display(self, option=DISPLAY_DEFAULT, image_name="Image", resize_factor=1):
        """
        Displays the processed image based on the specified display option.

        Args:
            option (int, optional): The display option to choose from the class constants.
                                    Defaults to DISPLAY_DEFAULT.
            image_name (str, optional): The name to display as the window title. Defaults to "Image".
            resize_factor (float, optional): The factor by which to resize the displayed image. Defaults to 1.
        """

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
                image = np.array(self.ndvi_contrasted_reversed, dtype=float) / float(
                    255
                )
                image_name = "NDVI contrasted reversed"
            case 5:
                image = np.array(self.colored, dtype=float) / float(255)
                image_name = "NDVI colored"

        shape = image.shape
        height = int(shape[0] * resize_factor)
        width = int(shape[1] * resize_factor)
        image = cv2.resize(image, (width, height))
        cv2.namedWindow(image_name)
        cv2.imshow(image_name, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def __contrast_stretch(self, im, min_val=0.0, max_val=255.0):
        """
        Applies contrast stretching to the input image.

        Args:
            im (numpy.ndarray): The input image array.
            min_val (float, optional): The minimum output value. Defaults to 0.0.
            max_val (float, optional): The maximum output value. Defaults to 255.0.

        Returns:
            numpy.ndarray: The contrast-stretched image array.
        """

        in_min = np.percentile(im, 5)
        in_max = np.percentile(im, 95)

        out_min = min_val
        out_max = max_val

        out = im - in_min
        out *= (out_min - out_max) / (in_min - in_max)
        out += in_min

        return out

    def __calc_ndvi(self):
        """
        Calculates the NDVI values for the input image.

        Returns:
            numpy.ndarray: The NDVI array.
        """

        b, g, r = cv2.split(self.data)
        bottom = r.astype(float) + b.astype(float)
        bottom[bottom == 0] = 0.01
        ndvi = (b.astype(float) - r) / bottom
        return ndvi

    def save_contrasted(self, directory, filename, extension):
        """
        Saves the contrasted image to a file.

        Args:
            directory (str): The directory to save the file.
            filename (str): The base filename for the saved image.
            extension (str): The image file extension (e.g., 'jpg', 'png').
        """

        cv2.imwrite(
            os.path.join(directory, f"{filename}_contrasted.{extension}"),
            self.contrasted,
        )

    def save_ndvi(self, directory, filename, extension):
        """
        Saves the NDVI image to a file.

        Args:
            directory (str): The directory to save the file.
            filename (str): The base filename for the saved image.
            extension (str): The image file extension (e.g., 'jpg', 'png').
        """

        cv2.imwrite(
            os.path.join(directory, f"{filename}_ndvi.{extension}"),
            self.ndvi,
        )

    def save_ndvi_contrasted(self, directory, filename, extension):
        """
        Saves the contrasted NDVI image to a file.

        Args:
            directory (str): The directory to save the file.
            filename (str): The base filename for the saved image.
            extension (str): The image file extension (e.g., 'jpg', 'png').
        """

        cv2.imwrite(
            os.path.join(directory, f"{filename}_ndvi_contrasted.{extension}"),
            self.ndvi_contrasted,
        )

    def save_ndvi_contrasted_reversed(self, directory, filename, extension):
        """
        Saves the reversed contrasted NDVI image to a file.

        Args:
            directory (str): The directory to save the file.
            filename (str): The base filename for the saved image.
            extension (str): The image file extension (e.g., 'jpg', 'png').
        """

        cv2.imwrite(
            os.path.join(directory, f"{filename}_ndvi_contrasted_reversed.{extension}"),
            self.ndvi_contrasted_reversed,
        )

    def save_colored(self, directory, filename, extension):
        """
        Saves the colored NDVI image to a file.

        Args:
            directory (str): The directory to save the file.
            filename (str): The base filename for the saved image.
            extension (str): The image file extension (e.g., 'jpg', 'png').
        """

        cv2.imwrite(
            os.path.join(directory, f"{filename}_colored.{extension}"),
            self.colored,
        )
