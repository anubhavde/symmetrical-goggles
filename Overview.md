.md-content p { text-align: justify; } .md-content pre { padding: 16px; overflow: auto; font-size: 75%; line-height: 1.45; background-color: #f6f8fa; border-radius: 6px; border: 1px solid #d0d0d0; } .md-content .color-green { color: green; } .md-content .color-red { color: red; } .md-content .color-mute { color: #8e8d8d; }

# 🕵️‍♂️ Introduction

One of the important challenges of autonomous flight is the Sense and Avoid (SAA) task to maintain enough separation from obstacles. While the route of an autonomous drone might be carefully planned ahead of its mission, and the airspace is relatively sparse, there is still a chance that the drone will encounter unforeseen airborne objects or static obstacles during its autonomous flight.

The autonomous SAA module has to take on the tasks of situational awareness, decision making, and flying the aircraft, while performing an evasive maneuver.

There are several alternatives for onboard sensing including radar, LIDAR, passive electro-optical sensors, and passive acoustic sensors. Solving the SAA task with visual cameras is attractive because cameras have relatively low weight and low cost.

**For the purpose of this challenge, we consider a  solution that solely relies on a single visual camera and Computer Vision technique that analyzes a monocular video.**

Flying airborne objects pose unique challenges compared to static obstacles. In addition to the typical small size, it is not sufficient to merely detect and localize those objects in the scene, because prediction of the future motion is essential to correctly estimate if the encounter poses a collision threat to the drone and create a safer route. Such prediction will typically rely on analysis of the motion over a period of time, and therefore requires association of the detected objects across the video frames.

**As a preliminary stage for determining collision threat**, this challenge will be concerned with spatio - temporal airborne object detection and tracking, given a new Airborne Object Tracking dataset, and perform **two benchmarks**:

1.  Airborne detection and tracking
2.  Frame-level airborne detection

# 💾 Dataset

## **Airborne Object Tracking Dataset (AOT) Description**

<span lang="EN-US" style="font-size:15.0pt"><span style="font-family:&quot;Arial&quot;,sans-serif"><span style="color:black">The Airborne Object Tracking (AOT) dataset is a collection of flight sequences collected onboard aerial vehicles with high-resolution cameras. T</span></span></span><span lang="EN-US" style="font-size:15.0pt"><span style="font-family:&quot;Arial&quot;,sans-serif">o generate those sequences, t<span style="color:black">wo aircraft are equipped with sensors and fly <i>planned</i> encounters (e.g., Helicopter1 in Figure 1(a)). The trajectories are designed to create a wide distribution of distances, closing velocities, and approach angles. </span>In addition to the so-called <i>planned</i> aircraft, AOT also contains other <i>unplanned</i> airborne objects, which may be present in the sequences (e.g., Airborne1 in Figure 1(a)). Those objects are also labeled but their distance information is not available. <span style="color:black">Airborne objects usually appear quite small at the distances which are relevant for early detection: </span>0.01% of the image size on average, down to a few pixels in area<span style="color:black"> (compared to common object detection datasets, which exhibit objects covering more considerable portion of the image). This makes AOT a new and challenging dataset for the detection and tracking of potential aerial collision threats.</span></span></span> 

![](https://images.aicrowd.com/uploads/ckeditor/pictures/356/image.png =750x630)

_Figure 1: Overview of the Airborne Object Tracking (AOT) dataset, more details in the "Data Diversity" section_

**In total, AOT includes close to 164 hours of flight data:**

*   4,943 flight sequences of around 120 seconds each, collected at 10 Hz in diverse conditions. Each sequence typically includes at most one planned encounter, although some may include more.
*   5.9M+ images
*   3.3M+ 2D annotation

* * *

## **Dataset Diversity**

A unique feature of AOT compared to comparable existing datasets is the wide spectrum of challenging conditions it covers for the detection and tracking of airborne objects.   
 

![](https://images.aicrowd.com/uploads/ckeditor/pictures/348/image.png =600x305)

_Figure 2: Samples images showcasing the diversity in AOT dataset_

*   <span style="font-size:12pt"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="font-size:15.0pt"><span style="font-family:&quot;Arial&quot;,sans-serif">Airborne object size:&nbsp;often a direct proxy to a distance to the object, the area of objects in the dataset varies from 4 to 1000 pixels, as illustrated in Fig. 1 (b). Note that the ground truth for tiny and small objects cannot be marked perfectly tight, instead it is approximated with circles of radius 3 and 8 pixels respectively, which yield two bright horizontal lines in the Fig. 1 (b).</span></span></span></span>
*   <span style="font-size:12pt"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="font-size:15.0pt"><span style="font-family:&quot;Arial&quot;,sans-serif">Planned encounters:</span></span></span></span>
    *   <span style="font-size:12pt"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="font-size:15.0pt"><span style="font-family:&quot;Arial&quot;,sans-serif">Distance to the object: concentrated between 600 to 2,000 meters (25-75 percentiles)</span></span></span></span>
    *   <span style="font-size:12pt"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="font-size:15.0pt"><span style="font-family:&quot;Arial&quot;,sans-serif">Closing velocity (the velocity with which the object approaches the camera): up to 70 meters per second</span></span></span></span>
    *   <span style="font-size:12pt"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="font-size:15.0pt"><span style="font-family:&quot;Arial&quot;,sans-serif">Angle of approach:</span></span></span></span>
        *   <span style="font-size:12pt"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="font-size:15.0pt"><span style="font-family:&quot;Arial&quot;,sans-serif">Azimuth: from -60 to 60 degrees</span></span></span></span>
        *   <span style="font-size:12pt"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="font-size:15.0pt"><span style="font-family:&quot;Arial&quot;,sans-serif">Elevation: from -45 to 45 degrees</span></span></span></span>
    *   <span style="font-size:12pt"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="font-size:15.0pt"><span style="font-family:&quot;Arial&quot;,sans-serif">Collision risk: out of the planned encounters, it is estimated that 55% of them would qualify as potential collision trajectories and close encounters</span></span></span></span>
*   <span style="font-size:12pt"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="font-size:15.0pt"><span style="font-family:&quot;Arial&quot;,sans-serif">Camera roll angle: related to camera trajectory, the bank angle goes up to 60 degrees in high bank turns</span></span></span></span>
*   <span style="font-size:12pt"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="font-size:15.0pt"><span style="font-family:&quot;Arial&quot;,sans-serif">Altitude: the altitude of the camera varies from 24 to 1,600 meters above mean sea level <a>(MSL) </a></span></span><span lang="EN-US" style="font-size:15.0pt"><span style="font-family:&quot;Arial&quot;,sans-serif">with most captures between 260 and 376 meters MSL. The captures are as low as 150 meters above ground, which is challenging to capture.</span></span></span></span>
*   <span style="font-size:12pt"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="font-size:15.0pt"><span style="font-family:&quot;Arial&quot;,sans-serif">Distance to visual&nbsp;horizon: 80% of targets are above the horizon, 1% on the horizon, and 19% below. This feature particularly affects the amount of clutter in the background of the object.</span></span></span></span>
*   <span style="font-size:12pt"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="font-size:15.0pt"><span style="font-family:&quot;Arial&quot;,sans-serif">Airborne object type: see Figure 1 (d) and Table 1 below</span></span></span></span>
*   <span style="font-size:12pt"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="font-size:15.0pt"><span style="font-family:&quot;Arial&quot;,sans-serif">Sky conditions and visibility: sequences with clear, partly cloudy, cloudy, and overcast skies are provided, 69% of the sequences have good visibility, 26% have medium visibility, and 5% exhibit poor visibility conditions.</span></span></span></span>
*   <span style="font-size:12pt"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="font-size:15.0pt"><span style="font-family:&quot;Arial&quot;,sans-serif">Light conditions:</span></span></span></span>
    *   <span style="font-size:12pt"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="font-size:15.0pt"><span style="font-family:&quot;Arial&quot;,sans-serif">Back-lit aircraft, sun flare, or overexposure are present in 5% of the sequences</span></span></span></span>
    *   <span style="font-size:12pt"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="font-size:15.0pt"><span style="font-family:&quot;Arial&quot;,sans-serif">Time of the day: data was captured only during well lit daylight operations but a different times of the day, creating different sun angle conditions</span></span></span></span>
    *   <span style="font-size:12pt"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="font-size:15.0pt"><span style="font-family:&quot;Arial&quot;,sans-serif">Terrain: flat horizon, hilly terrain, mountainous terrain, shorelines</span></span></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><span lang="EN-US" style="font-size:15.0pt"><span style="font-family:&quot;Arial&quot;,sans-serif">Table 1 below provides an overview of the objects present in the dataset. There are 3,306,350 frames without labels as they contain no airborne objects. Note that all airborne objects are labeled.&nbsp;For images with labels, there are on average 1.3 labels per image.</span></span></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">Split</span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">All Airborne Objects</span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">Airplane</span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">Helicopter</span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">Bird</span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">Other*</span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">Training</span></span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">2.89M</span></span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">0.79M</span></span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">1.22M</span></span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">0.33M</span></span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">0.54M</span></span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">Planned</span></span></span></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">1.39M</span></span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">0.24M</span></span></span></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">1.15M</span></span></span></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">0.00M</span></span></span></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">0.00M</span></span></span></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">Unplanned</span></span></span></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">1.50M</span></span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">0.56M</span></span></span></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">0.07M</span></span></span></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">0.33M</span></span></span></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">0.54M</span></span></span></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">Test</span></span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">0.50M</span></span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">0.13M</span></span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">0.17M</span></span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">0.06M</span></span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">0.14M</span></span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">Planned</span></span></span></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">0.20M</span></span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">0.04M</span></span></span></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">0.16M</span></span></span></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">0.00M</span></span></span></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">0.00M</span></span></span></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">Unplanned</span></span></span></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">0.29M</span></span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">0.08M</span></span></span></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">0.00M</span></span></span></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">0.06M</span></span></span></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">0.14M</span></span></span></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">Total</span></span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">3.39M</span></span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">0.92M</span></span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">1.39M</span></span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">0.39M</span></span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">0.69M</span></span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif"><span style="color:black">* includes hot air balloons, ultra lights, drones, etc</span></span></span></span></span>

_Table 1: Types and distribution of airborne object labels_

## **Data Collection Process**

During a given data capture, the two sensor-equipped aircraft perform several planned rectilinear encounters, repositioning in between maneuvers. This large single data record is then split into digestible sequences of 120 seconds. Due to those cuts in the original record, individual sequences may comprise a mix of: rectilinear approaches, steep turns, with or without the aircraft in sight. As an example, it is possible to have a single rectilinear approach split across two sequences. In addition to the planned aircraft, a given sequence might contain other unplanned airborne objects like birds and small airplanes, or even no airborne objects.

## **Data Format**

The data obtained from two front-facing cameras, the Inertial Navigation System (INS), and the GPS provide the onboard imagery, the orientation and position of the aircraft. The provided dataset will therefore include:

1.  Front-view, low-altitude videos (sampled as .png images at 10 FPS) 
2.  Distance to planned aircraft (calculated based on their GPS) 
3.  Manually labeled ground truth bounding boxes for all visible airborne objects. 

## **Additional details on the dataset**

Dataset Folder Structure: The dataset is given as a _training_ directory, while the validation and test sets are kept separate and not available to competitors. To ensure generalization, sequences collected the same day are either in the training dataset, or in validation / test dataset. They cannot be split between the two datasets (validation and test sets can share common days/ areas).  
The training set is further split into smaller directories (to facilitate download), each one containing _ImageSets_ and _Images_ folders. 

## **The _ImageSets_ folder holds:**

1.  _groundtruth.json_ (and its tabular representation  _groundtruth.csv_), which contains metadata and ground truth information about sequence images.
2.  _valid\_encounters\_maxRange700\_maxGap3\_minEncLen30.json_ contains information about encounters (defined in the Benchmarks section) with planned aircraft within 700m. distance, which last at least 3 seconds. For each encounter, we provide the corresponding sequence (sub-folder) name, relevant image names and additional information on distance statistics of aircraft in the encounter, if the encounter is below or above horizon and its length in frames. **This file provides information on a representative set of images / sequences to start training with, in case usage of the full dataset is not possible.**
3.  _valid\_encounters\_maxRange700\_maxGap3\_minEncLen30.csv_ – tabular representation of encounter information from _valid\_encounters\_maxRange700\_maxGap3\_minEncLen30.json_ (image names that correspond to each encounter are omitted.

The _Images_ folder finally holds images sampled from one sequence per directory (directory name is unique per each Images folder, but can repeat across in different Images folders). An overview of the dataset split is provided in Table 2 below. 

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-family:&quot;Calibri Light&quot;,sans-serif">Directory</span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-family:&quot;Calibri Light&quot;,sans-serif"><span style="color:black">Size (TB)</span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-family:&quot;Calibri Light&quot;,sans-serif"><span style="color:black">Sequences</span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-family:&quot;Calibri Light&quot;,sans-serif"><span style="color:black">Images</span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-family:&quot;Calibri Light&quot;,sans-serif"><span style="color:black">Labels</span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri Light&quot;,sans-serif"><span style="color:black">training</span></span></span></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri Light&quot;,sans-serif"><span style="color:black">11.3</span></span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri Light&quot;,sans-serif"><span style="color:black">4,154</span></span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri Light&quot;,sans-serif"><span style="color:black">4,975,765</span></span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri Light&quot;,sans-serif"><span style="color:black">2,891,891</span></span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri Light&quot;,sans-serif"><span style="color:black">validation + test</span></span></span></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri Light&quot;,sans-serif">2.1</span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri Light&quot;,sans-serif">789</span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri Light&quot;,sans-serif">943,852</span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri Light&quot;,sans-serif">496,075</span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri Light&quot;,sans-serif"><span style="color:black">TOTAL</span></span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri Light&quot;,sans-serif"><span style="color:black">13.4</span></span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri Light&quot;,sans-serif"><span style="color:black">4,943</span></span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri Light&quot;,sans-serif"><span style="color:black">5,919,617</span></span></span></b></span></span>

<span style="font-size:12pt"><span style="font-family:&quot;Times New Roman&quot;,serif"><b><span lang="EN-US" style="font-size:11.0pt"><span style="font-family:&quot;Calibri Light&quot;,sans-serif"><span style="color:black">3,387,966</span></span></span></b></span></span>

_Table 2: Dataset size_

**Sequence format**: Each sequence is contained in a directory label with a universally unique identifier (UUID), the directory then contains the images of the sequence captured at 10 Hz.

**Image format**: 2448 pixels wide by 2048 pixels high, encoded as 8-bit grayscale images and saved as PNG files (lossless compression). The filenames follow the convention _<timestamp><uuid>.png_. The timestamp is 19 characters, and the UUID is 32 characters. The field of view of the camera is 67.8 by 56.8 degrees, for an angular resolution of 0.48 mrad per pixel.

**Ground truth format**: The _groundtruth.json_ files contain 2 keys: _metadata_ and _samples_ organized as follows.

{
  <span class="color-green">"metadata"</span>: {
    <span class="color-green">"description"</span>: "PrimeAir, camera 0 ",  <span class="color-mute"># Description of the sequences</span>
    <span class="color-green">"last_modified"</span>: "Jan-08-2021 23:27:55",  <span class="color-mute"># Last time the file was modified</span>
    <span class="color-green">"version"</span>: "1.0",  <span class="color-mute"># Version of the ground truth file</span>
  },
  <span class="color-green">"samples"</span>: "\[...\]",  <span class="color-mute"># Collection of sample sequences</span>
}

_Code Block 1: structure of the groundtruth.json files_

Each sample sequence is then provided with its own _metadata_ and _entitites_:

{
  <span class="color-green">"metadata"</span>: {
    <span class="color-green">"data_path"</span>: "train/673f29c3e4b4428fa26bc55d812d45d9/",  <span class="color-mute"># Relative path to video</span>
    <span class="color-green">"fps"</span>: 10.0,  <span class="color-mute"># Frequency of the capture in frames per second (FPS)</span>
    <span class="color-green">"number_of_frames"</span>: 1199,  <span class="color-mute"># Number of frames in the sequence</span>
    <span class="color-green">"resolution"</span>: {
        <span class="color-green">"height"</span>: 2048,  <span class="color-mute"># Height of the images in the sequence</span>
        <span class="color-green">"width"</span>: 2448,  <span class="color-mute"># Width of the images in the sequence</span>
    },
  },
  <span class="color-green">"entities"</span>: \[...\],  <span class="color-mute"># Collection of entities (frames / objects)</span>
}

_Code Block 2: structure of a sample sequence_

Finally, each _entity_ corresponds to an image ground truth label. If the label corresponds to a planned airborne object, its distance information may be available. Note that distance data is not available for other non-planned airborne objects in the scene. When such fields may not be available, they are marked as optional below. For example, one image frame may not contain an object label if not airborne object is present in the scene, however some information about the image is still provided (frame number and timestamp).

{
  <span class="color-green">"time"</span>: 1573043646380340792,  <span class="color-mute"># Timestamp associated with the image</span>
  <span class="color-green">"blob"</span>: {
    <span class="color-green">"frame"</span>: 3,  <span class="color-mute"># Frame number associated with the image</span>
    <span class="color-green">"range_distance_m"</span>: 1366,  <span class="color-mute"># (optional) Distance to planned airborne objects [m]</span>
  },
  <span class="color-green">"id"</span>: "Airplane1",  <span class="color-mute"># (optional) Identifier for the label (unique for the sequence)</span>
  <span class="color-green">"bb"</span>: \[1355.2, 1133.4, 6.0, 6.0\],  <span class="color-mute"># (optional), Bounding box [top, left, width, height]</span>
  <span class="color-green">"labels"</span>: {
    <span class="color-green">"is_above_horizon"</span>: -1, <span class="color-mute"># the object is Below(-1)/Not clear(0)/Above(1) the horizon</span>
  },
  <span class="color-green">"flight_id"</span>: "673f29c3e4b4428fa26bc55d812d45d9",
  <span class="color-green">"img_name"</span>: "1566556046185850341673f29c3e4b4428fa26bc55d812d45d9.png",
}

_Code Block 3: structure of an entity (image label)_

# **🎯 Benchmarks**

The Challenge has two benchmarks: the airborne detection and tracking benchmark and the frame-level airborne object detection benchmark. Teams must clearly indicate which benchmark(s) the submission is participating in. The benchmarks are explained below.

## **1\. Airborne Detection and Tracking Benchmark**

Airborne detection and tracking task is essentially an online multi-object tracking with private detections (i.e., detections generated by the algorithm and not provided from external input). There is a wide range of evaluation metrics for multi-object tracking, however the unique nature of the problem imposes certain requirements that help us to define specific metrics for Airborne Detection and Tracking Benchmark. Those requirements and metrics are outlined below.  
To ensure safe autonomous flight, the drone should be able to detect a collision threat and maneuver to prevent it. However, unless there is a real threat of collision, the best way to ensure a safe flight is to follow the originally planned route. Deviating from the planned route increases the chances of encounters with other airborne objects and static obstacles, previously not captured by the drone camera. As such, false alarms that might trigger unnecessary maneuvers should be avoided, which imposes a very low budget of false alarms (high precision detection). Another consideration is that while early detection is generally desired, relying only on information from early stages of the encounter might not be indicative of the future motion of the detected airborne object. Therefore, an effective alert must be based on detection (or tracking) that is not too early to allow accurate prediction of future motion, and yet early enough to allow time to maneuver. Typically, such temporal window will depend on a closing velocity between the drone and the other airborne object. However, for simplicity, we will refer to the distance between the drone and the encountered airborne object, to establish when the detections must occur. Finally, to capture sufficient information for future motion prediction, the object should be tracked for several seconds.

To summarize, the requirements for desired solutions are:

1.  Very low number of false alarms 
2.  Detections of the airborne object within the distance that allows maneuver (i.e., not too close) and is informative for future motion prediction (i.e., not too far away)
3.  Tracking the airborne object for sufficient time to allow future motion prediction 

Next, we define airborne metrics that will evaluate if the above terms are met.

The airborne metrics measures:

1.  **Encounter-Level Detection Rate (EDR)** \- number of successfully detected encounters divided by the total number of encounters that should be detected, where an encounter is defined as a temporal sequence (a subset of frames) in which the same planned aircraft (airborne object) is visible (i.e., is manually labeled) and is located within the pre-defined range of distances. The encounter is successfully detected if:
    1.  ​​Its respective airborne object is tracked for at least 3 seconds within the encounter duration.
    2.  The detection and 3 second tracking occur before the airborne object is within 300m to the drone or within the first 3 seconds of the encounter.
2.  **False Alarm Rate (HFAR) per hour** \- a number of unique reported track ids, which correspond to at least one false positive airborne report, divided by total number of hours in the dataset

**Evaluation of submissions**

As previously outlined, one of the requirements of safe autonomous flight is very low number of false alarms. Any solution that exceeds the available budget of false alarms will not be usable in practice due to safety concerns. To encourage realistic solutions and simplify the evaluation, we define a HFAR budget of 2 false alarm per 10 hours of flight = 0.2. _Any submission with HFAR > 0.2 will be published on the leaderboard, but not be considered for ranking. All the submissions that have HFAR <= 0.2 will be ranked based on EDR._ 

## **2\. Frame-level Airborne Object Detection Benchmark**

While the first benchmark of this challenge involves tracking, participants can also submit results for frame-level airborne object detection benchmark. The frame-level metrics will measure:

1.  **Average frame-level detection rate (AFDR)** - a ratio between the number of the detected airborne objects and all the airborne objects that should be detected. For the purpose of this calculation, all the planned airborne aircraft within 700m distance will be considered. 
2.  **False positives per image (FPPI)** \- a ratio between the number of false positive airborne reports and the number of images in the dataset.

**Evaluation of submissions**

To simplify the evaluation and encourage development of realistic solution, the results will be evaluated based on AFDR with a budget of FPPI. _Any submission with FPPI > 0.0002 will be published on the leaderboard, but NOT considered for ranking. All the submissions that have FPPI <= 0.0002 will be ranked based on AFDR._

**Additional details on detection evaluation and false alarms calculation** 

We elaborate on a definition of encounters that form the set of encounters for detection and tracking benchmark. Recall that a planned aircraft is equipped with GPS during data collection and therefore provides GPS measurements associated with its physical location. We further define, a valid airborne encounter as an encounter with planned aircraft during which the maximum distance to the aircraft is at most _UPPER\_BOUND\_MAX\_DIST_. The upper bound on the maximum distance ensures that the detection will be benchmarked with respect to airborne objects that are not too far away from the camera. In addition, an upper bound on the minimum distance in the encounter is defined as _UPPER\_BOUND\_MIN\_DIST_ (to disregard encounters that do not get sufficiently close to the camera).  
Note that dataset videos and the provided ground truth labels might contain other airborne objects that are not planned, or planned airborne objects that do not belong to valid encounters. The airborne metrics does not consider those objects for detection rate calculation and treats them as ‘don’t care’ (i.e., those detections will not be counter towards false alarms). Frame-level metrics consider non-planned objects and planned objects at range > 700m as 'don't care'.

Any airborne report (as defined in Table 3) that does not match an airborne object is considered a false positive and is counted once per the same track id as a false alarm. The reason behind it is that a false alarm might trigger a potential maneuver and hence false positives that occur later and correspond to the same object has lower overall impact in real scenarios.

The definitions of successful detection and false positive depend on the matching criteria between the bounding box produced by the detector and the ground truth bounding box. A common matching measure for object detection is Intersection over Union (IoU). However, IoU is sensitive to small bounding boxes, and since our dataset contains very small objects, we propose to use extended IoU, defined as:

![](https://images.aicrowd.com/uploads/ckeditor/pictures/349/image.png =598x76)

In words: 

*   If the ground truth area >= _MIN\_OBJECT\_AREA_ extended IoU = IoU, and
*   If the ground truth area < _MIN\_OBJECT\_AREA_, the ground truth bounding box is dilated to have at least minimum area = _MIN\_OBJECT\_AREA_, and all the detections (matched against this ground truth) are dilated to have at least minimum area = _MIN\_OBJECT\_AREA_. The dilation operation will maintain aspect ratio of the bounding boxes.

The reported bounding box is considered a match, if the _eIoU_ between the reported bounding box and the ground truth bounding box is greater than _IS\_MATCH\_MIN\_IOU\_THRESH_.

  
If the _eIoU_ between the reported bounding box and any ground truth is less than _IS\_NO\_MATCH\_MAX\_IOU\_THRESH_ the reported bounding box is considered a false positive.

  
Any other case that falls in between the two thresholds is considered neutral (‘don’t care’), due to possible inaccuracies in ground truth labeling.  

Please refer to Tables 3-4 for further clarifications on the terms mentioned in this section.

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif"><b><span lang="EN-US" style="font-size:12.0pt">Term</span></b></span></span></span>

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif"><b><span lang="EN-US" style="font-size:12.0pt"><span style="color:black">Definition</span></span></b></span></span></span>

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="color:black">Bounding box</span></span></span></span>

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="color:black">[top, left, width, height]</span></span></span></span>

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="color:black">Planned airborne object</span></span></span></span>

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif">An airborne object with GPS (in the currently available datasets - Helicopter1, Airplane1) and manulally labeled ground truth bounding box in the image.</span></span></span>

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="color:black">Encounter</span></span></span></span>

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="color:black">1) An interval of time of at least MIN_SECS with a planned airborne object<br>2) The segment can have gaps of length &lt;= 0.1 * MIN_SECS, during which the ground truth might be missing<br>or the object is at a farther range / not visible in the image<br>3) A single encounter can include one airborne object only</span></span></span></span>

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="color:black">Valid encounter (should be detected)</span></span></span></span>

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif">The encounter with airborne object, such that:<br>minimum distance to the object &lt;= UPPER_BOUND_MIN_DIST<br>maximum distance to the object &lt;= UPPER_BOUND_MAX_DIST</span></span></span>

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="color:black">Airborne report</span></span></span></span>

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="color:black">Predicted bounding box, frame id, detection confidence score<br>Optional: track id. If not provided detection id will be used</span></span></span></span>

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="color:black">False positive airborne report</span></span></span></span>

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif">An airborne report that cannot be matched to ANY airborne object (i.e. eIoU with any airborne object is below IS_NO_MATCH_MAX_IOU_THRESH)</span></span></span>

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="color:black">Detected Airborne Object</span></span></span></span>

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="color:black">An airborne object that can be matched with an airborne report</span></span></span></span>

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="color:black">Frame level detection rate <u>per encounter</u></span></span></span></span>

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif">A ratio between the number of frames in which a specific airborne object is detected out of all the frames that this object should be detected in the considered temporal window of frames.</span></span></span>

_Table 3: Glossary_

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif"><b><span lang="EN-US" style="font-size:12.0pt">Constant</span></b></span></span></span>

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif"><b><span lang="EN-US" style="font-size:12.0pt"><span style="color:black">Units</span></span></b></span></span></span>

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif"><b><span lang="EN-US" style="font-size:12.0pt"><span style="color:black">Value</span></span></b></span></span></span>

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif"><b><span lang="EN-US" style="font-size:12.0pt"><span style="color:black">Comments</span></span></b></span></span></span>

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="color:black">UPPER_BOUND_MIN_DIST</span></span></span></span>

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="color:black">m</span></span></span></span>

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="color:black">330</span></span></span></span>

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="color:black">UPPER_BOUND_MAX_DIST</span></span></span></span>

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif">m</span></span></span>

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif">700</span></span></span>

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="color:black">MIN_OBJECT_AREA</span></span></span></span>

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="color:black">pixels</span></span></span></span>

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="color:black">100</span></span></span></span>

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="color:black">At the ground truth resolution</span></span></span></span>

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="color:black">IS_MATCH_MIN_IOU_THRESH</span></span></span></span>

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif">N/A</span></span></span>

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif">0.2</span></span></span>

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="color:black">IS_NO_MATCH_MAX_IOU_THRESH</span></span></span></span>

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="color:black">N/A</span></span></span></span>

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="color:black">0.02</span></span></span></span>

<span style="font-size:11pt"><span style="line-height:normal"><span style="font-family:Calibri,sans-serif"><span lang="EN-US" style="color:black">0&lt; IS_NO_MATCH_MAX_IOU_THRESH &lt;= IS_MATCH_MIN_IOU_THRESH</span></span></span></span>

_Table 4: Constants_

The metrics can evaluate .json files with the following dictionaries:

<span class="color-green">Result</span> – <span class="color-red">List[Dict]</span>:  with the following fields per element
<span class="color-green">'img_name'</span>  - img\_name as appears in the ground truth file
<span class="color-green">'detections'</span>  - <span class="color-red">List[Dict]</span>: with the following fields per element:
    <span class="color-green">'n'</span>  - name of the class (typically airborne)
    <span class="color-green">'x'</span>  - x coordinate of the center of the bounding box
    <span class="color-green">'y'</span>  - y of the center of the bounding box
    <span class="color-green">'w'</span>  - width 
    <span class="color-green">'h'</span>  - height
    <span class="color-green">'s'</span>  – confidence / score
    <span class="color-green">'track_id'</span>  / <span class="color-green">'object_id'</span>  - optional track or object id associated with the detection 

## **Please Note:**

1.  It is very important to provide the correct _img\_name_, such that the detections can be matched against ground truth 
2.  _x,y,w,h_ should be provided in the coordinate system of the original image, with _x,y_ representing the top-left pixel for the bounding box, and _w_ and _h_ representing the width and height respectively.

## **Example:**

\[
  {
    <span class="color-green">"detections"</span>: \[
      {
        <span class="color-green">"x"</span>: 37.619754791259766,
        <span class="color-green">"y"</span>: 1843.8494873046875,
        <span class="color-green">"w"</span>: 63.83501434326172,
        <span class="color-green">"h"</span>: 69.88720703125,
        <span class="color-green">"track_id"</span>: 0,
        <span class="color-green">"n"</span>: "airborne",
        <span class="color-green">"s"</span>: 0.9474319815635681
      }
    \],
    <span class="color-green">"img_name"</span>: "1568151307970878896b37adfedec804a08bcbde18992355d9b.png"
  },
  {
    
  {
    <span class="color-green">"detections"</span>: \[
      {
        <span class="color-green">"x"</span>: 35.92606735229492,
        <span class="color-green">"y"</span>: 1838.3416748046875,
        <span class="color-green">"w"</span>: 71.85213470458984,
        <span class="color-green">"h"</span>: 84.0302734375,
        <span class="color-green">"track_id"</span>: 0,
        <span class="color-green">"n"</span>: "airborne",
        <span class="color-green">"s"</span>: 0.6456623077392578
      }
    \],
    <span class="color-green">"img_name"</span>: "1568151308170494735b37adfedec804a08bcbde18992355d9b.png"
  },
….

# 💪 Baselines 

The baselines for the two benchmarks of the challenge are provided by AWS Rekognition based on SIAM-MOT model ([https://arxiv.org/abs/2004.07786](https://arxiv.org/abs/2004.07786)) trained on AOT dataset. To simulate different submissions, Table 5 outlines the metrics results for various working points - different detection score thresholds and minimum track length required for airborne reports (see Table 3 for definition of airborne report). The inference was performed on test dataset (which is not available to public) and will be used to evaluate performance on the Public board during the challenge.

Note that while we present metrics for all the results, only the results marked with green (with corresponding HFAR < 0.5) will be ranked on the Detection and Tracking Benchmark board based on their EDR values (with ties broken based on lower HFAR). Similarly, only the results marked with green and yellow (with corresponding FPPI < 0.0005) will be ranked on the Detection Benchmark board based on their AFDR values (with ties broken based on lower FPPI). All the other results, e.g., those reported in the rows with red background, will be presented but not ranked.

If participants do not indicate specific benchmark, they will be evaluated in both benchmarks and will be eligible for ranking based on the specific rule of each benchmark.

![](https://images.aicrowd.com/uploads/ckeditor/pictures/357/image.png =750x510)

_Table 5: Benchmark of Track-RCNN_

# 🚀 Submissions

Coming soon...🚀

# 📅 Timeline

Coming soon...🚀

# 🏆 Prizes

Coming soon...🚀

# 📝 Community Contribution Prizes

Coming soon...🚀

# 🔗 Links

[🏆 Discussion Forum](https://discourse.aicrowd.com/c/airborne-object-tracking-challenge-1/767) 

# **📱 Contact**  
 

TBA

# 📚 Acknowledgements

TBA