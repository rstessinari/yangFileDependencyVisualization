"""
    ** Yang dependency tree visualizer **
    Created by: Rodrigo S. Tessinari
                {rodrigostange@gmail.com}
                18/01/2019
"""

import sys
from os import walk

def run(root_folder):
    num_dir = 0
    num_files = 0
    fail_flag = False

    try:
        open('missing_files.txt','w')
    except:
        print('Could not open file... this is odd.')

# with open('result.txt', 'w+') as resultFile:    
    for (dirpath, dirnames, filenames) in walk(root_folder):
        num_dir = num_dir + len(dirnames)
        num_files = num_files + len(filenames)

        # resultFile.write('Pasta ' + dirpath + '\n\n')
        for file in filenames:
            try:
                with open(dirpath+'\\'+file) as data:
                    resultFile.write("Arquivo \'%s\':\n%s\n" % (file,data.read()))
            except:
                with open('missing_files.txt','a') as missingFiles:
                    missingFiles.write(dirpath+'\\'+file)
                    fail_flag = True

        # resultFile.write('\n')
    if fail_flag:
        print('Failed to open the following files:')
        try:
            with open('missing_files.txt','r') as missingFiles:
                print(missingFiles.read())
        except:
            print('Could not open \'missing_files.txt\'... this is odd.')
    else:
        print('All folders read =)')



if __name__ == "__main__":
    root_folder = ''
    if (len(sys.argv) != 2):
        root_folder = 'C:\\Users\\rodri\\Desktop\\elastico\\src'
        print("You did not choose a folder.")
    else:
        root_folder = sys.argv[1]
    print("Using \"%s\" as root folder." % (root_folder))
    
    run(root_folder)
    
    print('Job done.')





from os import listdir
from os.path import isfile, join
import networkx as nx
import matplotlib.pyplot as plt
from astropy.units import degree
import numpy as npy

n = 9
draw_topos = True
calculate_statistics = False
with_avg_files = False


folder_path = "../topologies/graph/2C/n" + str(n)+ '/'
result_drawed_graph_path = "C:/omnetpp-4.6/_workspace/flexigrid_results/graphs/_drawed_topos/n"+str(n)+"/"
result_statistics_path = "C:/omnetpp-4.6/_workspace/flexigrid_results/graphs/_calculated_statistics/"

result_statistics_filename = 'n'+str(n)+".txt"

print "Reading graphs from",folder_path+'.'
file_list = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]
graph_file_list = [x for x in file_list if x.find(".txt") != -1]
print len(graph_file_list), "files found."

if (with_avg_files):
    avg_path = "../results/_charts/"
    print "Reading average files for n=" + str(n) + " from",avg_path+'.'
    file_list = [f for f in listdir(avg_path) if isfile(join(avg_path, f))]
    avg_file_list = [y for y in file_list if y.find("_average_n"+str(n)) != -1]
    print len(avg_file_list), "files found."

graph_list = []
for f in graph_file_list:
    with open(folder_path+f) as txtFile:
        file = txtFile.read()
        lineList = file.split('\n')
         
        print len(lineList)-1, "graphs found in", f+". Processing..."
        for y in lineList:
            if (y != ''):
                line_elems = y.split(' ')
#                 print line_elems
                  
                graph_n = int(line_elems[0])
                G = nx.Graph()
                G.add_nodes_from(range(1,graph_n+1))
#                 print G.number_of_nodes()
 
                del line_elems[0:2]     # just ignore second element (line_elems[1])
#                 print line_elems
                  
                for i in range(0,len(line_elems)):
                    if (i % 2 == 0):
#                         print " i par =",i
#                         print "edge",line_elems[i],line_elems[i+1]
                        G.add_edge(int(line_elems[i]),int(line_elems[i+1]))
                 
                graph_list.append(G)
#                 print graph_list
#         print lineList
    txtFile.close()

index_init = index_end = 1 
# index_init = 10333 # continuing n = 9
# index_end = 140
label_index = 10801
if (index_end == 1):
    index_end = len(graph_list)
    
if (calculate_statistics):
    print "Calculating graphs statistics for", len(graph_list), "graphs..."
    result_table = ''
    delimeter = '\t'
    table_header = "topo_name" + delimeter
    table_header += "n" + delimeter
    table_header += "m" + delimeter
    table_header += "var(degree)" + delimeter
    table_header += "avg(dist)" + delimeter
    table_header += "betweenness (max-min)" + delimeter
    table_header += "betweenness (max)"
    if (with_avg_files):
        table_header +=  delimeter + "Block Rate (simulation)"
    table_header += '\n'
    
    result_table += table_header
        
    for index in range(index_init-1,index_end):
        graph_filename = 'n' + str(graph_n) + '_g' + str(label_index) + '.png'
        graph_n = graph_list[index].order()
        graph_m = graph_list[index].size()
        graph_degree_vet = []
        for i in graph_list[index]:
            graph_degree_vet.append(graph_list[index].degree(i))
        graph_degree_variance = npy.var(graph_degree_vet)
        graph_average_node_degree = npy.average(graph_degree_vet)
        graph_diameter = nx.diameter(graph_list[index])
        #esta imprimindo int ao inves de float     (graph_average_distance)
        #>>> import math
        #>>> math.ceil(4500/1000)
        #4.0
        #>>> math.ceil(4500/1000.0)
        #5.0
        graph_average_distance = nx.average_shortest_path_length(graph_list[index])
        graph_edge_betweenness = nx.edge_betweenness_centrality(graph_list[index])
        graph_edge_betweenness_max_value = 0
        graph_edge_betweenness_min_value = 1
        for b in graph_edge_betweenness.keys():
            if (graph_edge_betweenness[b] > graph_edge_betweenness_max_value):
                graph_edge_betweenness_max_value = graph_edge_betweenness[b]
            if (graph_edge_betweenness[b] < graph_edge_betweenness_min_value):
                graph_edge_betweenness_min_value = graph_edge_betweenness[b]
        
        if (with_avg_files):
            # check if there is request blocking chart.
            if (index+1 < 10):
                avg_file = [y for y in avg_file_list if y.find('_g0'+str(label_index)+'_') != -1]
            else:
                avg_file = [y for y in avg_file_list if y.find('_g'+str(label_index)+'_') != -1]
            
            if (len(avg_file) != 1):
                print "Can't find average file for n" + str(graph_n) + "_g" + str(label_index) + "."
            else:
                with open(avg_path+avg_file[0]) as txtFile:
                    file = txtFile.read()
                    lineList = file.split('\n')
                    graph_curve_average = lineList[1].split('\t')[1]
    
        result_line = ''
        result_line += graph_filename + delimeter
        result_line += str(graph_n) + delimeter
        result_line += str(graph_m) + delimeter
        result_line += str(graph_degree_variance) + delimeter
        result_line += str(graph_diameter) + delimeter
        result_line += str(graph_average_distance) + delimeter
        result_line += str(graph_edge_betweenness_max_value - graph_edge_betweenness_min_value) + delimeter
        result_line += str(graph_edge_betweenness_max_value)
        if (with_avg_files):
            result_line += delimeter + str(graph_curve_average)
        result_line += '\n'
        result_table += result_line
        if (draw_topos):
            nx.draw_circular(graph_list[index])
            plt.savefig(result_drawed_graph_path+graph_filename)
            plt.clf()
#             print "Drawing graph",str(index+1-index_init)+'/'+str(index_end-index_init)+'.'
        label_index += 1
    
    result_file = open(result_statistics_path+result_statistics_filename, 'w+')
    result_file.write(result_table)
    result_file.close()
elif (draw_topos):
    for index in range(index_init-1,index_end):
        graph_filename = 'n' + str(graph_n) + '_g' + str(label_index) + '.png'
        nx.draw_circular(graph_list[index])
        plt.savefig(result_drawed_graph_path+graph_filename)
        plt.clf()
        label_index += 1
#         print "Drawing graph",str(index+1-index_init)+'/'+str(index_end-index_init)+'.'
else:
    print "Nothing to be done."
print "Job done =)"