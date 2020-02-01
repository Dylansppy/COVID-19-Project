# -*- coding: utf-8 -*-
"""
Epidemiological Model
Author: Dylan Shen
"""

## 感染率拟合
# 以2 0 1 9 年12 月8 日为第0 天， 起始感染者为1 人
# 政府官方公布的数据
# t = [0, 42, 43, 44, 45, 46]'; % 时间
# I = [1 ,198 ,218 ,320 ,478 ,639] '; % 感染人数

# 回溯传播模型估算的数据
#  t = [0 , 36 , 42] '; % 时间
#  I = [1 ,1182 , 2758] '; % 感染人数

ft = fittype('exp ((5*b -1/14)*x)'); % k = 5; D = 14;
f = fit(t,I,ft , 'Startpoint ', 0.1)
plot(f,t,I, 'o')

## 微分方程组
def odesir(t, y, beta , gamma , N):
    dy = [ -beta*y(1)*y(2)/N;
          beta*y(1)*y(2)/N - gamma*y(2);
          gamma*y(2)]
    return dy
     

## SIR
N = 11000000; % 武汉人口
ts = [0, 270]; % 求解时间区间
y0 = [N-1, 1 , 0]; % 初始条件[ S0 I0 R0 ]
C = 14; % 感染的平均持续时间
gamma = 1/C;
k = 5; % 感染者每天平均接触人数
b = 0.04133; % 接触时的传染概率
% b = 0 . 0 5 2 1 4 ;
beta = k*b;
d = 0.03; % 死亡率
 
[t, y] = ode45(@odesir , ts ,y0 , [], beta ,gamma , N);
y(C+1 : e n d ,4) = (N-y(1 : e n d -C,1))*d;
plot(t,y);
xlabel('Time (days)'); ylabel('Population ')
legend('S', 'I', 'R', 'D')


## 不同管控强度SIR 模型
N = 11000000; % 武汉人口
C = 14; % 感染的平均持续时间
gamma = 1/C;
#b = 0 . 0 4 1 3 3 ;
b = 0.05214; # 接触时的传染概率
d = 0.03; # 死亡率

# 第一阶段： 政府未管控
ts = [0, 46];
y0 = [N-1, 1 , 0];
k = 5;
beta = k*b;
[t1 , y1] = ode45(@odesir , ts , y0 , [], beta ,gamma , N);

# 第二阶段： 政府管控
y0 = y1(end ,:);
ts = [47, 250];
k = 1.0;
beta = k*b;
[t2 , y2] = ode45(@odesir , ts , y0 , [], beta ,gamma , N);4

# 合并两个阶段
t = [t1; t2(2 : e n d )];
y = [y1; y2(2 : e n d ,:)];
y(C+1 : e n d ,4) = (N-y(1 : e n d -C,1))*d;
2plot(t,y(:,2 : e n d ));
xlabel('Time (days)'); ylabel('Population ')
 legend('I', 'R', 'D')
 
 
## SEIR 模型
N = 11000000; % 武汉人口
ts = [0, 250]; % 求解时间区间
y0 = [N-1, 1 , 0, 0]; % 初始条件[ S0 I0 R0 ]
C = 14; % 感染的平均持续时间
gamma = 1/C;
k = 5; % 感染者每天平均接触人数
b = 0.05214; % 接触时的传染概率
beta = k*b;
alpha = 1/7;
[t, y] = ode45(@odeseir , ts ,y0 , [], beta ,gamma ,alpha ,N);
plot(t,y);
xlabel('Time (days)'); ylabel('Population ')
legend('S', 'E', 'I', 'R')
def odeseir(t, y, beta , gamma , alpha , N):
    dy = [ -beta*y(1)*y(2)/N;
          beta*y(1)*y(2)/N - alpha*y(2);
          alpha*y(2) - gamma*y(3)
          gamma*y(3)];
    return dy

## 元胞自动机模型
m = 500;n = 500; % 元胞自动空间大小
# 用1 , 2 , 3 , 4 分别表示S , E , I , R . 无人区域用0 表示
[S, E, I, R] = deal (1,2,3,4);

rhoS = 0.95; % 初始易感人群密度
rhoE = 2758/11000000; % 初始潜伏人群密度

# X 为每个元胞的状态
X = zeros(m,n); X(rand(m,n)<rhoS) = S; X(rand(m,n)<rhoE) = E;

time = zeros(m,n); % 计时： 用于计算潜伏时间和治疗时间
# 邻居方位d
d = {[1,0], [0,1], [-1,0], [0,-1]};

T = 7; % 平均潜伏期
D = 14; % 平均治愈时间
P = 3.6/T/4; % R0 = 3.6 ， 潜伏期平均感染3.6 个

# 每个元胞的潜伏期和治愈时间服从均值为T 和D 的正态分布
Tmn = normrnd(T,T/2,m,n); Dmn = normrnd(D,D/2,m,n);

figure('position ' ,[50 ,50 ,1200 ,400])
subplot (1,2,1)
h1 = imagesc(X);
colormap(jet (5))
labels = {'无人',' 易感',' 潜伏',' 发病',' 移除'};
lcolorbar(labels);
subplot (1,2,2)
h2 = plot(0, [0,0,0,0]); axis ([0,400,0,m*n])

for t = 1:450
# 邻居中潜伏和发病的元胞数量
N = zeros(size(X));
for j = 1: length(d)
N = N + (circshift(X,d{j})==E|circshift(X,d{j})==I);
end
# 分别找出四种状态的元胞
isS = (X==S); isE = (X==E); isI = (X==I); isR = (X==R);

# 将四种状态的元胞数量存到Y 中
Y(t,:) = sum([isS (:) isE (:) isI (:) isR (:)]);

# 计算已经潜伏的时间和已经治疗的时间
time(isE|isI) = time(isE|isI) + 1;

# 规则一： 如果S 邻居有N 个染病的， 则S 以概率N * P 变为E ， 否则保持为S
ifS2E = rand(m,n) <(N*P);
Rule1 = E*(isS & ifS2E) + S*(isS & :ifS2E);

# 规则二： 如果E 达到潜服期， 则转变为I ， 否则保持为E
ifE2I = time >Tmn;
Rule2 = I*(isE & ifE2I) + E*(isE & :ifE2I);
time(isE & ifE2I) = 0;

# 规则三： 如果I 达到治愈时间， 则转变为R ， 否则保持为I
ifI2R = time >Dmn;
Rule3 = I*(isI & :ifI2R) + R*(isI & ifI2R);

# 规则四： 已经治愈R 有抗体， 保持为R
Rule4 = R*isR;

# 叠加所有规则， 更新所有元胞状态
X = Rule1 + Rule2 + Rule3 + Rule4;

set(h1 , 'CData ', X);
for i = 1:4; set(h2(i), 'XData ', 1:t, 'YData ', Y(1:t,i)); end
drawnow
end

 
 
 
 
      