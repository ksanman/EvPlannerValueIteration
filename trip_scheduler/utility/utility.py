from decimal import Decimal, ROUND_HALF_UP

def RoundHalfUpToInt(number):
    return int(Decimal(number).quantize(Decimal('0'), rounding=ROUND_HALF_UP))

def ConvertFromSecondsToFifteenMinuteBlock(seconds):
    minutes = seconds / 60
    return RoundHalfUpToInt(minutes / 15)

def ConvertFromTimeBlockToHours(timeBlock):
    """ Converts a 15 minute time block to hours

        Keyword arguments:

        timeBlock -- A block of time. Each interger increment is 15 minutes. 
    """
    hours = (timeBlock * 15) / 60.0
    return hours
