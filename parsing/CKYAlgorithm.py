from tabulate import tabulate

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

#Initialize CKY table with terminal grammar and X's
for j in range(0,columns):
    for i in range(rows):
        if j>i:
            if i+1==j:
                CKYtable[i][j] = checkGrammar("initialiaze", words[i], terminal, nonterminal)
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

#print cky table
print tabulate(CKYtable)     