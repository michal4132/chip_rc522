#!/usr/bin/env python
# -*- coding: utf8 -*-

#Fixes bricked Magic Cards

import RC522
import time

continue_reading = True
wr = False
MIFAREReader = RC522.Reader(32766, 0, "U14_14")

def hex(hex):
    ret = ""
    for h in hex:
        if(32<int(h, 16)<106):
            ret+=chr(int(h, 16))
        else:
            ret+="."
    return ret


print("Place card on reader")
# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:

    status,TagType = MIFAREReader.RC522_Request(MIFAREReader.PICC_REQIDL)
    
    if status == MIFAREReader.MI_OK:
        print("Card detected")

        MIFAREReader.OpenBackdoor()

#        block_zero = [222, 173, 190, 239, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        block_zero = [0x01, 0x02, 0x03, 0x04, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

        if(MIFAREReader.RC522_Write(0, block_zero)):
            print("OK")

