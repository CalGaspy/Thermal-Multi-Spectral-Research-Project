# Multispectral and Thermal UAV Camera System

This project is a UAV-based camera trigger system designed to control and synchronize a **multispectral camera** and a **thermal camera** during flight. The system uses a **Raspberry Pi 4**, **MAVLink communication**, **GPS data logging**, and a **laptop control station** to trigger image capture and record location data for environmental monitoring and wildfire research.

## Overview

The setup is built around a drone-mounted sensing platform that includes:

- Multispectral camera
- Thermal camera
- Raspberry Pi 4
- RTK GPS system
- Multispectral GPS
- Power supply and voltage regulation
- USB-C radio link
- Laptop ground station

The laptop sends MAVLink trigger commands through a radio link to the Raspberry Pi. The Raspberry Pi receives those commands and triggers the cameras while also logging GPS data for each event.

## Main Features

- Trigger multispectral camera capture
- Start and stop thermal camera recording
- Log GPS coordinates for each trigger event
- Store event data in a CSV file
- Control trigger timing from a laptop GUI
- Separate onboard and ground-station scripts

## System Architecture

### Ground Station
The laptop runs a Python-based control interface that:

- Connects to the radio link
- Sends MAVLink commands
- Starts and stops camera triggering
- Adjusts trigger interval
- Displays connection status and activity logs

### Onboard System
The Raspberry Pi:

- Waits for incoming MAVLink commands
- Triggers the multispectral camera through GPIO
- Controls the thermal camera using PWM
- Reads GPS data from `gpsd`
- Logs each event with timestamp and coordinates

## Files

- `LaptopTrggercode.py`  
  Ground control station interface for connecting, triggering, and adjusting timing.

- `RaspberryPiTrigger.py`  
  Onboard Raspberry Pi script for receiving commands, triggering cameras, and logging GPS data.

## How It Works

1. The laptop connects to the radio link.
2. The operator starts the trigger loop from the GUI.
3. MAVLink commands are sent to the Raspberry Pi.
4. The Raspberry Pi:
   - pulses GPIO for the multispectral camera
   - sends PWM-based control for the thermal camera
   - records GPS data at the time of each event
5. Images are saved to each camera’s SD card
6. Trigger events are saved in a CSV log

## Hardware Used

- DJI M600 drone
- Raspberry Pi 4
- Multispectral camera
- Thermal camera
- RTK GPS
- USB-C radio link
- Voltage regulator board
- Power supply

## Software / Libraries

- Python
- `pymavlink`
- `RPi.GPIO`
- `gps`
- `customtkinter`

## Example Logged Data

Each trigger event is saved to a CSV file with:

- event time
- UTC timestamp
- MAVLink command
- event label
- latitude
- longitude
- altitude
- GPS fix quality

## Applications

This system was developed for research applications such as:

- wildfire monitoring
- vegetation analysis
- thermal mapping
- environmental sensing
- geotagged aerial data collection

## Future Improvements

- automatic image-to-log synchronization
- improved fault handling
- mission-based trigger automation
- tighter integration with flight controller telemetry
- post-processing pipeline for thermal and multispectral datasets

## Repository Goal

The goal of this repository is to document the development of a low-cost UAV sensing platform that integrates thermal and multispectral imaging for field research and environmental monitoring.
