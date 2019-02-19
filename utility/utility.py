from decimal import Decimal, ROUND_HALF_UP

def roundHalfUpToInt(number):
    return int(Decimal(number).quantize(Decimal('0'), rounding=ROUND_HALF_UP))