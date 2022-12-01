from tabulate import tabulate
import operator
from search_codes import search_stadium_by_id

def get_VIP_expense_average(data_base):
  '''
    Calculates an average of expenses by VIP average 

  Searches the data base of clients to sum all the VIP client expenses and count the number of clients, 
  then it calculates it calculates the average

  Params
  --------
    data base: dict
      Data base of all the program's information

  Returns
  --------
    Prints the result
  '''
  list_clients=data_base.get('client')
  if len(list_clients)!=0:
    total_expenses=0
    total_vip_clients=0
    for client in list_clients:
      if client.kind=='VIP':
        total_expenses+=client.expenses
        total_vip_clients+=1
    average=total_expenses/total_vip_clients
    print('On average, VIP Clients spend ${}'.format(average))
  else:
    print('No Clients Registered')
  


def get_most_assisted_match(data_base):
  '''
    Gets the most assisted match

  Searches all matches in the data base to get the most assisted one based
  on the length of the list of tickets registered as assistant

  Params
  --------
    data base: dict
      Data base of all the program's information
  Returns
  --------
    most_assisted_match: Match
      Match object with the most tickets registered as assistant
    '''
  list_matches=data_base.get('matches')
  most_assistence=0
  for match in matches:
    if len(match.assistence)>most_assistence:
      most_assistence=len(match.assistence)
      most_assisted_match=match

  return most_assisted_match

def get_most_sold_match(data_base):
  '''
    Gets the most sold match

  Searches all matches in the data base to get the most sold one based
  on the length of the list of tickets sold

  Params
  --------
    data base: dict
      Data base of all the program's information
  Returns
  --------
    most_sold_match: Match
      Match object with the most tickets sold
    '''
  list_matches=data_base.get('matches')
  most_sold=0
  for match in matches:
    if len(match.tickets_sold)>most_sold:
      most_sold=len(match.tickets_sold)
      most_sold_match=match

  return most_sold_match

def organize_clients(data_base):
  '''
    Sorts list of clients by number of tickets bought

  Searches all clients in the data base and sorts them based on the lenght of the list
  of tickets bought registered to the client, from most to least

  Params
  --------
    data base: dict
      Data base of all the program's information
  Returns
  --------
    list_clients: list
      sorted list
    '''
  list_clients=data_base.get('client')
  list_clients.sort(key=lambda x:len(x.ticket), reverse=True)
  return list_clients

def top_client(data_base):
  '''
    Prints top 3 clients by tickets bought

  Takes a sorted list of clients and it prints the first three elements
  with their name, id, and amount of tickets bought

  Params
  --------
    data base: dict
      Data base of all the program's information
  Returns
  --------
    void()
    Prints the info
    '''
  sorted_clients=organize_clients(data_base)
  print('----------- TOP 3 CLIENTS BY TICKETS BOUGHT -----------'.center(150))
  for x in range(len(sorted_clients[0:3])):
    print ('***** {} --- {}\n***** TICKETS BOUGHT: {}'.format(sorted_clients[x].name, sorted_clients[x].client_id, len(sorted_clients[x].ticket)))


def organize_products(list_products):
  '''
    Sorts list of products by its stock

  Searches all products in list and sorts them by their available stock from
  least to most, as the least available product will be the better sold one

  Params
  --------
    data base: dict
      Data base of all the program's information
  Returns
  --------
    list_products: list
      sorted list
    '''
  list_products.sort(key=operator.itemgetter('stock'))
  return list_products

def top_products(data_base):
  '''
    Prints top 3 products by availability

  Takes a sorted list of products and it prints the first three elements
  by restaurant with their name

  Params
  --------
    data base: dict
      Data base of all the program's information
  Returns
  --------
    void()
    Prints the info
    '''
  list_restaurants=data_base.get('restaurant')
  for restaurant in list_restaurants:
    sorted_products=organize_products(restaurant.products)
    print(f'----------- TOP 3 PRODUCTS IN {restaurant.name} -----------'.center(150))
    for x in range(len(sorted_products[0:3])):
      print('*** {}'.format(sorted_products[x]['name']))

def organize_matches(data_base):
  '''
    Sorts list of matches by assistence

  Searches all matches in list and sorts them by the lenght of the list of tickets
  registered as assistent from best to worst

  Params
  --------
    data base: dict
      Data base of all the program's information
  Returns
  --------
    list_matches: list
      sorted list
    '''
  list_matches=data_base.get('matches')
  list_matches.sort(key=lambda x:len(x.assistence), reverse=True)
  return list_matches

def get_match_name(sorted_matches, table_dict_name):
  '''
    Creates list of match names 

  Creates the string of the match name based on the teams playing and
  and adds it to a list to create the table of match assitence

  Params
  --------
    table_dict_name: list
      List to add match names
    sorted_matches: list
      List of matches organized by assistence
  Returns
  --------
    void()
    '''
  for match in sorted_matches:
    match_name=f'{match.local_team} VS {match.visit_team}'
    table_dict_name.append(match_name)

def get_match_stadium(sorted_matches, table_dict_stadium, data_base):
  ''' 
  Creates list of match stadium names 

  Adds the stadium name searched by the id saved in the object
  to the list according to the tabulate

  Params
  --------
    table_dict_stadium: list
      List to add match stadiums
    sorted_matches: list
      List of matches organized by assistence
    data_base: dict
      Data base of all the program's information
  Returns
  --------
    void()
  '''
  for match in sorted_matches:
    stadium=search_stadium_by_id(data_base, match.stadium)
    table_dict_stadium.append(stadium.name)

def get_match_sold(sorted_matches, table_dict_assitence):
  ''' 
  Creates list of match tickets sold

  Adds the number of tickets sold to a list 

  Params
  --------
    table_dict_assistence: list
      List to add match tickets sold
    sorted_matches: list
      List of matches organized by assistence
  Returns
  --------
    void()
  '''
  for match in sorted_matches:
    tickets_sold=len(match.tickets_sold)
    table_dict_assitence.append(tickets_sold)

def get_match_assistence(sorted_matches, table_dict_assitence):
  ''' 
  Creates list of match assitence

  Adds the number of assistants to a list 

  Params
  --------
    table_dict_assistence: list
      List to add match tickets sold
    sorted_matches: list
      List of matches organized by assistence
  Returns
  --------
    void()
  '''
  for match in sorted_matches:
    assitence=len(match.assistence)
    table_dict_assitence.append(assitence)

def get_match_relation(sorted_matches, table_dict_assitence):
  ''' 
  Creates list of match percentage relation between tickets sold and assistence

  Adds the relation to a list 

  Params
  --------
    table_dict_assistence: list
      List to add match tickets sold
    sorted_matches: list
      List of matches organized by assistence
  Returns
  --------
    void()
  '''
  for match in sorted_matches:
    if len(match.tickets_sold)!=0:
      relation=(len(match.assistence)/len(match.tickets_sold))*100
      table_dict_assitence.append(relation)
    else:
      table_dict_assitence.append('N/A')

def get_assistence_table(data_base):
  ''' 
  Tabulates the most relevant information from each match

  Creates a dictionary with the information for the table and then uses tabulate
  to create the table

  Params
  --------
    data_base: dict
      Data base with all the programs information
  Returns
  --------
    tabulate(table_dict, headers='keys'): str
      Table with all the information found
  '''
  table_dict={'Match Name': [], 'Stadium':[], 'Tickets Sold':[], 'Assistence':[], 'Assitence %':[]}
  sorted_matches=organize_matches(data_base)
  get_match_name(sorted_matches, table_dict['Match Name'])
  get_match_stadium(sorted_matches, table_dict['Stadium'], data_base)
  get_match_sold(sorted_matches, table_dict['Tickets Sold'])
  get_match_assistence(sorted_matches, table_dict['Assistence'])
  get_match_relation(sorted_matches, table_dict['Assitence %'])
  return tabulate(table_dict, headers='keys')
  
