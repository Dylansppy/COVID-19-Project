data <- read.csv("Country_Level_Info.csv", header=TRUE)

subdata <- data[data[,'Country_Region'] == 'China', ]
print(subdata)

ggplot(subdata, aes(Date, New_Confirmed_Cases)) + geom_line() + xlab(" ") + ylab("Daily Views")

country_name <- unique(data[,"Country_Region"])

print(country_name)

data$Date <- as.Date(data$Date)
typeof(data$Date)
print(data)


# 定义初始状态各人数
N = 10000
E = 0
I = 1
S = N-I
R = 0

# 常量赋值
r = 20
B = 0.03
a = 0.1
y = 0.1

#设置时间观察到第150天
T = 150

#用for循环的方式构建上述方程组
for (i in 1:(T-1)){
  S[i+1] = S[i] - r*B*S[i]*I[i]/N
  E[i+1] = E[i] + r*B*S[i]*I[i]/N - a*E[i]
  I[i+1] = I[i] + a*E[i] - y*I[i]
  R[i+1] = R[i] + y*I[i]
  
}

#生成表格并查看，表格就是每天S、E、I、R的值
result <- data.frame(S, E, I, R)
View(result)

#作图
X_lim <- seq(1,T,by=1)
plot(S~X_lim, pch=15, col="DarkTurquoise", main = "SEIR Model", type = "l", xlab = "时间T", ylab = "各人数", xlim = c(0,T), ylim = c(0,10000))
lines(S, col="DeepPink", lty=1) 
lines(E, col="DarkTurquoise", lty=1)
lines(I, col="RosyBrown", lty=1)
lines(R, col="green", lty=1)
legend(120,8000,c("S","E","I","R"),col=c("DeepPink","DarkTurquoise","RosyBrown"),text.col=c("DarkTurquoise","DeepPink","RosyBrown","Green"),lty=c(1,1,1,1))
