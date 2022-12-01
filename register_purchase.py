from class_client_ticket import Client
from class_stadium import Stadium, Restaurants
from class_match import Match
from class_products import Food, Beverage
from get_from_api import check_product_exists
from validation_codes import validate_input_num, validate_options, validate_input_str, validate_boolean
from search_codes import search_stadium_by_id, search_restaurants, search_match

def find_client(list_of_clients, client_id):
  ''' 
  Finds the client by the id given

  Params
  --------
  list_of_clients: list
    list of available clients
  client_id: int
    id input by user
  
  Return
  --------
  client: Client
    client who matches the id given
  '''
  for client in list_of_clients:
    if client.client_id == client_id:
      return client

def register_client(data_base):
  ''' 
  Validates the input from the user to continue the process
  
  Checks if the input is valid and the client is VIP

  Params
  --------
  data_base: dict
    Data base with all the program's information
  
  Return 
  --------
  client_obj: Client
    Client corresponding to the input given

  '''
  client_id=validate_input_num('the clients identification')
  list_of_clients=data_base.get('client')
  client_obj=find_client(list_of_clients, client_id)
  while client_obj==None:
    print('INVALID INPUT \n CLIENT NOT FOUND \n')
    client_id=validate_input_num('the clients identification')
    client_obj=find_client(list_of_clients, client_id)
  while client_obj.kind!='VIP':
    print('INVALID INPUT \n NOT A VIP CLIENT \n')
    client_id=validate_input_num('the clients identification')
    client_obj=find_client(list_of_clients, client_id)
  return client_obj
  
def show_available_restaurants(data_base, stadium):
  '''
  Prints the restaurants available based on the stadium chosen

  Params
  --------
  data_base: dict
    Data base with all the program's information
  stadium: Stadium
    stadium chosen by user

  '''
  restaurants_available=search_restaurants(data_base, stadium)
  for restaurant in restaurants_available:
    print('RESTAURANT #{} '.format(restaurants_available.index(restaurant)+1))
    print(restaurant.name)

def check_if_legal(client):
  '''
  Checks the client's age to confirm if legal

  Params
  --------
  client: Client
    Client object found by id
  
  Return
  --------
  True, False, according if client age is above 18
  '''
  if client.age>=18:
    return True
  else:
    return False

def print_product_info(available_products, product_name, restaurant):
  '''
  Prints the information for the available products in the restaurants

  Params
  -------
  available_products: list
    list of Products available at all restaurants
  product_name:
    name for the product available in the restaurant
  restaurant: Restaurant
    chosen restaurant

  '''
  for product in available_products:
    if check_product_stock(restaurant, product_name)>0:
      if product.name==product_name:
        print('*** {}'.format(product.name))
        print('**** ${}'.format(product.price))
    else:
        print('*** {}'.format(product.name))
        print('**** OUT OF STOCK')

def check_product_stock(restaurant, product_name):
  ''' 
  Gets the product's wanted stock
  
  Params
  -------
  restaurant: Restaurant
    restaurant chosen
  product_name: str
    product name wanted
  
  Return
  -------
  product['stock']: int
    stock available for the stock

  '''
  for product in restaurant.products:
    if product['name']==product_name:
      return product['stock']

def check_if_product_bought(product_wanted, products_bought):
  ''' 
  Checks if the product was previously bought

  Params
  --------
  product_wanted: str
    name of the product wanted
  products_bought: list
    list of products previously bought
  

  Return
  -------
  True if product found in list of products
  '''
  for product in products_bought:
    if product_wanted==product[0]:
      return True

def get_product_wanted(available_products, legal,restaurant, products_bought):
  ''' 
  Creates a register of all wanted products

  Params
  --------
  available_products: list
    All available products
  legal: bool
    The client is legal or not
  restaurant: Restaurant
    restaurant chosen
  products_bought: list
    products in the client's order

  Return
  --------
  tuple
    name of product wanted, total price, quantity of product wanted
  '''
  product_wanted=validate_input_str('the name of product wanted').capitalize()
  while check_if_product_bought(product_wanted, products_bought):
    product_wanted=validate_input_str('a different product, not chosen before').capitalize()
  while not check_product_exists(product_wanted, available_products):
    product_wanted=validate_input_str('a valid product').capitalize()
  for product in available_products:
    if product.name==product_wanted:
      if isinstance(product, Beverage) and product.alcohol and not legal:
        print('This product is unavailable for under 18 clients')
      elif check_product_stock(restaurant, product_wanted)==0:
        print('This product is unavaible \n')
      else:
        quantity=validate_input_num('the amount wanted')
        while not quantity<=check_product_stock(restaurant, product_wanted):
          print('Quantity unavailable \n Available: {}'.format(check_product_stock(restaurant, product_wanted)))
          quantity=validate_input_num('a valid amount wanted')
        return (product.name, product.price*quantity, quantity)

def get_total(products_bought):
  '''
  Calculates the total for all the products bought 

  Params
  ------
  products_bought: list
    all products bought by the client

  Return
  -------
  total: int
    total amount to pay for purchase
  '''
  total=0
  for product in products_bought:
    total+=product[1]
  return total

def is_perfect(client_id):
  '''
  Checks if the client's id is a perfect number

  Params
  --------
  client_id: int
    number to be checked
  
  Return
  --------
  bool
    if the number is perfect
  '''
  n_sums=0
  for x in range(1, client_id):
    if client_id%x==0:
      n_sums+=x

  if n_sums==client_id:
    return True
  else: 
    return False

def get_discount(total, client_id):
  ''' 
  Calculates the discount given to the total price

  Params
  --------
  total: int
    total price 
  client_id: int
    number to check if its perfect

  Return
  ---------
  discount: int
    value to be decreased from total
  '''
  if is_perfect:
    discount=total*.15
  else:
    discount=0
  return discount

def print_receipt(products_bought, client_id):
  ''' 
  Prints the receipt for the order 

  Params
  --------
  products_bought: list
    products bought by the client
  client_id: int
    client's identification number

  Return
  --------
  full_total: int
    total of the purchase including discount
  '''
  print('---------- RECEIPT ----------')
  for product in products_bought:
    print('{} -------- ${}'.format(product[0], product[1]))
  gross_total=get_total(products_bought)
  discount=get_discount(gross_total, client_id)
  full_total=gross_total-discount
  print('SUBTOTAL: {:.2f}'.format(gross_total))
  print('DISCOUNT: {:.2f}'.format(discount))
  print('TOTAL: {:.2f}'.format(full_total))
  return full_total

def update_stock(restaurant_wanted, products_bought):
  '''
  Modifies the products stock when bought

  Params
  --------
  restaurant_wanted: Restaurant
    restaurant chosen
  products_bought: list
    list of products bought by client

  '''
  for product_bought in products_bought:
    for product in restaurant_wanted.products:
      for name in product.keys():
        if name == product_bought[0]:
          product['stock']-=product_bought[2]
          
def get_client_matches(tickets):
  ''' 
  Gets the matches id the client has bought tickets for

  Params
  --------
  tickets: list
    list of tickets the client has bought
  
  Return 
  --------
  matches: list
    list of matches id the client can attend 

  '''
  matches=[]
  for ticket in tickets:
    match_id=ticket[8:10]
    if not match_id in matches:
      matches.append(match_id)
  return matches

def select_match_present(matches, data_base):
  ''' 
  Gets the match the client is attending 

  Params
  -------
  matches: list 
    matches id the client could be attending
  data_base: dict
    Data base for all the programs information

  Return
  --------
  match_present: int
    match id for match selected

  '''
  for match in matches:
    print('**{}. {} VS {}'.format(match, search_match(data_base, int(match)).local_team, search_match(data_base, int(match)).visit_team))
  match_present=validate_options('match attending', '', matches)
  return match_present


def register_client_purchase(data_base,available_products):
  '''
  Registers the purchase a client makes in the restaurant

  Params
  ---------
  data_base: dict
     Data base for all the program's information
  available_products: list
    all available products in the program

   '''
  new_purchase={}
  client_obj=register_client(data_base)
  legal=check_if_legal(client_obj)
  client_matches=get_client_matches(client_obj.ticket)
  match_present=select_match_present(client_matches, data_base)
  client_match=search_match(data_base, int(match_present)).stadium
  stadium_client=search_stadium_by_id(data_base, int(client_match))
  show_available_restaurants(data_base, stadium_client)
  available_restaurants=search_restaurants(data_base, stadium_client)
  restaurant_wanted=available_restaurants[validate_options('the number of restaurant wanted', '', str(range(1, len(available_restaurants))))-1]
  for product in restaurant_wanted.products:
    print_product_info(available_products, product['name'],restaurant_wanted)
  add=True
  products_bought=[]
  while add:
    products_bought.append(get_product_wanted(available_products, legal, restaurant_wanted, products_bought))
    add=validate_boolean('Would you like to buy more products?')
  total=print_receipt(products_bought, client_obj.client_id)
  complete=validate_boolean('Would you like to complete the order?')
  if complete:
    new_purchase[client_obj.client_id]=total
    restaurant_wanted.sales.append(new_purchase)
    client_obj.add_expenses(total)
    update_stock(restaurant_wanted, products_bought)
  
  

  
    

  
    





