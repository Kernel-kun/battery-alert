import psutil                       # Retrieve SystemInfo
from playsound import playsound     # To play audio file in background
from plyer import notification      # To display Windows Notification
import time                         # For sleep() func.

# pycaw libraries:
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


# Get default audio device using PyCAW
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))


# Function Call to Play Alarm Audio
def playAudio():
    currentVolumeDb = volume.GetMasterVolumeLevel()
    volume.SetMasterVolumeLevel(-7.74639749, None)
    playsound('C:\Windows\Media\Ring08.wav')
    volume.SetMasterVolumeLevel(currentVolumeDb, None)


while(True):

    #Get Current Volume Level
    currentVolumeDb = volume.GetMasterVolumeLevel()
    #Get Battery Info
    battery = psutil.sensors_battery()
    percent = battery.percent

    if(percent >= 82 and battery.power_plugged):
        notification.notify( 
            title="High Charging", 
            message=str(percent)+"% Battery remaining", 
            timeout=10
        )
        playAudio()
    elif(percent <= 34 and not battery.power_plugged):
        notification.notify( 
            title="Low Charging", 
            message=str(percent)+"% Battery remaining", 
            timeout=10
        )
        playAudio()

    # after every 5 mins (i.e 60*5 sec) check will rerun
    time.sleep(60*5)

    continue
