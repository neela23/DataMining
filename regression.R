library(MASS)
library(ISLR)
dt<-read.csv("C:/sneha/spring16/Data_Mining/Project/code/scores.csv")

newdata <- dt[which(dt$food!=0), ]

newdata$reviewnum<-seq(1, 554, by=1)
newdata.train<-newdata[1:400,1:length(newdata)]
newdata.test<-data.frame(newdata[400:554,1:(length(newdata)-1)])
label<-data.frame(newdata[400:554,1],newdata[400:554,length(newdata)])

#linear regression Model fitting

lm.fit.mult <- lm(stars ~ food + service + place + price,data = newdata.train)
summary(lm.fit.mult)
result<-predict(lm.fit.mult,newdata.test )
result<-data.frame(round(result,0),newdata[400:554,length(newdata)])
normalized = ((result$round.result..0.-min(result$round.result..0.))/(max(result$round.result..0.)-min(result$round.result..0.))*4)+1
result$round.result..0.=normalized
plot(result$round.result..0.,result$newdata.400.554..length.newdata..)

#svr
library(e1071)
svm.fit<-svm(stars ~ food + service + place + price,data = newdata.train,kernel="radial",cost = 5)
svm.result<-predict(svm.fit,newdata.test)
summary(svm.fit)
svm.result<-data.frame(round(svm.result,0),newdata[400:554,length(newdata)])
plot(svm.result$round.svm.result..0.,svm.result$newdata.400.554..length.newdata..)
normalized = ((svm.result$round.svm.result..0.-min(svm.result$round.svm.result..0.))/(max(svm.result$round.svm.result..0.)-min(svm.result$round.svm.result..0.))*4)+1
svm.result$round.svm.result..0.=normalized
plot(svm.result$round.svm.result..0.,svm.result$newdata.400.554..length.newdata..)
#training error
set.seed(10)
tune.out = tune(svm, stars ~ food + service + place + price, data = newdata.train, kernel="radial", ranges = list(cost = c(0.01, 0.1, 1, 5, 10, 100)))
summary(tune.out)
bmodel =tune.out$best.model
summary (bmodel)

#error
rmse <- function(error)
{
  sqrt(mean(error^2))
}
mape <- function(error)
{
  mean(abs(1-error)*100)
}

###linear regression errors 

error=result$round.result..0.-result$newdata.400.554..length.newdata..
lm.error<-rmse(error)

m_error=result$round.result..0./result$newdata.400.554..length.newdata..
m.lm.error<-mape(m_error)

###SVR errors

error=svm.result$round.svm.result..0.- svm.result$newdata.400.554..length.newdata..
svm.error<-rmse(error)

m_error=svm.result$round.svm.result..0./svm.result$newdata.400.554..length.newdata..
m.svm.error<-mape(m_error)
