try:
    num = int(input("Enter a number: ")) 
    result = 10 / num  
    print("Result:", result)
except ZeroDivisionError:
    print("Error: Cannot divide by zero!")
except ValueError:
    print("Error: Please enter a valid number!")


try:
    lst = [1, 2, 3]
    print(lst[5]) 
except (IndexError, KeyError):
    print("Error: Invalid index or key!")

try:
    num = int(input("Enter a number: "))
    print("Valid number entered:", num)
except ValueError:
    print("Error: Not a valid integer!")
else:
    print("This runs only if no error occurs.")
finally:    
    print("This runs no matter what!")

def check_age(age):
    if age < 18:
        raise ValueError("Age must be 18 or above!")
    return "Access granted."

try:
    print(check_age(15))
except ValueError as e:
    print("Exception:", e)
