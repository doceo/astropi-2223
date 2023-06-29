# Astropi 
2022/2023

**MENTOR**: Prof. Diomede Mazzone

**GROUP** : AstroNat

**MEMBERS** :  Biasi Luca, Bocchetti Francesco, Ferrante Gabriele, Mariano Raffaele, Patruno Luca 

**SCHOOL** :  Liceo Ginnasio "G. B. Vico", Naples - Italy
***
## Comparison of images
Once the photos from space were obtained, the most significant ones were selected, those with fewer clouds and that depicted areas of the planet subject to major changes in recent years, the comparison with the past was made using Google Earth Engine, which offers images of planet earth from 1999 to the present.
Photos were selected when available, in order to have a good ratio between the number of photos and the number of changes

## Criticalities
An unknown error during the experiment in space (which never occurred during the test phase carried out on Earth) deleted the coordinates where each photo was taken from the CSV file, which were fundamental for the processing of the images. To make up for this error, a reverse engineering approach was chosen and applied using a python script.
The "[isstracker](http://www.isstracker.com/historical)" website has been automated, which allows one to find the geographical coordinates of the ISS at a given time, thanks to the "Selenium" library. The script then extrapolated the date and time of the shooting of each photo from the EXIF metadata and inserted them into the website, thus obtaining the coordinates of the ISS at the time of capture.
The program outputs a json file with:
*the time of capture
*the name of the photo file
*geographical coordinates
*the link to the coordinates on Google Earth Engine

## Photographed area

| | |


The photographed area is located on the border between South Africa, Botswana and Zimbabwe, we found it particularly interesting because a single photo shows the following nature reserves:
* Lesheba Wilderness Reserve
* Blouberg Nature Reserve
One of the main causes of deforestation in South Africa is the expansion of agricultural land, especially for crops such as sugar cane, corn and palm oil. 
This agricultural expansion can lead to the conversion of forests into agricultural land, resulting in the loss of wildlife habitat and a decrease in forest cover.


## NDVI Calculation

When we received the data, on Earth we applied the NDVI to the pictures taken and compared them with past satellite images taken from Google Earth Engine.
In order to obtain a coherent NDVI value, we chose the most interesting photo and divided it in two zones, both characterised by a large amount of vegetation, the Blouberg Nature Reserve and the Lesheba Wilderness Reserve.

To obtain the NDVI data we use two different techniques:
* For the images taken from Google Earth Engine, red and infrared colour bands were taken and used to calculate the NDVI value per pixel, by dividing the difference with the sum of the bands.
* For the images taken from the ISS, we used the Python script given by the Astro Pi team, which divides the difference and the sum of the red and blue values of the photos.

The NDVI values of the pixels were then averaged and used to create a temporal series to understand the trend and then it was expanded through a predictive model. The predictive model used was SARIMAX, a model specific for time series forecasting.

## NDVI value interpretation

| NDVI value | Interpretation |
| ------ | --------------------|
| <0.1| Bare ground or clouds|
| 0.1-0.2 | Almost absent plant cover|
| 0.2-0.3 |Very low plant cover |
| 0.3-0.4 | Low plant cover with low vigour or very low plant cover with high vigour|
| 0.4-0.5 | Medium-low plant cover with low vigour or very low plant cover with high vigour|
| 0.5-0.6 |Medium plant cover with low vigour or medium-low plant cover with high vigour |
| 0.6-0.7 | Medium plant cover with low vigour or medium-low plant cover with high vigour|
| 0.7-0.8 |High vegetable cover with high vigour |
| 0.8-0.9 | Very high plant cover with very high vigour|
| 0.9-1.0 | Total plant cover with very high vigour|



## Comparison with the past
The average NDVI value of the individual photos was used as a comparator.
### Blouberg Nature Reserve
| Year | Average NDVI |
| ------ | --------------------|
| 1999 | 0.180974654100000 |
| 2000 | 0.297206569843044 |
| 2001 | 0.252122867858757 |
| 2003 | 0.289401363210102 |
| 2005 | 0.201709501203556 |
| 2006 | 0.258469707921507 |
| 2007 | 0.274601114314674 |
| 2008 | 0.296191658842473 |
| 2009 | 0.349054008366084 |
| 2010 | 0.434939683854799 |
| 2013 | 0.411087932136699 |
| 2014 | 0.307478395255208 |
| 2015 | 0.325029822217378 |
| 2016 | 0.361566611198860 |
| 2017 | 0.245379800210799 |
| 2018 | 0.226133076753798 |
| 2019 | 0.242040742251530 |
| 2020 | 0.302622472289386 |
| 2021 | 0.324795672452039 |
| 2022 | 0.261477623621633 |
| 2023 | 0.235300149631186 |
| 2024 | 0.235733306859671 |
| 2025 | 0.232484347998562 |
| 2026 | 0.229235389137454 |
| 2027 | 0.225986430276346 |
| 2028 | 0.222737471415237 |
| 2029 | 0.219488512554129 |
| 2030 | 0.216239553693021 |
| 2031 | 0.212990594831913 |
| 2032 | 0.209741635970805 |
| 2033 | 0.206492677109697 |




Average NDVI value from 1999 to 2023 of Blouberg Nature Reserve
Vegetation in this area went through drastic changes throughout the years.




### Lesheba Wilderness Reserve
| Year | Average NDVI |
| ------ | --------------------|
| 1999 | 0.204469556415898 |
| 2000 | 0.224939244000000 |
| 2001 | 0.216773297900000 |
| 2003 | 0.223180526400000 |
| 2005 | 0.232205660500000 |
| 2006 | 0.298944037600000 |
| 2007 | 0.301793634100000 |
| 2008 | 0.287186731000000 |
| 2009 | 0.356331938200000 |
| 2010 | 0.405120404900000 |
| 2013 | 0.387292728900000 |
| 2014 | 0.325753250300000 |
| 2015 | 0.350778378100000 |
| 2016 | 0.354227588500000 |
| 2017 | 0.287174352100000 |
| 2018 | 0.289198407400000 |
| 2019 | 0.279123785900000 |
| 2020 | 0.281143947600000 |
| 2021 | 0.350103526200000 |
| 2022 | 0.325949358100000 |
| 2023 | 0.256620839600000 |
| 2024 | 0.256620839600000 |
| 2025 | 0.232484347998562 |
| 2026 | 0.229235389137454 |
| 2027 | 0.225986430276346 |
| 2028 | 0.222737471415237 |
| 2029 | 0.219488512554129 |
| 2030 | 0.216239553693021 |
| 2031 | 0.212990594831913 |
| 2032 | 0.209741635970805 |
| 2033 | 0.206492677109697 |



Average NDVI value from 1999 to 2023 of Leshiba Wilderness Reserve
Vegetation trend in this area is more consistent throughout the years.

In both graphs, the fact that the NDVI values range from 0.18 and 0.43 indicates that the vegetation coverage is low with high vigour.
Furthermore, we could not find in which seasons the Google Earth Engine photos were captured, such information would have been crucial for a better understanding of the data.

In both graphs the peak corresponds with 2010, we hypothesise that such value can be a result of the measures that the South African government has implemented several measures to address deforestation in recent years, including the promotion of sustainable farming practices, the regulation of timber extraction and the conservation of protected forest areas. 
In addition, the commitment to sustainable forest management has been strengthened through participation in international initiatives such as the Forest Stewardship Council (FSC). South Africa also collaborates with international organizations, such as the United Nations Development Programme (UNDP) and the Food and Agriculture Organization (FAO), to address deforestation and promote sustainable forest management.

Moreover, the government promotes afforestation (planting trees in areas without forest cover) and reforestation (replanting trees in deforested areas) initiatives. 
These programs aim to increase forest cover, restore degraded ecosystems, and enhance carbon sequestration.

|  |  |
     Example of Google Earth Engine photo        Example of NDVI processed photo

## Conclusion
Our project aimed to investigate the variation of biomass on planet Earth,
comparing the photographs taken on the ISS with satellite images from the past
and also created a collection containing the images we took and their geographical
coordinates, available for future use by other teams.
During phase 4, we analysed the images received, selecting the most suitable
ones, namely two nature reserves located in South Africa.
The analysis of the data obtained from the application of NDVI to infrared images has
partially confirmed our predictions about biomass variation.
What surprised us is that from 1999 to 2010 the vegetation has increased, probably
thanks to the several measures taken by the South African government. However, all
those manoeuvres do not seem to have worked properly in the last 13 years, as the
vegetative mass has suffered a decrease, which according to our predictive series, is
going to continue for the next decade.
Looking back at our project there are a few things that could have been done
differently. For example, it would have been better to avoid the use of the NIR filter on
the camera, which made the comparison with the satellite images way more difficult.

