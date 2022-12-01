from class_match import Match
from class_stadium import Stadium, Restaurants
from class_team import Team
from class_products import Food, Beverage
from search_codes import search_stadium_by_id
import requests

def get_from_api(url):
  '''
      Imports and transforms information from API

    Takes the given url and using the module requests gets the data from the link
    and decodes the json found data from it into python structures

    Params
    ---------
    url: str
      from where the data is taken

    Return
    ---------
    found_data: list
      decoded data found
  '''
  response= requests.get(url)
  found_data=response.json()
  print(type(found_data))
  return found_data

def get_teams():
  ''' 
    Transforms data in Team type objects

    Takes the decoded data from the API and turns it into a unique object,
    creating a list of Team objects

    Returns 
    ---------
    teams: list(Team)
     List of all instances of Team 
  '''
  teams=[]
  list_of_teams = get_from_api('https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/teams.json')
  for team in list_of_teams:
    teams.append(Team(team['name'], team['fifa_code'], team['group']))
  return teams
    
def get_restaurant_inventory(product_list):
  '''
    Transforms the restaurant available products into a dictionary

    Takes the information given from the API for each restaurant and it turns it into
    a list of dictionaries with each product name and stock, to be used in the purchase module

    Params
    --------
      product_list: list(Dict)
        List of available products given by the API
    
    Returns 
    --------
      inventory: list
        Available products in the restaurant with name and stock
  '''
  inventory=[]
  for product in product_list:
    new_product={}
    new_product['name']=product['name']
    new_product['stock']= product['quantity']
    inventory.append(new_product)
  return inventory

def get_restaurants():
  ''' 
    Transforms data in Restaurant type objects

    Takes the decoded data from the API and turns it into a unique object,
    creating a list of Restaurant objects

    Returns 
    ---------
    restaurants: list(Restaurant)
     List of all instances of Restaurant 
  '''
  restaurants=[]
  list_of_stadiums=get_from_api('https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/stadiums.json')
  for stadium in list_of_stadiums:
    stadium_id=stadium['id']
    for restaurant in stadium['restaurants']:
      restaurants.append(Restaurants(stadium_id, restaurant['name'], get_restaurant_inventory(restaurant['products'])))
  return restaurants

def get_stadiums():
  ''' 
    Transforms data in Stadium type objects

    Takes the decoded data from the API and turns it into a unique object,
    creating a list of Stadium objects

    Returns 
    ---------
    stadiums: list(Stadium)
     List of all instances of Stadium 
  '''
  stadiums=[]
  list_of_stadiums= get_from_api('https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/stadiums.json')
  for stadium in list_of_stadiums:
    stadiums.append(Stadium(stadium['id'], stadium['name'], stadium['capacity'], stadium['location']))
  return stadiums

def check_product_exists(prod_name, products):
  '''
    Checks if the product exists in the list of products

  To create a list of object Products with all available products across all restaurant,
  the function checks if the product has already been added to tha list

  Params
  --------
    prod_name: str
      Name of the product to check
    products: list(Product)
      List of already added products

  Returns
  --------
    True if the product is found on the list
  '''
  for product in products:
    if prod_name==product.name:
      return True

def get_product_price(price):
  '''
    Calculates the product's price with the 16% Tax

    Params
    -------
     price: int
      Product price

    Returns 
    --------
    price+tax : int
      Sum of the base price and the calculated tax
  '''
  tax=price*.16
  return price+tax

def define_beverage_type(alcohol):
  '''
    Turns the attribute alcohol into a boolean

    From the information, given in the API it casts the string information into boolean

    Params
    --------
    alcohol: str 
      Information from the API

    Returns
    --------
    True if the beverage is alcoholic
    False if the beverage is non-alcoholic
  '''
  if alcohol=='alcoholic':
    return True
  elif alcohol=='non-alcoholic':
    return False

def get_products():
  products=[]
  list_of_stadiums=get_from_api('https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/stadiums.json')
  for stadium in list_of_stadiums:
    for restaurant in stadium['restaurants']:
      for product in restaurant['products']:
        exists=check_product_exists(product['name'].title(), products)
        if exists:
          continue
        else:
          if product['type']=='food':
            products.append(Food(product['name'].title(), get_product_price(product['price']), product['adicional'].capitalize()))
          elif product['type']=='beverages':
            products.append(Beverage(product['name'].title(), get_product_price(product['price']), define_beverage_type(product['adicional'])))
  return products


def create_row(index):
  rows=['A','B','C','D','E','F', 'G', 'H', 'I', 'J', 'K', 'L']
  row=[]
  seat_num=1
  while len(row)<10:
    row.append('{}{}'.format(rows[index-1],seat_num))
    seat_num+=1
  return row

def seats_for_match(stadium):
  capacity=stadium.capacity
  general=[]
  index=0
  for row in range(1,capacity[0]+1,10 ):
    index+=1
    general.append(create_row(index))
  vip=[]
  for row in range(1,capacity[1]+1,10 ):
    index+=1
    vip.append(create_row(index))
  seats=[general,vip]
  return seats
  
def get_capacity(stadium):
  tickets_left=stadium.capacity[0]+stadium.capacity[1]
  return tickets_left

def get_matches(data_base):
  ''' 
    Transforms data in Match type objects

    Takes the decoded data from the API and turns it into a unique object,
    creating a list of Match objects. It takes the defined data base to obtain the
    seats available for the match, using other functions.

    Params
    ---------
    data_base: dict
      Dictionary with all team and stadium objects

    Returns 
    ---------
    matches: list(Match)
     List of all instances of Match 
  '''
  matches=[]
  list_of_matches= get_from_api('https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/matches.json')
  for match in list_of_matches:
    matches.append(Match(int(match['id']), match['home_team'], match['away_team'], match['date'], match['stadium_id'], seats_for_match(search_stadium_by_id(data_base, match['stadium_id'])),get_capacity(search_stadium_by_id(data_base, match['stadium_id']))))
  return matches

def get_available_matches(list_of_matches):
  matches=[]
  for match in list_of_matches:
    if match.tickets_left>0:
      matches.append(match)
  return matches








