from ota.ota_updater import OTAUpdater
import ota.secrets as secrets
import math, random, time, machine, network, gc

# Exponential Time Interval
def time_interval(mean = 5):
    x = round(-1.0 * mean * math.log(1 - random.random()))
    print("Time:", x)
    return x

def connectToWifiAndUpdate():
    time.sleep(time_interval() + 1)
    print("Memory free:", gc.mem_free())
    
    # Connecting to WiFi
    sta = network.WLAN(network.STA_IF)
    if not sta.isconnected():
        print("Connecting to Network...")
        sta.active(True)
        #sta.connect('your wifi ssid', 'your wifi password')
        sta.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)
        while not sta.isconnected():
            pass
    print("Network Config:", sta.ifconfig())

def download_and_install_update_if_available():
    otaUpdater = OTAUpdater("https://github.com/Lezgend/LoRAWAN-KKU-OTAUpdater/", main_dir="main")
    hasUpdated = otaUpdater.install_update_if_available()
    if hasUpdated:
        machine.reset()
    else:
        del(otaUpdater)
        gc.collect()
        # Run a update code
        import main.start

def boot():
    connectToWifiAndUpdate()
    download_and_install_update_if_available()
    
boot()