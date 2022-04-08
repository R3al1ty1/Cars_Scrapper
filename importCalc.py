import datetime

def carAge(manufactureYear):
    todayYear = datetime.date.today().year
    return todayYear - manufactureYear
def taxProtocol(rubPrice):
    if rubPrice < 200000:
        return 775
    elif rubPrice < 450000:
        return 1550
    elif rubPrice < 1200000:
        return 3100
    elif rubPrice < 2700000:
        return 8530
    elif rubPrice < 4200000:
        return 12000
    elif rubPrice < 5500000:
        return 15500
    elif rubPrice < 7000000:
        return 20000
    elif rubPrice < 8000000:
        return 23000
    elif rubPrice < 9000000:
        return 25000
    elif rubPrice < 10000000:
        return 27000
    else:
        return 30000

def recyclingCollection(carAge, volume, isCargo = False, isCompany = False):
    isOlderThan3Years = carAge >= 3
    coef = 0
    basePrice = 20000 * (not isCargo) + 150000 * (isCargo)
    if isCompany:
        if volume == 0:
            coef = 6.1 if isOlderThan3Years else 1.63
        elif volume <= 1000:
            coef = 6.15 if isOlderThan3Years else 2.41
        elif volume <= 2000:
            coef = 15.69 if isOlderThan3Years else 8.92
        elif volume <= 3000:
            coef = 24.01 if isOlderThan3Years else 14.08
        elif volume <= 3500:
            coef = 28.5 if isOlderThan3Years else 12.98
        else:
            coef = 35.01 if isOlderThan3Years else 22.25
    else:
        coef = 0.25 if isOlderThan3Years else 0.17

    return basePrice * coef

def excise(hp):
    if hp < 90:
        return 0
    elif hp < 150:
        return hp * 51
    elif hp < 200:
        return hp * 491
    elif hp < 300:
        return hp * 804
    elif hp < 400:
        return hp * 1370
    elif hp < 500:
        return hp * 1418
    else:
        return hp * 1464

def customsDuty(carAge, euroPrice, volume, isCompany = False, isDiesel = False):
    if isCompany:
        if isDiesel:
            if carAge < 3:
                return euroPrice * 0.15
            elif carAge < 7:
                if volume <= 1500:
                    return max(euroPrice * 0.2, 0.32 * volume)
                elif volume <= 2500:
                    return max(euroPrice * 0.2, 0.4 * volume)
                else:
                    return max(euroPrice * 0.2, 0.8 * volume)
            else:
                if volume <= 1500:
                    return 1.5 * volume
                elif volume <= 2500:
                    return 2.2 * volume
                else:
                    return 3.2 * volume
        else:
            if carAge < 3:
                if volume <= 3000:
                    return 0.15 * volume
                else:
                    return 0.125 * volume
            elif carAge < 7:
                if volume <= 1000:
                    return max(euroPrice * 0.2, 0.36 * volume)
                elif volume <= 1500:
                    return max(euroPrice * 0.2, 0.4 * volume)
                elif volume <= 1800:
                    return max(euroPrice * 0.2, 0.36 * volume)
                elif volume <= 3000:
                    return max(euroPrice * 0.2, 0.44 * volume)
                else:
                    return max(euroPrice * 0.2, 0.8 * volume)
            else:
                if volume <= 1000:
                    return 1.4 * volume
                elif volume <= 1500:
                    return 1.5 * volume
                elif volume <= 1800:
                    return 1.6 * volume
                elif volume <= 3000:
                    return 2.2 * volume
                else:
                    return 3.2 * volume
    else:
        if carAge < 3:
            if euroPrice <= 8500:
                return max(euroPrice * 0.54, 2.5 * volume)
            elif euroPrice <= 16700:
                return max(euroPrice * 0.48, 3.5 * volume)
            elif euroPrice <= 42300:
                return max(euroPrice * 0.48, 5.5 * volume)
            elif euroPrice <= 84500:
                return max(euroPrice * 0.48, 7.5 * volume)
            elif euroPrice <= 169000:
                return max(euroPrice * 0.48, 15 * volume)
            else:
                return max(euroPrice * 0.48, 20 * volume)
        elif carAge < 5:
            if volume <= 1000:
                return 1.5 * volume
            elif volume <= 1500:
                return 1.7 * volume
            elif volume <= 1800:
                return 2.5 * volume
            elif volume <= 2300:
                return 2.7 * volume
            elif volume <= 3000:
                return 3 * volume
            else:
                return 3.6 * volume
        else:
            if volume <= 1000:
                return 3 * volume
            elif volume <= 1500:
                return 3.2 * volume
            elif volume <= 1800:
                return 3.5 * volume
            elif volume <= 2300:
                return 4.8 * volume
            elif volume <= 3000:
                return 5 * volume
            else:
                return 5.7 * volume
