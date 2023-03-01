# 07-streaming-data-final-project
The final project for Streaming Data
> Use RabbitMQ to create 1 producer and 4 consumers that will be used to monitor data from patients with sensors monitoring their troponin levels. Read one value every hour.

## Before You Begin
- [x] Fork this starter repo into your GitHub.
- [x] Clone your repo down to your machine.
- [x] View / Command Palette - then Python: Select Interpreter
- [x] Select your conda environment. 

## Prerequisites
* RabbitMQ Server running
* Pika
* Sys
* Webbrowser
* CSV
* Time

## Background
Troponin is a protein in the heart muscle that regulates heart muscle contractions. A troponin test is a laboratory test that measures troponin levels in the blood. Troponin levels found in the blood is often an indicator of heart damage.

Normally, there is no troponin circulating in the blood. However, when the heart muscle cells sustain damage, it releases troponin. The more damage to the heart muscle cells, the higher the troponin levels will go. A high-sensitivity cardiac troponin T (hscTnT) test has a general cutoff to rule out heart damage. The cutoff level is 10 nanograms per liter (ng/L) or lower for females. The level is 15 ng/L or lower for males.

The main cause of elevated troponin level is injury to the heart muscle, specifically a heart attack. However, there are several other cardiac conditions that can damage the heart or reduce blood flow, and thus, result in an increase in troponin levels. These conditions include, but are not limited to:
*	Cardiomyopathy
*	Heart failure
*	Kidney Failure
*	Sepsis
*	Stroke

The assessment of patients with acute chest pain in the emergency room is a time-consuming diagnostic challenge. Recently, it’s been shown that measurements of the cardiac-specific proteins Troponin T and Troponin I are superior to conventional measurement for the detection of even minor injury to the heart.

The use of troponin measurements in the emergency room is impaired by the limited availability of analytic techniques and long turnover times.

## The Project

I did some reading about Continuous Glucose Monitoring (CGM) which are devices that help manage Type 1 and Type 2 diabetes. A sensor is placed just under your skin that measures your glucose levels for 24 hours. A transmitter sends results to a device or cell phone. This allows the person with the GCM to receive data that shows blood sugar level changes over time; allows for their healthcare provider to review the patient’s data for personalized care; and the device sends alerts when glucose levels rise or fall allowing the patient to make changes quickly.

After reading about CGMs, I started thinking about other potential devices that could monitor other health concerns more closely to detect problems and provide early intervention to prevent further damage to the body or even death.

This led to my researching heart attacks, damage to the heart, and heart failure.

What if there was a monitor, similar to the CGM, that tested troponin levels periodically and sent alerts to doctors when numbers increased at certain intervals and/or were at or above certain levels that may indicate heart damage?

I created a fake data set to monitor 4 patients in 24 hours. Their troponin levels were read once every hour and monitored for changes. Patient_troponin_levels.csv has 4 columns:
* [0] Time = Date-time stamp for the sensor
* [1] patient1 = The first patient’s troponin levels --> send to message queue “patient1”
* [2] patient2 = The second patient’s troponin levels --> send to message queue “paitent2”
* [3] patient3 = The third patient’s troponin levels --> send to message queue “patient3” 
* [4] patient4 = The fourth patient’s troponin levels --> send to message queue “patient4”

#### Significant Events
We want to know if:
1. A patient’s troponin levels increased by 7 or more ng/l in the last hour and/or
1. A patient’s troponin levels were at or above 30 ng/l

I came up with which alerts to set from this inforgraphic from the "Troponin fact sheet for Primary Care" from the Department of Clinical Biochemistry. A general guidance on the ranges of troponin in the blood that may suggest myocardial infarction (MI), or heart attack.

![0](https://user-images.githubusercontent.com/105391626/222038771-94380cb3-32f8-4a1f-acca-6af21a4ddd37.jpeg)

https://www.nbt.nhs.uk/sites/default/files/Trop%20w%20%20header.pdf

#### My dataset tells 4 stories:
1. Patient 1 levels are low and consistent. Doesn't indicate any reason for alarm
2. Patient 2 levels increases quickly and gets pretty high. I only entered 10 rows of data for patient 2 to imply that the numbers increased high enough and quick enough there was some kind of intervention happening.
3. Patient 3 levels remained  relatively low for most of the 24 hours and then begin to increase quickly and suddenly.
4. Patient 4 levels were mostly random. Both high and low at times to show the importance of monitoring because sometimes you don't always know what will happen.

## The Significance
* 10-15% of heart attack patients die before arriving at the hospital. 10% of heart attack patients die at the hospital. 
* With each passing minute after a heart attack, more heart tissue loses oxygen and deteriorates or dies. If there is a large area of damaged heart muscle, the patient may have prolonged health complications.
* Timely treatment of a heart attack is vital. 
* If there is something that can help in the early detection and, therefore, early intervention of a heart attack then more patients may have a better chance at living a longer, healthier life.

## Sources
https://www.rabbitmq.com
https://www.medicinenet.com/high_sensitivity_troponin_test_ranges_and_values/article.htm
https://www.healthgrades.com/right-care/heart-health/troponin-levels?tpc=latest-news
https://www.bangkokhearthospital.com/en/content/heart-attack-early-diagnosis-and-treatment-can-save-your-life
https://my.clevelandclinic.org/health/drugs/11444-glucose-continuous-glucose-monitoring

## Screenshots

### Producer
![troponin_producer](https://user-images.githubusercontent.com/105391626/222039679-bc5a6b56-2075-4e0c-aca1-8bad68fe9c3c.png)

### Patient 1 Consumer
![patient1_Consumer](https://user-images.githubusercontent.com/105391626/222039712-1ddafc2c-c273-4be2-b08d-a0cea5a6d799.png)

### Patient 2 Consumer
![patient2_consumer](https://user-images.githubusercontent.com/105391626/222039749-11ce6815-31f5-4b8c-9bbe-74cba93aab6f.png)

### Patient 3 Consumer
![patient3_consumer](https://user-images.githubusercontent.com/105391626/222040541-249f7a04-08ae-4ce6-bb81-a708d44ab64e.png)

### Patient 4 Consumers
![patient4_consumer](https://user-images.githubusercontent.com/105391626/222040566-c951a811-d9d4-4e81-a437-d917b2f646d8.png)

### RabbitMQ Admin Site
![frontpage](https://user-images.githubusercontent.com/105391626/222040678-9e4b48e3-365f-493d-b610-b62547ed56cb.png)

![Blank 4 Grids Collage](https://user-images.githubusercontent.com/105391626/222040647-fe175866-a433-47ca-ac33-5e3e2ddc51ad.png)
