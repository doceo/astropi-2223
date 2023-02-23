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
LOOP_TIME = 25

# The sleep between each cycle
SLEEP_TIME = 16

# The temperature limit under which the Raspberry can operate safely
TEMPERATURE_LIMIT = 65

# The max space that the images can reach (2.9 GB) minus the maximum weight of an image (6.9 MB)
MAX_SPACE = 3106616115.2


# Wait until the cpu temperature decrease
def wait_for_cpu():
    cooldown_time = 0
    while float(CPUTemperature().temperature) >= 60:
        sleep(3)
        cooldown_time += 3

    return cooldown_time


# Defining the main function
def main_function():

    base_folder = path.dirname(__file__)

    # Initialise the CSV file
    data_file = path.join(base_folder, "data.csv")
    create_csv(data_file)

    # Inizialise the Log file
    log_file = path.join(base_folder, "events.log")
    create_log(log_file)
    logfile(log_file)

    # Collecting current time
    start_time = datetime.now()
    now_time = datetime.now()

    # Loop is the variable needed to save
    loop = 0

    total_size = 0

    day_time = 0
    night_time = 0
    cooldown_time = 0
    photos_taken = 0
    temperatures = []

    # Run loop for three hours
    while now_time <= start_time + timedelta(seconds=10800 - LOOP_TIME):

        loop += 1

        # Save each lap in log
        logger.info(f"Loop number {loop} started")

        # Update the current time
        now_time = datetime.now()
        print(now_time)

        # Cpu temperature monitoring
        cpu = CPUTemperature()
        logger.info(f"Current CPU temperature {cpu.temperature}")
        temperatures.append(float(cpu.temperature))

        if cpu.temperature > TEMPERATURE_LIMIT:
            logger.info("Temperature limit reached - Waiting until the cpu cools down")
            cooldown_time += wait_for_cpu()
            logger.info("Temperature is now stable - Resuming the loop")
            continue

        light = day_night()

        # If the ISS is not orbiting above the illuminated part of the earth run this code
        if light is False:
            logger.info("night - wait 20 seconds")
            night_time += 20
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

        # Capturing the images
        try:
            save_file = capture(path_image, data_file)
            # Add the size of the last picture taken to the total space occupied
            total_size += stat(save_file).st_size
        except Exception as e:
            logger.error(f"{e.__class__.__name__}: {e}")

        photos_taken += 1

        # Raspberry warm-up time in order to avoid thermal-throttling
        sleep(SLEEP_TIME)

        day_time += (datetime.now() - now_time).seconds

    logger.info("Ending the loop\n\n")

    average_temperature = sum(temperatures) / len(temperatures)
    then, now = start_time.strftime("%Y%m%d-%H%M%S"), datetime.now().strftime(
        "%Y%m%d-%H%M%S"
    )
    total_duration = (datetime.now() - start_time).seconds

    to_GB = lambda x: x / (1024**3)

    free_space = MAX_SPACE - total_size

    logger.info(
        f"{day_time}s spent in day cycles, {night_time}s spent in night cycles, {cooldown_time}s spent cooling down"
    )

    logger.info(
        f"The code started at {then} and ended at {now} - total duration: {total_duration}s"
    )

    logger.info(f"Average temperature: {average_temperature}")

    logger.info(
        f"{photos_taken} photos were taken, {to_GB(total_size)}GB was occupied, {to_GB(free_space)}GB are still available"
    )


# Main code
if __name__ == "__main__":
    print("main.py - AstroPI 2022/2023")

    main_function()
