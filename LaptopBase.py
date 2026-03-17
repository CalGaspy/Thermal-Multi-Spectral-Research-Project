import customtkinter as ctk
from pymavlink import mavutil
import threading
import time


# Global Variables 
mav = None
connected = False 
triggering = False
trigger_interval = 1.0


# Mavlink Functions 
def connect_radio():
    global mav, connected

    try:
        status_label.configure(text="Connecting...", text_color="#f5f5f5")

        mav = mavutil.mavlink_connection("COM7", baud=57600)

        print("Sending heartbeat...")
        mav.mav.heartbeat_send(
            mavutil.mavlink.MAV_TYPE_GCS,
            mavutil.mavlink.MAV_AUTOPILOT_INVALID,
            0, 0, 0
        )

        time.sleep(1)

        connected = True
        status_label.configure(text="Connected", text_color="#00ff88")
        log_box.insert("end", "Connected to radio (COM7)\n")
        log_box.see("end")

    except Exception as e:
        connected = False
        status_label.configure(text="Connection Failed", text_color="#ff4444")
        log_box.insert("end", f"ERROR: {str(e)}\n")
        log_box.see("end")


def send_altum_trigger():
    mav.mav.command_long_send(
        1, 1,
        mavutil.mavlink.MAV_CMD_USER_1,
        0,
        1, 0, 0, 0, 0, 0, 0
    )


def send_flir_start():
    mav.mav.command_long_send(
        1, 1,
        mavutil.mavlink.MAV_CMD_VIDEO_START_CAPTURE,
        0,
        0, 0, 0, 0, 0, 0, 0
    )


def send_flir_stop():
    mav.mav.command_long_send(
        1, 1,
        mavutil.mavlink.MAV_CMD_VIDEO_STOP_CAPTURE,
        0,
        0, 0, 0, 0, 0, 0, 0
    )


def trigger_both():
    send_altum_trigger()
    send_flir_start()


# ---------------- TRIGGER LOOP ----------------
def trigger_loop():
    global triggering

    while triggering:
        try:
            trigger_both()
            log_box.insert("end", "Triggered: Altum + FLIR START\n")
            log_box.see("end")

        except Exception as e:
            log_box.insert("end", f"Trigger Error: {str(e)}\n")
            log_box.see("end")

        time.sleep(trigger_interval)


# ---------------- UI CALLBACKS ----------------
def connect_button_pressed():
    thread = threading.Thread(target=connect_radio)
    thread.daemon = True
    thread.start()


def start_triggering_pressed():
    global triggering

    if not connected:
        log_box.insert("end", "ERROR: Not connected.\n")
        log_box.see("end")
        return

    if triggering:
        log_box.insert("end", "Already triggering.\n")
        log_box.see("end")
        return

    triggering = True
    status_label.configure(text="Triggering...", text_color="#ffaa00")
    log_box.insert("end", "Started triggering loop...\n")
    log_box.see("end")

    thread = threading.Thread(target=trigger_loop)
    thread.daemon = True
    thread.start()


def stop_triggering_pressed():
    global triggering

    if not connected:
        return

    triggering = False

    try:
        send_flir_stop()
    except:
        pass

    status_label.configure(text="Connected (Idle)", text_color="#00ff88")
    log_box.insert("end", "Stopped triggering loop.\n")
    log_box.see("end")


def update_interval(value):
    global trigger_interval
    trigger_interval = float(value)
    interval_value_label.configure(text=f"{trigger_interval:.2f} sec")


# ---------------- UI SETUP ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("Camera Control Station")
app.geometry("900x600")
app.configure(fg_color="#000000")


# ---------------- HEADER ----------------
title_label = ctk.CTkLabel(
    app,
    text="CAMERA CONTROL STATION",
    font=("Arial", 26, "bold"),
    text_color="#ffffff"
)
title_label.pack(pady=20)


status_label = ctk.CTkLabel(
    app,
    text="Disconnected",
    font=("Arial", 16, "bold"),
    text_color="#ff4444"
)
status_label.pack(pady=5)


# ---------------- CONTROL FRAME ----------------
control_frame = ctk.CTkFrame(app, fg_color="#0a0a0a", corner_radius=20)
control_frame.pack(pady=15, padx=20, fill="x")


connect_btn = ctk.CTkButton(
    control_frame,
    text="Connect",
    font=("Arial", 16, "bold"),
    height=50,
    corner_radius=25,
    fg_color="#1d9bf0",
    hover_color="#1681c7",
    command=connect_button_pressed
)
connect_btn.pack(pady=15, padx=25, fill="x")


start_btn = ctk.CTkButton(
    control_frame,
    text="Start Triggering",
    font=("Arial", 16, "bold"),
    height=50,
    corner_radius=25,
    fg_color="#00c853",
    hover_color="#00a444",
    command=start_triggering_pressed
)
start_btn.pack(pady=10, padx=25, fill="x")


stop_btn = ctk.CTkButton(
    control_frame,
    text="Stop Triggering",
    font=("Arial", 16, "bold"),
    height=50,
    corner_radius=25,
    fg_color="#ff1744",
    hover_color="#d5002f",
    command=stop_triggering_pressed
)
stop_btn.pack(pady=10, padx=25, fill="x")


# ---------------- INTERVAL SLIDER ----------------
interval_frame = ctk.CTkFrame(app, fg_color="#0a0a0a", corner_radius=20)
interval_frame.pack(pady=10, padx=20, fill="x")

interval_label = ctk.CTkLabel(
    interval_frame,
    text="Trigger Interval (seconds)",
    font=("Arial", 15, "bold"),
    text_color="#ffffff"
)
interval_label.pack(pady=10)

interval_slider = ctk.CTkSlider(
    interval_frame,
    from_=0.2,
    to=5.0,
    number_of_steps=48,
    command=update_interval
)
interval_slider.set(trigger_interval)
interval_slider.pack(padx=30, pady=5, fill="x")

interval_value_label = ctk.CTkLabel(
    interval_frame,
    text=f"{trigger_interval:.2f} sec",
    font=("Arial", 14),
    text_color="#aaaaaa"
)
interval_value_label.pack(pady=10)


# ---------------- LOG BOX ----------------
log_frame = ctk.CTkFrame(app, fg_color="#0a0a0a", corner_radius=20)
log_frame.pack(pady=15, padx=20, fill="both", expand=True)

log_label = ctk.CTkLabel(
    log_frame,
    text="Activity Log",
    font=("Arial", 16, "bold"),
    text_color="#ffffff"
)
log_label.pack(pady=10)

log_box = ctk.CTkTextbox(
    log_frame,
    font=("Consolas", 13),
    text_color="#ffffff",
    fg_color="#000000",
    corner_radius=15
)
log_box.pack(padx=20, pady=10, fill="both", expand=True)


# ---------------- RUN APP ----------------
app.mainloop()
