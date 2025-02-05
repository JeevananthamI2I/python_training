#1.Write a Python program to count the number of characters in a string. Go to the editor
#Sample String : 'google.com'
#Expected Result : {'o': 3, 'g': 2, '.': 1, 'e': 1, 'l': 1, 'm': 1, 'c': 1}
from functools import reduce
def count_str():
    name="google.com"
    dict1={val:name.count(val) for val in name}
    print("dict1",dict1)

#list comprehension
def list_comprehension():
    List=[A for A in range(10) if A%2==0]
    print("listComprehension",List)

def list_test1():
    list_a=[2,5,6,10,12]
    list_b=[i*2 for i in list_a]
    print("list_b",list_b)

def create_dict():
    list1=[1,2,3,4,5,7,8]
    sample_dict={i:i*2 for i in range(9)}
    print(sample_dict)

# Using if-else in Dictionary Comprehension
def numbers():
    nums={i:("even" if i%2==0 else "odd") for i in range(20)}
    print("nums",nums)

#swapping keys
def swap_keys():
    test={1:'a',2:"ba",3:"cat"}
    new_test={j:i for i,j in test.items()}
    print("swap_keys",new_test)

#merging two list
def merge_list():
    list1=["name","age","place"]
    list2=["jeeva",25,"chennai"]
    merge_dict={list1[i]:list2[i] for i in range(len(list1))}
    print("merge_list",merge_dict)

#counting strings
def count_string():
    hw="Hello World"
    hw_count={char:hw.count(char) for char in hw}
    print("hw",hw_count)
#remove duplicates
def remove_duplicate():
    rm=[1,2,2,3,4,5,6,4,5]
    rm_set={i for i in rm}
    print("remove duplicate",rm_set)
list_comprehension()
list_test1()

def test_set():
    list1=[1,2,3,4,5,6]
    list2=[2,3,4,5,6,7]
    test_tubles={(i,j) for i in range(len(list1)) for j in range(len(list2)) if (list1[i]+list2[j])%2==0 }
    print("set comprehension",test_tubles)

def nested_dict():
    students={"Jeeva","Adhi","Vasanth"}
    subjects=["Tamil","English","Maths","Science","Social"]
    marks=[90,92,95,97,97]
    dictt={student:{subjects[i]:marks[i] for i in range(len(subjects))}for student in students}
    print("dictt",dictt)

def generator_fun():
   squares_gen = (x for x in range(5))
   print(squares_gen)

   print(next(squares_gen))  
   print(next(squares_gen))  
   print(next(squares_gen))  

#Sample List : ['abc', 'xyz', 'aba', '1221']
def num_of_str():
    list1=['abc', 'xyz', 'aba', '1221']
    count=0
    list2={count+1 for i in list1 if(i[0]==i[-1] and len(i)>=2)}   
    print("list2",list2)   

#postionall arquement and keyword arquement
def count_string():
    def count_str(*args,**kwargs):
        print("args",args)
        print("kwargs",kwargs)
    count_str(1,2,3,4,5,6,7,8,9,10,name="jeeva",age=25,place="chennai")

def outer():
    print("Outer function")

    def inner():
        print("Inner function")

    # inner()  # Call the inner function

#anonymouns function
add = lambda x,y:x+y
print("anonymous",add(2,3))

#generator
def gen():
    gen=(i for i in range(20))
    print("generator",next(gen))
    print("generator",next(gen))
    print("generator",next(gen))

#recursion
def recurse_fun(n):
    if n==10:
        return n*n,n
    else:
        return recurse_fun(n+1)

#map
def square_map():
    list1=[2,3,4,5,6,7]
    list2=[9,8,7,6]
    square_val=list(map(lambda x,y:x*y,list1,list2))
    print("square_val",square_val)


#zip
def join_map():
    list1=['a','b','c','d']
    list2=[1,2,3,4,5]
    list3=list(zip(list1,list2))
    print(list3)


#filter
def filter_even():
    list1=[1,2,3,4,5,6,7,8]
    even_num=list(filter(lambda x:x%2==0,list1))
    print("even_num",even_num)

#reduce
def max_nums():
    numbers=[2,3,4,10,6,7,8]
    max_num =  reduce(lambda x, y: x if x > y else y, numbers)
    print("reduce",max_num)
#enumerate
def find_index():
    numbers=[2,3,4,10,6,7,8]
    for i,j in enumerate(numbers):
        print(i,j)

#id
def id_fun():
    x=5
    y=5
    print(x is y)
    print("id",id(x),id(y))
gen()
recurse_fun(1)
print("recurse fun",recurse_fun(1))
# #dictionary
# print(count_str())
# create_dict()
# numbers()
# swap_keys()
# merge_list()
# count_string()
# #set 
# remove_duplicate()
# test_set()
# nested_dict()
# generator_fun()
# print("num_of_str",num_of_str())

# #python function
# count_string()
# outer()
square_map()
join_map()
filter_even()
max_nums()
find_index()
id_fun()