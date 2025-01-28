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