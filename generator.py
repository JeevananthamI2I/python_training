import time

def my_generator():
    yield 1
    yield 2
    yield 3

gen = my_generator()

print(next(gen))
print(next(gen))
print(next(gen))

#generator with loops

def my_generator():
    for i in range(3):
        yield i

for num in my_generator():
    print("num",num)
    
#generatoe expression
gen = (x * 2 for x in range(6))
print(next(gen)) 
print(next(gen)) 
print(list(gen))

#reading files with generator
def read_large_file(file_path):
    with open(file_path, "r") as file:
        for line in file:
            yield line.strip()
count=0
for line in read_large_file("sample.txt"):
    count+=1
    print(f'{count}::{line}')

#generator with loops
def infinite_numbers():
    num = 0
    while True:
        yield num
        num += 1

gen = infinite_numbers()
print(next(gen)) 
print(next(gen)) 
print(next(gen)) 

#Delegating to Another Generator
def gen1():
    yield 1
    yield 2

def gen2():
    yield from gen1()  # Calls another generator
    yield 3

for num in gen2():
    print("Delegating Another::",num)

#list in generator
gen = (x * 2 for x in range(5))
print("list in generator:::",list(gen))

import sys

# List stores all elements in memory
list_nums = [x for x in range(10000)]
print("List size:", sys.getsizeof(list_nums))

# Generator yields elements one by one
gen_nums = (x for x in range(10000))
print(list(gen_nums))
print("Generator size:", sys.getsizeof(gen_nums))


#speed of generator

# List Comprehension
start = time.time()
sum([x for x in range(10000)])
end = time.time()
print("List Time:", end - start)

# Generator Expression
start = time.time()
sum(x for x in range(10000))
end = time.time()
print("Generator Time:", end - start)

