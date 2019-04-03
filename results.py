from metrics.influxdb import InfluxDB
from datetime import datetime
from datetime import timedelta
import numpy as np
from argparse import ArgumentParser
from metrics.kubernetes import Kubernetes  
                    
def main():
    parser = ArgumentParser(description='rank page')
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
    k8s = Kubernetes()
    metrics_storage = InfluxDB(args)
    output_mean = open('output_mean','w') 
    output_seq = open('output_seq','w')
    output_dist_2n_0 = open('output_dist_2n_0','w')
    output_dist_2n_1 = open('output_dist_2n_1','w')
    output_dist_3n_0 = open('output_dist_3n_0','w')
    output_dist_3n_1 = open('output_dist_3n_1','w')
    output_dist_3n_2 = open('output_dist_3n_2','w')
    
    finished_pods = k8s.list_finished_pods()
    grouped_cpu_results = {'dist2n': {}, 'dist3n': {}, 'seq': []}
    grouped_power_results = {'dist2n': {}, 'dist3n': {}, 'seq': []}
    grouped_duration_results = {'dist2n': {}, 'dist3n': {}, 'seq': []}
    power_results_by_min = {'dist2n': {}, 'dist3n': {}, 'seq': []}
    cpu_results_by_min  = {'dist2n': {}, 'dist3n': {}, 'seq': []}
    for pod in finished_pods:
        started = int(k8s.get_started_at(pod))*1000000000
        finished = int(k8s.get_finished_at(pod))*1000000000
        host = k8s.get_host_node(pod)
        pod_name = k8s.get_name(pod)
        cpu_values = metrics_storage.get_cpu(host, started, finished)
        cpu_by_min = metrics_storage.get_grouped_cpu(host, started, finished)
        power_values = metrics_storage.get_power(host, started, finished)
        power_by_min = metrics_storage.get_grouped_power(host, started, finished)
        pod_duration = (finished - started)/1000000000
        pod_type = pod_name.split("-")[1]
        if pod_type == 'dist2n' or pod_type == 'dist3n':
            pod_id = pod_name.split("-")[3]
            if pod_id not in grouped_cpu_results[pod_type].keys():
                grouped_cpu_results[pod_type][pod_id] = []
                grouped_power_results[pod_type][pod_id] = []
                grouped_duration_results[pod_type][pod_id] = []
                power_results_by_min[pod_type][pod_id] = []
                cpu_results_by_min[pod_type][pod_id] = []
            #print(grouped_cpu_results)
            grouped_cpu_results[pod_type][pod_id].append(cpu_values)
            grouped_power_results[pod_type][pod_id].append(power_values)
            grouped_duration_results[pod_type][pod_id].append(pod_duration)
            power_results_by_min[pod_type][pod_id].append(power_by_min)
            cpu_results_by_min[pod_type][pod_id].append(cpu_by_min)
        else:
            grouped_cpu_results[pod_type].append(cpu_values)
            grouped_power_results[pod_type].append(power_values)
            grouped_duration_results[pod_type].append(pod_duration)
            power_results_by_min[pod_type].append(power_by_min)
            cpu_results_by_min[pod_type].append(cpu_by_min)
        #pod_cpu = np.mean(cpu_values)
        #pod_energy = np.trapz(power_values)
        #print(pod_name + "," + str(pod_cpu) + "," + str(pod_energy) + "," + str(pod_duration))
    #print(grouped_cpu_results)
    
    cpu_seq = 0
    for cpu_values in grouped_cpu_results['seq']:
        cpu_seq += np.mean(cpu_values)
    cpu_seq = cpu_seq/len(grouped_cpu_results['seq'])
    
    energy_seq = 0
    for energy_values in grouped_power_results['seq']:
        energy_seq += np.trapz(energy_values)
        print(np.trapz(energy_values))
    energy_seq = energy_seq/len(grouped_power_results['seq'])

    duration_seq = 0
    for duration in grouped_duration_results['seq']:
        duration_seq += duration
    duration_seq = duration_seq/len(grouped_duration_results['seq'])
    
    cpu_dist = {'0': 0, '1': 0}
    for dist_id in grouped_cpu_results['dist2n'].keys():
        for cpu_values in grouped_cpu_results['dist2n'][dist_id]:
            if cpu_values != None:
                cpu_dist[dist_id] += np.mean(cpu_values)
        if (dist_id in grouped_cpu_results['dist2n'].keys()) > 0:
            cpu_dist[dist_id] = cpu_dist[dist_id]/len(grouped_cpu_results['dist2n'][dist_id])

    energy_dist = {'0': 0, '1': 0}
    for dist_id in grouped_power_results['dist2n'].keys():
        for energy_values in grouped_power_results['dist2n'][dist_id]:
            energy_dist[dist_id] += np.trapz(energy_values)
        energy_dist[dist_id] = energy_dist[dist_id]/len(grouped_power_results['dist2n'][dist_id])

    energy_dist3 = {'0': 0, '1': 0, '2':0}
    for dist_id in grouped_power_results['dist3n'].keys():
        for energy_values in grouped_power_results['dist3n'][dist_id]:
            energy_dist3[dist_id] += np.trapz(energy_values)
        energy_dist3[dist_id] = energy_dist3[dist_id]/len(grouped_power_results['dist3n'][dist_id])

    duration_dist = {'0': 0, '1': 0}
    for dist_id in grouped_duration_results['dist2n'].keys():
        for duration in grouped_duration_results['dist2n'][dist_id]:
            duration_dist[dist_id] += duration
        duration_dist[dist_id] = duration_dist[dist_id]/len(grouped_duration_results['dist2n'][dist_id])
    
    duration_dist3 = {'0': 0, '1': 0, '2': 0}
    for dist_id in grouped_duration_results['dist3n'].keys():
        for duration in grouped_duration_results['dist3n'][dist_id]:
            duration_dist3[dist_id] += duration
        duration_dist3[dist_id] = duration_dist3[dist_id]/len(grouped_duration_results['dist3n'][dist_id])

    output_mean.write("1 "+str(energy_seq)+" "+str(duration_seq)+"\n")
    #print(np.sum(energy_dist.values()))
    output_mean.write("2 "+str(sum(energy_dist.values()))+" "+str(max(duration_dist.values()))+"\n")
    output_mean.write("3 "+str(sum(energy_dist3.values()))+" "+str(max(duration_dist3.values()))+"\n")
    
    power_by_min_seq = power_results_by_min['seq'][0]
    cpu_by_min_seq = cpu_results_by_min['seq'][0]
    power_by_min_dist_0 = power_results_by_min['dist2n']['0'][0]
    power_by_min_dist_1 = power_results_by_min['dist2n']['1'][0]
    cpu_by_min_dist_0 = cpu_results_by_min['dist2n']['0'][0]
    cpu_by_min_dist_1 = cpu_results_by_min['dist2n']['1'][0]
    cpu_by_min_dist3_0 = cpu_results_by_min['dist3n']['0'][0]
    cpu_by_min_dist3_1 = cpu_results_by_min['dist3n']['1'][0]
    cpu_by_min_dist3_2 = cpu_results_by_min['dist3n']['2'][0]
    power_by_min_dist3_0 = power_results_by_min['dist3n']['0'][1]
    power_by_min_dist3_1 = power_results_by_min['dist3n']['1'][1]
    power_by_min_dist3_2 = power_results_by_min['dist3n']['2'][1]


    for i in range(len(power_by_min_seq)):
        output_seq.write("%d %f %f\n" % (i, power_by_min_seq[i], cpu_by_min_seq[i]))
    for i in range(len(power_by_min_dist_0)):
        output_dist_2n_0.write("%d %f %f\n" % (i, power_by_min_dist_0[i], cpu_by_min_dist_0[i]))
    for i in range(len(power_by_min_dist_1)):
        output_dist_2n_1.write("%d %f %f\n" % (i, power_by_min_dist_1[i], cpu_by_min_dist_1[i]))
    for i in range(len(cpu_by_min_dist3_0)):
        output_dist_3n_0.write("%d %f %f\n" % (i, power_by_min_dist3_0[i], cpu_by_min_dist3_0[i]))
    for i in range(len(cpu_by_min_dist3_1)):
        output_dist_3n_1.write("%d %f %f\n" % (i, power_by_min_dist3_1[i], cpu_by_min_dist3_1[i]))
    for i in range(len(cpu_by_min_dist3_0)):
        output_dist_3n_2.write("%d %f %f\n" % (i, power_by_min_dist3_2[i], cpu_by_min_dist3_2[i]))
if __name__ == '__main__':
    main()

