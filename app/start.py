from machine import UART, Pin, Timer
import time, sys, os, math, random

def sendATcommand(ATcommand):
    rstr = ""
    print("Command: {0}\r\n".format(ATcommand))
    uart.write("{0}\r\n".format(ATcommand))
    rstr = uart.read().decode("utf-8")
    print(rstr)
    return rstr
    
def sendHello():
    # Send 5 characters from string "HELLO"
    try:
        x = round(-1.0 * 5 * math.log(1-random.random()) * 100)
        timer1 = Timer(0)
        timer1.init(period=x, mode=Timer.PERIODIC, callback=lambda t: sendATcommand("AT+NCMGS=5,HELLO"))

    except KeyboardInterrupt:
        print("Interrupted!!")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

def Config():
    # OTAA
    sendATcommand("AT+DEVEUI")
    sendATcommand("AT+APPKEY")
    
    # ABP
    #sendATcommand("AT+APPSKEY")
    #sendATcommand("AT+NWKSKEY")
    #sendATcommand("AT+ADDR")
    
    sendATcommand("AT+DEBUG=1")
    sendATcommand("AT+ISMBAND=6")
    sendATcommand("AT+CLASS=A")
    sendATcommand("AT+ACTIVATE=1")
    sendATcommand("AT+PORT=20")
    sendATcommand("AT+CFM=1")
    sendATcommand("AT+RXWIN2=923200000,2")
    sendATcommand("AT+SAVE")

    Restart()
    sendATcommand("AT+NCONFIG");sendATcommand("AT+CHSET") 

def Restart():
    # Restart MAXIIOT DL7612-AS923-TH

# LOOP OTAA
    sendATcommand('AT+NRB')
    time.sleep(5)
    # Check LoRaWAN Network Server Connection (AT+CGATT)
    print("Check LoRaWAN Network Server Connection (If 1 mean module has connected)\n")
    print("PLEASE WAIT!")
    time.sleep(20.0)

    rstr = sendATcommand("AT+CGATT")
    tryno = 1
    while rstr != "+CGATT:1":
        rstr = sendATcommand("AT+CGATT")
        print("Respond String")
        print(rstr)
        if rstr.startswith("+CGATT:1"):
            print("*******OTAA OK*******")
            break
        else:
            print("Retry OTAA Continue")
        
            b = str(tryno)
            print(b[-1:])
            if b[-1:] == "0":
                print("YES")
                sendATcommand('AT+NRB')
            else:
                print("NO")
                tryno = tryno+1
            time.sleep(20.0)
            print("Join Success")
# END LOOP OTAA
        
if __name__ == "__main__":
    uart = UART(2, baudrate=115200, bits=8, parity=None, stop=1, timeout=1000, timeout_char=1000)
    #sendATcommand("AT+CLAC")
    #sendATcommand("AT+RESTORE");sendATcommand("AT+NCONFIG")
    #sendATcommand("AT+DEVEUI");sendATcommand("AT+APPKEY")
    ##sendATcommand("AT+NCONFIG");sendATcommand("AT+CHSET")                            
    #Config()
    Restart()
    sendHello()

