from search_codes import search_stadium_by_id, search_team

def validate_country(data_base):
  ''' 
  Checks if the country given is a valid option to search

  Params
  ---------
  data_base: dict
    Data base for all program's information
  
  Return
  ---------
  team: Team
    team that matches the country given
  '''
  is_valid=False
  teams=data_base.get('team')
  while is_valid==False:
    wanted=input('\nPlease enter the name of the country: \n >>> ').capitalize()
    for team in teams:
        if wanted==team.country:
          is_valid=True
          return team
    print('INVALID INPUT \n')
    
def search_by_country(data_base):
  ''' 
  Finds matches based on the team country

  Params
  --------
  data_base: dict
    Data base for all program's information
  '''
  count=0
  matches=data_base.get('matches')
  wanted= validate_country(data_base)
  print('--------------- {} MATCHES ---------------'.format(wanted.country).center(150))
  for match in matches:
    if match.local_team==wanted.country or match.visit_team==wanted.country:
      print('\n')
      match.print_info(data_base)

def validate_stadium(data_base):
  ''' 
  Checks if the stadium given is a valid option to search

  Params
  ---------
  data_base: dict
    Data base for all program's information
  
  Return
  ---------
  stadium: Stadium
    stadium that matches the name given
  '''
  stadiums=data_base.get('stadium')
  is_valid=False
  while is_valid==False:
    wanted=input('\nPlease enter a valid stadium name: \n >>>').title()
    for stadium in stadiums:
        if wanted==stadium.name:
          is_valid=True
          return stadium
  
def search_by_stadium(data_base):
  ''' 
  Finds matches based on the stadium name

  Params
  --------
  data_base: dict
    Data base for all program's information
  '''
  count=0
  matches=data_base.get('matches')
  wanted=validate_stadium(data_base)
  print('--------------- {} MATCHES --------------- \n ------ {} ------'.format(wanted.name, wanted.location).center(150))
  for match in matches:
    if match.stadium==wanted.id:
      print('\n')
      match.print_info(data_base)


def validate_date(data_base, matches):
  ''' 
  Checks if the date given is a valid option to search

  Params
  ---------
  data_base: dict
    Data base for all program's information
  
  Return
  ---------
  wanted: str
    date wanted to find matches for 
  '''
  is_valid=False
  while is_valid==False:
    wanted=input('\nPlease enter a valid date: \n Follow format: MM/DD/YYYY \n >>> ').capitalize()
    for match in matches:
        date_time=match.date.split()
        if wanted==date_time[0]:
          is_valid=True
          return wanted
    print('INVALID INPUT')
    

def search_by_date(data_base):
  ''' 
  Finds matches based on the date given

  Params
  --------
  data_base: dict
    Data base for all program's information
  '''
  count=0
  matches=data_base.get('matches')
  wanted=validate_date(data_base, matches)
  print('--------------- {} MATCHES ---------------'.format(wanted).center(150))
  for match in matches:
    date_time=match.date.split()
    if date_time[0]==wanted:
      print('\n')
      match.print_info(data_base)





  
