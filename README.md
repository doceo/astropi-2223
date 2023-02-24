# Astropi 
2022/2023

**MENTOR**: Prof. Diomede Mazzone

**GROUP** : AstroNat

**MEMBERS** :  Biasi Luca, Bocchetti Francesco, Ferrante Gabriele, Mariano Raffaele, Patruno Luca 

**SCHOOL** :  Liceo Ginnasio "G. B. Vico", Naples - Italy
***
## Abstract
The aim of the project is to study the variation of biomass on planet Earth. To achieve this goal, it was assumed to photograph the planet with the infrared camera, identifying the areas with the presence of vegetation through NDVI (Normalized Difference Vegetation Index) processing. To obtain the state and the variation of biomass in a given period of time, a comparison with archive photographs was hypothesized.
Before the acquisition of the images, the software verifies that the space station flies over a sunlit area, taking photographs with a cadence compatible with the memory occupation established by the AstroPi team.

The project foresees the study of the collected photographs, comparing the NDVI value of the biomass areas not covered by clouds with the value of the archive photographs, in order to verify the differences and possible contractions of the areas covered by vegetation. Once this comparison has been made, it will be possible to obtain a predictive series regarding the percentage of biomass.


## Criticality of the objectives
In relation to the intended objectives set, a prerequisite for the comparison on NDVI values, as confirmed by the AstroPi team, some of the archive photos provided by the experiences of previous years are not usable, because taken with different tools, unsuitable filters and the earth was mainly obscured by clouds. Downstream of the selection, they will be properly compared with archive images of other sensors (for example the satellite "sentinel 2”) . Another benefit of the massive collection of images, without any selection before saving, is the availability to offer them for future scientific projects. In this way it will be possible to build up an archive of images taken with updated tools, to be able, possibly in a future project, to compare photographs with the same tool. Based on the constraints imposed and the hardware available, it was decided to take a maximum of 420 photographs during the daytime overflight phase. In order to obtain the maximum definition possible, the photographs are taken at the resolution 4060 x 3040 px.


## Development process
As described above, the software performs a continuous cycle lasting 180 minutes, as indicated by the Support Team. Inside the cycle, it is checked whether the overflight area is illuminated by the sun. During the test phase, the reliability of the function that verifies this condition was verified, by comparing the data extracted from it with others on the astronomical site, which reports the position of the ISS in real time. In this way it was found out that for the function implemented by AstroNat the duration of the day is 5 minutes longer than the one of the site. For reasons related to the organization of the project, it was not possible to optimize this aspect, and in any case the error committed by the implemented functionality is considered acceptable. Once the position has been verified, the photograph is taken and the CSV file, which contains the collection of information related to the position, is updated: longitude, latitude and altitude.This information is associated with the file through its name, which contains the date and the time when the photo is taken. To know how often the Raspberry should take a photo, it has been tested how many photos could be taken and then how many seconds to wait between each iteration of the loop, in order to leave some free storage space at the end of the experiment. In the end the folder inside the project will contain from 350 to 500 photographs for a total wait time of 14 seconds, including a delay of 2 seconds due to the execution time, between one shot and the next, for a total occupied storage space of up to 2.9 Gb.  
  
Experiments included extensive log analysis to pinpoint problems, such as a loop iteration taking too long or exceeding the photo limit.
In order to make the comparison between the photos taken during the experiment and the old photos, the Department of Electrical Engineering and Information Technologies (DIETI) of the University of Naples Federico II has been contacted, to better understand the management and the evaluation of the NDVI value. This comparison will be made on earth after the experiment in order to avoid slowing down the execution of the software in space.

## Safety technical choices
To avoid a possible overheating of the raspberry, knowing that the maximum temperature at which it can operate is 70 ºC, if the temperature should reach 65 ºC, the shooting of the photos is interrupted for all the period of time necessary for the raspberry to cool down at the temperature of 60°C.  
Moreover, it was also implemented a conditional check which verifies that the amount of space occupied by the photos does not get over 2.9 GB.  
If the camera does not take the picture, the program makes sure to report the error in the logs.

## Code structure
The software was structured in modules. The main function is developed in such a way as to import the necessary external modules, and the utils module developed by the AstroNat team.  
The functions used by main_function() in the main.py file have been implemented in utils.py.
```
main.py
utils.py
de421.bsp
README.md
events.log
example_logs / working_events.log
example_logs / space_error.log
images / main_function.jpg
```

### utils.py
The functions present in utils.py are:

* `create_log(log_file)` checks if the log file exists, and it creates the file if it doesn’t.
* `convert(angle)` converts a “skyfield” angle to an EXIF-appropriate representation (positive rationals) and returns a tuple containing a boolean and the converted angle, with the boolean indicating if the angle is negative.
* ` day_night() `allows you to distinguish day and night, it is based on the orbit and skyfield.api library and utilizes the de421.bsp file to define the position of the ISS in orbit.
* ` capture(imName, dFile, test) ` allows the acquisition of the image, saving it in jpg format with the name consisting of the date and time of the acquisition. It includes the addition of data regarding the acquired image to the csv file which collects all the data of the shots, it is based on the picamera and time library. It takes as input, in order: the name of the image to be saved, the name of the CSV file on which to save the information and a Boolean variable that allows you to test the software even in the absence of a piCamera.

* ` create_csv(data_file) `  is the function that creates the csv file and structures the columns, it is based on the csv and path library. It takes in input the name of the file to create.

* ` add_csv_data(data_file, data) `is the function that uses capture to add the data of the image acquired into the csv, it is based on the csv and path library. It takes as input the name of the file on which to write and the line to put in the queue.

### events.log
`events.log` is the main log file. Each time the code runs it checks if the file exists with the `create_log` function and it writes in it every useful information.


### example_logs
`example_logs` is a folder which contains two log files.  
Each of them shows for each cycle the number, the CPU temperature, the result of the `day_night` function, with the corresponding sleep established, the time and date of when the code has been executed and the line number from which it was written.

* `working_events.log` is the log obtained from a code test, left to run for 3 consecutive hours.
* `space_error.log` is the log obtained from a test aimed at reaching the memory limit. To achieve this quickly the limit was decreased to allow the program to store only a small number of photos.



### main.py structure
The main file initializes the csv file, if it is not present. Then it sets the time variables to manage the 180 minute cycle that starts immediately after. The light condition is checked within the cycle, through the day_night() function, the logic summarized by macro blocks is as follows:
![diagramma flusso 2](https://user-images.githubusercontent.com/74982114/221209695-e56156e5-83c5-4838-b9f7-5713b52bf735.jpg)




