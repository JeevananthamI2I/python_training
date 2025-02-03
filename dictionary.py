from collections import ChainMap

# Two dictionaries
dict1 = {"a": 1, "b": 2}
dict2 = {"b": 20, "c": 30}

# Combine using ChainMap
combined = ChainMap(dict1, dict2)
combined["b"] = 40
print(combined)  # Output: ChainMap({'a': 1, 'b': 2}, {'b': 20, 'c': 30})
print(combined["a"]) 
print(combined["b"])  # Output: 2 (dict1 has priority over dict2)
print(combined["c"])  
# print(combined["d"])  # Output: KeyError: 'd' (key not found in any dict)
