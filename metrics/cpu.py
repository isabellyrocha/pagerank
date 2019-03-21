from datetime import datetime

timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    

def main():
    parser = ArgumentParser(description='rank page')
    parser.add_argument('--node', nargs='?', const='root', metavar='influx-user', type=str,
                        help='string corresponding to the node name')
    
    args = parser.parse_args()

    metrics_storage = InfluxDB(args)
    
    cmd = ['ssh', '-oStrictHostKeyChecking=no', '%s.maas' % (args.node), 'top', '-b', '-d1', '-n1', '|', 'grep', '-i', '"Cpu(s)"', '|', 'head', '-c21', '|', 'cut', '-d', '' '', '-f3', '|', 'cut', '-d', "'%'", '-f1']
    result = subprocess.run(cmd, stdout=subprocess.PIPE)
    result.stdout.decode('utf-8')

if __name__ == '__main__':
    main()
