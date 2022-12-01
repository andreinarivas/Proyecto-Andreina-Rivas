from class_products import Food, Beverage
from validation_codes import validate_input_str, validate_options, validate_input_num

def validate_product_exists(wanted_product, product_list):
  ''' 
  Checks if the product exists in the list given

  Params
  ---------
  wanted_product: str
    product name wanted
  product_list: list
    list of available products 
  
  Return
  ---------
  True if found
  '''
  exists=False
  while exists==False:
    for product in product_list:
      if wanted_product==product.name:
        return True
    print('INVALID INPUT\n ')
    wanted_product=validate_input_str('a valid product name').capitalize()
    

def search_by_name(product_list):
  ''' 
  Finds products based on the name given

  Params
  --------
  product_list: list
    list of all available products
  '''
  wanted_product=validate_input_str('the products name').capitalize()
  if validate_product_exists(wanted_product, product_list):
    for product in product_list:
      if wanted_product==product.name:
        print('\n')
        product.print_information()



def search_by_type(product_list):
  ''' 
  Finds products based on the type given

  Params
  --------
  product_list: list
    list of all available products
  '''
  wanted_product=validate_options('the products type', '1. Food \n 2. Beverages', ['1','2'])
  if wanted_product==1:
    kind=Food 
  else:
    kind=Beverage
  for product in product_list:
    if isinstance(product, kind):
      print('\n')
      product.print_information()
   
      
def search_by_price_range(product_list):
  ''' 
  Finds products based on the price range given

  Params
  --------
  product_list: list
    list of all available products
  '''
  minimum=validate_input_num('the minimum price wanted')
  maximum=validate_input_num('the maximum price wanted')
  for product in product_list:
    if product.price>=minimum and product.price<=maximum:
      print('\n')
      product.print_information()
