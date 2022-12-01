from class_match import Match
from class_stadium import Stadium, Restaurants
from class_team import Team
from class_products import Food, Beverage
from class_client_ticket import Client, Ticket
from validation_codes import validate_options, validate_boolean
from get_from_api import get_teams, get_stadiums, get_matches, get_available_matches, get_restaurants, get_products
from search_matches import search_by_country, search_by_stadium, search_by_date
from get_tickets import show_available_matches, register_purchase
from register_assistence import validate_ticket_code
from search_products import search_by_name, search_by_type, search_by_price_range
from register_purchase import register_client_purchase
from get_statistics import get_VIP_expense_average, top_client, top_products, get_most_assisted_match, get_most_sold_match, get_assistence_table
import json
from datetime import datetime

def validate_date(date_text):
  '''
  Validates inputs are date form

  It uses the datetime module to specify which format the dates have to follow for the data log
  Based on try, except to raise a Value error

  Params
  ----------
  date_text: str
    Input from user

  Return
  ---------
  bool: bool
    Indicates if the input is valid or not
  '''
  try:
    if date_text != datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
      raise ValueError
    return True
  except ValueError:
      return False

def main_menu():
  '''
  Prints the main screen of program

  It gives the user the options of available modules to use in the program

  Return
  ---------
  module_select: int
    Module the user wants to use

  '''
  print(' ---------  WELCOME TO QUATAR 2022 ⚽ --------- \n \n \n'.center(150))
  print('**** MAIN MENU **** \n \n '.center(150))
  module_select= validate_options('a module to operate', '1. Search Matches \n 2. Ticket Purchase \n 3. Register Assistence to Match \n 4. Search Restaurant Products \n 5. Register Restaurant Purchase \n 6. See Statistic Data \n 7. Save and Quit Data', [str(x) for x in range(1,8)])
  return module_select

def menu_search_match():
  '''
  Prints the menu for search module

  It gives the user the options of available search modes to use in the program

  Return
  ---------
  option_select: int
    Search mode the user wants to use
    
  '''
  print(' ---------  SEARCH MATCHES --------- \n \n \n'.center(150))
  print('**** SEARCH OPTIONS **** \n \n '.center(150))
  option_select= validate_options('search mode', '1. Match by country \n 2. Match by stadium \n 3. Match by date', ['1','2','3'])
  return option_select

def menu_search_product():
  '''
  Prints the menu for search module

  It gives the user the options of available search modes to use in the program

  Return
  ---------
  option_select: int
    Search mode the user wants to use
    
  '''
  print(' ---------  SEARCH PRODUCTS --------- \n \n \n'.center(150))
  print('**** SEARCH OPTIONS **** \n \n '.center(150))
  option_select= validate_options('search mode', '1. Product by Name \n 2. Product by Type \n 3. Product by Price Range', ['1','2','3'])
  return option_select


def main():
  data_base = {'team':get_teams(),'stadium': get_stadiums(), 'matches':[],'restaurant': get_restaurants(),'client':[]}
  data_base['matches']=get_matches(data_base)
  available_products=get_products()
  available_matches=get_available_matches(data_base['matches'])
  run=True
  while run:
    module_selected=main_menu()
    if module_selected==1:
      option_select=menu_search_match()
      if option_select==1:
        search_by_country(data_base)
      if option_select==2:
        search_by_stadium(data_base)
      if option_select==3:
        search_by_date(data_base)
    if module_selected==2:
      print(' ---------  PURCHASE TICKETS --------- \n \n \n'.center(150))
      register_purchase(data_base, available_matches)
    if module_selected==3:
      validate_ticket_code(data_base)
    if module_selected==4:
      search_mode_selected=menu_search_product()
      if search_mode_selected==1:
        search_by_name(available_products)
      if search_mode_selected==2:
        search_by_type(available_products)
      if search_mode_selected==3:
        search_by_price_range(available_products)
    if module_selected==5:
      print(' ---------  RESTAURANT PURCHASE --------- \n \n \n'.center(150))
      register_client_purchase(data_base, available_products)
    if module_selected==6:
      print('\n\n')
      print('--------------- AVERAGE SPENDING ---------------\n'.center(150))
      get_VIP_expense_average(data_base)
      print('\n\n')
      top_client(data_base)
      print('\n\n')
      print('-------------- TOP PRODUCTS SOLD BY RESTAURANT --------------'.center(150))
      top_products(data_base)
      print('\n\n')
      print('----------------- MACTH INFORMATION TABLE -----------------'.center(150))
      print(get_assistence_table(data_base))
      print('\n \n ')
    if module_selected==7:
      print('-------------- THANK YOU FOR USING THE SYSTEM -------------- \n \n'.center(150))
      run=False
   
  date=input('Please enter the date for the log information: \n Enter in YYYY-MM-DD format \n >>> ')
  while validate_date(date)==False:
    date=input('INVALID INPUT \n Please enter a valid date: \n Do so in YYYY-MM-DD format \n >>> ')
  with open('data_log.txt', 'a') as file:
    file.write('\n \n')
    file.write('****** SYSTEM INFORMATION {}******\n'.format(date))
    file.write('--------- CLIENT INFORMATION -----------\n')
    for objects in data_base['client']:
      file.write(json.dumps(objects.__dict__))
      file.write('\n')
    file.write('--------- RESTAURANTS INFORMATION -----------\n')
    for objects in data_base['restaurant']:
      file.write(json.dumps(objects.__dict__))
      file.write('\n')
    file.write('--------- MATCHES INFORMATION -----------\n')
    file.write(get_assistence_table(data_base))
    file.close()

  
  
    



  

  
  

  

  





main()