class Father:
    def skills(self):
        return "Driving"

class Mother:
    def skills(self):
        return "Cooking"

class Child(Father, Mother):
    def own_skill(self):
        return "Dancing"

c = Child()
print(c.skills())   
print(c.own_skill())
