###########################################################
###########################################################

################ CALCULADORA TI - HI ######################

###########################################################

####################### DESCRIPTION #######################
# Programa que permite calcular el TI y el HI de un pallet
# teniendo como insumo las dimensiones del pallet y las 
# dimensiones de la caja y dando como resultado el número
# de cajas por plancha (TI) y el numero de planchas por pallet (HI).

######################### AUTHOR ##########################
# Ing. DANIEL EDUARDO MONTERO RAMÍREZ - DataLog Desarrollo Logistico


from gekko import GEKKO

def Calculo_TI(Ancho_Caja, Largo_Caja,  Ancho_Pallet, Largo_Pallet):
    m = GEKKO()  # Initialize gekko
    # Initialize variables
    x1 = m.Var(value = 1, integer=True) # Columnas PN
    x2 = m.Var(value = 1, integer=True) # Filas PN
    x3 = m.Var(value = 1, integer=True) # Columnas PI
    x4 = m.Var(value = 1, integer=True) # Filas PI
    # Parameters
    c1 = m.Param(Ancho_Caja) # Ancho Caja
    c2 = m.Param(Largo_Caja) # Largo Caja
    c5 = m.Param(Ancho_Pallet) # Ancho Pallet
    c6 = m.Param(Largo_Pallet) # Largo Pallet
    # Restrictions
    m.Equation(c1 * x1 <= c5) # Restricción 1
    m.Equation(c2 * x2 <= c6) # Restricción 2
    m.Equation(c2 * x3 <= c5) # Restricción 3
    m.Equation(c1 * x4 <= c6) # Restricción 4
    m.Equation((c2 * x2) + (c1 * x4) <= c6) # Restricción 5
    m.Equation((c1*c2*x1*x2)+(c1*c2*x3*x4) <= c5 * c6) # Restricción 6
    # Objective
    m.Maximize(x1 * x2 + x3 * x4) 
    #Method
    m.options.IMODE = 3
    m.options.SOLVER = 1
    # Solve
    m.solve()  

    TI = int(m.options.OBJFCNVAL) * -1

    return TI

def Calculo_HI(TI,Alto_Caja, Peso_Caja,Max_Peso, Max_Altura, Altura_Estiba):
    m = GEKKO()  # Initialize gekko
    # Initialize variables
    Hi = m.Var(value=1,integer=True)
    # Parameters
    c3 = m.Param(Alto_Caja) # Alto Caja
    c4 = m.Param(Peso_Caja) # Peso Caja
    c7 = m.Param(Max_Peso) # Max Peso Pallet
    c8 = m.Param(Max_Altura) # Max Altura Pallet
    c9 = m.Param(Altura_Estiba) # Altura Estiba
    # Equations
    m.Equation(Hi * TI * c4 <= c7) # Restricción 1
    m.Equation(Hi * c3 <= (c8 - c9)) # Restricción 2
    # Objetive
    m.Maximize(Hi)
    # Method
    m.options.IMODE = 3
    m.options.SOLVER = 1
    # Solve
    m.solve()
    
    HI = int(m.options.OBJFCNVAL) * -1
    
    return HI

def run():
    # Parametros
    Ancho_Caja = 25  # Ancho Caja
    Largo_Caja = 20 # Largo Caja
    Alto_Caja = 15 # Alto Caja
    Peso_Caja = 2000 # Peso Caja
    Ancho_Pallet = 200 # Ancho Pallet
    Largo_Pallet = 200 # Largo Pallet
    Max_Peso = 200000 # Max Peso
    Max_Altura = 155 # Max Altura
    Altura_Estiba = 15 # Altura Estiba

    TI = Calculo_TI(Ancho_Caja, Largo_Caja,  Ancho_Pallet, Largo_Pallet)

    HI = Calculo_HI(TI,Alto_Caja, Peso_Caja,Max_Peso, Max_Altura, Altura_Estiba)

    print ("TI: " + str(TI))
    print ("HI: " + str(HI))

if __name__ == "__main__":
    run()
