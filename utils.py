# Modules for daynight function
from orbit import ISS
from skyfield.api import load

# Module for csv
import csv

# Modules for camera
from picamera import PiCamera
from time import sleep

# Define the function for capturing the images
def capture(imName, dFile, test):

    if not test:
        
        """
        ** name_image, is the key in the csv file to identify an image
        ** save_file, is the image's name 
        """

        name_image = imName.split('/')[5]
        save_file = imName + ".jpg"
        
        # Variables for Picamera
        camera = PiCamera()
        camera.resolution = (4056, 3040)
        
        # Obtain the current ISS coordinates
        location = ISS.coordinates()
        print(location)

        # Collect and add the coordinates, related to the captured photo, to the csv
        row = (name_image, location.latitude.degrees, location.longitude.degrees, location.elevation.km)
        
        # Adding the image correlated data to the CSV file
        add_csv_data(dFile, row)
        print(row)
        
        # Capturing the image
        camera.capture(f"{save_file}")
        
        # Closing camera
        camera.close()
        
        # Camera warm-up time
        sleep(2)
        
        return True


# Define the function that determines if the ISS is orbiting above the illuminated part of the earth
def dayNight():
    
    timescale = load.timescale().now()
    
    # Load ephemeris (high accuracy table with position of celestial objects)
    ephemeris = load('de421.bsp')
    
    if ISS.at(timescale).is_sunlit(ephemeris):
        return True
    else:
        return False


# Define the function that creates the CSV file and write the first row
def create_csv(data_file):
    
    with open(data_file, 'w') as f:
        writer = csv.writer(f)
        header = ("Date/time", "Latitude", "Longitude", "Elevation")
        writer.writerow(header)


# Define the function that writes other rows and the data
def add_csv_data(data_file, data):
    
    with open(data_file, 'a+') as f:
        writer = csv.writer(f)
        writer.writerow(data)       