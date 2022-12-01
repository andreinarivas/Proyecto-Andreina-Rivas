from class_client_ticket import Client, Ticket
from class_match import Match
from validation_codes import validate_boolean

def check_code(code):
  ''' 
  Checks if the code input follows the format for ticket codes

  Params
  --------
  code: str
    code to check

  Return
  -------
  False or True, if code follows the format
  match_id: str
    match id for chosen
  '''
  code_parts=[ x for x in code]
  local_team=''.join(code_parts[0:3])
  visit_team=''.join(code_parts[5:8])
  match_id=''.join(code_parts[8:10])
  if match_id[0]=='0':
    match_id=match_id[1]
  seat=''.join(code_parts[10:12])
  while not len(code_parts)==12 or not local_team.isalpha() or not visit_team.isalpha() or not match_id.isnumeric() or not seat[0].isalpha() or not seat[1].isnumeric():
    return False, match_id
  return True, match_id
  


def check_ticket_match(match_id, data_base):
  '''
  Checks if the code from the code exists 

  Params
  --------
  match_id: str
    match id for chosen
  data_base: dict
    Data base for all the systems information

  Return
  -------- 
  ticket_match: Match
    match object for ticket code given
  '''
  matches_list= data_base['matches']
  exists=False
  for matches in matches_list:
    if int(match_id)==matches.id:
      exists=True
      ticket_match=matches
  if exists:
    return ticket_match
  else:
    print('Ticket is invalid')
    
def check_ticket_exists(code, match_id, data_base):
  ''' 
  Checks if the code input given exists in the data base and if it has been registered before

  Params
  ---------
  code: str
    input given 
  match_id: str
    match id for the ticket match
  data_base: dict
    Data base information for all the program

  '''
  ticket_match=check_ticket_match(match_id, data_base)
  exists=False
  registered=False
  for ticket in ticket_match.tickets_sold:
    if code==ticket:
      exists=True
  for ticket in ticket_match.assistence:
    if code==ticket:
      registered=True
  if exists and registered==False: 
    ticket_match.print_info(data_base)
    add=validate_boolean('Do you wish to confirm the register?')
    if add:
      ticket_match.assistence.append(code)
  elif exists==False:
    print('Ticket doesnt exist')
  elif registered:
    print('Ticket has already been registered')

  

def validate_ticket_code(data_base):
  ''' 
  Takes and validates input from user

  Params
  --------
  data_base: dict
    Data base with all the program information
  
  '''
  match_id=''
  code_input=input('Please enter the ticket code: \n >>> ')
  is_valid, match_id=check_code(code_input)
  while is_valid==False:
    code_input=input('INVALID INPUT \n Please check the codes spelling \n \n \n Please enter the ticket code \n >>> ')
    is_valid, match_id=check_code(code_input)
  check_ticket_exists(code_input, match_id, data_base)



