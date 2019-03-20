
class InfluxTest():
    def __init__(self):
        self.data = {}
    
    def write_rank(self, page, iteration, rank):
        self.data[(page, iteration)] = rank

    def get_rank(self, page, iteration):
        result = self.data[(page, iteration)]
        return result
        
    def create_database(self):
        self.data = {}
        
    def drop_database(self):
        self.data = {}
