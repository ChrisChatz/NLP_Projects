from tabulate import tabulate

def rightChild(row,col,cky,nodes,level,words):
    tmp=nodes[row][col]
    if tmp=="terminal":
        print "\t"*level,"(%s %s)" %(cky[row][col],words[row])       
    else:
        print "\t"*level,"(%s" %cky[row][col]
        level+=1
        [r1,r2], [l1,l2]=tmp
        rightChild(r1,r2,cky,nodes,level,words)
        leftChild(l1,l2,cky,nodes,level,words)
        print "\t"*(level-1),")"
    
def leftChild(row,col,cky,nodes,level,words):
    tmp=nodes[row][col]
    if tmp=="terminal":
        print "\t"*level,"(%s %s)" %(cky[row][col],words[row])
    else:
        print "\t"*level,"(%s" %cky[row][col]
        level+=1
        [r1,r2], [l1,l2]=tmp
        rightChild(r1,r2,cky,nodes,level,words)
        leftChild(l1,l2,cky,nodes,level,words)
        print "\t"*(level-1),")"
        
def readGrammar():
    f = open("grammar")
    grammarLines = f.readlines()
    grammarLines = [line.replace(" -> ", " ").split(" ") for line in grammarLines]
    terminal = []
    nonterminal = []
    for line in grammarLines:
        line = [i.strip() for i in line]
        if len(line) == 2:
            terminal.append(line)
        else:
            nonterminal.append(line)

    return terminal, nonterminal

def checkGrammar(turn, word, terminal, nonterminal):
    if turn == "initialiaze":
        for t in terminal:
            if t[1] == word:
                return t[0]
    else:
        rule = word.split(",")
        left = rule[0]
        right = rule[1]
        f = []
        for nt in nonterminal:
            if left == nt[1] and right == nt[2]:
                f.append(nt[0])
        return ','.join(f)

terminal,nonterminal=readGrammar()
sentence="she eats a fish with a fork"
words= sentence.split(" ")
rows=len(words)
columns= len(words)+1
           
CKYtable=[["" for j in range(columns)] for i in range(rows)]

storedNodes=[[[] for j in range(columns)] for i in range(rows)]
#Initialize CKY table with terminal grammar and X's
for j in range(0,columns):
    for i in range(rows):
        if j>i:
            if i+1==j:
                CKYtable[i][j] = checkGrammar("initialiaze", words[i], terminal, nonterminal)
                storedNodes[i][j]="terminal"
        else:
            CKYtable[i][j] = "X"
            
#Fill up the rest of the table
tmpList=[]
for j in range(1,columns):
    for i in range(rows,-1,-1):
        if j>i+1:
            tmpList = ""
            for k in range(1,j):
                if (CKYtable[i][k] != "X" and CKYtable[k][j] != "X") and (CKYtable[i][k] != "" and CKYtable[k][j] != ""):
                    tmpList = CKYtable[i][k] + "," + CKYtable[k][j]
                    if CKYtable[i][j] == checkGrammar("other", tmpList, terminal, nonterminal):
                        CKYtable[i][j] = checkGrammar("other", tmpList, terminal, nonterminal)
                    elif checkGrammar("other", tmpList, terminal, nonterminal) != "": 
                        CKYtable[i][j] += checkGrammar("other", tmpList, terminal, nonterminal)
                        storedNodes[i][j].extend([[i, k], [k, j]])

#print cky table
print tabulate(CKYtable) 

#print syntax tree"
print "The syntax tree/trees is/are the following:"
count=1;
level=1;
for i in range(rows):
    for j in range(columns):
        if CKYtable[i][j]=="S":
            print "------------%s sentence-----------" %count
            print "(S"
            count+=1
            [r1,r2], [l1,l2]=storedNodes[i][j]
            rightChild(r1,r2,CKYtable,storedNodes,level,words)
            leftChild(l1,l2,CKYtable,storedNodes,level,words)
            print ")"