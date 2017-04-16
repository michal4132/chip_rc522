#!/usr/bin/env python
# -*- coding: utf8 -*-

import RC522
import time,sys

continue_reading = True
wr = False
MIFAREReader = RC522.Reader(32766, 0, "U14_14")

try:
  fun = sys.argv[1]
except:
  print("Options: -d - dump")
  print("         -w - write")
  print("         -r - read")
  print("         -c - change UID")
  print("         -s - show UID")
  continue_reading = False

def hex(hex):
  ret = ""
  for h in hex:
    if(32<int(h, 16)<106):
      ret+=chr(int(h, 16))
    else:
      ret+="."
  return ret


print("Place card on reader")

while continue_reading:

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
    for u in uid:
        print(str(format(u, '02x')), end=" ")
    print()

    # This is the default key for authentication
    if(fun != "-s"):
      key = input("Key>")
    else:
      key = []
    if(len(key)<17):
      key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
    else:
      key = key.split(" ")
      wrb = []
      for k in key:
        wrb.append(int(k, 16))
      key = wrb

    # Select the scanned tag
    MIFAREReader.RC522_SelectTag(uid)

    if(fun == "-r"):
      sec = int(input("Sector: "))
      status = MIFAREReader.RC522_Auth(MIFAREReader.PICC_AUTHENT1A, sec, key, uid)
      if status == MIFAREReader.MI_OK:
        out = MIFAREReader.RC522_Read(sec)
        print(out)
        r = []
        for t in out:
          r.append(format(t, '02x'))
        print(str(sec)+": "+" ".join(r)+"|"+hex(r))
      else:
        print("Authentication error")
    elif(fun == "-w"):
      sec = int(input("Sector: "))
      status = MIFAREReader.RC522_Auth(MIFAREReader.PICC_AUTHENT1A, sec, key, uid)
      # Check if authenticated
      if status == MIFAREReader.MI_OK:
        data = input("Data>").split(' ')
        wrb = []
        for d in data:
          wrb.append(int(d, 16))
        print("Current data:")
        print(MIFAREReader.RC522_Read(sec))
        if(input("Write? [Y/N] ")=="Y"):
          print("Writing")
          # Write the data
          if(MIFAREReader.RC522_Write(sec, wrb)):
            print("OK")
          print("NOW:")
          print(MIFAREReader.RC522_Read(sec))
      else:
        print("Auth error")
    elif(fun == "-d"):        
      fn = input("File name: ")
      if(len(fn)<1):
        wr = False
      else:
        f = open(fn, 'w')
        wr = True
      for d in range(64):
        status = MIFAREReader.RC522_Auth(MIFAREReader.PICC_AUTHENT1A, d, key, uid)
        if status == MIFAREReader.MI_OK:
          out = MIFAREReader.RC522_Read(d)
          r = []
          for t in out:
              r.append(format(t, '02x'))
          de = hex(r)
          print(str(d).zfill(2)+": "+" ".join(r)+"|"+de)
          if(wr):
            f.write(" ".join(r)+"|"+de+"\n")
        else:
            status,TagType = MIFAREReader.RC522_Request(MIFAREReader.PICC_REQIDL)
            if status == MIFAREReader.MI_OK:
              (status,uid) = MIFAREReader.RC522_Anticoll()
              MIFAREReader.RC522_SelectTag(uid)
            print("Authentication error at: "+str(d))
    elif(fun == "-c"):
      new_uid = input("UID>").upper()
      if(len(new_uid)<11):
        new_uid = [0xDE,0xAD,0xBE,0xEF]
      else:
        new_uid = new_uid.split(" ")
        nud = []
        for k in new_uid:
          nud.append(int(k, 16))
        new_uid = nud
        
      status = MIFAREReader.RC522_Auth(MIFAREReader.PICC_AUTHENT1A, 0, key, uid)
      if status == MIFAREReader.MI_OK:
        block_zero = MIFAREReader.RC522_Read(0)
        bcc = 0
        for i in range(len(uid)-1):
          block_zero[i] = new_uid[i]
          bcc ^= new_uid[i]
        block_zero[len(uid)-1] = bcc
        MIFAREReader.RC522_StopCrypto1()
        if(MIFAREReader.OpenBackdoor() != MIFAREReader.MI_OK):
          print("Backdoor error")
        if(MIFAREReader.RC522_Write(0, block_zero) == MIFAREReader.MI_OK):
          print("OK")
        else:
          print("Error writting")
      else:
        print("Auth error")
    elif(sys.argv[1] == "-s"):
      pass

    MIFAREReader.RC522_StopCrypto1()
    
    if(wr):
      f.close()
    if(fun != "-s"):
      continue_reading = False
