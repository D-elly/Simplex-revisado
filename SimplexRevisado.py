import numpy as np
global Quan_R ## quantidade de linhas de restrições
global QuantV  ##quantidade de variaveis

Quan_R = 0
QuantV = 0

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
    C = np.delete(Matriz, (Quan_R-1, Quan_R -2), axis = 0)
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
    global A
    alpha = ""
    global Matriz, QuantV
    for j in line:
        if(j == "<"):
            newcol = np.zeros(Quan_R)
            new_M = np.insert(Matriz, QuantV, newcol, axis = 1)
            new_M[linha_c][QuantV] = 1
            QuantV +=1
            Matriz = np.array(new_M) 
        elif(j == ">"):
            new_cols = np.zeros((QuantV, Quan_R))
            A_new = np.insert(Matriz, QuantV, new_cols, axis = 1)
            A_new[linha_c][QuantV] = -1
            QuantV += 1
            A_new[linha_c][QuantV] = 1
            A_new[0][QuantV] = 1
            Matriz = np.array(A_new)

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
    Quan_R += 1
    return (Restricoes, Fo)

def ProcurarColuna(cols):
    return Matriz[:,cols]

Restricoes, Fo = LerArquivo()

Aux_restricoes = []
for i in Restricoes:
    Aux_restricoes.append(BuscaInt(i))

aux_Fo = BuscaInt(Fo)

Matriz = np.array([aux_Fo])
Matriz = np.array(Aux_restricoes)

b = np.delete(Matriz, (QuantV-1, QuantV -2), axis = 1)
Matriz = np.delete(Matriz, 2, axis = 1)
Matriz = np.insert(Matriz, 0, aux_Fo, axis = 0)

######Colocando na forma padrão

Fo = MaxOrMin(Fo)
Matriz = np.delete(Matriz, 0, axis = 0)
Matriz = np.insert(Matriz, 0, Fo, axis = 0)
for i in range(len(Restricoes)):
    VarExcFol(Restricoes[i], i + 1) 

C = np.delete(Matriz, (Quan_R-1, Quan_R -2), axis = 0) #de novo pq atualizou a matriz possivelmenete

print("Matriz b: \n", b)
print("Matriz C: \n", C)
print("Matriz completa: \n", Matriz)

cr = C[np.where(C != 0)]
cb = C[np.where(C == 0)]

cols = np.where(C != 0 )[1]
colsb = np.where(C == 0 )[1]

R = np.delete(ProcurarColuna(cols), 0, axis= 0)
B = np.delete(ProcurarColuna(colsb), 0, axis = 0)

def EntrarBase():
    Indice = np.argmin(cr)
    if(cr[Indice] < 0):
        ColEntrada = ProcurarColuna(Indice)
        print("Col entrada\n", ColEntrada)

EntrarBase()