import unittest
from typewise_alert import *
from breach_classifier import *
from breach_detecter import *
from sender import *
class TypewiseTest(unittest.TestCase):
  def test_check_and_alert(self):
    batteryChar = {}

    batteryChar['coolingType'] = 'PASSIVE_COOLING'
    alertTarget = 'TO_CONTROLLER'
    temperatureInC = 50
    self.assertTrue(check_and_alert(alertTarget,batteryChar,temperatureInC) == True) 

    batteryChar['coolingType'] = 'PASSIVE_COOLING'
    alertTarget = 'TO_EMAIL'
    temperatureInC = 50
    self.assertTrue(check_and_alert(alertTarget,batteryChar,temperatureInC) == True) 

    batteryChar['coolingType'] = 'PASSIVE_COOLING'
    alertTarget = 'TO_EMAIL'
    temperatureInC = 25
    self.assertTrue(check_and_alert(alertTarget,batteryChar,temperatureInC) == False) 

    batteryChar['coolingType'] = 'HI_ACTIVE_COOLING'
    alertTarget = 'TO_CONTROLLER'
    temperatureInC = 0
    self.assertTrue(check_and_alert(alertTarget,batteryChar,temperatureInC) == True) 

    batteryChar['coolingType'] = 'HI_ACTIVE_COOLING'
    alertTarget = 'TO_EMAIL'
    temperatureInC = 45
    self.assertTrue(check_and_alert(alertTarget,batteryChar,temperatureInC) == False) 

    batteryChar['coolingType'] = 'HI_ACTIVE_COOLING'
    alertTarget = 'TO_EMAIL'
    temperatureInC = 50
    self.assertTrue(check_and_alert(alertTarget,batteryChar,temperatureInC) == True) 

    batteryChar['coolingType'] = 'MED_ACTIVE_COOLING'
    alertTarget = 'TO_CONTROLLER'
    temperatureInC = 0
    self.assertTrue(check_and_alert(alertTarget,batteryChar,temperatureInC) == True) 

    batteryChar['coolingType'] = 'MED_ACTIVE_COOLING'
    alertTarget = 'TO_EMAIL'
    temperatureInC = 45
    self.assertTrue(check_and_alert(alertTarget,batteryChar,temperatureInC) == True) 

    batteryChar['coolingType'] = 'MED_ACTIVE_COOLING'
    alertTarget = 'TO_EMAIL'
    temperatureInC = 20
    self.assertTrue(check_and_alert(alertTarget,batteryChar,temperatureInC) == False) 
    
    batteryChar['coolingType'] = 'HI_ACTIVE_COOLING'
    alertTarget = 'TO_SMS'
    temperatureInC = 50
    self.assertTrue(check_and_alert(alertTarget,batteryChar,temperatureInC) == None) 

  def test_infers_and_limits_as_per_cooling_type(self):
    self.assertTrue(classify_temperature_breach('PASSIVE_COOLING',100) == 'TOO_HIGH')
    self.assertTrue(classify_temperature_breach('PASSIVE_COOLING',36) == 'TOO_HIGH')
    self.assertTrue(classify_temperature_breach('PASSIVE_COOLING',35.1) == 'TOO_HIGH')
    self.assertTrue(classify_temperature_breach('PASSIVE_COOLING',35) == 'NORMAL') 
    self.assertTrue(classify_temperature_breach('PASSIVE_COOLING',25) == 'NORMAL') 
    self.assertTrue(classify_temperature_breach('PASSIVE_COOLING',0) == 'NORMAL') 
    self.assertTrue(classify_temperature_breach('PASSIVE_COOLING',-0.01) == 'TOO_LOW') 
    self.assertTrue(classify_temperature_breach('PASSIVE_COOLING',-1) == 'TOO_LOW') 
    self.assertTrue(classify_temperature_breach('PASSIVE_COOLING',-25) == 'TOO_LOW') 

    self.assertTrue(classify_temperature_breach('HI_ACTIVE_COOLING',100) == 'TOO_HIGH')
    self.assertTrue(classify_temperature_breach('HI_ACTIVE_COOLING',46) == 'TOO_HIGH')
    self.assertTrue(classify_temperature_breach('HI_ACTIVE_COOLING',45.1) == 'TOO_HIGH')
    self.assertTrue(classify_temperature_breach('HI_ACTIVE_COOLING',45) == 'NORMAL') 
    self.assertTrue(classify_temperature_breach('HI_ACTIVE_COOLING',25) == 'NORMAL') 
    self.assertTrue(classify_temperature_breach('HI_ACTIVE_COOLING',0) == 'NORMAL') 
    self.assertTrue(classify_temperature_breach('HI_ACTIVE_COOLING',-0.01) == 'TOO_LOW') 
    self.assertTrue(classify_temperature_breach('HI_ACTIVE_COOLING',-1) == 'TOO_LOW') 
    self.assertTrue(classify_temperature_breach('HI_ACTIVE_COOLING',-25) == 'TOO_LOW') 

    self.assertTrue(classify_temperature_breach('MED_ACTIVE_COOLING',100) == 'TOO_HIGH')
    self.assertTrue(classify_temperature_breach('MED_ACTIVE_COOLING',46) == 'TOO_HIGH')
    self.assertTrue(classify_temperature_breach('MED_ACTIVE_COOLING',40.1) == 'TOO_HIGH')
    self.assertTrue(classify_temperature_breach('MED_ACTIVE_COOLING',40) == 'NORMAL') 
    self.assertTrue(classify_temperature_breach('MED_ACTIVE_COOLING',25) == 'NORMAL') 
    self.assertTrue(classify_temperature_breach('MED_ACTIVE_COOLING',0) == 'NORMAL') 
    self.assertTrue(classify_temperature_breach('MED_ACTIVE_COOLING',-0.01) == 'TOO_LOW') 
    self.assertTrue(classify_temperature_breach('MED_ACTIVE_COOLING',-1) == 'TOO_LOW') 
    self.assertTrue(classify_temperature_breach('MED_ACTIVE_COOLING',-25) == 'TOO_LOW')
    
    self.assertTrue(classify_temperature_breach('None',-25) == 'TOO_LOW') 
    self.assertTrue(classify_temperature_breach('None',25) == 'TOO_HIGH') 
    self.assertTrue(classify_temperature_breach('None',0) == 'NORMAL') 

  def test_infers_breach_as_per_limits(self):
    self.assertTrue(infer_breach(20, 50, 100) == 'TOO_LOW')
    self.assertTrue(infer_breach(2, 3, 5) == 'TOO_LOW')
    self.assertTrue(infer_breach(4, 1, 10) == 'NORMAL')
    self.assertTrue(infer_breach(-4, -100, -2) == 'NORMAL')
    self.assertTrue(infer_breach(0.4, 0.1, 1.0) == 'NORMAL')
    self.assertTrue(infer_breach(1.2, 0.1, 1.0) == 'TOO_HIGH')
    self.assertTrue(infer_breach(0.02, 0.1, 1.0) == 'TOO_LOW')

  def test_sender(self):
    self.assertTrue(send_to_controller('TOO_HIGH') == True) 
    self.assertTrue(send_to_controller('TOO_LOW') == True) 
    self.assertTrue(send_to_controller('NORMAL') == True) 

    self.assertTrue(send_to_email('TOO_HIGH') == True) 
    self.assertTrue(send_to_email('TOO_LOW') == True) 
    self.assertTrue(send_to_email('NORMAL') == False) 
if __name__ == '__main__':
  unittest.main()
