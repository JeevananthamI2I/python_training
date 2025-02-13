#Decorators

def my_dec(func):
    def sum_of_num(a,b):
        if b > a:
            a,b = b,a
            return a,b
    return sum_of_num
@my_dec
def subract_num(a,b):
    return a-b
#sub_num = my_dec(subract_num)

print(subract_num(5,6))