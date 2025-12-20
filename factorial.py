number = int(input("Enter a number: "))

# 1. Initialize a variable to store the result
factorial = 1

if number < 0:
    print("Factorial is not defined for negative numbers.")
elif number == 0:
    # 2. Handle the special case for 0! = 1
    print("The factorial of 0 is 1.")
else:
    # 3. Loop from 1 up to (and including) the number
    #    range(1, number + 1) gives 1, 2, 3, ... up to 'number'
    for i in range(1, number + 1):
        # 4. Multiply the current result by the loop number
        factorial = factorial * i
        
    print(f"The factorial of {number} is {factorial}.")