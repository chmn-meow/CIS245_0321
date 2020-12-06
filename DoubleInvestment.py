P = float(input("What is your intial investment?"))
R = float(input("Enter you annual interest rate in %:"))
Year = 0
investment = P
target = 2*P

while investment <= target:
    Year += 1
    #investment = (P*R*1) + P
    investment = (investment * (1+(R/100)))
    if investment >= target:
        break
print ("It will take", Year, "years", "to double your investment")
    

    
 
