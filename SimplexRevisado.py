import numpy as np
import sys
global Quan_R ## quantidade de linhas de restrições
global QuantV  ##quantidade de variaveis
global C

Quan_R = 0
QuantV = 0
Vartificiais = []#guardar variaveis artificial

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

def BuscaInt(a_lin):
    integers = [int(num) for num in a_lin.split() if num.lstrip('-').isdigit()]  ##split == divide strings em caracteres
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

def VarExcFol(line, linha_c):
    global A, C
    global Matriz, QuantV
    for j in line:
        if(j == "<"):
            newcol = np.zeros(Quan_R)
            new_M = np.insert(Matriz, QuantV, newcol, axis = 1)
            new_M[linha_c][QuantV] = 1
            QuantV +=1
            Matriz = np.array(new_M) 
            C = np.append(C, [0])
        elif(j == ">"):
            new_cols = np.zeros((QuantV, Quan_R))
            A_new = np.insert(Matriz, QuantV, new_cols, axis = 1)
            A_new[linha_c][QuantV] = -1
            QuantV += 1
            A_new[linha_c][QuantV] = 1
            A_new[0][QuantV] = 1
            Matriz = np.array(A_new)
            C = np.append(C, [0])
            C = np.append(C, [1])

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

def ProcurarColuna(cols, matriz = []):
    if(len(matriz) > 0):
        return matriz[:, cols]
    return Matriz[:, cols]

Restricoes, Fo = LerArquivo()

Aux_restricoes = []
for i in Restricoes:
    Aux_restricoes.append(BuscaInt(i))

Matriz = np.array(Aux_restricoes)

b = np.delete(Matriz, (QuantV-1, QuantV -2), axis = 1)
Matriz = np.delete(Matriz, 2, axis = 1)

######Colocando na forma padrão
C = np.array(BuscaInt(Fo))
C = MaxOrMin(Fo)

for i in range(len(Restricoes)):
    VarExcFol(Restricoes[i], i ) 

print("Matriz b: \n", b)
print("Matriz C: \n", C)
print("Matriz completa: \n", Matriz)

cr = np.where(C != 0)[0] ## esse guard indice
cb = np.where(C == 0 )[0] 

R = ProcurarColuna(cr)
B = ProcurarColuna(cb)

def trocar_colunas(Matriz, col1, col2):
    Matriz[:, [col1, col2]] = Matriz[:, [col2, col1]]

def EntrarBase():
    Indice = np.argmin(ProcurarColuna(cr, C))
    if(C[0][Indice] < 0):
        ColEntrada = np.delete(ProcurarColuna(Indice), 0, axis = 0) #apagar aqui
        ColEntrada = ColEntrada.reshape(-1, 1)
        LinSaida = np.argmin(np.divide(b, ColEntrada))
        print("Linsaida\n", LinSaida )
        return ColEntrada, LinSaida
    else:
        print("Solução Ótima")
        sys.exit()

EntrarBase()
#Testar se é ótima ✅
#Calcular Cr ✅
#Trocar Colunas que entram e saem ✅
#recalcular variáveis básicas b = B^-1 * b
#recalcular R = B−1 ⋅ R
#FO = cB ⋅ B−1 ⋅ b
