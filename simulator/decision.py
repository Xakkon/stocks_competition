
class Decision:
    name = "Decision"

    def validate(self, current, history, balance):
        raise NotImplementedError()

    def apply(self, current, history, balance):
        raise NotImplementedError()

class Buy(Decision):
    name = "Buy"
    def __init__(self, amount):
        self.amount = amount

    def validate(self, current, history, balance):
        if type(self.amount) is not int:
            return f"Can buy only integer amount of stocks, not {self.amount}"
        if self.amount <= 0:
            return f"Invalid number of stocks to buy: {self.amount}"
        if current.price * self.amount > balance.money:
            return f"Cannot buy {self.amount} stocks at {current.price}$ while having only {balance.money}"
        return None

    def apply(self, current, history, balance):
        balance.money -= current.price * self.amount
        balance.stock += self.amount

    def __str__(self):
        return f"Buy {self.amount}"

class Sell(Decision):
    name = "Sell"
    def __init__(self, amount):
        self.amount = amount

    def validate(self, current, history, balance):
        if type(self.amount) is not int:
            return f"Can sell only integer amount of stocks, not {self.amount}"
        if self.amount <= 0:
            return f"Invalid number of stocks to sell: {self.amount}"
        if self.amount > balance.stock:
            return f"Cannot sell {self.amount} stocks while having only {balance.stock}"
        return None

    def apply(self, current, history, balance):
        balance.stock -= self.amount
        balance.money += current.price * self.amount
    
    def __str__(self):
        return f"Sell {self.amount}"

class Nothing(Decision):
    name = "Nothing"

    def validate(self, current, history, balance):
        return None

    def apply(self, current, history, balance):
        pass

    def __str__(self):
        return f"Do nothing"

