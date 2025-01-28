import numpy as np
import sys
global Quan_R ## quantidade de linhas de restrições
global QuantV  ##quantidade de variaveis
global C, Vartificiais
global Solution
Quan_R = 0
QuantV = 0
Vartificiais = 0 #guardar variaveis artificial
global Indice, col_troca
#Quan_R = 3
#QuantV = 2
 ##haro heheheheh
f = open("solucaounica.txt", "r")
cr = []
b = []
cb = []
num = ""
C = [] #armazena função objetivo total
Matriz = []
R = []
B = []

def BuscaInt(a_lin):
    integers = [float(num) for num in a_lin.split() if num.lstrip('-').isdigit()]  ##split == divide strings em caracteres
    return integers

def MaxOrMin(line):
    global Matriz
    global C
    alpha = ""
    for j in line:
        if(j.isalpha()):
            alpha += j
            if(alpha == "Max"):
                C = C * -1
                return C
            elif(alpha == "Min"):
                pass

#problema ao adicionar variaveis de folga/excesso resolvido
def VarExcFol(line, linha_c):
    global A, C
    global Matriz, QuantV, Vartificiais
    for j in line:
        if(j == "<"):
            newcol = np.zeros(Quan_R)
            new_M = np.insert(Matriz, QuantV, newcol, axis = 1)
            new_M[linha_c][QuantV] = 1
            QuantV +=1
            Matriz = np.array(new_M) 
            C = np.append(C, [0])
            C = np.append(C, [1])
            break
        elif(j == ">"):
            new_cols = np.zeros((QuantV, Quan_R))
            A_new = np.insert(Matriz, QuantV, new_cols, axis = 1)
            A_new[linha_c][QuantV] = -1
            QuantV += 1
            A_new[linha_c][QuantV] = 1
            QuantV += 1
            Vartificiais += 1
            Matriz = np.array(A_new)
            C = np.append(C, [0])
            break
        elif( j == '='):
            newcol = np.zeros(Quan_R)
            new_M = np.insert(Matriz, QuantV, newcol, axis = 1)
            new_M[linha_c][QuantV] = 1
            QuantV +=1
            Vartificiais += 1
            Matriz = np.array(new_M)
            C = np.append(C, [0])
            C = np.append(C, [1]) 
            break
            

def LerArquivo():
    global Quan_R, QuantV
    lines = f.readlines()
    Restricoes = []
    for i in lines:  ##i = linhas do arquivo
        i = i.strip()
        if(i): # se for diferente de vazio
            if("M" in i):
                Fo = i
            else:
                QuantV = min(len(i.split('<')[0].split()), len(i.split('>')[0].split()))
                Quan_R += 1
                Restricoes.append(i)
    return (Restricoes, Fo)

def ProcurarColuna(cols, matriz = None):
    if matriz is None: ##se não é especificado matriz, retorna as colunas da Matriz principal
        return Matriz[:, cols]
    elif(matriz.ndim == 1):  ##verifica se é apenas um vetor
        matriz = np.array(matriz)
        return matriz[cols]

Restricoes, Fo = LerArquivo()

Aux_restricoes = []
for i in Restricoes:
    Aux_restricoes.append(BuscaInt(i))

Matriz = np.array(Aux_restricoes)

b = np.insert(Matriz, 0, QuantV, axis = 1)
Matriz = np.delete(Matriz, QuantV, axis = 1)

######Colocando na forma padrão
C = np.array(BuscaInt(Fo))
C = MaxOrMin(Fo)

for i in range(len(Restricoes)):
    VarExcFol(Restricoes[i], i ) 

print("Matriz completa: \n", Matriz)

cr = np.where(C != 0)[0] ## esse guard indice
cb = np.where(C == 0 )[0] 
R = ProcurarColuna(cr)
B = ProcurarColuna(cb)

def trocar_colunas(col1, col2, matriz = None):
    global cb, cr
    if(matriz is None):
        Matriz[:, [col1, col2]] = Matriz[:, [col2, col1]]
    elif(matriz.ndim == 1):  ##verifica se é apenas um vetor
        matriz[[col1, col2]] = matriz[[col2, col1]]

def EntrarBase():
    global Matriz, R, B, C, cr, cb, R, B, b, Solution, col_troca, Indice, new_C
    Indice = ProcurarColuna(cr, C)
    Indice = np.argmin(Indice) #Cr
    if(C[Indice] < 0):
        ColEntrada = Matriz[:, Indice]
        ColEntrada = ColEntrada.reshape(-1, 1)
        
        LinSaida = np.argmin(np.divide(b, ColEntrada))

        col_troca = np.where(Matriz[LinSaida, :] == 1)[0] #cb
        
        teste = ProcurarColuna(col_troca, C)
        if(teste == 0):
            
            cr[np.where(cr == Indice)[0][0]] = col_troca[0]
            cb[np.where(cb == col_troca[0])[0][0]] = Indice
            
            R = ProcurarColuna(cr)
            B = ProcurarColuna(cb)
            return
    else:
        print("Matriz completa: \n", Matriz)
        print("C completo: \n", C)
        print("Cr novo: \n", cr)
        print("Cb novo: \n", cb)
        print("R novo: \n", R)
        print("B novo: \n", B)
        print("b novo: \n", b)
        new_C = C.copy()
        Solution = CalcFo()
        print("Fo: \n", Solution)
        sys.exit()

#Calcular Cr =  cR − cB ⋅ B−1 ⋅ R✅
def Calculo_Cr():
    global cr, cb, C, B, R
    cr_aux = ProcurarColuna(cr, C)
    cb_aux = ProcurarColuna(cb, C)
    Binverso = np.linalg.inv(B)
    return cr_aux - cb_aux @ (Binverso @ R)

def Calculo_R():
    global B, R, Matriz, cr
    Binverso = np.linalg.inv(B)
    R = Binverso @ R

def CalcFo():
    global cb, b, B
    cb_aux = ProcurarColuna(cb, new_C)
    print("b: ", b)
    print("cb_aux: ", cb_aux)
    Fo_val = cb_aux @ np.linalg.inv(B) @ b
    return Fo_val

def Calcb():
    global b, B
    Binverso = np.linalg.inv(B)
    b = Binverso @ b
global new_C
while True:
    EntrarBase()
    new_C = C.copy()
    new_C[cr] = Calculo_Cr()
    if(new_C[np.argmin(new_C[cr])] >= 0):
        
        Solution = CalcFo()
        print("Fo: ", Solution)
        sys.exit()
    
    Calcb()
    Calculo_R()
    trocar_colunas(Indice, col_troca[0])
    trocar_colunas(Indice, col_troca[0], C)
    Matriz[:, cr] = R
    C[cr] = new_C[cr]
    
    #C[cb] = np.zeros(len(cb))