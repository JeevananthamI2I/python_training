#range in index list (x) or (x,y) or (x,y,z)
def rangeList(x,y=0,z=0):
    if x!=0 and y==0 and z==0:
        count=0
        countList=[]
        while count<x:
            countList+=[count]
            count+=1
            # print(count)
        return countList
    elif x!=0 and y!=0 and z==0:  
        count=x
        countList=[]
        while count<y:
            countList+=[count]
            count+=1
            print(count)
        print("countList::",countList)
        return countList
    elif x!=0 and y!=0 and z!=0:
        count=x
        countList=[]
        while count<y:
            countList+=[count]
            count+=z
            print(count)
        print("countList::",countList)
        return countList
    

#Length of list
def lenList(list):
    count=0
    for i in list:
        count+=1
    return count


#add element in end
def appendList(list1,list2):
    list1=list1+[list2]
    return list1


#extend list 
def extendList(list3,list4):
    list3
    for i in rangeList(lenList(list4)):
        list3=list3+[list4[i]]
    return list3

#insert element in list
def insertList(list5,indexValue,element):
    list6=[]
    if lenList(list5)<=indexValue:
        list6=list5+[element]
        return list6
    elif lenList(list5)>indexValue:
        list7=[]           
        for i in rangeList(lenList(list5)+1):
            if i<indexValue:
                list7=list7+[list5[i]]
            elif i==indexValue:
                list7=list7+[element]
            elif i>indexValue:
                list7=list7+[list5[i-1]]
        return list7
    
#short list
def shortList(list,reverse=False):
    list1=[]
    list2=[]
    for i in list:
        if i<i+1:
           print("list",list[1])
           list1=list1+[list[i]]
    if reverse:
       print("List",list1)
       print("range",range(len(list1)))
       for i in range(len(list1)):
          if i>range(len(list1):
           print("list",list1)
           list2=list2+[list1[i]]
           i--
       return list2
    print("shoettcd",list2)
    return list2
            	   
            
        
	



list1=[1,2,3,4,5]
list2=[6,7,8,9,10]
list3=[1,2,3,4,5]
list4=[6,7,8,9,10,11,12,13,14,15]
list5=[0,9,8,7,6,5,4,3,2,1]
print("Extend::",extendList(list3,list4))
print("Append:::",appendList(list1,list2))
print("Insert::",insertList(list5,5,10))
print("Range::",rangeList(10))
print("Length::",lenList(list1))
print("Short::",shortList(list5))

