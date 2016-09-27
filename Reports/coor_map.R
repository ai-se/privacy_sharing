library(ggplot2)
library(reshape)
library(scales)
library(corrplot)
school=read.csv('~/Desktop/school.csv')
s=as.matrix(as.data.frame(school))

#create correlation matrix
cor_jnk=cor(s)
#plot cor matrix
corrplot(cor_jnk, order="AOE", method="circle", tl.pos="lt", type="upper",        
         tl.col="black", tl.cex=0.6, tl.srt=45, 
         addCoef.col="black",
         p.mat = 1-abs(cor_jnk), sig.level=0.50, insig = "blank")  

