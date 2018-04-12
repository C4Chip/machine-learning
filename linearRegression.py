import matplotlib.pyplot as plt

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

def linearReg(xarray,yarray):
    m_x=mean(xarray)
    m_y=mean(yarray)
    n=float(len(xarray))
    ssxy=0.000
    ssxx=0.0000
    for x,y in zip(xarray,yarray):
        ssxy=ssxy+(x*y-n*m_x*m_y)
    for x in xarray:
        ssxx=ssxx+(x*x-n*m_x*m_x)
    b1=ssxy/ssxx
    b0=m_y-b1*m_x
    plt.scatter(xarray,yarray,color='r',marker='o')
    y_pred=[]
    for ele in xarray:
        y_pred.append(ele*b1+b0)    
    plt.plot(xarray,y_pred, color = "g")
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()

xarr=[]
yarr=[]

filename = "linearTrainingData.csv"
with open(filename) as file:
    #skip the first line
    file.readline()
    for line in file.readlines():
        x,y= line.strip().split(',')
        x = float(x)
        y=float(y)
        xarr.append(x)
        yarr.append(y)
        
linearReg(xarr,yarr)

