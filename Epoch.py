from Adafruit_I2C import *
import datetime
import smbus

DS3231_I2C_ADDR = 104

def bcd2dec(bcd):
    '''
    convert binary coded decimal to decimal
    '''
    return (((bcd & 0b11110000)>>4)*10 + (bcd & 0b00001111));

def dec2bcd(dec):
    '''
    convert decimal to binary coded decimal 
    '''
    t = dec / 10;
    o = dec - t * 10;
    return (t << 4) + o;

class Epoch:
    def __init__(self, bus=smbus.SMBus(1)):
        self.ds3231 = Adafruit_I2C(DS3231_I2C_ADDR, bus)

    def getTime(self):
        data = self.ds3231.readList(0, 7)
        data = [bcd2dec(d) for d in data]
        
        ss, mm, hh, junk, DD, MM, YY = data
        YY += 2000
        # print YY, MM, DD, hh, mm, ss
        return datetime.datetime(YY, MM, DD, hh, mm, ss)
    def setTime(self, when):
        '''
        Set the RTC to when, a datetime object
        '''
        data = [when.second, when.minute, when.hour, 0, when.day, when.month, when.year - 2000]
        data = [dec2bcd(d) for d in data]
        self.ds3231.writeList(0, data[:7])

if __name__ == '__main__':
    epoch = Epoch()
    print epoch.getTime()
    epoch.setTime(datetime.datetime.now())
    print epoch.getTime()
