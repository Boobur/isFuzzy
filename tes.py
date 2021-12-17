#coding=utf8
import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import OpenOPC
import win32ui
import time

import sys

reload(sys)
sys.setdefaultencoding('utf8')
# Sparse universe makes calculations faster, without sacrifice accuracy.
# Only the critical points are included here; making it higher resolution is
# unnecessary.

universe1 = np.linspace(-3, 3, 5)
universe2 = np.linspace(-3, 3, 5)
universe3 = np.linspace(-1, 1, 5)

# Create the three fuzzy variables - two inputs, one output
error = ctrl.Antecedent(universe1, 'error')
delta = ctrl.Antecedent(universe2, 'delta')
output = ctrl.Consequent(universe3, 'output')

# Here we use the convenience `automf` to populate the fuzzy variables with
# terms. The optional kwarg `names=` lets us specify the names of our Terms.

error['nb'] = fuzz.trimf(universe1, [-3,-3,-1.5])
error['ns'] = fuzz.trimf(universe1, [-3,-1.5,-0])
error['ze'] = fuzz.trimf(universe1, [-1.5,0,1.5])
error['ps'] = fuzz.trimf(universe1, [0,1.5,3])
error['pb'] = fuzz.trimf(universe1, [1.5,3,3])

delta['nb'] = fuzz.trimf(universe2, [-3,-3,-1.5])
delta['ns'] = fuzz.trimf(universe2, [-3,-1.5,-0])
delta['ze'] = fuzz.trimf(universe2, [-1.5,0,1.5])
delta['ps'] = fuzz.trimf(universe2, [0,1.5,3])
delta['pb'] = fuzz.trimf(universe2, [1.5,3,3])

output['nb'] = fuzz.trimf(universe3, [-1,-1,-0.5])
output['ns'] = fuzz.trimf(universe3, [-1,-0.5,0])
output['ze'] = fuzz.trimf(universe3, [-0.5,0,0.5])
output['ps'] = fuzz.trimf(universe3, [0,0.5,1])
output['pb'] = fuzz.trimf(universe3, [0.5,1,1])


rule0 = ctrl.Rule(antecedent=((error['nb'] & delta['nb']) |
          (error['ns'] & delta['nb']) |
          (error['ze'] & delta['nb']) |
          (error['ns'] & delta['ns']) |
          (error['nb'] & delta['ze']) |
          (error['nb'] & delta['ns'])),
consequent=output['nb'], label='rule nb')

rule1 = ctrl.Rule(antecedent=((error['nb'] & delta['ps']) |
          (error['ns'] & delta['ze']) |
          (error['ps'] & delta['nb'])),
consequent=output['ns'], label='rule ns')

rule2 = ctrl.Rule(antecedent=((error['nb'] & delta['pb']) |
          (error['ns'] & delta['ps']) |
          (error['ze'] & delta['ze']) |
          (error['ps'] & delta['ns']) |
          (error['pb'] & delta['nb'])),
consequent=output['ze'], label='rule ze')

rule3 = ctrl.Rule(antecedent=((error['ns'] & delta['pb']) |
          (error['ze'] & delta['ps']) |
          (error['ps'] & delta['ze']) |
          (error['pb'] & delta['ns'])),
consequent=output['ps'], label='rule ps')

rule4 = ctrl.Rule(antecedent=((error['ps'] & delta['pb']) |
          (error['pb'] & delta['pb']) |
          (error['pb'] & delta['ze']) |
          (error['ps'] & delta['ps']) |
          (error['ze'] & delta['pb']) |
          (error['pb'] & delta['ps'])),
consequent=output['pb'], label='rule pb')

system = ctrl.ControlSystem(rules=[rule0, rule1, rule2, rule3, rule4])
command = ctrl.ControlSystemSimulation(system)

try:
    opc = OpenOPC.client()
    opc.connect('OPCServer.WinCC.1')
except Exception:
	win32ui.MessageBox("No connection with Server", "Error")

while True :
    rd1 = opc.read('E_ACT')
    rd2 = opc.read('DELTA_E')
    print rd1, rd2
    command.input['error'] = float(rd1[0])
    command.input['delta'] = float(rd2[0])
    command.compute()
    wr1 = command.output['output']
    print wr1
    opc.write(('FUZZY_CTRL_LMN', wr1))
    time.sleep(0.5)
