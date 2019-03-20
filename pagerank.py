from __future__ import division
from argparse import ArgumentParser
from page import Page
from metrics.Dummy import InfluxTest
from metrics.InfluxDB import InfluxDB
import traceback

class PageRank:
    def __init__(self, args):
        #self.metrics_storage = InfluxDB(args)
        self.metrics_storage = InfluxTest()
        self.iterations = args.iterations
        self.number_of_nodes = args.number_of_nodes
        self.node_id = args.node_id
        self.pages = {}

        self.load_graph(args.pages_file_name)
        
    def load_graph(self, pages_file_name):
        with open(pages_file_name) as pages_file:
            for line in pages_file:
                if (not line.startswith('#')):
                    line_array = line.split('\t')
                    
                    fromNodeId = int(line_array[0])
                    toNodeId = int(line_array[1].rstrip())
                    
                    fromPage = self.get_page(fromNodeId)
                    toPage = self.get_page(toNodeId)
                    
                    toPage.addInConnection(fromPage)
                    fromPage.addOutConnection()
                    
    def get_page(self, pageId):
        if (pageId not in self.pages.keys()):
            self.pages[pageId] = Page(pageId)
        return self.pages[pageId]

    def compute_next_rank(self, page, iteration):
        next_rank = 0
        for connection in self.pages[page].getInConnections():
            connection_rank = self.metrics_storage.get_rank(int(connection.getID()), iteration-1)
            number_of_out_connections = connection.getOutConnections()
            next_rank += connection_rank/number_of_out_connections
        self.metrics_storage.write_rank(page, iteration, next_rank)
    
    def compute_final_rank(self):
        final_rank = {}
        for page in self.pages.values():
            pageId = page.getID()         
            rank = self.metrics_storage.get_rank(pageId, self.iterations)
            final_rank[rank] = pageId
        print(final_rank)
    
    def run(self):
        self.metrics_storage.create_database()
        
        total_pages = list(self.pages.keys())
        pages_per_node = int(len(total_pages)/self.number_of_nodes)
        node_pages = total_pages[(pages_per_node*self.node_id):(pages_per_node*(self.node_id+1))]

        initial_rank = 1/len(total_pages)
        for page in node_pages:
            self.metrics_storage.write_rank(page, 0, initial_rank)
        
        for i in range(1, self.iterations+1):
            try:
                for page in node_pages:
                    self.compute_next_rank(page, i)
            except Exception:
                traceback.print_exc()
                pass
        self.metrics_storage.drop_database()
                
def main():
    parser = ArgumentParser(description='rank page')
    parser.add_argument('--pages-file-name', nargs='?', const='page-rank', metavar='pagerank-input', type=str,
                        help='string corresponding to the name of file to be used as input')
    parser.add_argument('--iterations', nargs='?', const='page-rank', metavar=3, type=int,
                        help='integer corresponding to the number of iterations the algorithm should perform')
    parser.add_argument('--number-of-nodes', nargs='?', const='number-of-nodes', metavar=3, type=int,
                        help='integer corresponding to the number of nodes the algorithm will be running in')
    parser.add_argument('--node-id', nargs='?', const='page-rank', metavar=3, type=int,
                        help='integer corresponding to the id of the corresponding node')
    parser.add_argument('--influx-user', nargs='?', const='root', metavar='influx-user', type=str,
                        help='string corresponding to the user name of the influx database')
    parser.add_argument('--influx-pass', nargs='?', const='root', metavar='influx-pass', type=str,
                        help='string corresponding to the password of the influx database')
    parser.add_argument('--influx-host', metavar='influx-host', type=str,
                        help='string corresponding to the host address of the influx database')
    parser.add_argument('--influx-port', metavar='influx-port', type=int,
                        help='int corresponding to the port of the influx database')
    parser.add_argument('--influx-database', nargs='?', const='k8s', metavar='influx-database', type=str,
                        help='string corresponding to the name of the influx database')
    parser.add_argument('-D', nargs='?', const='DEBUG', metavar='DEBUG', type=str,
                        help='Flag to decide if we want the debug mode or not')

    args = parser.parse_args()
    page_rank = PageRank(args)
    page_rank.run()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass       
        
    
