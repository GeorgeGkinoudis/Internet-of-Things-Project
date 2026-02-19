import smtplib
import os
import cv2 
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep, time 
from datetime import datetime
from gpiozero import MotionSensor, LED 

# --- Configuration ---
PIR_PIN_GPIO = 27 
LED_PIN_GPIO = 17 
CAMERA_INDEX = 0
FILE_PATH="/home/pi/python_code/capture/"  


RUNTIME_SECONDS = 60 # System runs for 60 seconds (1 minute)
COOLDOWN_SECONDS = 5 # Cooldown period after an alert


pir_sensor = MotionSensor(PIR_PIN_GPIO)
alert_led = LED(LED_PIN_GPIO) 


subject='Security Alert: Motion Detected (Image Attached)'
bodyText="""\
Hi,
A motion has been detected in your room.
Please check the attached image sent from the Raspberry Pi security system.
"""

SMTP_SERVER='smtp.gmail.com'
SMTP_PORT=587
USERNAME='[giorgosginoudhs@gmail.com]'     
PASSWORD='exqw ybtx iuyh xodm' 
RECIEVER_EMAIL='[giorgosginoudhs@gmail.com]' 

FILENAME_PART1="alert_capture"
FILE_EXT=".jpg"


print("Initializing USB Camera...")
camera = cv2.VideoCapture(CAMERA_INDEX)
if not camera.isOpened():
    print(f"Error: Could not open USB camera at index {CAMERA_INDEX}. Exiting.")
    exit()
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) 
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
print("USB Camera initialized and ready.")

def get_filename_details():
    now = datetime.now()
    current_datetime = now.strftime("%Y%m%d_%H%M%S")
    filename_only = FILENAME_PART1 + "_" + current_datetime + FILE_EXT
    full_filepath = FILE_PATH + filename_only
    return filename_only, full_filepath

def send_email(filename_only, full_filepath):
    message = MIMEMultipart()
    message["From"] = USERNAME
    message["To"] = RECIEVER_EMAIL
    message["Subject"] = subject
    message.attach(MIMEText(bodyText, 'plain'))
    
    try:
        with open(full_filepath, "rb") as attachment:
            img = MIMEImage(attachment.read(), name=filename_only) 
        img.add_header('Content-Disposition', f"attachment; filename= {filename_only}")
        message.attach(img)
        
        session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        session.starttls()
        session.login(USERNAME, PASSWORD)
        session.sendmail(USERNAME, RECIEVER_EMAIL, message.as_string())
        session.quit()
        print("📧 Email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def capture_picture(full_filepath):
    os.makedirs(FILE_PATH, exist_ok=True) 
    ret, frame = camera.read()
    if ret:
        cv2.imwrite(full_filepath, frame) 
        print(f"📸 Picture captured: {full_filepath}")
        return True
    else:
        print("Error: Failed to read frame from camera for capture.")
        return False

def remove_file(full_filepath):
    if os.path.exists(full_filepath):
        os.remove(full_filepath)
        print(f"🗑️ Cleaned up file: {full_filepath}")
        

def motion_detected_action():
    print("\n🚨 Motion Detected. Capturing picture and sending email...")
    
    # 1. Turn on the LED
    alert_led.on() 
    
    # 2. Capture and Send
    filename_only, full_filepath = get_filename_details()
    if capture_picture(full_filepath):
        send_email(filename_only, full_filepath)
        remove_file(full_filepath)
    
    # 3. Turn LED off
    alert_led.off() 
    
    # 4. Implement Cooldown
    print(f"Sleeping for {COOLDOWN_SECONDS} seconds (Cooldown)...")
    sleep(COOLDOWN_SECONDS)
    print("Monitoring resumed.")


print(f"Security System Active for {RUNTIME_SECONDS} seconds (Monitoring GPIO 27)...")


start_time = time()

# Set up the motion handler
pir_sensor.when_motion = motion_detected_action

try:
    # Loop for the duration 
    while time() < start_time + RUNTIME_SECONDS:
        sleep(0.1)

except KeyboardInterrupt:
    pass 

finally:
    print(f"\nTime limit reached ({RUNTIME_SECONDS}s). System shutting down.")
    camera.release()
    pir_sensor.close()
    alert_led.close()