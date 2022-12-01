from validation_codes import validate_input_num, validate_input_str, validate_options, validate_boolean
from class_client_ticket import Client, Ticket
from class_match import Match
from search_codes import search_stadium_by_id, search_team, search_client
import itertools as it


def validate_client_exists(client_id, data_base):
  '''
  Checks if the client exists in the data base

  Takes the input for client id and compares it with all registered clients

  Params
  ----------
  client_id: int
    Validated input from user for client id
  data_base: dict
    Data base with all the program's information

  Returns 
  ----------
  True if the client id is found in the data base
  '''
  list_clients=data_base.get('client')
  for client in list_clients:
    if client.client_id==client_id:
      return True

def validate_match_available(match_num, available_matches):
  ''' 
  Validate if a match number is present in the available matches

  Takes an input match id and compares it to all available matches to validate
  it exists, until the input is valid

  Params 
  --------
  match_num: int
    Input match id
  available_matches: list
    List of Match objects

  Return 
  --------
    match: Match
      Match object corresponding to the given match id
  '''
  is_valid=False
  while is_valid==False:
    for match in available_matches:
      if match.id==match_num:
        is_valid=True
        return match
    match_num=validate_input_num('match number')

def get_seat_index(wanted_seat, match, zone):
  ''' 
  Recovers the index numbers for the selected seat

  Searches the available seat attribute from the selected match to search for the 
  seat input by the user. It continues until it validates the input given is found
  available

  Params
  --------
    wanted_seat: list(srt)
      List of elements of input
    match: Match
      Object match chosen
    zone: int
      index for the kind of ticket bought
        1- VIP
        0- General
  Returns
  --------
    index: list
      index for the seat chosen
    wanted_seat: str
      input for the wanted seat

  '''
  wanted_seat=''.join(wanted_seat)
  found=False
  while found==False:
    wanted_seat=''.join(wanted_seat)
    for i in range(0, len(match.seats[zone])):
      for j in range(0, 10):
        if match.seats[zone][i][j]==wanted_seat:
          index=[i, j]
          found=True
          return index, wanted_seat
    wanted_seat=input('Please choose a valid seat in the selected zone \n  \n >>> ')
    wanted_seat=[index for index in wanted_seat]
    wanted_seat=validate_seat_input(wanted_seat)

  

def validate_seat_input(wanted_seat):
  ''' 
  Validate if the input for wanted seat follows the format

  Checks if the first element of a list of elements from the input follows the format
  for seat names. The first must be alpabetic and the second must be a number from 1-10

  Params
  --------
    wanted_seat: list
       List of elements of input
  Returns
  --------
    wanted_seat: list
       validated list of elements of input
  '''
  while len(wanted_seat)<2 or not wanted_seat[0].isalpha() or not wanted_seat[1] in [str(x) for x in range(1,11)]:
    wanted_seat=input('Please enter a valid seat: \n Remember to introduce in ROW SEAT form \n >>> ')
    wanted_seat=[index for index in wanted_seat]
  return wanted_seat
  
def validate_seat_num(wanted_seat, zone, match,seats):
  ''' 
  Validate if the input for wanted seat has been chosen before

  Checks if the input given by the client is the same as one given before by them


  Params
  --------
    wanted_seat: list
       List of elements of input
    zone: int
      index for the kind of ticket bought
        1- VIP
        0- General
    match: Match
      Object match chosen 
    seats: list
      list of previously chosen seats
    
  Returns
  --------
    wanted_seat: list
       validated list of elements of input
    seat_index: list
      index for the seat chosen

  '''
  wanted_seat=validate_seat_input(wanted_seat)
  for seat in seats:
    wanted_seat=''.join(wanted_seat)
    if wanted_seat==seat[0]:
      wanted_seat=input('Please choose a different seat: \n >>> ')
      wanted_seat=[index for index in wanted_seat]
      wanted_seat=validate_seat_input(wanted_seat)
  seat_index, wanted_seat=get_seat_index(wanted_seat, match, zone)
  return wanted_seat, seat_index
      
def occupy_seat(match,zone, wanted_seat):
  ''' 
  Occupies seat in the matrix for the match's available seats

  Searches the specified index given to change the vacancy of the seats bought

  Params 
  -------
  match: Match
    Object match chosen
  zone: int
      index for the kind of ticket bought
        1- VIP
        0- General
  wanted_seat: list
    Index for the seat bought
  '''
  match.seats[zone][wanted_seat[0]][wanted_seat[1]-1]='X'

def select_seat(match, kind, quantity):
  ''' 
  Select seat for the amount of tickets bought

  Does all the validation for availability and format for the tickets by the kind of ticket bought

  Params 
  -------
  match: Match
    Object match chosen
  kind: str
    Type of ticket chosen
  quantity: int
    Number of ticket boughts

  Returns
  ---------
    seats: list(tuples)
      List of tuples with seat and their corresponding index
  '''
  match.show_available_seats()
  seats=[]
  for x in range(quantity):
    if kind=='VIP':
      wanted_seat=input('Please enter the desired seat: \n >>> ')
      while wanted_seat in seats:
        wanted_seat=input('Please choose a different seat: \n >>> ')
      wanted_seat=[index for index in wanted_seat]
      wanted_seat, seat_index = validate_seat_num(wanted_seat, 1, match, seats)
    elif kind=='General':
      wanted_seat=input('Please enter the desired seat: \n >>> ')
      while wanted_seat in seats:
        wanted_seat=input('Please choose a different seat: \n >>> ')
      wanted_seat=[index for index in wanted_seat]
      wanted_seat, seat_index = validate_seat_num(wanted_seat, 0, match,seats)
    seat=''.join(wanted_seat)
    seats.append((seat, seat_index))
  return seats

def check_fifa_code_length(code):
  '''
  Validates the length for a teams fifa code is 3

  To follow format for ticket codes, all fifa codes must be 3 elements long
  if not, it adds a X at the beggining to not alter the ticket code format


  Params
  -------
    code: str
      Fifa code to check
  Returns
  -------
    team_code: str
      Validated fifa code
  '''
  if len(code)<3:
    team_code='X'+code
  else:
    team_code=code
  return team_code
  
def generate_ticket_code(match,seat, data_base):
  '''
  Generates a unique ticket code

  Based on the teams playing, the match id, and seat corresponding

  Params
  --------
  match: Match
    match chosen
  seat: str
    seat chosen
  data_base: dict
    Data base with all the programs information

  Returns
  ----------
  ticket_code: srt
    generated ticket code
  '''
  match_id=str(match.id)
  seat=str(seat)
  if len(match_id)<2:
    ticket_code='{}VS{}0{}{}'.format(check_fifa_code_length(search_team(data_base, match.local_team).fifa_code), check_fifa_code_length(search_team(data_base, match.visit_team).fifa_code),match_id,seat)
  else:
    ticket_code='{}VS{}{}{}'.format(check_fifa_code_length(search_team(data_base, match.local_team).fifa_code), check_fifa_code_length(search_team(data_base, match.visit_team).fifa_code),match_id,seat)
  return ticket_code


def show_available_matches(matches, data_base):
  ''' 
  Prints a list of matches with seats available

  Params 
  -----------
  matches: list(Matches)
    all matches available
  data_base: dict
    Data base with all the programs information
  '''
  for match in matches:
    match.print_info(data_base)

def buy_tickets(available_matches, data_base, kind):
  ''' 
  Collects all the information to complete the purchase of tickets

  Allows the user to select an available match, get a valid number of tickets, and select the wanted seats for all tickets wanted
  Creates the corresponding Ticket objects for each ticket

  Params
  --------
  available_matches: list
    List of all available matches
  data_base: dict
    Data base of all the programs information
  kind: str
    Type of tickets wanted

  Returns
  --------
  match: Match
    chosen match
  seats: list
    all seats chosen
  tickets: list
    ticket codes generated
  '''
  show_available_matches(available_matches, data_base)
  match=validate_match_available(validate_input_num('match number'),available_matches)
  quantity=validate_input_num('number of tickets')
  if match.get_num_available_seats(kind)==0:
    print('This zone is unavailable \n Please quit the purchase \n \n ')
  else:
    while not quantity<=match.get_num_available_seats(kind):
      print('This number of seats is not available \n Available: {}'.format(match.get_num_available_seats(kind)))
      quantity=validate_input_num('number of tickets')
    seats=select_seat(match, kind, quantity)
    tickets=[]
    for x in range(quantity):
      ticket=Ticket(generate_ticket_code(match, seats[x][0], data_base), seats[x][0])
      tickets.append(ticket.code)
    return match, seats, tickets

def validate_zone_available(kind, match):
  '''
  Check if there are available seats for a specific type 

  It avoids the user from buying tickets in a zone where there are no more available

  Params 
  ---------
  kind: str
    type of ticket chosen
  match: Match
    chosen match
  '''
  if match.get_num_available_seats(kind)==0:
    kind=validate_options('ticket type', f'{kind} is unavailable', ['1'])

def get_client_data(available_matches, data_base):
  '''
  Collects all the information from the client

  Takes all the information from the client to generate the purchase
  It validates if the client already exists in the system

  Params 
  -------
  available_matches: list
    list of all available matches
  data_base: dict
    data base with all the programs information
  
  Returns
  ---------
  new_client: Client
    Object with client information
  match: Match
    chosen match
  seats: list
    chosen seats
  tickets: list
    ticket codes generated
  '''
  client_id=validate_input_num('id')
  exists=validate_client_exists(client_id, data_base)
  if exists:
    print('\n CLIENT ALREADY REGISTERED \n \n')
    client=search_client(data_base, client_id)
    match, seats, tickets = buy_tickets(available_matches, data_base, client.kind)
    client.ticket+=tickets
    return client, match, seats, tickets
  else:
    print('\nNEW CLIENT \n \n')
    name=validate_input_str('name')
    age=validate_input_num('age')
    kind=validate_options('ticket type', '1. VIP --- 120$ \n 2. General --- 50$', ['1','2'])
    if kind==1:
      kind='VIP'
    else:
      kind='General'
    match, seats, tickets = buy_tickets(available_matches, data_base, kind)
    new_client=(Client(name, client_id, age, kind))
    new_client.ticket+=tickets
    return new_client, match, seats, tickets

def print_tickets_bought(seats):
  '''
  Creates a string of the number seats bought for the receipt

  Params
  -------
  seats: list
    seats bought
   Return 
   --------
   seats_bought: str
    all seats bought in a string 
  '''
  seats_bought='Seats Bought: '
  for x in range(len(seats)):
    seats_bought+='  {}'.format(seats[x][0])
  return seats_bought

def print_ticket_codes(tickets):
  ''' 
  Print ticket codes bought

  Params 
  ---------
  tickets: list
    list of ticket codes
  '''
  print('\n ****** TICKET CODES ******')
  for ticket in tickets:
    print('***   {}'.format(ticket))


def register_purchase(data_base, available_matches):
  '''
  Collects all the information necessary to process the purchase of match tickets

  Takes all the information, prints the receipt and adds it all to the data base
  
  Params
  ---------
  data_base: dict
    data base with all the programs information
  available_matches: list
    list of Match objects for matches with available tickets
  
  '''
  client, match, seats, tickets =get_client_data(available_matches, data_base)
  if client.kind=='VIP':
    ticket_price=120
  else:
    ticket_price=50
  total, discount, tax =get_total(client.kind, client.client_id, ticket_price, len(seats))
  print('--------------- RECEIPT ---------------')
  print('TICKET FOR MATCH {} VS {} - {}'.format(search_team(data_base, match.local_team).country, search_team(data_base, match.visit_team).country, match.date))
  print('Name: {} \n ID: {} \n Zone: {}\n {} \n Quantity: {} \n Ticket Price: {} \n Discount: {:.2f} \n IVA: {:.2f} \n TOTAL: {:.2f}'.format(client.name, client.client_id, client.kind, print_tickets_bought(seats),len(seats), ticket_price,discount, tax, total ))
  add=validate_boolean('Would you like to continue with the purchase?')
  if add:
    client.expenses+=total
    add_ticket(match.id, tickets , seats, client.kind, available_matches)
    data_base['client'].append(client)
    print_ticket_codes(client.ticket)
    print('This information will be needed to register your asistence to the match')
    print('\n ------ Your payment was successful! ------- \n \n'.center(150))
    print('---------Thank you for your purchase ---------\n'.center(150))
  else:
    print('Thank you for using our system \n Come back later!')

def get_fangs(num_str):
  '''
  Gets the 'fangs' for a vampire number to check if the number is vampire

  Params
  ---------
  num_str: str
    number to check in string

  Returns
  ---------
  True if the fangs follow the conditions
  False if not
  '''
  num_iter = it.permutations(num_str, len(num_str))
  for num_list in num_iter:
        v = ''.join(num_list)
        x, y = v[:int(len(v)/2)], v[int(len(v)/2):]
        if x[-1] == '0' and y[-1] == '0':
            continue
        if int(x) * int(y) == int(num_str):
            return True
  return False

def is_vampire(m_int):
  '''
  Determines whether a integer is a vampire number

  Params
  --------
  m_int: int
    integer to check

  Returns
  ---------
  True if vampire
  False if not
  '''
  n_str = str(m_int)
  if len(n_str) % 2 == 1:
    return False
  fangs = get_fangs(n_str)
  if not fangs:
    return False
  return True

def get_discount(client_id,total):
  '''
  Calculates the discount for the purchase total

  Params
  --------
  client_id: int
    ID for the client who makes the purchase
  total: int
    total price of tickets

  Return
  --------
  discount: int
    value of discount
  '''
  if is_vampire(client_id):
    discount=total*.5
  else:
    discount=0
  return discount


def get_tax(total):
  '''
  Calculates the tax for the purchase total

  Params
  --------
  total: int
    total price of tickets

  Return
  --------
  tax: int
    value of 16% of the total
  '''
  tax=total*.16
  return tax

def get_total(kind, client_id, ticket_price, quantity):
  '''
  Calculates the complete total for the purchase

  Params
  --------
  kind: str
    type of ticket bought
  client_id: int
    ID for the client who makes the purchase
  ticket_price: int
    price for the type of ticket bought
  quantity: int
    amount of tickets bought

  Return
  --------
  ticket_price: int
    total from the purchase
  discount: int
    value of discount
  tax: int
    value for tax
  '''
  ticket_price=ticket_price*quantity
  discount= get_discount(client_id, ticket_price)
  ticket_price-=discount
  tax=get_tax(ticket_price)
  ticket_price+=tax
  return ticket_price, discount, tax




def add_ticket(match_num:Match, ticket:list, seats, kind,available_matches):
  '''
  Adds the ticket information once the purchase has been confirmed

  Params
  --------
  match_num: Match
    object match chosen
  ticket: list
    list of tickets
  seats: list
    list of seats bought
  kind: str
    type of tickets bought
  available_matches: 

  Return
  --------
  discount: int
    value of discount
  '''
  chosen_match=validate_match_available(match_num, available_matches)
  for x in range(len(ticket)):
    if kind=='VIP':
      occupy_seat(chosen_match, 1, seats[x][1])
    else:
      occupy_seat(chosen_match, 0, seats[x][1])
    chosen_match.tickets_sold.append(ticket[x])
    chosen_match.tickets_left-=1



  
