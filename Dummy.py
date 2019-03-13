
class InfluxTest():
    def __init__(self):
        self.data = {}
    
    def write_rank(self, page, iteration, rank):
        self.data[(page, iteration)] = rank

    def get_rank(self, page, iteration):
        return self.data[(page, iteration)]
