
def validate_input_num(required):
  '''
  Validates an input is numeric

  Params
  ---------
  required: str
    given question to ask

  Return
  --------
  int(number)
    input validated
   '''
  number=input('Please enter {}: \n >>> '.format(required))
  while not number.isnumeric():
    number=input('INVALID INPUT\n Remember to enter a number \n \n Please enter {}: \n >>> '.format(required))
  return int(number)

def validate_input_str(required):
  '''
  Validates an input is a string

  Params
  ---------
  required: str
    given question to ask

  Return
  --------
  string: str
    validated string 
   '''
  string=input('Please enter {}: \n >>> '.format(required))
  string=string.replace(' ','')
  while not string.isalpha():
    string=input('INVALID INPUT \n Remember to enter only letters \n \n Please enter {}: \n >>> '.format(required))
  return string

def validate_options(required, possible, options):
  '''
  Validates an input is withing given options

  Params
  ---------
  required: str
    given question to ask
  possible: str
    possible options to give 
  options: list
    list within the input must be

  Return
  --------
  int(option)
    input validated
   '''
  option=input('Please enter the option for {} you would like: \n {} \n >>> '.format(required, possible))
  while not option in options:
    option=input('INVALID OPTION. \n Please enter a valid option for {} you would like: \n {} \n >>> '.format(required, possible))
  return int(option)

def validate_boolean(question):
  '''
  Validates an input is boolean

  Params
  ---------
  question: str
    question to ask

  Return
  --------
  bool
    based on answer
   '''
  question=input('{} \n Yes (Y) or NO (N) \n >>> '.format(question)).capitalize()
  while question not in ['Y', 'N']:
    question=input('INVALID INPUT \n \n {} \n Yes (Y) or NO (N) \n >>> '.format(question)).capitalize()
  if question=='Y':
    return True
  else:
    return False