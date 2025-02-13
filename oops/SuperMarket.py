class SuperMarket:
    def __init__(self, name, price, discount):
        self.name = name
        self.price = price
        self.discount = discount
    def product_details(self):
        #return '{} {}'.format(self.name,self.discount)
        return self.name, self.discount
product1 = SuperMarket('Soap',20,0.05)
product2 = SuperMarket('Shamboo',10,0.04)

#product1.name='soap'
#product1.price='20'
#product1.discount='0.05'
print(product1.product_details())
print(product2.price)

#product1.name='shampoo'
#product1.price='10'
#product1.discount='0.06' 