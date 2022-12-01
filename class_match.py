from search_codes import search_stadium_by_id, search_team
class Match:
  def __init__(self, identification, local_team, visit_team, date, stadium, seats, tickets_left):
    self.id=identification
    self.local_team=local_team
    self.visit_team=visit_team
    self.date=date
    self.stadium=stadium
    self.tickets_left=tickets_left
    self.seats=seats
    self.tickets_sold=[]
    self.assistence=[]

  def print_info(self, data_base):
    print('MATCH #{} \n  Home Team : {} \n Away Team : {} \n Date & Time: {} \n Stadium :{} \n'.format(self.id, search_team(data_base, self.local_team).country, search_team(data_base, self.visit_team).country, self.date, search_stadium_by_id(data_base, self.stadium).name))

  def show_available_seats(self):
    print('--------- GENERAL SECTION ---------')
    for row in self.seats[0]:
      print(' '.join(row))
    print('--------- VIP SECTION ---------')
    for row in self.seats[1]:
      print(' '.join(row))
  
  def get_num_available_seats(self, kind):
    count=0
    if kind=='VIP':
      for row in self.seats[1]:
        for seat in row:
          if seat!='X':
            count+=1
    else:
      for row in self.seats[0]:
        for seat in row:
          if seat!='X':
            count+=1
    return count


