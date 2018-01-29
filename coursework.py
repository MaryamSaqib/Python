def Calculations(currentPrice, storedPrice): #defining the function called Calculations and storing the variables into the parameters. 
    if currentPrice - storedPrice < 0: #If Statement to calculate if the current price is less than the stored price so the program knows whether it should print the output to the user.
        print ('This item is reduced. ') #This is the output that will be outputted to the user if the current price is less than the stored price 

    percentageReduction = ((float(currentPrice) / storedPrice) * 100) #Calculation showing how to calculate the percentage reduction 
    if currentPrice - storedPrice < 0:
    print('the percentage reduction for this item is ' + str(percentageReduction) + '%') #Cancatination of the string and integer in order to tell the user the percentage reduction of the reduced item.

Calculations(2,4) #This is the call to the function with the values for the variables stored in the parameters. 

def BooleanAlerts(alerts, currentPrice, storedPrice): #defining the function called BooleanAlerts and storing the variables into the parameters. 
    if currentPrice - storedPrice < 0: #If Statement to calculate if the current price is less than the stored price so the program knows whether it should set the Boolean should be set to True
        alerts = True  #If the statement is true then the boolean called alerts will be set to True 

BooleanAlerts(False,2,4) #This is the call to the function with the values for the variables stored in the parameters.

#testing the function 
if BooleanAlerts: #The colon after the funtion is telling the program to output the print statement only if the boolean is set to True. 
    print('An alert has been sent via email.') #This print statement will tell me whether the boolean has changed to True and this will show me if it works appropriately. 



