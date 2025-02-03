#1.Write a Python program to count the number of characters in a string. Go to the editor
#Sample String : 'google.com'
#Expected Result : {'o': 3, 'g': 2, '.': 1, 'e': 1, 'l': 1, 'm': 1, 'c': 1}

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
#dictionary
print(count_str())
create_dict()
numbers()
swap_keys()
merge_list()
count_string()
#set 
remove_duplicate()
test_set()
nested_dict()
generator_fun()
print("num_of_str",num_of_str())
