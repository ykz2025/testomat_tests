# int, float; operations; math; string to number
from typing import List

index = 10
print(index)

price = 10.99
print(price)

price_from_text = float("10.98")
print(price_from_text+4.02)

index_of_page = "2"
print(int(index_of_page)+1)

actual_prices: List[str] = ["10.99", "99.43", "12.03"]

print(actual_prices)
print(max(actual_prices))

def is_first_price_the_highest(t_prices: List[str]):
    return t_prices[0] == max(t_prices)

print(is_first_price_the_highest(actual_prices))

actual_prices.sort(reverse=True)
print(actual_prices)

print(is_first_price_the_highest(actual_prices))


print(int(index_of_page)+57458586)

class Popo:

    name:str
    dsfsged:str

    def __init__(self, name: str):
        self.name = name
        self.dsfsged = name

    def printpopo(self):
        print(self.name)

    def fdghgrhr(self):
        print(self.name)
        print(self.dsfsged)