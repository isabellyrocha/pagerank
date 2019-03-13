

class Page:
    def __init__(self, name):
        self.name = name
        self.rank = None
        self.in_connections = []
        self.out_connections = []

    def get_name(self):
        return self.name;
        
    def add_in_connections(self,pages):
        self.in_connections = pages
        
    def add_in_connection(self, page):
        self.in_connections.append(page)
    
    def get_in_connections(self):
        return self.in_connections
        
    def add_out_connection(self, page):
        self.out_connections.append(page)

    def add_out_connections(self, pages):
        self.in_connections = pages

    def get_out_connections(self):
        return len(self.out_connections)
