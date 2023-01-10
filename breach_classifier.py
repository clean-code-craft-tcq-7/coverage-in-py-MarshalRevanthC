from configuration import *
from breach_detecter import *
def classify_temperature_breach(coolingType, temperatureInC):
  lowerLimit = 0
  upperLimit = 0
  if coolingType in limits:
    lowerLimit = limits[coolingType]['lowerLimit']
    upperLimit = limits[coolingType]['upperLimit']
  return infer_breach(temperatureInC, lowerLimit, upperLimit)
