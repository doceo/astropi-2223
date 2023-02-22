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
ADVANCE_LOG = True


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

    day_cycle = 0
    night_cycle = 0
    cooldown_cycle = 0
    temperatures = []

    # Run loop for three hours
    while now_time < start_time + timedelta(seconds=10800 - LOOP_TIME):

        loop += 1

        # Save each lap in log
        logger.info(f"Loop number {loop} started")

        # Cpu temperature monitoring
        cpu = CPUTemperature()
        logger.info(f"Current CPU temperature {cpu.temperature}")
        temperatures.append(float(cpu.temperature))

        if cpu.temperature > TEMPERATURE_LIMIT:
            logger.info("Temperature limit reached - Waiting 15 seconds to cool down")
            cooldown_cycle += 1
            sleep(15)
            continue

        light = day_night()

        # Update the current time
        now_time = datetime.now()
        print(now_time)

        # If the ISS is not orbiting above the illuminated part of the earth run this code
        if light is False:
            logger.info("night - wait 20 seconds")
            night_cycle += 1
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
            save_file = capture(path_image, data_file)
            # Add the size of the last picture taken to the total space occupied
            total_size += stat(save_file).st_size
        except Exception as e:
            logger.error(f"{e.__class__.__name__}: {e}")

        day_cycle += 1

        # Raspberry warm-up time in order to avoid thermal-throttling
        sleep(11)

    logger.info("Ending the loop\n\n")

    if ADVANCE_LOG is False:
        return

    average_temperature = sum(temperatures) / len(temperatures)
    then, now = start_time.strftime("%Y%m%d-%H%M%S"), datetime.now().strftime(
        "%Y%m%d-%H%M%S"
    )
    total_duration = (datetime.now() - start_time).seconds

    to_GB = lambda x: x / (1024**3)

    free_space = MAX_SPACE - total_size

    logger.info(
        f"Executed: {day_cycle} day cycles, {night_cycle} night cycles, during the day, {cooldown_cycle} cooldown cycles"
    )

    logger.info(
        f"The code started at {then} and ended at {now} - total duration: {total_duration}s"
    )

    logger.info(f"Average temperature: {average_temperature}")

    logger.info(
        f"{to_GB(total_size)}GB was occupied of the {to_GB(MAX_SPACE)}GB available - {to_GB(free_space)}GB are still available"
    )


# Main code
if __name__ == "__main__":
    print("main.py - AstroPI 2022/2023")

    main_function()
