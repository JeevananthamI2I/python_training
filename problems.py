#python problems solving

#1.Input: nums = [2,7,11,15], target = 9
#Output: [0,1]
#Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

class Solution:
    list1=[2,7,11,15]
    target=26
    def twoSum(list1, target):
    	for i in range(len(list1)):
            for j in range(1, len(list1)):
                value=list1[i]+list1[j]
                if value==target:
                    return i,j
    print(twoSum(list1, target))

def two_sum(nums, target):
    seen = {}  
    for i, num in enumerate(nums):
        diff = target - num
        print("diff",diff)
        print("seen:::::",seen)
        if diff in seen:  
            print("seen[diff]",seen[diff])
            return [seen[diff], i]  
        seen[num] = i  
        print("seen",seen)
    return None

nums = [2, 7, 11, 15]
target = 18
print(two_sum(nums, target))  # Output: [0, 1]

my_dict = {"name": "Alice", "age": 25}
print(hash("name") % 8)  # Hash value mod table size
print(hash("age") % 8) 

# Input: l1 = [2,4,3], l2 = [5,6,4]
# Output: [7,0,8]
# Explanation: 342 + 465 = 807.
def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) :
    l1=[2,4,3]
    l2=[5,6,4]
    str1=""
    l3=[str1+i for i in range(len(l1) if len(l1)!=0]
    

    