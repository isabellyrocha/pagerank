

class Page:
    def __init__(self, name):
        self.name = name
        self.rank = None
        self.in_connections = []
        self.num_out_connections = 0

    def get_name(self):
        return self.name;
        
    def add_in_connection(self, page):
        self.in_connections.append(page)
    
    def get_in_connections(self):
        return self.in_connections
        
    def add_out_connection(self):
        self.num_out_connections = self.num_out_connections + 1

    def get_out_connections(self):
        return self.num_out_connections
