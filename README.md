# Multispectral and Thermal UAV Camera System

![System Diagram](images/system_diagram.png)

This project integrates thermal and multispectral imaging sensors onto a UAV platform for environmental monitoring and wildfire research. The system uses a Raspberry Pi 4, GPS data logging, and MAVLink communication to trigger image capture and synchronize data collection during flight.

The goal of this project is to build a low-cost aerial sensing platform capable of collecting geotagged multispectral and thermal data for applications such as vegetation analysis, wildfire monitoring, and environmental research.

---

## System Architecture

The platform is mounted on a DJI M600 drone and integrates:

- Multispectral camera  
- Thermal camera  
- Raspberry Pi 4  
- RTK GPS system  
- Multispectral GPS module  
- Power supply and voltage regulator  
- USB-C radio link  
- Laptop ground station  

Power from the drone is routed through a power supply and voltage regulator board which distributes:

- 12V power to the multispectral camera  
- 5V power to the Raspberry Pi and communication modules  

A laptop ground station sends trigger commands through a radio link. These commands are received by the Raspberry Pi onboard the drone.

The Raspberry Pi then:

- receives trigger commands from the ground station  
- triggers the multispectral camera through GPIO  
- controls the thermal camera signal  
- reads GPS information from the RTK system  
- logs event metadata for each image capture  

Images are stored locally on each camera’s SD card while GPS metadata is logged for synchronization and geotagging.

---

## Repository Structure

project-root/

README.md

scripts/
  RaspberryPiTrigger.py
  LaptopTriggerCode.py

images/
  system_diagram.png
  development/

stl_mounts/
  3D printed mounts for cameras and electronics

---

## Code

### Raspberry Pi Script

scripts/RaspberryPiTrigger.py

Runs onboard the drone and is responsible for:

- receiving MAVLink commands  
- triggering the multispectral camera  
- controlling the thermal camera signal  
- collecting GPS data using gpsd  
- logging trigger events to a CSV file  

---

### Ground Station Script

scripts/LaptopTriggerCode.py

Runs on the laptop ground station and provides:

- connection to the drone radio link  
- camera trigger control  
- adjustable trigger intervals  
- system status monitoring  

---

## Development Process

Development images documenting the build and testing process can be found in:

images/development/

These include:

- early hardware integration  
- camera mounting prototypes  
- Raspberry Pi wiring  
- system testing and validation  

Example files:

images/development/
  mount_prototype.jpg
  wiring_setup.jpg
  pi_integration.jpg
  field_test.jpg

---

## 3D Printed Mounts

The repository includes STL files for the 3D printed mounts used to attach cameras and onboard electronics to the UAV platform.

All STL files are located in:

stl_mounts/

These mounts were designed to securely hold:

- multispectral camera  
- thermal camera  
- Raspberry Pi  
- sensor mounting plates  

The files can be directly used for 3D printing or modified for different UAV frames or sensor configurations.

Example structure:

stl_mounts/
  multispectral_camera_mount.stl
  thermal_camera_mount.stl
  raspberry_pi_mount.stl
  mounting_plate.stl

---

## Applications

This system supports several research applications including:

- wildfire monitoring  
- vegetation health analysis  
- thermal mapping  
- environmental sensing  
- geotagged aerial data collection  

---

## Future Improvements

Possible future extensions include:

- automated mission-based triggering  
- tighter integration with flight controller telemetry  
- improved data synchronization  
- automated post-processing pipeline  
- onboard sensor fusion and data analysis  

---

## Project Goal

The goal of this repository is to document the development of a UAV-based multisensor imaging platform capable of collecting synchronized thermal and multispectral datasets for environmental and wildfire research.
