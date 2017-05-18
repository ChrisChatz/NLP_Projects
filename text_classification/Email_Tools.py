import pickle

def createObjFile(listT,fileName):
    object_pi=listT
    file_pi = open(fileName, 'w') 
    pickle.dump(object_pi, file_pi) 
    file_pi.close()

def readFileReturnList(filename):
    fileT = open(filename, 'r') 
    listT = pickle.load(fileT)
    fileT.close()
    return listT