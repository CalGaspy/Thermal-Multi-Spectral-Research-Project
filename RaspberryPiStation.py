#!/usr/bin/env python3

from pymavlink import mavutil
import RPi.GPIO as GPIO
import time
import csv
import os
from gps import gps, WATCH_ENABLE, WATCH_NEWSTYLE

# ---------------- USER SETTINGS ----------------

CSV_PATH = "/home/pi/camera_trigger/trigger_gps_log.csv"
WAIT_FOR_FIX_SEC = 0.5

# ---------------- GPIO SETTINGS ----------------

ALTUM_GPIO = 22
PULSE_WIDTH = 0.005   # 5 ms

FLIR_PWM_PIN = 27
FLIR_FREQ = 50

GPIO.setmode(GPIO.BCM)
GPIO.setup(ALTUM_GPIO, GPIO.OUT)
GPIO.output(ALTUM_GPIO, GPIO.LOW)

GPIO.setup(FLIR_PWM_PIN, GPIO.OUT)
flir_pwm = GPIO.PWM(FLIR_PWM_PIN, FLIR_FREQ)
flir_pwm.start(5.0)   # idle LOW

# ---------------- GPSD CONNECTION ----------------

print("Connecting to gpsd...")
gpsd_session = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)
print("gpsd connected.")

def get_current_fix(timeout_sec=1.0):
    deadline = time.time() + timeout_sec

    while time.time() < deadline:
        try:
            report = gpsd_session.next()

            if report['class'] == 'TPV':
                lat = getattr(report, 'lat', None)
                lon = getattr(report, 'lon', None)
                alt = getattr(report, 'alt', None)
                mode = getattr(report, 'mode', 0)

                if mode >= 2 and lat is not None and lon is not None:
                    return {
                        "lat": lat,
                        "lon": lon,
                        "alt": alt,
                        "fix_quality": mode
                    }

        except StopIteration:
            continue
        except KeyError:
            continue

    return None

# ---------------- CSV LOGGING ----------------

def ensure_csv_has_header(path: str):
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return

    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "event_time_epoch",
            "event_time_utc",
            "mav_command",
            "event_label",
            "lat_deg",
            "lon_deg",
            "alt_m",
            "fix_quality"
        ])

def log_event(event_label: str, mav_command: int):
    ensure_csv_has_header(CSV_PATH)

    event_time = time.time()
    event_utc = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(event_time))

    fix = get_current_fix(timeout_sec=WAIT_FOR_FIX_SEC)

    if fix:
        row = [
            event_time,
            event_utc,
            mav_command,
            event_label,
            fix["lat"],
            fix["lon"],
            fix["alt"],
            fix["fix_quality"]
        ]
    else:
        row = [
            event_time,
            event_utc,
            mav_command,
            event_label,
            None,
            None,
            None,
            0
        ]

    with open(CSV_PATH, "a", newline="") as f:
        w = csv.writer(f)
        w.writerow(row)

    print(f"[CSV] Logged: {event_label} at {event_utc}")

# ---------------- MAVLINK SETTINGS ----------------

print("Waiting 10 seconds for boot devices to finish loading...")
time.sleep(10)

mav = mavutil.mavlink_connection("/dev/ttyUSB0", baud=57600)

print("Waiting for heartbeat from laptop...")
mav.wait_heartbeat()
print("Heartbeat received. Listening for commands...")

try:
    while True:
        msg = mav.recv_match(type="COMMAND_LONG", blocking=True)

        if not msg:
            continue

        cmd = msg.command

        # ---------------- ALTUM TRIGGER ----------------
        if cmd == mavutil.mavlink.MAV_CMD_USER_1:
            GPIO.output(ALTUM_GPIO, GPIO.HIGH)
            time.sleep(PULSE_WIDTH)
            GPIO.output(ALTUM_GPIO, GPIO.LOW)
            print("Altum triggered (GPIO 22 pulse)")

            log_event("ALTUM_TRIGGER", cmd)

        # ---------------- FLIR START ----------------
        elif cmd == mavutil.mavlink.MAV_CMD_VIDEO_START_CAPTURE:
            print("FLIR START RECORDING")
            flir_pwm.ChangeDutyCycle(10.0)
            time.sleep(0.1)

            log_event("FLIR_START", cmd)

        # ---------------- FLIR STOP ----------------
        elif cmd == mavutil.mavlink.MAV_CMD_VIDEO_STOP_CAPTURE:
            print("FLIR STOP RECORDING")
            flir_pwm.ChangeDutyCycle(5.0)
            time.sleep(0.1)

            log_event("FLIR_STOP", cmd)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    flir_pwm.stop()
    GPIO.cleanup()