# AstroNat Modules
from utils import *

# Modules for logging
from logzero import logger, logfile

# Module for path of the CSV file
from pathlib import Path

# Module for warm-up
from time import sleep

# Module for the while loop
from datetime import datetime, timedelta

# Defining the main function
def main_function():

    # Initialise the CSV file
    base_folder = Path(__file__).parent.resolve()
    data_file = str(base_folder) + '/data.csv'
    create_csv(data_file)

    # Inizialise the Log File
    logfile(base_folder/"events.log")

    # Collecting current time
    start_time = datetime.now()
    now_time = datetime.now()

    # Loop is the variable needed to save
    loop = 0

    # Run loop for three hours
    while (now_time < start_time + timedelta(minutes=180)):

        # Save each lap in log
        logger.info(f'Loop number {loop+1} started')

        # Variables for the dayNight function
        timescale = load.timescale().now()
        # Load ephemeris (high accuracy table with position of celestial objects)
        ephemeris = load('de421.bsp')
        light = dayNight()

        # If the ISS is orbiting above the illuminated part of the earth run this code
        if light == True:
            logger.info('day - save image')

            # Determine the path and name of the images
            image_name = str(datetime.now().strftime("%Y%m%d-%H%M%S"))
            path_image = str(base_folder) + '/images/' + image_name             
            
            # Capturing the images
            try: 
                camera.capture(f"{save_file}")
                #capture(path_image, data_file, 0)
            except Exception as e:
                logger.error(f'{e.__class__.__name__}: {e}')
            
        else:
            logger.info('night - wait 20 seconds')
            sleep(20)

        # Update the current time
        now_time = datetime.now()
        print(now_time)
        
        # Raspberry warm-up time in order to avoid thermal-throttling
        sleep(9.5)
        
        loop += 1


# Main code
if __name__ == '__main__':
    print('main.py - AstroPI 2021/2022')

    main_function()