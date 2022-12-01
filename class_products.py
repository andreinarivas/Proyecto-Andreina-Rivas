class Product:
  def __init__(self, name, price):
    self.name=name
    self.price=price

  def print_information(self):
    for attribute, data in self.__dict__.items():
      print('{}: {}'.format(attribute.capitalize(), data))

class Food(Product):
  def __init__(self, name, price, kind):
    Product.__init__(self, name, price)
    self.type=kind

class Beverage(Product):
  def __init__(self, name, price, alcohol):
    Product.__init__(self, name, price)
    self.alcohol=alcohol

  def print_information(self):
    for attribute, data in self.__dict__.items():
      if attribute=='alcohol':
        if data:
          print('This beverage is alcoholic')
        else:
          print('This beverage is non-alcoholic')
      else:
        print('{}: {}'.format(attribute.capitalize(), data))
    