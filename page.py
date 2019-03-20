

class Page:
    def __init__(self, name):
        self.ID = name
        self.inConnections = []
        self.numOutConnections = 0

    def getID(self):
        return self.ID;
        
    def addInConnection(self, page):
        self.inConnections.append(page)
    
    def getInConnections(self):
        return self.inConnections
        
    def addOutConnection(self):
        self.numOutConnections = self.numOutConnections + 1

    def getOutConnections(self):
        return self.numOutConnections
