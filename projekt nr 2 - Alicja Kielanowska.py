import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

t = np.array([1.0, 2.0, 3.5, 5.0, 6.0, 9.0, 9.5])
y = np.array([3.0, 1.0, 4.0, 0.0, 0.5, -2.0, -3.0])

data = np.array([[1.0, 3.0], [2.0, 1.0], [3.5, 4.0], [5.0, 0.0], [6.0, 0.5], [9.0, (-2.0)], [9.5, (-3.0)]])

n = data.shape[0]-1

h = np.zeros(n)
b = np.zeros(n)

for i in range(n):
    h[i] += data[i+1, 0] - data[i, 0]    
    b[i] += (6/h[i]) * (data[i+1, 1] - data[i, 1])
    
#print(h, b)

u = np.zeros(n)
v = np.zeros(n)

u[1] = 2 * (h[0] + h[1])
v[1] = b[1] - b[0]

#print(u, v)

for i in range(2, n):
    u[i] = 2 * (h[i-1] + h[i]) - ((h[i-1])**2)/(u[i-1])
    v[i] = b[i] - b[i-1] - ((h[i-1]) * (v[i-1]))/(u[i-1])
    
#print(u, v)

z = np.zeros(data.shape[0] + 1)


for i in range(1, n-1):
    z[i] = (1/(u[i])) * (v[i] - (h[i]) * (z[i+1]))
    
#print(z)

A = np.zeros(data.shape[0] + 1)
B = np.zeros(data.shape[0] + 1)
C = np.zeros(data.shape[0] + 1)

for i in range(n-1):
    A[i] = (1/(6 * h[i])) * (z[i+1] - z[i])
    B[i] = (z[i])/2
    C[i] = ((-(h[i])/6) * (z[i+1] + 2 * z[i])) + (1/(h[i]) * (data[i+1, 1] - data[i, 1]))
    
#print(A, B, C)

x = np.linspace(0, 10, 100)

S_i = np.zeros(x.shape)
S = np.zeros(x.shape)

for i in range(data.shape[0] - 1):
    S_i += (data[i, 1] + (x - data[i, 0]) * (C[i] + (x - data[i, 0]) * (B[i] + ((x - data[i, 0]) * A[i])))) * ((x > data[i, 0]) & (x <= data[i+1, 0]))
    
for i in range(data.shape[0] - 1):
    if i == 0:
        S += S_i * (x <= data[i+1, 0])
    elif i == data.shape[0] - 2:
        S += S_i * (x > data[i, 0])
    else: 
        S += S_i * ((x > data[i, 0]) & (x <= data[i+1, 0]))
        
cs = CubicSpline(t, y, bc_type='natural')
p = np.linspace(min(t), max(t), 1000)
q = cs(x)

fig = plt.figure()
axes = fig.add_subplot(1, 1, 1)
plt.xlabel('x')
plt.ylabel('S(x)')
plt.scatter(t, y, color='red', label = 'węzły')
plt.plot(x, S, label = 'funkcja sklejana 3 st.')
plt.plot(x, q, label = 'funkcja z modułu Scipy')
plt.legend()
plt.show

N = data.shape[0]
lagrange_poly = np.ones((N, x.shape[0]))
for i in range(N):
    for j in range(N):
        if j!=i:
            lagrange_poly[i,:] *= (x-data[j,0])/(data[i,0]-data[j,0])
            
p = np.zeros(x.shape[0])
for n in range(N):
    p += lagrange_poly[n, :] * data[n, 1]
   

fig2 = plt.figure()
axes = fig2.add_subplot(1, 1, 1)
axes.plot(x, p, label="$P_{%s}(x)$" % N)
for point in data:
    axes.plot(point[0], point[1], 'ko')

plt.show()

