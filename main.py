
from re import X
import autograd as ad
from autograd import grad, jacobian
import autograd.numpy as np

# Define equations at nodes
f1 = lambda x: x[0] + x[5] - 2.5
f2 = lambda x: -x[0] + x[1] + x[6]
f3 = lambda x: -x[1] + x[2] + 0.5
f4 = lambda x: -x[2] - x[3] + 1
f5 = lambda x: x[3] - x[4] - x[6] + 1

# Define equations of the loops
f6 = lambda x: 130703.32 * (x[1]**2) + 43567.77 * (x[2]**2) - 130703.32 * (x[3]**2) - 330842.79 * (x[6]**2)
f7 = lambda x: 10163.49 * (x[0]**2) + 130703.32 * (x[4]**2) - 10338.84 * (x[5]**2) + 330842.79 * (x[6]**2)

# Calculate Jacobians
jac_f1 = jacobian(f1)
jac_f2 = jacobian(f2)
jac_f3 = jacobian(f3)
jac_f4 = jacobian(f4)
jac_f5 = jacobian(f5)
jac_f6 = jacobian(f6)
jac_f7 = jacobian(f7)

# Initialize variables for Newton-Raphson iteration
i = 0
error = 500
tol = 0.001
maxiter = 500

# 7x1 Matrix
M = 7
N = 7

# Initial guess for the flow rates
x_0 = np.array([0, 1, 1, 0, 2, 2, 0], dtype=float).reshape(N, 1)

# Perform Newton-Raphson iteration
while np.any(abs(error) > tol) and i < maxiter:
    fun_evaluate = np.array([f1(x_0), f2(x_0), f3(x_0), f4(x_0), f5(x_0), f6(x_0), f7(x_0)]).reshape(M, 1)
    flat_x_0 = x_0.flatten()
    jac = np.array([jac_f1(flat_x_0), jac_f2(flat_x_0), jac_f3(flat_x_0), jac_f4(flat_x_0), jac_f5(flat_x_0), jac_f6(flat_x_0), jac_f7(flat_x_0)])
    jac = jac.reshape(N, M)

    x_new = x_0 - np.linalg.inv(jac) @ fun_evaluate

    error = x_new - x_0

    x_0 = x_new

    print(f"Iteration {i}")
    print("Error:", error)
    print("--------------------------")

    i += 1

print("The Solution is")
print(x_new)
print("Q(AB)", x_new[0], "m3/s")
print("Q(BC)", x_new[1], "m3/s")
print("Q(CD)", x_new[2], "m3/s")
print("Q(DE)", x_new[3], "m3/s")
print("Q(EF)", x_new[4], "m3/s")
print("Q(FA)", x_new[5], "m3/s")
print("Q(BE)", x_new[6], "m3/s")

# Define arrays for length, diameter & elevation
lengths = np.array([1500, 1500, 1200, 1500, 1500, 1200, 1200])
diameters = np.array([0.8, 0.6, 0.7, 0.7, 0.7, 0.7, 0.7])
elevations = np.array([30, 25, 20, 20, 22, 25])
friction_factor = 0.2
initial_head = 15

# Head calculation
print("Head at node 1 is =", initial_head, "m")
head = initial_head

for i in range(5):
    hf_next = (16 * friction_factor * lengths[i] * (x_new[i]**2)) / (2 * 9.81 * diameters[i]**5 * np.pi**2)
    if elevations[i] > elevations[i + 1]:
        head = head - hf_next
    else:
        head = head + hf_next
    
    print(f"Head at node {i + 2} is =", head, "m")
    initial_head = head
