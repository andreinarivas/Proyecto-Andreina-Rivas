def search_team(data_base, wanted):
  '''
  Gets an object team by the team's country

  Params
  --------
  data_base: dict
    Data base with all the program's information
  wanted: str
    country wanted

  Return
  --------
  team: Team
    object team corresponding to the country given
   '''
  team_list= data_base.get('team')
  for team in team_list:
    if team.country==wanted:
      return team

def search_team_code(data_base, wanted):
  '''
  Gets an object team by the team's code

  Params
  --------
  data_base: dict
    Data base with all the program's information
  wanted: str
    code wanted

  Return
  --------
  team: Team
    object team corresponding to the code given
   '''
  team_list= data_base.get('team')
  for team in team_list:
    if team.fifa_code==wanted:
      return team

def search_match(data_base, wanted):
  '''
  Gets an object match by the match's id

  Params
  --------
  data_base: dict
    Data base with all the program's information
  wanted: str
    match_id wanted

  Return
  --------
  match: Match
    object match corresponding to the id given
   '''
  match_list=data_base.get('matches')
  for match in match_list:
    if match.id==wanted:
      return match

def search_stadium_by_id(data_base, wanted):
  '''
  Gets an object stadium by the stadium's id

  Params
  --------
  data_base: dict
    Data base with all the program's information
  wanted: str
    stadium id wanted

  Return
  --------
  stadium: Stadium
    object stadium corresponding to the id given
   '''
  stadium_list= data_base.get('stadium')
  for stadium in stadium_list:
    if stadium.id==wanted:
      return stadium
      
def search_restaurants(data_base, stadium):
  '''
  Gets an object restaurant by the restaurant's stadium id

  Params
  --------
  data_base: dict
    Data base with all the program's information
  stadium: Stadium
    stadium wanted

  Return
  --------
  restaurants: list
    list of restaurants in a stadium
   '''
  restaurants=[]
  restaurant_list=data_base.get('restaurant')
  for restaurant in restaurant_list:
    if restaurant.stadium_id==stadium.id:
      restaurants.append(restaurant)
  return restaurants

def search_client(data_base,client_id):
  '''
  Gets an object client by the client's

  Params
  --------
  data_base: dict
    Data base with all the program's information
  client_id: int
    client id wanted to find

  Return
  --------
  client: Client
    object client corresponding to the id given
   '''
  list_clients=data_base.get('client')
  for client in list_clients:
    if client.client_id==client_id:
      return client