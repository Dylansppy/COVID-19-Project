# -*- coding: utf-8 -*-
"""
Epidemiological Model
"""

## 感染率拟合
# 以2 0 1 9 年12 月8 日为第0 天， 起始感染者为1 人
# 政府官方公布的数据
t = [0, 42, 43, 44, 45, 46] # 时间
I = [1 ,198 ,218 ,320 ,478 ,639] # 感染人数

# -----------------------------------------------------------------
# 回溯传播模型估算的数据
# t = [0 , 36 , 42] # 时间
# I = [1 ,1182 , 2758] # 感染人数

def func(b, x):
    return exp((5*b -1/14)*x) # k = 5; D = 14;

popt, pcov = optimize.curve_fit(func, t, I)
    DA[i, ] = popt


ft = fittype('exp ((5*b -1/14)*x)')
f = fit(t,I,ft , 'Startpoint ', 0.1)
plot(f,t,I, 'o')

## 微分方程组
def odesir(t, y, beta , gamma , N):
    dy = [ -beta*y(1)*y(2)/N;
          beta*y(1)*y(2)/N - gamma*y(2);
          gamma*y(2)]
    return dy

# ---------------------------------------------------------------
# logistic increasing model
"""
拟合2019-nCov肺炎感染确诊人数
"""
import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def logistic_increase_function(t, K, P0, r):
    t0 = 11
    # t:time   t0:initial time    P0:initial_value    K:capacity  r:increase_rate
    exp_value = np.exp(r * (t - t0))
    return (K * exp_value * P0) / (K + (exp_value - 1) * P0)

fast_r = 0.40
slow_r = 0.64

def faster_logistic_increase_function(t, K, P0, ):
    return logistic_increase_function(t, K, P0, r=fast_r)

def slower_logistic_increase_function(t, K, P0, ):
    return logistic_increase_function(t, K, P0, r=slow_r)


'''
1.11日41例
1.18日45例
1.19日62例
1.20日291例
1.21日440例
1.22日571例
1.23日830例
1.24日1287例
1.25日1975例
1.26日2744例
1.27日4515例
1.28日5976例
1.29日7711例
1.30日9692例
1.31日11791例
'''

#  日期及感染人数
# t=[11,18,19,20 ,21, 22, 23, 24,  25,  26,  27,  28,  29  ,30]
t = [11, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
t = np.array(t)
# P=[41,45,62,291,440,571,830,1287,1975,2744,4515,5974,7711,9692]
P = [41, 45, 62, 291, 440, 571, 830, 1287, 1975, 2744, 4515, 5974, 7711, 9692, 11791]
P = np.array(P)

# 用最小二乘法估计拟合
# popt, pcov = curve_fit(logistic_increase_function, t, P)
popt_fast, pcov_fast = curve_fit(faster_logistic_increase_function, t, P)
popt_slow, pcov_slow = curve_fit(slower_logistic_increase_function, t, P)
# 获取popt里面是拟合系数
print("K:capacity  P0:initial_value   r:increase_rate   t:time")
# print(popt)
# 拟合后预测的P值
# P_predict = logistic_increase_function(t,popt[0],popt[1],popt[2])
P_predict_fast = faster_logistic_increase_function(t, popt_fast[0], popt_fast[1])
P_predict_slow = slower_logistic_increase_function(t, popt_slow[0], popt_slow[1])
# 未来长期预测
# future=[11,18,19,20 ,21, 22, 23, 24,  25,  26,  27,28,29,30,31,41,51,61,71,81,91,101]
# future=np.array(future)
# future_predict=logistic_increase_function(future,popt[0],popt[1],popt[2])
# 近期情况预测
tomorrow = [32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45]
tomorrow = np.array(tomorrow)
# tomorrow_predict=logistic_increase_function(tomorrow,popt[0],popt[1],popt[2])
tomorrow_predict_fast = logistic_increase_function(tomorrow, popt_fast[0], popt_fast[1], r=fast_r)
tomorrow_predict_slow = logistic_increase_function(tomorrow, popt_slow[0], popt_slow[1], r=slow_r)

# 绘图
plot1 = plt.plot(t, P, 's', label="confimed infected people number")
# plot2 = plt.plot(t, P_predict, 'r',label='predict infected people number')
# plot3 = plt.plot(tomorrow, tomorrow_predict, 's',label='predict infected people number')
plot2 = plt.plot(tomorrow, tomorrow_predict_fast, 's', label='predict infected people number fast')
plot3 = plt.plot(tomorrow, tomorrow_predict_fast, 'r')
plot4 = plt.plot(tomorrow, tomorrow_predict_slow, 's', label='predict infected people number slow')
plot5 = plt.plot(tomorrow, tomorrow_predict_slow, 'g')
plot6 = plt.plot(t, P_predict_fast, 'b', label='confirmed infected people number')

plt.xlabel('time')
plt.ylabel('confimed infected people number')

plt.legend(loc=0)  # 指定legend的位置右下角

print("32\n")
print(faster_logistic_increase_function(np.array(32), popt_fast[0], popt_fast[1]))
print(slower_logistic_increase_function(np.array(32), popt_slow[0], popt_slow[1]))

print("33\n")
print(faster_logistic_increase_function(np.array(33), popt_fast[0], popt_fast[1]))
print(slower_logistic_increase_function(np.array(33), popt_slow[0], popt_slow[1]))

plt.show()

print("Program done!")

# ---------------------------------------------------------------
# SI model
import scipy.integrate as spi
import numpy as np
import matplotlib.pyplot as plt

# Population
N = 1e7
# Simulation time / Day
T = 150
# Contact rate
lamda = 0.8
# Recovery rate
gamma = 0
# Infective ratio
i = np.zeros([T])
# Initial infective ratio
i[0] = 45.0 / N
# Susceptible ratio
s = np.zeros([T])
# Initial susceptible ratio
s[0] = 1 - i[0]
# Initial susceptible and infective ratio
INI = (s[0],i[0])

# Infective rate
for t in range(T-1):
    i[t + 1] = i[t] + i[t] * lamda * (1.0 - i[t])

# Infective rate plot
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(i, c='r', lw=2)
ax.set_xlabel('Day', fontsize=20)
ax.set_ylabel('Infective Ratio', fontsize=20)
ax.grid(1)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)

# Susceptible and infective population proportion
def funcSI(prop,_):
    Y = np.zeros(2) # Y[0] = s[t+1] - s[t], Y[1] = i[t+1] - i[t]
    X = prop # X[0] = s[t], X[1] = i[t]
    # Susceptible proportion change
    Y[0] = - lamda * X[0] * X[1] + gamma * X[1]
    # Infective proportion change
    Y[1] = lamda * X[0] * X[1] - gamma * X[1]
    return Y

T_range = np.arange(0,T + 1)
RES = spi.odeint(funcSI,INI,T_range)

# susceptible and infective proportion plot
plt.plot(RES[:,0],color = 'darkblue',label = 'Susceptible',marker = '.')
plt.plot(RES[:,1],color = 'red',label = 'Infection',marker = '.')
plt.title('SI Model')
plt.legend()
plt.xlabel('Day')
plt.ylabel('Proportion')
plt.show()

# ---------------------------------------------------------------
# SIS Model (recovered individual still susceptible)
import scipy.integrate as spi
import numpy as np
import matplotlib.pyplot as plt

# Population
N = 1e7
# Simulation time / Day
T = 150
# Contact rate
lamda = 0.2586
# Recovery rate
gamma = 0.0235
# Infective ratio
i = np.zeros([T])
# Initial infective ratio
i[0] = 45.0 / N
# Susceptible ratio
s = np.zeros([T])
# Initial susceptible ratio
s[0] = 1 - i[0]
# Initial susceptible and infective ratio
INI = (s[0],i[0])

# Rate
for t in range(T-1):
    i[t + 1] = i[t] + i[t] * lamda * (1.0 - i[t]) - gamma*i[t]

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(i, c='r', lw=2)
ax.set_xlabel('Day', fontsize=20)
ax.set_ylabel('Infective Ratio', fontsize=20)
ax.grid(1)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)

# Susceptible and infective population proportion
def funcSIS(prop,_):
    Y = np.zeros(2) # Y[0] = s[t+1] - s[t], Y[1] = i[t+1] - i[t]
    X = prop # X[0] = s[t], X[1] = i[t]
    # Susceptible proportion change
    Y[0] = - lamda * X[0] * X[1] + gamma * X[1]
    # Infective proportion change
    Y[1] = lamda * X[0] * X[1] - gamma * X[1]
    return Y

T_range = np.arange(0,T + 1)
RES = spi.odeint(funcSIS,INI,T_range)

# susceptible and infective proportion plot
plt.plot(RES[:,0],color = 'darkblue',label = 'Susceptible',marker = '.')
plt.plot(RES[:,1],color = 'red',label = 'Infection',marker = '.')
plt.title('SIS Model')
plt.legend()
plt.xlabel('Day')
plt.ylabel('Proportion')
plt.show()


# ---------------------------------------------------------------
## SIR (recovered individual with lifelong immunity)
import scipy.integrate as spi
import numpy as np
import matplotlib.pyplot as plt

# Population
N = 1e7
# Simulation time / Day
T = 150
# Contact rate
lamda = 0.2586
# Recovery rate
gamma = 0.0235
# Infective ratio
i = np.zeros([T])
# Initial infective ratio
i[0] = 45.0 / N
# Remove ratio
r = np.zeros([T])
# Initial remove ratio
#r[0] = gamma * i[0]
r[0] = 0
# Susceptible ratio
s = np.zeros([T])
# Initial susceptible ratio
s[0] = 1 - i[0] - r[0]
# Initial susceptible，infective and remove ratio
INI = (s[0],i[0],r[0])

# Rate
for t in range(T-1):
    i[t + 1] = i[t] + i[t] * lamda * s[t] - gamma*i[t]
    s[t + 1] = s[t] - i[t] * lamda * s[t]
    r[t + 1] = r[t] + gamma*i[t]

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(s, c='b', lw=2, label='S')
ax.plot(i, c='r', lw=2, label='I')
ax.plot(r, c='g', lw=2, label='R')
ax.set_xlabel('Day', fontsize=20)
ax.set_ylabel('Ratio', fontsize=20)
ax.grid(1)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.legend()

# Susceptible, infective, recovery population proportion
def funcSIR(prop,_):
    Y = np.zeros(3) # Y[0] = s[t+1] - s[t], Y[1] = i[t+1] - i[t]
    X = prop # X[0] = s[t], X[1] = i[t]
    # Susceptible proportion change
    Y[0] = - lamda * X[0] * X[1]
    # Infective proportion change
    Y[1] = lamda * X[0] * X[1] - gamma * X[1]
    # Remove proportion change
    Y[2] = gamma * X[1]
    return Y

T_range = np.arange(0,T + 1)
RES = spi.odeint(funcSIR,INI,T_range)

# susceptible and infective proportion plot
plt.plot(RES[:,0],color = 'darkblue',label = 'Susceptible',marker = '.')
plt.plot(RES[:,1],color = 'red',label = 'Infection',marker = '.')
plt.plot(RES[:,2],color = 'green', label = 'Recovery',marker = '.')
plt.title('SIR Model')
plt.legend()
plt.xlabel('Day')
plt.ylabel('Proportion')
plt.show()

# --------------------------------------------------------------------------
# SIRS Model (recovered individual with waning immunity)
import scipy.integrate as spi
import numpy as np
import matplotlib.pyplot as plt

# Population
N = 1e7
# Simulation time / Day
T = 150
# Contact rate
lamda = 0.2586
# Recovery rate
gamma = 0.0235
# Immunity waning rate
alpha = 0.6

# Infective proportion
i = np.zeros([T])
# Initial infective proportion
i[0] = 45.0 / N
# Recovery proportion
r = np.zeros([T])
# Initial recovery proportion
#r[0] = gamma * i[0]
r[0] = 0
# Susceptible proportion
s = np.zeros([T])
# Initial susceptible proportion
s[0] = 1 - i[0] - r[0]
# Initial susceptible，infective and remove ratio
INI = (s[0],i[0],r[0])

# Rate
for t in range(T-1):
    i[t + 1] = i[t] + i[t] * lamda * s[t] - gamma*i[t]
    s[t + 1] = s[t] - i[t] * lamda * s[t] + alpha * r[t]
    r[t + 1] = r[t] + gamma*i[t] - alpha * r[t]

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(s, c='b', lw=2, label='S')
ax.plot(i, c='r', lw=2, label='I')
ax.plot(r, c='g', lw=2, label='R')
ax.set_xlabel('Day', fontsize=20)
ax.set_ylabel('Ratio', fontsize=20)
ax.grid(1)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.legend()

# Susceptible and infective population proportion
def funcSIRS(prop,_):
    Y = np.zeros(3) # Y[0] = s[t+1] - s[t], Y[1] = i[t+1] - i[t]
    X = prop # X[0] = s[t], X[1] = i[t]
    # Susceptible proportion change
    Y[0] = - lamda * X[0] * X[1] + alpha * X[2]
    # Infective proportion change
    Y[1] = lamda * X[0] * X[1] - gamma * X[1]
    # Remove proportion change
    Y[2] = gamma * X[1] - alpha * X[2]
    return Y

T_range = np.arange(0,T + 1)
RES = spi.odeint(funcSIRS,INI,T_range)

# susceptible and infective proportion plot
plt.plot(RES[:,0],color = 'darkblue',label = 'Susceptible',marker = '.')
plt.plot(RES[:,1],color = 'red',label = 'Infection',marker = '.')
plt.plot(RES[:,2],color = 'green', label = 'Recovery',marker = '.')
plt.title('SIRS Model')
plt.legend()
plt.xlabel('Day')
plt.ylabel('Proportion')
plt.show()

# --------------------------------------------------------------------------
# SEIR Model
import scipy.integrate as spi
import numpy as np
import matplotlib.pyplot as plt

# Population
N = 1e7
# Simulation time / Day
T = 150
# Contact rate
lamda = 0.2586
# Exposed to infective rate
sigma = 1/4
# Recovery rate
gamma = 0.0235
# Immunity waning rate
# alpha = 0.6

# Infective ratio
i = np.zeros([T])
# Initial infective ratio
i[0] = 5.0 / N
# Exposed ratio
e = np.zeros([T])
# Initial exposed ratio
e[0] = 40.0 / N
# Remove ratio
r = np.zeros([T])
# Initial remove ratio
#r[0] = gamma * i[0]
r[0] = 0
# Susceptible ratio
s = np.zeros([T])
# Initial susceptible ratio
s[0] = 1 - e[0] - i[0] - r[0]
# Initial susceptible，infective and remove ratio
INI = (s[0],i[0],e[0],r[0])


# Rate
for t in range(T-1):
    s[t + 1] = s[t] - i[t] * lamda * s[t]
    e[t + 1] = e[t] + lamda * s[t] * i[t] - sigma * e[t]
    i[t + 1] = i[t] + sigma * e[t] - gamma * i[t]
    r[t + 1] = r[t] + gamma * i[t]

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(s, c='b', lw=2, label='S')
ax.plot(e, c='y', lw=2, label='E')
ax.plot(i, c='r', lw=2, label='I')
ax.plot(r, c='g', lw=2, label='R')
ax.set_xlabel('Day', fontsize=20)
ax.set_ylabel('Ratio', fontsize=20)
ax.grid(1)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.legend()

# Susceptible and infective population proportion
def funcSEIR(prop,_):
    Y = np.zeros(4) # Y[0] = s[t+1] - s[t], Y[1] = e[t+1] - e[t], Y[2] = i[t+1] - i[t], Y[3] = r[t+1]-r[t]
    X = prop # X[0] = s[t], X[1] = i[t], X[2] = e[t], X[3]=r[t]
    # Susceptible proportion change
    Y[0] = - lamda * X[0] * X[1]
    # Infective proportion change
    Y[1] = sigma * X[2] - gamma * X[1]
    # Exposed proportion change
    Y[2] = lamda * X[0] * X[1] - sigma * X[2]
    # Remove proportion change
    Y[3] = gamma * X[1]
    return Y

T_range = np.arange(0,T + 1)
RES = spi.odeint(funcSEIR,INI,T_range)

# susceptible and infective proportion plot
plt.plot(RES[:,0],color = 'darkblue',label = 'Susceptible',marker = '.')
plt.plot(RES[:,1],color = 'red',label = 'Infection',marker = '.')
plt.plot(RES[:,2],color = 'orange',label = 'Exposed',marker = '.')
plt.plot(RES[:,3],color = 'green',label = 'Recovery',marker = '.')
plt.title('SEIR Model')
plt.legend()
plt.xlabel('Day')
plt.ylabel('Proportion')
plt.show()

# --------------------------------------------------------------------------
# SEIR Model (considering motality)
import scipy.integrate as spi
import numpy as np
import matplotlib.pyplot as plt

# Population
N = 1e7
# Simulation time / Day
T = 150
# Contact rate
lamda = 0.2586
# Exposed to infective rate
sigma = 1/4
# Motality
die = 0.02691
# Recovery rate
gamma = 0.0235
# Immunity waning rate
# alpha = 0.6

# Infective rate
i = np.zeros([T])
# Initial infective proportion
i[0] = 5.0 / N
# Exposed rate
e = np.zeros([T])
# Initial exposed proportion
e[0] = 40.0 / N
# Remove rate
r = np.zeros([T])
# Initial remove proportion
#r[0] = gamma * i[0]
r[0] = 0
# Susceptible proportion
s = np.zeros([T])
# Initial susceptible proportion
s[0] = 1 - e[0] - i[0] - r[0]
# Motality
d = np.zeros([T])
# Initial motality
d[0] = 0
# Initial susceptible，infective and remove ratio
INI = (s[0],i[0],e[0],r[0],d[0])

# Rate
for t in range(T-1):
    s[t + 1] = s[t] - i[t] * lamda * s[t]
    e[t + 1] = e[t] + lamda * s[t] * i[t] - sigma * e[t]
    i[t + 1] = i[t] + sigma * e[t] - gamma * i[t] - die * i[t]
    r[t + 1] = r[t] + gamma * i[t]
    d[t + 1] = d[t] + die * i[t]

# Plot
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(s, c='b', lw=2, label='S')
ax.plot(e, c='y', lw=2, label='E')
ax.plot(i, c='r', lw=2, label='I')
ax.plot(r, c='g', lw=2, label='R')
ax.plot(d, c='black', lw=2, label='D')
ax.set_xlabel('Day', fontsize=20)
ax.set_ylabel('Rate', fontsize=20)
ax.grid(1)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.legend()

# Population proportion
def funcSEIRD(prop,_):
    Y = np.zeros(5) # Y[0] = s[t+1] - s[t], Y[1] = e[t+1] - e[t], Y[2] = i[t+1] - i[t], Y[3] = r[t+1]-r[t], Y[4]=d[t+1]-d[t]
    X = prop # X[0] = s[t], X[1] = i[t], X[2] = e[t], X[3]=r[t], X[4]=d[t]
    # Susceptible proportion change
    Y[0] = - lamda * X[0] * X[1]
    # Infective proportion change
    Y[1] = sigma * X[2] - gamma * X[1] - die * X[1]
    # Exposed proportion change
    Y[2] = lamda * X[0] * X[1] - sigma * X[2]
    # Remove proportion change
    Y[3] = gamma * X[1]
    # Motality change
    Y[4] = die * X[1]
    return Y

T_range = np.arange(0,T + 1)
RES = spi.odeint(funcSEIRD,INI,T_range)

# plot
plt.plot(RES[:,0],color = 'darkblue',label = 'Susceptible',marker = '.')
plt.plot(RES[:,1],color = 'red',label = 'Infection',marker = '.')
plt.plot(RES[:,2],color = 'orange',label = 'Exposed',marker = '.')
plt.plot(RES[:,3],color = 'green',label = 'Recovery',marker = '.')
plt.plot(RES[:,4],color = 'black',label = 'Demise',marker = '.')
plt.title('SEIR Model (with motality)')
plt.legend()
plt.xlabel('Day')
plt.ylabel('Proportion')
plt.show()
 
 
 
 
      