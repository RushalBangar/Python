num=int(input("Enter Number : "))
n=num
rev=0
while n!=0 :
    digit=n%10
    rev=rev*10+digit
    n=n//10
print("The reverse of given number is : ",rev)
if(num==rev):
    print("The given number is palindrome")
else:
    print("The given number is not palidrome")