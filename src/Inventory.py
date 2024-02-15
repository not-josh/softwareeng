class Inventory:
    def __init__(self):
        self.items:dict = {}

    def add_item(self, item):
        if item in self.items:
            self.items[item] += 1
        else:
            self.items[item] = 1

    def add_items(self, item, amount):
        if item in self.items:
            self.items[item] += amount
        else:
            self.items[item] = amount

    def remove_item(self, item):
        if item in self.items:
            if self.items[item] >= 1:
                self.items[item] -= 1
            else:
                raise Exception("Tried to remove " + item + "but there are < 1 items left to remove")
        else:
            raise Exception("Tried to remove a(n) " + item + "but that item does not exist in the inventory")

    def remove_items(self, item, amount):
        if item in self.items:
            if self.items[item] >= amount:
                self.items[item] -= amount
            else:
                raise Exception("Tried to remove " + amount + "" + item + "s but there are not enough items left to remove that many")
        else:
            raise Exception("Tried to remove multiple " + item + "s but that item does not exist in the inventory")