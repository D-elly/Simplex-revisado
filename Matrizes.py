import numpy as np
global Quan_R, QuantV ## quantidade de linhas de restrições
Quan_R = 0
QuantV = 0  ##quantidade de variaveis

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
    global C, QuantV
    C = np.delete(Matriz, (QuantV-1, QuantV -2), axis = 0)
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
    global Matriz, QuantV, Quan_R
    for j in line:
        if(j == "<"):
            newcol = np.zeros(QuantV)
            print("New Col: ", newcol)
            new_M = np.insert(Matriz, Quan_R, newcol, axis = 1)
            new_M[linha_c][Quan_R] = 1
            Quan_R +=1
            Matriz = np.array(new_M) 
        elif(j == ">"):
            new_cols = np.zeros((Quan_R, QuantV))
            A_new = np.insert(Matriz, Quan_R, new_cols, axis = 1)
            A_new[linha_c][Quan_R] = -1
            Quan_R += 1
            A_new[linha_c][Quan_R] = 1
            A_new[0][Quan_R] = 1
            Matriz = np.array(A_new)

def LerArquivo():
    global Quan_R, QuantV
    lines = f.readlines()
    Restricoes = []
    for i in lines:
        i = i.strip()
        if(i): # se for diferente de vazio
            if("M" in i):
                Fo = i
            else:
                QuantV = len(i.replace("<", "").replace(">", "").replace("=", "").split())
                Quan_R += 1
                Restricoes.append(i)
    return (Restricoes, Fo)

Restricoes, Fo = LerArquivo()
Aux_Restricoes = []
for i in range(len(Restricoes)):
    Aux_Restricoes.insert(i, BuscaInt(Restricoes[i]))

aux_Fo = BuscaInt(Fo)

Matriz = np.array([aux_Fo])
Matriz = np.array(Aux_Restricoes)

#Quantidade de Restrições é 2 e de variáveis é 3, no código anteior aqui usava  QuanV, mas QuanV estava valendo 2, quando na verdade vale 3
#Por isso utilizei Quan_R no lugar, os números estavam trocados
b = np.delete(Matriz, (Quan_R-1, Quan_R -2), axis = 1) 

Matriz = np.delete(Matriz, 2, axis = 1)
Matriz = np.insert(Matriz, 0, aux_Fo, axis = 0)

Fo = MaxOrMin(Fo)

Matriz = np.delete(Matriz, 0, axis = 0)
Matriz = np.insert(Matriz, 0, Fo, axis = 0)

for i in range(Quan_R):
    VarExcFol(Restricoes[i], i+1)

C = np.delete(Matriz, (QuantV-1, QuantV -2), axis = 0) #de novo pq atualizou a matriz possivelmenete

print("Matriz b: \n", b)
print("Matriz C: \n", C)
print("Matriz completa: \n", Matriz)

cr = C[np.where(C != 0)]
cb = C[np.where(C == 0)]

cols = np.where(C != 0 )[1]

test = []
def ProcurarColuna(cols):
    for j in cols:
        for i in range(QuantV):
            if(len(test) < QuantV):
                test.append([Matriz[i][j]])
            else:
                test[i].append(Matriz[i][j])
    return test

R = np.delete(ProcurarColuna(cols), 0, axis= 0)
print(R)

def EntrarBase():
    Indice = np.argmin(cr)
    print(ProcurarColuna([Indice]))
    if(cr[Indice] < 0):
        ColEntrada = Matriz[:][Indice]
        print("Col entrada\n", ColEntrada)
        #ColEntrada = np.delete(ColEntrada, 0, axis = 0)
        print("Col entrada\n", ColEntrada)
        #Menor = np.argmin( np.divide(b, ColEntrada))
        #print(Menor)
        pass

EntrarBase()
print(Quan_R)
print(QuantV)