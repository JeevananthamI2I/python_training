#python learning
print("Hello world")
def exampleComplex():
#Complex
 comp1=1+5j
 comp2=1-7j
 print(comp1+comp2)
 

##Tuble
def exambleTuple():
 fruit=("banana","apple","Orange","Orange")
 print(fruit)
 print("Fruit2::::",fruit.index("apple",1,2))
 #fruit[1]="Tomato" ###Tuble cannot modified
 print("Fruit1::::",fruit.count("Orange"))
 print("fruit::"+fruit[2])
 test1=(1,2)+(44,5)
 print("test1:::",test1)
 test2=(3,1,2)*4
 print("test2::",test2)
 test3=3 in (5,3,4)
 print("test3::",test3)
 print("lentest::",len(test1))
 for x in ("apple","banana"):
     print("iter tuble::",x)
##Set
def setlearn():
 movie=set(["Goat","Leo","Beast","Beast","Villu"])
 movies={2,3,4,5,6,7,88,100}
 print("movies::",movies,type(movies))
 movie.add("Thuppaki")
 print("set add:::",movie)
 movie.remove("Goat")
 #remove can be throw error in value not exists in set
 print("set remove:::",movie) 
 #discard can't be throw error in value not exists in set,value is exist it will removed
 movie.discard("velayudham") 
 print("set discard:::",movie)

 if "Leo" in movie:
     movie.update(["Sura"])
     print("Set Update::::",movie)
 for i in movie:
    print("movie:::"+i)

 movie.clear()
 print("set clear:::",movie)

##List
def listlearn():
 
 cars=["BMW","Lotus","Lotus","Lotus","Audi",1,2,3]
 print("cars count",cars.count("Lotus"))
 print("cars:::::",cars)
 print(cars[-1],cars[2]) 
 cars[2]="Mahendra"
 print("Cars:::::",cars[-1],cars[2])
 bird=["peacock","crow"]

 ######example 1.add/insert#####
 cars.append(bird)
 cars.extend(bird)
 #print("extend::",cars.extend(bird))
 cars.insert(3,"Lamborgini")
 print("add/ins cars::::",cars)

 #########example 2.remove#######
 cars.remove(1) #it exists in list will delete if not list show error
 print("remove car:::",cars)
 cars.pop()
 print("pop car:::",cars)
 #cars.clear()
 print("clear car:::",cars)

 ########example 3. Search #######
 car1= cars.index("Lotus",0,3)
 print("car1:::",car1)
 ### ex 4.Count######
 print("cars count",cars.count("Lotus"))

 #####example 4. short #####
 birds=["hen","crow","sparrow","duck"]
 birds.sort(reverse=True)
 nums=[5,5,3,2,6,7,8]
 nums.sort()
 print("shortbird::",birds)

 ####example 5.copy ###
 birds1=birds.copy()
 print("copy birds::",birds1)

 ### ex 6.len
 print("length birds2:::",len(birds1))
 print("length birds3:::",birds1.__len__())

###Dictionary##
def demoDic():
   dict={"name":"jeeva","age":25,"place":"chennai","name":"arun","id":2,"contact":9874344324}
   print("dict:::",dict)
   print("keys",dict.keys())    #all keys
   print("age_value",dict["age"]) # print key return value
   print("getKey::",dict.get("dob","Not found"))  #saferr error throw and get value
   dict["dob"]="24/01/2000"   # add item in dict
   print("add item:::",dict)
   dict["dob"]="24/10/2000"     #update item in dict
   print("add item1:::",dict)
   print("add item:::",dict.update({"place":"guindy"}))  
   itemPop=dict.pop("name")       #remove item mentioned and return that value
   print("remove dict::",itemPop)
   del dict["id"]   #del that item
   item2=dict.popitem()    #removes and return last key values pair
   print("pop item::",item2)
   print("items",dict.items()) #return the object containing key value pair tubles
   print("Values::",dict.values())
   #dict.clear()
   print(dict)
def iterateDict():
   card={"tamil":90,"english":93,"maths":95,"science":98,"social":100}
   #iterate key
   for key in card:
      print("card::",key)
   #iter values
   for value in card.values():
      print("values::",value)
   #iter key ,value
   for key,value in card.items():
      print("Key value pair::",f"{key}:{value}")
   

exampleComplex()
listlearn()
exambleTuple()
setlearn()
demoDic()
iterateDict()
