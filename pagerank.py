from __future__ import division
from argparse import ArgumentParser
from page import Page
from Dummy import InfluxTest
from InfluxDB import InfluxDB
import traceback

class PageRank:
    def __init__(self, args):
        self.metrics_storage = InfluxDB(args)
        #self.metrics_storage = InfluxTest()
        self.pages_file_name = args.pages_file_name
        self.iterations = args.iterations
        self.start = args.start
        self.end = args.end
        self.pages = {}
        page_index = 0
        with open(self.pages_file_name) as pages_file:
            for line in pages_file:
                if not self.pages:
                    line_array = line.split(" ")
                    for page_name in line_array:
                        self.pages[int(page_name)] = Page(page_name)
                else:
                    line_array = line.split(" ")
                    page = self.pages[int(line_array[0])]
                    inConnections = line_array[0:]
                    for page_name in inConnections:
                        in_connection = self.pages[int(page_name)]
                        page.add_in_connection(in_connection)
                        in_connection.add_out_connection(page)
                
    
    def compute_next_rank(self, page: int, iteration: int):
        next_rank = 0
        for connection in self.pages[page].get_in_connections():
            connection_rank = self.metrics_storage.get_rank(int(connection.get_name()), iteration-1)
            number_of_out_connections = connection.get_out_connections()
            next_rank += connection_rank/number_of_out_connections
        self.metrics_storage.write_rank(page, iteration, next_rank)
        
    def run(self):
        pages = self.pages.keys()
        initial_rank = 1/len(pages)
        
        for page in range(self.start, self.end+1):
            self.metrics_storage.write_rank(page, 0, initial_rank)
        
        for i in range(1, self.iterations):
            try:
                for page in range(self.start, self.end+1):
                    self.compute_next_rank(page, i)
            except Exception:
                traceback.print_exc()
                pass
    
def main():
    parser = ArgumentParser(description='rank page')
    parser.add_argument('--pages-file-name', nargs='?', const='page-rank', metavar='pagerank-input', type=str,
                        help='string corresponding to the name of file to be used as input')
    parser.add_argument('--iterations', nargs='?', const='page-rank', metavar=3, type=int,
                        help='integer corresponding to the number of iterations the algorithm should perform')
    parser.add_argument('--start', nargs='?', const='page-rank', metavar=0, type=int,
                        help='int corresponding to the name of page the program should start')
    parser.add_argument('--end', nargs='?', const='page-rank', metavar=0, type=int,
                        help='int corresponding to the name of page the program should end')
    
    args = parser.parse_args()
    page_rank = PageRank(args)
    
    page_rank.run()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass       
        
    
