from csv import reader

def load_csv(filename):
    file = open(filename, "r")
    lines = reader(file)
    dataset = list(lines)
    return dataset

def confusion_report(ans,pred):
    countyesyes=0
    countnono=0
    countyesno=0
    countnoyes=0
    right='yes'
    wrong='no'
    for i in range(len(ans)):
        if ans[i]==right and pred[i]==right:
            countyesyes+=1
        elif ans[i]==right and pred[i]==wrong:
            countyesno+=1
        elif ans[i]==wrong and pred[i]==wrong:
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
    print("no\t"+repr(precision2)+"  "+repr(recall2)+"  "+repr(f1score2))
    print("yes\t"+repr(precision4)+"  "+repr(recall4)+"  "+repr(f1score4))

def evaluate_dt(trainset,testset,algodt,deep,size):
    predicted=algodt(trainset,testset,deep,size)
    ans=[ele[-1] for ele in testset]
    confusion_report(ans,predicted)


def try_split(index,value,data):
    left=list()
    right=list()
    for ele in data:
        if ele[index] <value:
            left.append(ele)
        else:
            right.append(ele)
    return left,right
#calculate entory
def entory(groups,classes):
    from math import log
    ent=0
    for gourp in groups:
        gsize=len(gourp)
        if gsize==0:
            continue
        logsum=0
        for ele in classes:
            num=[mem[-1] for mem in gourp].count(ele)
            p=float(num/gsize)
            if p==0:
                logsum=logsum
            else:
                logsum=logsum+p*(log(p)/log(2))
        ent=ent-logsum

    return ent

# Select the best split point for a dataset

def create_split(data):
    values=list(set(ele[-1] for ele in data))
    tem_index=999
    tem_value=999
    tem_score=999
    tem_group=None
    for i in range(len(data[0])-1):
        for ele in data:
            groups=try_split(i,ele[i],data)
            ent=entory(groups,values)
            if ent <tem_score:
                tem_index=i
                tem_value=ele[i]
                tem_score=ent
                tem_group=groups
    
    return {'index':tem_index, 'value':tem_value, 'groups':tem_group}

# Create a terminal node value
def to_terminal(group):
    outcomes = [row[-1] for row in group]
    return max(set(outcomes), key=outcomes.count)
def stoppoint(group):
    res=[row[-1] for row in group]
    return (max(set(res), key=res.count))

# Create child splits for a node or make terminal
def split(vertex, max_depth, size, depth):
    left, right = vertex['groups']
    del(vertex['groups'])
    # check for a no split
    if not left or not right:
        vertex['left'] = vertex['right'] = stoppoint(left + right)
        return
    # check for max depth
    if depth >= max_depth:
        vertex['left'], vertex['right'] = stoppoint(left), stoppoint(right)
        return
    # process left child
    if len(left) <= size:
        vertex['left'] = stoppoint(left)
    else:
        vertex['left'] = create_split(left)
        split(vertex['left'], max_depth, size, depth+1)
    # process right child
    if len(right) <= size:
        vertex['right'] = stoppoint(right)
    else:
        vertex['right'] = create_split(right)
        split(vertex['right'], max_depth,size, depth+1)


def build_tree(train, max_depth, size):
    root = create_split(train)
    split(root, max_depth, size, 1)
    return root


def predict(vertex,row):
    if row[vertex['index']] < vertex['value']:
        if isinstance(vertex['left'],dict):
            return predict(vertex['left'],row)
        else:
            return vertex['left']
    else:
        if isinstance(vertex['right'],dict):
            return predict(vertex['right'],row)
        else:
            return vertex['right']

def decision_tree(train,test,max_deep,size):
    tree=build_tree(train,max_deep,size)
    predicts=list()
    for ele in test:
        pred=predict(tree,ele)
        predicts.append(pred)
    return (predicts)

deep=5
size=10
filename = "Assignment 4 - Question 3 training data.csv"
filename2="Assignment4 - Question 3  test_data.csv"
train_data=load_csv(filename)
test_data=load_csv(filename2)
evaluate_dt(train_data,test_data,decision_tree,deep,size)