import datetime as dt
import math as mt
import numscrypt as ns

'''General utilities, possibly used in many places
'''
def colVec (*entries):
    return ns.array (entries) .reshape (len (entries), 1)

def radFromDeg (degrees):
    '''Get radians from degrees
    '''
    
    return (degrees / 180) * mt.pi

def degFromRad (rad):
    '''Get degrees from radians
    '''
    
    return (rad / mt.pi) * 180;
    
        
def raDecFromXyz (xyz):
    '''Get right ascension and declination from x y z coords
    '''
    
    return (
        ((12/mt.pi) * mt.atan2 (xyz [1], xyz [0]) + 24) % 24,
        (180/mt.pi) * mt.atan (xyz [2] / mt.sqrt (xyz [0] * xyz [0] + xyz [1] * xyz [1]))
    )

def decimalHours (hoursMinutes):
    '''Convert <hours>.<minutes> to <hours>.<decimal fraction>
    '''

    return mt.floor (hoursMinutes) + (100 / 60) * (hoursMinutes - mt.floor (hoursMinutes)
    
def julianDayNr (dateTime):
    '''Get julian day number from date and time
    '''

    a = (14 - dateTime.month) / 12
    y = dateTime.year + 4800 - a
    m = dateTime.month + 12 * a - 3
    
    jdnInt = dateTime.day + (153 * m + 2) / 5 + 365 * y + y/4 - y/100 + y/400 - 32045
    
    secPerDay = 24 * 3600;
    sec = dateTime.hour * 3600 + dateTime.minute * 60 + dateTime.second
    frac = sec / secPerDay
    
    return jdnInt + frac
