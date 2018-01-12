def Calculations(currentPrice, storedPrice):
    if currentPrice - storedPrice < 0:
        print ('This item is reduced. ')

    percentageReduction = ((currentPrice - storedPrice) * 100)
    print(percentageReduction)

Calculations(2,4)

def BooleanAlerts():
    print('in the boolean alerts function') 


BooleanAlerts() 
