from decision import Buy, Nothing, Sell
import random

def act(current, history, balance):
    maximum_can_buy = balance.money // current.price
    if maximum_can_buy > 0:
        return Buy(maximum_can_buy)
    else:
        if random.random() > 0.5:
            return Sell(balance.stock)
        else:
            return Nothing()