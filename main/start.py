from machine import UART
import time, sys, os, math, random, network

# Send AT Command function with <CR><LF>
def sendATcommand(ATcommand):
    rstr = ""
    print("Command: {0}\r\n".format(ATcommand))
    uart.write("{0}\r\n".format(ATcommand))
    rstr = uart.read().decode("utf-8")
    print(rstr)
    return rstr

# Exponential Time Interval
def time_interval(mean = 5):
    x = round(-1.0 * mean * math.log(1 - random.random()))
    print("Time:", x)
    return x

# Send HEX function
def sendHello():
    count = 0
    
    try:
        while True:
            #rstr = sendATcommand("AT+NCMGS=5,HELLO")
            rstr = sendATcommand("AT+NMGS=20,48454c4c4f484f57415245594f55544f4441593f")
            time.sleep(time_interval() + 1)
            count += 1
            print("Cycle: ", count)
            if count == 1000:       
                break
            
    # When do Ctr+C for tnterrupting routines
    except KeyboardInterrupt:
        print("Interrupted!!")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

# Config module function
def Config():
#     sendATcommand("AT+DEBUG=1")
#     sendATcommand("AT+ISMBAND=6")
#     sendATcommand("AT+CLASS=A")
#     sendATcommand("AT+ACTIVATE=1")
#     sendATcommand("AT+ADR=1")
#     sendATcommand("AT+CFM=1")
#     sendATcommand("AT+SAVE")
    
    sendATcommand("AT+DEBUG=1")
    sendATcommand("AT+ADR=0")
    sendATcommand("AT+DR=2")
    sendATcommand("AT+SAVE")

#     Restart()
#     sendATcommand("AT+NCONFIG");sendATcommand("AT+CHSET")

# Seb-string find index and do striping
def return_join_value(rstr):
    y = -1 
    cgatt_start_index = rstr.find(":") + 1
    cgatt_end_index = rstr.find("\n", cgatt_start_index)
    
    new_str = rstr[cgatt_start_index:cgatt_end_index] 
    return new_str.strip()
   
# Restart the module (MAXIIOT DL7612-AS923-TH)
def Restart():
    # LOOP OTAA
    sendATcommand("AT+NRB")
    # Check LoRaWAN Network Server Connection (AT+CGATT)
    print("Check LoRaWAN Network Server Connection (If 1 mean module has connected)\n")
    print("PLEASE WAIT!")
    time.sleep(time_interval())

    rstr = sendATcommand("AT+CGATT")
    
    # Check OTAA join value
    check = 0
    while return_join_value(rstr) != "1":
        rstr=sendATcommand("AT+CGATT")
        time.sleep(time_interval())
        print("Respond String")
        print(rstr)
        if return_join_value(rstr) == "1":
           print("++++OTAA OK+++++") 
           break
        elif return_join_value(rstr) == "2":
            print("Retry OTAA Continue")
            print("NOOOOOOOOOOOO")
            check += 1
            print("Check =", check)
            if check == 3:
                Restart()
    # END LOOP OTAA
        
uart = UART(2, baudrate=115200, bits=8, parity=None, stop=1, timeout=500, timeout_char=500)                 
Config()
Restart()
sendHello()
