
class Client:
  def __init__(self, name, client_id, age, kind, expenses=0):
    self.name=name
    self.client_id=client_id
    self.age=age
    self.kind=kind
    self.ticket=[]
    self.expenses=expenses
    

  def add_expenses(self,gained):
    self.expenses+=gained



class Ticket:
  def __init__(self, code, seat):
    self.code=code
    self.seat=seat

    