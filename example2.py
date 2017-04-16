#
# Example of usage
# Script block internet traffic if card detected. Working on Tenda 11N

import requests
import RC522
import time

MIFAREReader = RC522.Reader(32766, 0, "U14_14")

def sta(state):

    data = {"Username":"admin", "Password":"pass"}
    s = requests.Session()

    r = s.post('http://192.168.0.1/LoginCheck', data=data)
    r = s.get('http://192.168.0.1/goform/trafficForm?GO=net_tc.asp&tc_enable='+str(state)+'&up_Band=12800&down_Band=12800&cur_number=1&tc_list_1=80,111,111,1,1,1,1,1')

def main():

    state = 0

    print("Started")

    while True:
        # Scan for cards
        status,TagType = MIFAREReader.RC522_Request(MIFAREReader.PICC_REQIDL)

        # If a card is found
        if status == MIFAREReader.MI_OK:
            print("Card detected")

        # Get the UID of the card
        (status,uid) = MIFAREReader.RC522_Anticoll()

        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:

            # Print UID
            print("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
            if(state==0):
                sta(1)
                state = not state
            else:
                sta(0)
                state = not state
        time.sleep(1)

try:
    main()
except KeyboardInterrupt:
    MIFAREReader.RC522_Reset()
