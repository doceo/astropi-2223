import numpy as np
from PIL import Image, ImageDraw
import os


def cropping(image):
    # Open the input image as numpy array, convert to RGB
    img = Image.open(image).convert("RGB")
    np_image = np.array(img)

    # Create same size alpha layer with circle
    alpha = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([829, 29, 3669, 2889], 0, 360, fill=255)

    # Convert alpha Image to numpy array
    np_alpha = np.array(alpha)

    # Add alpha layer to RGB
    np_image = np.dstack((np_image, np_alpha))

    # Save with alpha
    name = str(image)
    Image.fromarray(np_image).save(name + ' crop' + '.png')
