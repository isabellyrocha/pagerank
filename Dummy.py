
class InfluxTest():
    def __init__(self):
        self.data = {}
    
    def write_rank(self, page: int, iteration: int, rank: float):
        self.data[(page, iteration)] = rank

    def get_rank(self, page: int, iteration: int) -> float:
        return self.data[(page, iteration)]
