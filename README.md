# Astropi 
2022/2023

**MENTOR**: Prof. Diomede Mazzone

**GROUP** : AstroNat

**MEMBERS** :  Biasi Luca, Bocchetti Francesco, Mariano Raffaele, Patruno Luca, Ferrante Gabriele

**SCHOOL** :  Liceo Ginnasio "G. B. Vico", Naples - Italy
***
## Abstract
The aim of the project is to study the variation of biomass on planet Earth. To achieve this goal, it was assumed to photograph the planet with the infrared camera, identifying the areas with the presence of vegetation through NDVI (Normalized Difference Vegetation Index) processing. To obtain the state and the variation of biomass in a given period of time, a comparison with archive photographs was hypothesized.
Substantially, the software verifies that the space station flies over a sunlit area, taking photographs with a cadence compatible with the memory occupation established by Team AstroPi.

The project foresees the study of the collected photographs, comparing the ndvi value of the biomass areas not covered by clouds with the value of the archive photographs, in order to verify the differences and possible contractions of the areas covered by vegetation.


## Criticality of the objectives

In relation to the intended objectives set, a prerequisite for the comparison on NDVI values, as confirmed by the Astropi team, the archive photos provided by the experiences of previous years are not usable, because taken with different tools, unsuitable filters and the earth was mainly obscured by clouds. 
We will then proceed with the collection of the images which in a next phase will be discarded according to the biomass areas detected. Downstream of the selection, they will be properly compared with archive images of other sensors(for example the satellite "sentinel 2”) . In order to make this comparison, parametric corrections will be made for the calculation of the NDVI value, as suggested by the Department of Electrical Engineering and Information Technologies (DIETI) of the University of Naples Federico II, contacted to better understand the management and the evaluation of the NDVI value. Another benefit of the massive collection of images, without any selection before saving, is the availability to offer them for future scientific projects. In this way it will be possible to build up an archive of images taken with updated tools, to be able, possibly in a future project, to compare photographs with the same tool.
Based on the constraints imposed and the hardware available, it was decided to take 501 photographs during the daytime overflight phase. In order to obtain the maximum definition possible, the photographs are taken at the resolution 4060 x 3040 px. To achieve this, the available memory of the GPU had to be expanded to 256 Mb.


## Development process

As described above, the software performs a continuous cycle lasting 180 minutes, as indicated by the Support Team. Inside the cycle, it is checked whether the overflight area is illuminated by the sun. During the test phase, the reliability of the function that verifies this condition was verified, by comparing the data extracted from this with others on the astronomical site, which reports the position of the ISS in real time. In this way it was found that for the function implemented by astroNat the duration of the day is 5 minutes longer than that of the site. For reasons related to the organization of the project, it was not possible to optimize this aspect, and in any case the error committed by the implemented functionality is considered acceptable. Once the position has been verified, the photograph is taken and the CSV file for the collection of information related to the position is updated: longitude, latitude and altitude. This information is associated with the file through its name, which contains the date and the time when the photo is taken. To create this software we proceeded by successive approximations, so as to be able to find a balance between the waiting time for shooting and the maximum amount of usable space.
The final result leads to the saving of 501 photographs for a total wait of 11.5 seconds between one shot and the next.

## Code structure
The software was structured in modules. The main function is developed in such a way as to import the necessary external modules, and the utils module developed by the astroNat team.
The functions used by main_function() in main.py file have been implemented in utils.py.
```
main.py
utils.py
de421.bsp
README.md
events.log
images / main_function.jpg
```



### utils.py
The functions present in utils.py are:

- ` dayNight() `allows you to distinguish day and night, it is based on the orbit and skyfield.api library and utilizes the de421.bsp file to define the position of the ISS in orbit.
- ` capture(imName, dFile, test) ` allows the acquisition of the image, saving it in jpg format with the name consisting of the date and time of the acquisition. It includes the addition of data regarding the acquired image to the csv file which collects all the data of the shots, it is based on the picamera and time library. It takes as input, in order: the name of the image to be saved, the name of the CSV file on which to save the information and a Boolean variable that allows you to test the software even in the absence of a piCamera.

- ` create_csv(data_file) `  is the function that creates the csv file and structures the columns, it is based on the csv and path library. It takes in input the name of the file to create.

- ` add_csv_data(data_file, data) `is the function that uses capture to add the data of the image acquired into the csv, it is based on the csv and path library. It takes as input the name of the file on which to write and the line to put in the queue.


### main.py structure
The main initializes the csv file, if it is not present. Then set the time variables to manage the 180 minute cycle that starts immediately after. The light condition is checked within the cycle, through the dayNight () function, the logic summarized by macro blocks is as follows:
![Diagramma](https://user-images.githubusercontent.com/74982114/155156249-377d8221-0992-41ec-a9af-f7810db8e412.jpg)


