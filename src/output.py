import csv
import networkx as nx
import pickle

def plot_graph(edge_weights):
	G = nx.Graph()
	for edge in edge_weights:
		left = list(edge)[0]
		right = list(edge)[1]
		weight = edge_weights[edge]

		G.add_edge(left, right, weight=weight)
	
	G = nx.convert_node_labels_to_integers(G)
	nx.draw(G, 'graph.png', format='png', prog='neato')

def export_to_csv(edge_weights, filename):
	with open(filename, 'wt') as f:
		print('Source;Target;Weight;Type', file=f)
		for edge in edge_weights:
			left = list(edge)[0]
			right = list(edge)[1]
			weight = edge_weights[edge]

			if weight > 0:
				print(left + ';' + right + ';' + str(int(weight)) + ";Undirected", file=f)
	print("Wrote graph to CSV file " + filename)

def save_words_to_pickle(words_by_file, filename):
	with open(filename, 'wb') as f:
		pickle.dump(words_by_file, f, pickle.HIGHEST_PROTOCOL)