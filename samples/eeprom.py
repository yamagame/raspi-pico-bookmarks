import time
from machine import Pin, I2C

eeeprom = I2C(1, scl=Pin(3), sda=Pin(2), freq=100000)


def write_eeprom(s):
    eeeprom.writeto_mem(0x50, 0x0F00, s.encode(), addrsize=16)
    time.sleep_ms(5)


def read_eeprom(len):
    return str(eeeprom.readfrom_mem(0x50, 0x0F00, len, addrsize=16))


write_eeprom("hello")
print(read_eeprom(5))
write_eeprom("world")
print(read_eeprom(5))
