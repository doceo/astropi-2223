# AstroNat Modules
from utils import *

# Modules for logging
from logzero import logger, logfile

# Module for path of the CSV file
from os import path, stat

# Module for warm-up
from time import sleep

# Module for the while loop
from datetime import datetime, timedelta

# Module for cpu temperature monitoring
from gpiozero import CPUTemperature

# The time (in seconds) taken for a loop iteration to happen, tested in worst case scenario
LOOP_TIME = 30

# The temperature limit under which the Raspberry can operate safely
TEMPERATURE_LIMIT = 63

# The max space that the images can reach (2.9 GB)
MAX_SPACE = 31138512892.6

TEST = False


# Defining the main function
def main_function():

    # Initialise the CSV file
    base_folder = path.dirname(__file__)
    data_file = path.join(base_folder, "data.csv")
    create_csv(data_file)

    # Inizialise the Log File
    logfile(path.join(base_folder, "events.log"))

    # Collecting current time
    start_time = datetime.now()
    now_time = datetime.now()

    # Loop is the variable needed to save
    loop = 0

    total_size = 0

    # Run loop for three hours
    while now_time < start_time + timedelta(seconds=10800 - LOOP_TIME):

        # Save each lap in log
        logger.info(f"Loop number {loop+1} started")

        # Cpu temperature monitoring
        cpu = CPUTemperature()
        logger.info(f"Current CPU temperature {cpu.temperature}")

        if cpu.temperature > TEMPERATURE_LIMIT:
            logger.info("Temperature limit reached - Waiting 15 seconds to cool down")
            sleep(15)
            loop += 1
            continue

        light = day_night()
        loop += 1

        # Update the current time
        now_time = datetime.now()
        print(now_time)

        # If the ISS is not orbiting above the illuminated part of the earth run this code
        if light is not True:
            logger.info("night - wait 20 seconds")
            sleep(20)
            continue

        # If the total size of the images is bigger than the free space available to use end the loop
        if total_size >= MAX_SPACE:
            logger.info("No empty space remained")
            break

        # If all the conditions are satisfied this part of the code is executed

        logger.info("day - save image")

        # Determine the path and name of the images
        path_image = path.join(
            base_folder, "images", str(datetime.now().strftime("%Y%m%d-%H%M%S"))
        )

        if TEST is True:
            sleep(11)
            break

        # Capturing the images
        try:
            capture(path_image, data_file)
            # Add the size of the last picture taken to the total space occupied
            total_size += stat(path_image).st_size
        except Exception as e:
            logger.error(f"{e.__class__.__name__}: {e}")

        # Raspberry warm-up time in order to avoid thermal-throttling
        sleep(11)

    logger.info("Ending the loop\n\n")


# Main code
if __name__ == "__main__":
    print("main.py - AstroPI 2022/2023")

    main_function()
