
from collections import Counter
from collections import defaultdict
from collections import OrderedDict
from collections import deque
from collections import namedtuple
from collections import ChainMap
from collections import UserDict 
from collections import UserList

#Counter
words = ["apple", "banana", "apple", "orange", "banana", "banana"]
counter = Counter(words)
print(counter)


#defaultdict
inventory = defaultdict(str)

inventory["apples"] += "red"
inventory["oranges"]
inventory["bananas"] += "yellow"

print(inventory)
print(inventory["bananas"])

#OrderedDict
ordered_dict = OrderedDict()
ordered_dict["banana"] = 2
ordered_dict["apple"] = 1
ordered_dict["orange"] = 3

print(ordered_dict)

#deque
queue = deque(["apple", "banana", "orange"])
queue.append("grape")  
queue.appendleft("mango")
print(queue)  

queue.pop() 
queue.popleft()
print(queue)

#namedtuple
Point = namedtuple("Point", ["x", "y"])
p = Point(1, y=2)       
print(p)
print(p.x, p.y)
print(p[0], p[1])
print(p._fields)
print(p._asdict())
print(p._replace(x=100))
print(p._make([10, 20]))

#ChainMap
default_settings = {"theme": "light", "language": "English"}
user_settings = {"theme": "dark"} 

config = ChainMap(user_settings, default_settings)
print(config)
print(config["theme"])  
print(config["language"]) 


#userdict       
class LoggedDict(UserDict):
    def __getitem__(self, key):
        print(f"Accessing key: {key}")
        return super().__getitem__(key)
    
    def __setitem__(self, key, value):
        print(f"Setting {key} to {value}")
        super().__setitem__(key, value)
    
    def __delitem__(self, key):
        print(f"Deleting key: {key}")
        super().__delitem__(key)

# Usage
data = LoggedDict({"name": "Jeeva", "age": 25})
print(data["name"])  
data["city"] = "Chennai"
del data["age"]  

#userlist
class NoNegativeList(UserList):
    def append(self, item):
        if item < 0:
            raise ValueError("Negative numbers are not allowed!")
        super().append(item)

numbers = NoNegativeList([1, 2, 3])
numbers.append(5)  
print(numbers)
