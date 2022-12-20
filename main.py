from ota.ota_updater import OTAUpdater
import ota.secrets as secrets
import time, network, gc

def connectToWifiAndUpdate(): 
    time.sleep(1)
    print('Memory free', gc.mem_free())
    
    # Connecting to WiFi
    sta = network.WLAN(network.STA_IF)
    if not sta.isconnected():
        print('connecting to network...')
        sta.active(True)
    #sta.connect('your wifi ssid', 'your wifi password')
        sta.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)
        while not sta.isconnected():
            pass
    print('network config:', sta.ifconfig())

def download_and_install_update_if_available():
    o = OTAUpdater("https://github.com/Lezgend/LoRAWAN-KKU-OTAUpdater/")
    o.install_update_if_available_after_boot(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)


def start():
     # your custom code goes here. Something like this: ...
     # from main.x import YourProject
     # project = YourProject()
     # ...
    time.sleep_ms(10000)
    import main.start


def boot():
    connectToWifiAndUpdate()
    download_and_install_update_if_available()
    start()

boot()