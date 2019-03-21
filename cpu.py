import subprocess
import os
from metrics.influxdb import InfluxDB
from argparse import ArgumentParser
from datetime import datetime
import time

#timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    

def main():
    parser = ArgumentParser(description='rank page')
    parser.add_argument('--node', nargs='?', const='root', metavar='influx-user', type=str,
                        help='string corresponding to the node name')
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
    args = parser.parse_args()
    node = args.node
    metrics_storage = InfluxDB(args)
    
    #cmd = ['ssh', '-oStrictHostKeyChecking=no', '%s.maas' % (node), 'top', '-b', '-d1', '-n1', '|', 'grep', '-i', '"Cpu(s)"', '|', 'head', '-c21', '|', 'cut', '-d', "\' \'", '-f3', '|', 'cut', '-d', "'%'", '-f1']
    cmd = ['ssh', '.maas' % (node), 'sar', '-P', 'ALL', '1', '1', '|', 'grep', '"Average:        all"|cut', '-b', '24,25,26,27,28,29,30']
    while True:
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        result = subprocess.run(cmd, stdout=subprocess.PIPE)
        cpu = float(result.stdout.decode('utf-8').strip())
        metrics_storage.write_cpu(timestamp, node, cpu)
        time.sleep(1)

if __name__ == '__main__':
    main()
