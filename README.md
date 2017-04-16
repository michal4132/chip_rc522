RC522-python
==============

A small class to interface with the RFID reader Module RC522 on the Chip.

##Requirements
This code requires you to have SPI-Py and CHIP_IO installed from the following repository:
https://github.com/lthiery/SPI-Py
https://github.com/xtacocorex/CHIP_IO

## Pins
You can use [this](http://docs.getchip.com/images/chip_pinouts.jpg) image for reference.

| Name | Pin #  | Pin name   |
|------|--------|------------|
| SDA  | U14_27 | CSIPCK     |
| SCK  | U14_28 | CSICK      |
| MOSI | U14_29 | CSIHSYNC   |
| MISO | U14_30 | CSIVSYNC   |
| IRQ  | None   | None       |
| GND  | Any GND| Any Ground |
| RST  | U14_14 | XIO-P1     |
| 3.3V | Any 3V3| Any 3V3    |

##Usage
Import RC522 in the top of your script. For more info see the example.
You may need to run "enable-spi" script before
