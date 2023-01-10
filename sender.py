from configuration import *
from printer import *

def send_to_controller(breachType):
  print_send_controller(header,breachType)
  return True

def send_to_email(breachType):  
  if breachType == 'TOO_LOW':
    print_send_email(recepient,'too low')
    return True
  elif breachType == 'TOO_HIGH':
    print_send_email(recepient,'too high')
    return True
  return False
