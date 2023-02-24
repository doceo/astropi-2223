# Modules for day_night function
from orbit import ISS
from skyfield.api import load as sky_load

# Module for csv
import csv

# Modules for camera
from picamera import PiCamera
from os import path

# Load ephemeris (high accuracy table with position of celestial objects)
EPHEMERIS = sky_load(path.join(path.dirname(__file__), "de421.bsp"))


# Define the function for capturing the images
def capture(imName, dFile):
    """
    ** name_image, is the key in the csv file to identify an image
    ** save_file, is the image's name
    """

    name_image = imName.split("/")[5]
    save_file = imName + ".jpg"

    # Variables for Picamera
    camera = PiCamera()
    camera.resolution = (4056, 3040)

    # Obtain the current ISS coordinates
    location = ISS.coordinates()
    print(location)

    # Collect and add the coordinates, related to the captured photo, to the csv
    row = (
        name_image,
        location.latitude.degrees,
        location.longitude.degrees,
        location.elevation.km,
    )

    # Adding the image correlated data to the CSV file
    add_csv_data(dFile, row)
    print(row)

    # Capturing the image
    camera.capture(f"{save_file}")

    # Closing camera
    camera.close()

    return save_file


# Define the function that determines if the ISS is orbiting above the illuminated part of the earth
def day_night():
    if ISS.at(sky_load.timescale().now()).is_sunlit(EPHEMERIS):
        return True
    return False


# Define the function that creates the CSV file and write the first row
def create_csv(data_file):
    with open(data_file, "w") as f:
        writer = csv.writer(f)
        header = ("Date/time", "Latitude", "Longitude", "Elevation")
        writer.writerow(header)


def create_log(log_file):
    # Check if the log file exists, otherwise it's created
    if path.exists(log_file) is False:
        with open(log_file, "w"):
            pass


# Define the function that writes other rows and the data
def add_csv_data(data_file, data):

    with open(data_file, "a+") as f:
        writer = csv.writer(f)
        writer.writerow(data)
