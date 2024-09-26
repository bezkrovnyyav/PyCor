'''
Modify your existing topology classes with at least one abstract class.

Add magic methods to recieve description of the objects.
Override at least one comparison method.
Override at least one arithmetic method.
Override at least one copying method.
'''

from abc import ABC, abstractmethod
from dataclasses import dataclass
from copy import copy



class Pizzeria(ABC):
    
    restaurant_name = "Pizzeria"
    pizza = ['American pizza', 'Italian pizza']
    
    def __init__(self, personal, stars):
        self.personal = personal
        self.stars = stars
   
    @classmethod    
    def get_open(cls):
        return f'{cls.restaurant_name} is opening'
    
    @abstractmethod
    def get_info(self):
        raise NotImplemented
        
@dataclass            
class Chef(Pizzeria):
    
    chef_name: str
    qualification: int
    salary: int
    
    def get_info(self):
        return f'Hi. I am {self.chef_name} - the chef with qualification {self.qualification}'
 
 
class Waiter(Pizzeria):
    
    def __init__(self, waiter_name, qualification, salary):
        self.waiter_name = waiter_name
        self.qualification = qualification
        self.salary = salary
    
    @classmethod   
    def get_new_salar(cls, waiter_name, qualification, new_salary):
        return f'I would like to have a new salary: {cls(waiter_name, qualification, new_salary).salary} dollars'
    
    def get_info(self):
        return f'Hi. My qualification  is {self.qualification}'


class Client(Pizzeria):
    
    def __init__(self, client_name, age, money):
        self.client_name = client_name
        self.age = age
        self.money = money
    
    @staticmethod   
    def make_chois(client_pizza):
        return f'I would like to have {client_pizza}'
    
    def get_info(self):
        return f'Hi. My name is {self.client_name}'


@dataclass            
class Food():
    name: str
    price: int
    
    def __eq__(self, other):
        if not isinstance(other, (int, Food)):
            raise TypeError("Here should be int or class Food")
 
        food_price = other if isinstance(other, int) else other.price
        return self.price == food_price
    
    def __add__(self, other):
        if not isinstance(other, Food):
            raise TypeError('Here should be only class Food')
        full_price = self.price + other.price
        return full_price

    def __copy__(self):
        cls = self.__class__
        new_copy = cls.__new__(cls)
        new_copy.__dict__.update(self.__dict__)
        return new_copy
    

chef = Chef("Andrii", 5, 1000)
print(chef.get_info())

client = Client("Andrii", 25, 200)
print(client.make_chois("Ukrainian pizza"))

waiter = Waiter("Nikita", 5, 500)
print(waiter.get_info())

brown_sugar = Food("Brown Sugar", 10)
white_sugar = Food("White Sugar", 10)
flour = Food('Flour', 5)

# create copy brown_sugar
copy_sugar = brown_sugar.__copy__()
print(f'It is copy of class {copy_sugar}')

#full price of gray sugar and flour
print(brown_sugar + flour)

#checking the price of gray sugar is equal to the price of copy brown_sugar
print(brown_sugar == copy_sugar)

