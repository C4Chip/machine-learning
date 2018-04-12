import math
import random

raw_training=[]
raw_target=[]
raw_test=[]
raw_test_ans=[]
test_pre=[]
with open("logicTraining.txt","r") as f_training:
    for line in f_training:
        line=line.split(',')
        line=list(map(int,line))
        raw_target.append(line.pop())
        line.pop(0)
        raw_training.append(line)
with open("logciTest.txt","r") as f_training:
    for line in f_training:
        line=line.split(',')
        line=list(map(int,line))
        raw_test_ans.append(line.pop())
        line.pop(0)
        raw_test.append(line)

def prediction(nums,weights):
    pre=0.0
    for num,weight in zip(nums,weights):
        pre=pre+num*weight
    result=1/(1+math.exp(-pre))
    return result

def logicReg(training,target,learnRate):
    weights=[]
    for i in range (9):
        weights.append(0)
    for ele,tar in zip(training,target):
        p=prediction(ele,weights)
        dlt=tar-p
        for i in range(9):
            weights[i]=weights[i]+learnRate*dlt*p*(1-p)*ele[i]
    return weights
def ConfusionMat(ans,pred):
    countnono=0
    countnoyes=0
    countyesno=0
    countyesyes=0
    for numa,nump in zip(ans,pred):
        if numa==4 and nump==4:
            countyesyes+=1
        elif numa==4 and nump==2:
            countyesno+=1
        elif numa==2 and nump==2:
            countnono+=1
        else:
            countnoyes+=1
    print ("\tpredict no  "+"  predict yes")
    print ("actual no: "+repr(countnono)+"  "+repr(countnoyes))
    print ("actual yes: "+repr(countyesno)+"  "+repr(countyesyes))
    print ("report: \n")

    precision4=float(countyesyes/(countyesyes+countnoyes))
    recall4=float(countyesyes/(countyesyes+countyesno))
    f1score4=float(2/(1/recall4+1/precision4))

    precision2=float(countnono/(countnono+countyesno))
    recall2=float(countnono/(countnono+countnoyes))
    f1score2=float(2/(1/recall2+1/precision2))
    print("\tprecision"+"  recall"+"  f1-score")
    print("2\t"+repr(precision2)+"  "+repr(recall2)+"  "+repr(f1score2))
    print("4\t"+repr(precision4)+"  "+repr(recall4)+"  "+repr(f1score4))





lt=5e-5
testWeights=logicReg(raw_training,raw_target,lt)
for ele in raw_test:
    res=0
    for i in range(9):
        res=res+ele[i]*testWeights[i]
    if res>1:
        test_pre.append(4)
    else:
        test_pre.append(2)
print ("confusion matrix \n")
ConfusionMat(raw_test_ans,test_pre)
