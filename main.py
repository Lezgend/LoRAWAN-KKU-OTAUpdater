from ota.ota_updater import OTAUpdater

def download_and_install_update_if_available():
    o = OTAUpdater("https://github.com/Lezgend/LoRAWAN-KKU-OTAUpdater/")
    o.install_update_if_available_after_boot(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)


def start():
     # your custom code goes here. Something like this: ...
     # from main.x import YourProject
     # project = YourProject()
     # ...
    utime.sleep_ms(10000)
    import main.start


def boot():
    download_and_install_update_if_available()
    start()

boot()
