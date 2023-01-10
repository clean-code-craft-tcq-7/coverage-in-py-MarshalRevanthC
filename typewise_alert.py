
from sender import *
from breach_detecter import *
from breach_classifier import *

def check_and_alert(alertTarget, batteryChar, temperatureInC):
  alert = None
  breachType =\
    classify_temperature_breach(batteryChar['coolingType'], temperatureInC)
  if alertTarget == 'TO_CONTROLLER':
    alert = send_to_controller(breachType)
  elif alertTarget == 'TO_EMAIL':
    alert = send_to_email(breachType)
  return alert
