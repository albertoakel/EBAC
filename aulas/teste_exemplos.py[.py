import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve


# Solução analítica
def u_analytical(x):
    return np.sin(x) / np.sin(1) - x


# Solução aproximada pelo Método de Galerkin
def u_approximate_galerkin(x, c1):
    return c1 * x * (1 - x)


# Solução aproximada pelo Método dos Mínimos Quadrados
def u_approximate_least_squares(x, c1):
    return c1 * x * (1 - x)


# Solução aproximada pelo Método de Colocação
def u_approximate_collocation(x, c1):
    return c1 * x * (1 - x)


# Função para calcular o resíduo
def residual(x, c1):
    return -2 * c1 + c1 * x * (1 - x) + x


# Método de Galerkin para encontrar c1
def galerkin_method():
    # Integração numérica usando a regra do trapézio
    def integrate(f, a, b, n=1000):
        x = np.linspace(a, b, n)
        y = f(x)
        return np.trapz(y, x)

    # Função para a integral do resíduo ponderado
    def integrand(x):
        return residual(x, c1) * x * (1 - x)

    # Chute inicial para c1
    c1 = 1.0

    # Resolver a equação integral numericamente
    def equation(c):
        return integrate(lambda x: residual(x, c) * x * (1 - x), 0, 1)

    c1 = fsolve(equation, c1)[0]
    return c1


# Método dos Mínimos Quadrados para encontrar c1
def least_squares_method():
    # Integração numérica usando a regra do trapézio
    def integrate(f, a, b, n=1000):
        x = np.linspace(a, b, n)
        y = f(x)
        return np.trapz(y, x)

    # Função para a integral do quadrado do resíduo
    def integrand(x):
        return residual(x, c1) ** 2

    # Chute inicial para c1
    c1 = 1.0

    # Resolver a equação integral numericamente
    def equation(c):
        return integrate(lambda x: residual(x, c) ** 2, 0, 1)

    c1 = fsolve(equation, c1)[0]
    return c1


# Método de Colocação para encontrar c1
def collocation_method():
    # Ponto de colocação (escolhemos x = 0.5)
    x_collocation = 0.5

    # Resolver o resíduo no ponto de colocação
    def equation(c):
        return residual(x_collocation, c)

    # Chute inicial para c1
    c1 = 1.0

    c1 = fsolve(equation, c1)[0]
    return c1


# Encontrar c1 usando os três métodos
c1_galerkin = galerkin_method()
c1_least_squares = least_squares_method()
c1_collocation = collocation_method()

print(f"Coeficiente c1 pelo Método de Galerkin: {c1_galerkin:.6f}")
print(f"Coeficiente c1 pelo Método dos Mínimos Quadrados: {c1_least_squares:.6f}")
print(f"Coeficiente c1 pelo Método de Colocação: {c1_collocation:.6f}")

# Gerar pontos para plotagem
x_values = np.linspace(0, 1, 100)
u_analytical_values = u_analytical(x_values)
u_galerkin_values = u_approximate_galerkin(x_values, c1_galerkin)
u_least_squares_values = u_approximate_least_squares(x_values, c1_least_squares)
u_collocation_values = u_approximate_collocation(x_values, c1_collocation)

# Plotar as soluções
plt.figure(figsize=(10, 6))
plt.plot(x_values, u_analytical_values, label="Solução Analítica", linewidth=2)
plt.plot(x_values, u_galerkin_values, label="Solução Aproximada (Galerkin)", linestyle="--", linewidth=2)
plt.plot(x_values, u_least_squares_values, label="Solução Aproximada (Mínimos Quadrados)", linestyle="-.", linewidth=2)
plt.plot(x_values, u_collocation_values, label="Solução Aproximada (Colocação)", linestyle=":", linewidth=2)
plt.title("Comparação entre Solução Analítica e Aproximada")
plt.xlabel("x")
plt.ylabel("u(x)")
plt.legend()
plt.grid(True)
plt.show()