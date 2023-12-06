import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import solve

print("\n####################################################")
print("######### Exercício Numérico - Exemplo 3-6 #########")
print("\nEncontrar a distribuição de cargas de um fio equipotencial.\n")

#---- DECLARAÇÃO DE VARIÁVEIS --------------------------------------------------
try:
    L = np.float64(input("Insira o comprimento do fio, em metros (float): "))
except:
    L = 0.2
    print("Erro encontrado. O valor padrão será utilizado: L = {} m\n".format(L))
try:
    N = int(input("Insira um número par de elementos finitos (inteiro): "))
except:
    N = 1000
    print("Erro encontrado. O valor padrão será utilizado: N = {}\n".format(N))
try:
    a = np.float64(input("Insira o raio do fio (float): "))
except:
    a = 0.001
    print("Erro encontrado. O valor padrão será utilizado: a = {} m\n".format(a))

if N%2 > 0: # Garantir um número par de elementos
  N += 1

try:
    phi = float(input("Insira o valor do potencial após a carga ser inserida (Volt): "))
except:
    phi = 5.0
    print("Erro encontrado. O valor padrão será utilizado: Phi = {} V\n".format(phi))

# descrever variáveis
d = np.float64(L/N/2)
A = np.zeros([int(N/2), int(N/2)], dtype=np.float64)
q = np.ones(int(N/2), dtype=np.float64)
Q = np.ones(N, dtype=np.float64)



print("\nComprimento do fio: {} \nNúmero de elementos finitos: {} \nComprimento de cada elemento finito: {}".format(L, N, d))

# ------------------------------------------------------------------------------

# Calcular Coeficientes 'A'
for i in range(int(N/2)):
    for j in range(i+1, int(N/2)):
        A[i][j] = 0.5*(np.log((j-i+0.5)/(j-i-0.5)) + np.log((N-i-j+(3/2))/(N-i-j+0.5)))

    for j in range(1, i-1):
        A[j][i] = A[i][j]

    A[i][i] = np.log(L/(N*a)) + 0.5*np.log((2*(N-2*i)+3)/(2*(N-2*i)+1))

# ------------------------------------------------------------------------------

q = solve(A, -10*np.ones(int(N/2)))

for i in range(int(N/2)):
    Q[i] = q[i]
    Q[N-i-1] = q[i]

Q_total = sum(Q)
print("\nA carga total do fio é: {} C\n".format(Q_total))

# ------------------------------------------------------------------------------
# Plotting
x = np.linspace(0, L, N)
fig, ax = plt.subplots(2, sharex=True, figsize=(6,3))
extent = [x[0]-2*d, x[-1]+2*d,0,1]
ax[0].imshow(Q[np.newaxis, :],  cmap="hot", aspect="auto", extent=extent)
ax[0].set_title("Distribuição de Carga")
ax[0].set_xlim(extent[0], extent[1])
ax[0].set_yticks([])
ax[1].plot(x, Q, color="red")
ax[1].set_ylabel("Carga (C)")
ax[1].set_xlabel("Comprimento (m)")
plt.tight_layout()
plt.show()
fig.savefig("ex1.png")

### Zoom
ind = list(Q).index(np.min(Q))
plt.clf()
plt.ylabel("")
plt.xlabel("")
plt.plot(x, Q, color="red")
plt.xlim(x[ind]-30*d, x[ind]+30*d)
plt.show()
fig.savefig("ex1-zoom.png")

'''
opcao = input("\nDeseja salvar a figura? (s ou n): ")
match opcao:
    case "s":
        nome = input("Insira o nome do arquivo (sem extensão): ")
        try:

            fig.savefig("{}.png".format(nome))
            print("Figura salva com sucesso!")
        except:
            print("Ocorreu um erro. A figura não pode ser salva.")
    case _:
        print("A figura não foi salva.\n")
'''