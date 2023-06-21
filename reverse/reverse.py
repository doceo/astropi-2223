from datetime import datetime
from glob import glob
from json import dump as js_dump
from os import getcwd
from os import name as os_name
from os import path
from time import sleep

from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import IEDriverManager


class Scraper:
    if os_name == "nt":
        # Driver name for Windows operating system
        DRIVERNAME = "msedgedriver.exe"
    else:
        # Driver name for other operating systems
        DRIVERNAME = "msedgedriver"

    def __init__(self) -> None:
        self.data = []  # List to store scraped data
        self.imgs = [
            {
                "name": i.strip("/\\images.jpg"),
                # In exif metadatas 3687 points to the date when the image was taken
                "date": Image.open(i)._getexif()[36867],
                "format_date": datetime.strptime(
                    Image.open(i)._getexif()[36867], "%Y:%m:%d %H:%M:%S"
                ).strftime("%Y-%m-%d %H:%M:%S+0000"),
                "file": i.replace("\\", "/"),
            }
            for i in glob(f"{getcwd()}/images/*")
        ]

        # Running the browser in headless mode (without GUI)
        headless = EdgeOptions()
        headless.add_argument("headless")

        if path.exists(Scraper.DRIVERNAME):
            # Checking if the Edge driver exists in the current directory
            self.driver = webdriver.Edge(
                service=Service(Scraper.DRIVERNAME), options=headless
            )
        else:
            # If the driver doesn't exist, download and install it using the Internet Explorer driver manager
            self.driver = webdriver.Edge(service=Service(IEDriverManager().install()))

        self.driver.get("http://www.isstracker.com/historical")

    def check_date(self, date, name, file):
        # Clearing the input field
        self.driver.find_element(By.ID, "historicalDateTime").clear()
        # Entering the specified date and time
        self.driver.find_element(By.ID, "historicalDateTime").send_keys(date)
        # Clicking the submit button
        self.driver.find_element(By.ID, "submitLookup").click()

        self.data.append(
            {
                "name": name.split("-")[1],
                "file": file.lstrip("images/"),
                "longitude": self.driver.find_element(By.ID, "longitudeValue").text,
                "latitude": self.driver.find_element(By.ID, "latitudeValue").text,
                # Generating an earthengine URL based on the latitude and longitude values
                "url": f"https://earthengine.google.com/timelapse/?authuser=1#v={self.driver.find_element(By.ID, 'latitudeValue').text},{self.driver.find_element(By.ID, 'longitudeValue').text},20.10,latLng",
            }
        )

    def dump_all(self):
        # Check where the ISS was at every date
        for i in self.imgs:
            self.check_date(i["format_date"], i["name"], i["file"])
            sleep(0.5)

        # Dump to json file
        with open("positions.json", "w") as outfile:
            js_dump(self.data, outfile, indent=4)

    def close(self):
        # Closing the webpage and calling the destructor method
        self.driver.close()
        self.__del__()


if __name__ == "__main__":
    scrape = Scraper()
    scrape.dump_all()
    scrape.close()
