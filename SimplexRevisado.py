import numpy as np
Quan_R = 3 ## quantidade de linhas de restrições
QuantV = 2  ##quantidade de variaveis

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
    lines = f.readlines()
    Restricoes = []
    for i in lines:
        i = i.strip()
        if(i): # se for diferente de vazio
            if("M" in i):
                Fo = i
            else:
                QuantR += 1
                Restricoes.append(i)
    return Restricoes

#LerArquivo()

Fo = f.readline().strip()
r1 = f.readline().strip()  ##pq eu não pesqisei antesaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
r2 = f.readline().strip() ##.strip() == remove espaços em branco e otras cositas se especificar

a_lin1 = BuscaInt(r1)
a_lin2 = BuscaInt(r2)
aux_Fo = BuscaInt(Fo)

Matriz = np.array([aux_Fo])
Matriz = np.array([a_lin1, a_lin2])

b = np.delete(Matriz, (QuantV-1, QuantV -2), axis = 1)
Matriz = np.delete(Matriz, 2, axis = 1)
Matriz = np.insert(Matriz, 0, aux_Fo, axis = 0)

######Colocando na forma padrão

Fo = MaxOrMin(Fo)
Matriz = np.delete(Matriz, 0, axis = 0)
Matriz = np.insert(Matriz, 0, Fo, axis = 0)
VarExcFol(r1, 1)
VarExcFol(r2, 2)

C = np.delete(Matriz, (Quan_R-1, Quan_R -2), axis = 0) #de novo pq atualizou a matriz possivelmente
Matriz = np.delete(Matriz, 0, axis = 0)
Quan_R-= 1
print("Matriz b: \n", b)
print("Matriz C: \n", C)
print("Matriz completa: \n", Matriz)

cr = C[np.where(C != 0)]
cb = C[np.where(C == 0)]

cols = np.where(C != 0 )[1]

test = []
def ProcurarColuna(cols):
    for j in cols:
        for i in range(Quan_R):
            if(len(test) < Quan_R):
                test.append([Matriz[i][j]])
            else:
                test[i].append(Matriz[i][j])
    return test

R = np.delete(ProcurarColuna(cols), 0, axis= 0)
print(R)

def EntrarBase():
    Indice = np.argmin(cr)
    if(cr[Indice] < 0):
        ColEntrada = Matriz[:][Indice]
        print("Col entrada\n", ColEntrada)
        #ColEntrada = np.delete(ColEntrada, 0, axis = 0)
        print("Col entrada\n", ColEntrada)
        #Menor = np.argmin( np.divide(b, ColEntrada))
        #print(Menor)
        pass

EntrarBase()

Indice = np.argmin(cr)
#retorna indice do elemento [-80] Saida indice = 1
#pesquisar na matriz (Matriz) a coluna com indice  ==1
##colocar essa coluna em outro vetor
##primeira 