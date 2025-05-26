#This code solves for T_initial in the following equation:
# m_fluid_final * u_fluid_final - (m_liquid_initial * u_liquid_initial + m_vapor_initial * u_vapor_initial)
# - (m_fluid_final - m_fluid_initial) * h_inlet  = parasite * time - m_tank * specific heat

# This is equation (7) from Clark, J., and Hartwig, J., 
#“Assessment of prediction and efficiency parameters for cryogenic no-vent fill,” 
#Cryogenics, Vol. 117,2021, 103309

#This provides the maximum allowable temperature for a succsesful No Vent Fill Transfer

import numpy as np
import matplotlib.pyplot as plt
import scipy as sc

#Based off assumtion that the tank holds 733,000 gallons and is spherical
m_tank = 1.6e6
m_fluid_final = 3e6 * 0.95
h_inlet = 0.5
#Assuming tank is empty after CHV
m_liquid_initial = 0
m_vapor_initial = 0
m_fluid_initial = 0

parasite = 0
end_pressure = 40

#Funtion that returns internal energy of liquid as a funtion of temperature
def u_liq_vap(T, liquid='LOX'):
    if liquid=='LOX':
        cv = 929.22
        mm = 16e-3
        T_final = 90.19
    elif liquid=='LHC4':
        cv = 2056.9
        mm = 52.05e-3  
        T_final = 117
        
    u_fluid_final = cv * m_fluid_final / mm * T_final 
    u_liquid_initial = cv * m_liquid_initial / mm * T
    u_vapor_initial = cv * m_vapor_initial / mm * T
    return u_fluid_final, u_liquid_initial, u_vapor_initial

#Function for specific heat of the tank at low temperatures(stainless steel)
def C_tank(T):
    a = 22.0061
    b = -127.5528
    c = 303.647
    d = -381.0098
    e = 274.0328
    f =  -112.9212
    g = 24.7593
    h = -2.239153
    i = 0
    logT = np.log10(T)
    exp1 = a + b*logT + c*logT**2 + d*logT**3
    exp2 = e*logT**4 + f*logT**5 + g*logT**6 + h*logT**7 + i*logT**8
    return 10**(exp1+exp2)


#Function that returns the left side of the equation minus the right side of the equation.
#Returns 0 when correct T_inital is inputed
def eqn(T_initial, liquid='LOX'):
    #Set T final as saturation temperaure
    if liquid=='LOX':
        T_final = 90.19
    elif liquid=='LHC4':
        T_final = 117

    #Call intenral energy function
    u_fluid_final, u_liquid_initial, u_vapor_initial = u_liq_vap(T_initial, liquid)
    #guessing internal energy because the function is currenty incorrect (it assumes ideal gas, not liquid)
    u_fluid_final, u_liquid_initial, u_vapor_initial = 3250, 3.4, 3.4

    #Terms in the equation
    fluid_energy_final = m_fluid_final * u_fluid_final
    liq_energy_initial = m_liquid_initial * u_liquid_initial
    vap_energy_initial = m_vapor_initial * u_vapor_initial
    inlet_heat = (m_fluid_final - m_fluid_initial) * h_inlet

    temps = np.linspace(T_initial, T_final, 1000)
    tank_heat = C_tank(temps)      
    final_heat = m_tank * np.trapz(tank_heat, temps)
    
    #Left side of equation
    fluid_energy_abosrbed = fluid_energy_final - (liq_energy_initial + vap_energy_initial) - inlet_heat
    #Right side of equation
    tank_energy_lost = parasite - final_heat
    
    # returns 0 when equation is true
    
    return (fluid_energy_abosrbed - tank_energy_lost)

#Print the temperature that returns 0
LOX_result = sc.optimize.brentq(eqn, 50, 350, args=('LOX'))
print('Maximum Initial Temp for LOX = %.2f K' %(LOX_result))

LHC4_result = sc.optimize.brentq(eqn, 50, 350, args=('LHC4'))
print('Maximun Initial Temp for LHC4 = %.2f K' %(LHC4_result))

#Result should be higher than saturation temperature by 10 K or higher
#Currently returns:
#'Maximum Initial Temp for LOX = 111.07 K'
#'Maximun Initial Temp for LHC4 = 134.60 K'
