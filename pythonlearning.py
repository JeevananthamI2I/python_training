#python learning
print("Hello world")
def auto():
 #Complex
 comp1=1+5j
 comp2=1-7j
 print(comp1+comp2)

 ##Sequence

 ##List
 cars=["BMW","Lotus","Audi",1,2,3]
 print(cars[-1],cars[2]) 
 cars[2]="Mahendra"
 print("Cars:::::",cars[-1],cars[2])

 ##Tuble
 fruit=("banana","apple","Orange")
 #fruit[1]="Tomato" ###Tuble cannot modified
 print(fruit)
 print("fruit::"+fruit[2],cars[1])

 ##Set
 movie=set(["Goat","Leo","Beast","Beast"])
 if "Leo" in movie:
     movie.add("Thuppaki")
     print("set add:::",movie)
     movie.update(["Sura"])
     print("Set Update::::",movie)
 for i in movie:
    print("movie"+i)
 
auto()