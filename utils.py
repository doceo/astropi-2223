# Modules for day_night function
from orbit import ISS
from skyfield.api import load as sky_load

# Module for csv
import csv

# Modules for camera
from picamera import PiCamera
from time import sleep

# Load ephemeris (high accuracy table with position of celestial objects)
EPHEMERIS = sky_load("de421.bsp")


def convert(angle):
    """
    Convert a `skyfield` Angle to an EXIF-appropriate
    representation (positive rationals)
    e.g. 98° 34' 58.7 to "98/1,34/1,587/10"

    Return a tuple containing a boolean and the converted angle,
    with the boolean indicating if the angle is negative.
    """
    sign, degrees, minutes, seconds = angle.signed_dms()
    exif_angle = f"{degrees:.0f}/1,{minutes:.0f}/1,{seconds*10:.0f}/10"
    return sign < 0, exif_angle


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

    # Convert the latitude and longitude to EXIF-appropriate representations
    south, exif_latitude = convert(location.latitude)
    west, exif_longitude = convert(location.longitude)

    # Set the EXIF tags specifying the current location
    camera.exif_tags["GPS.GPSLatitude"] = exif_latitude
    camera.exif_tags["GPS.GPSLatitudeRef"] = "S" if south else "N"
    camera.exif_tags["GPS.GPSLongitude"] = exif_longitude
    camera.exif_tags["GPS.GPSLongitudeRef"] = "W" if west else "E"

    # Capturing the image
    camera.capture(f"{save_file}")

    # Closing camera
    camera.close()

    return True


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


# Define the function that writes other rows and the data
def add_csv_data(data_file, data):

    with open(data_file, "a+") as f:
        writer = csv.writer(f)
        writer.writerow(data)
