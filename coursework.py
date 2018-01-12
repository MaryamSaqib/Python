def Calculations(currentPrice, storedPrice):
    if currentPrice < storedPrice:
        print ('This item is reduced. ')

    percentageReduction = ((float(currentPrice) / storedPrice) * 100)
    print('the percentage reduction for this item is ' + str(percentageReduction) + '%')

Calculations(2,4)

def BooleanAlerts(alerts, currentPrice, storedPrice):
    if currentPrice < storedPrice: 
        alerts = True     

BooleanAlerts(False,2,4) 

#testing the function 
if BooleanAlerts: 
    print('An alert has been sent via email.') 



