import random
import time
import numpy as np
from helpers import Point2D_to_tuple_list, Point2D_to_x_y_list
from custom_types import *
from scipy.spatial import cKDTree
import matplotlib.pyplot as plt 
from scipy.sparse.csgraph import shortest_path
		
def interpolate(start, end, resolution):
    vector = end-start
    if resolution > 1.0:
        raise("resolution cannot be greater than 1")
    solution_path = []
    for i in range(int(1/resolution)+1):
        solution_path.append(start + (vector * resolution* i).toInt())    
    return solution_path

	
class sPRM:
	def __init__(self, config_space, work_space):
		self.vertices = []
		self.edges = dict()
		self.cspace = config_space
		self.wspace = work_space
		self.p = 2
		self.samples = None
	def _createVertices(self, queries, samples):
		V = self.vertices
		resample = True
		if self.samples == samples:
			resample = False
		self.samples =samples
		for q in queries:
			start, end = q[0], q[1]
			V.insert(0,start)
			#V.append(end)
		if resample:
			print ("SAMPLING VERTICES")
			for i in range(samples):
				if i < int(samples/2):
					if i==0:
						print("bridgetest sampling active")
					config = self.cspace.CSampleSpace(self.wspace, 'bridgetest')
				else:
					if i == int(samples/2):
						print("uniform sampling active")
					config = self.cspace.CSampleSpace(self.wspace, 'uniform')
				V.append(config)
		else:
			print("USING EXISTING SAMPLING")
		V.append(end)
	def _createEdges(self, radius):
		V = self.vertices
		V_tuple_list = Point2D_to_tuple_list(V)
		self.kdtree = cKDTree(V_tuple_list)
		for index_v, v in enumerate(V):
			idx_neighbors = self.Neighbors(v, radius)
			if not idx_neighbors:
				self.edges[index_v] = []
				continue
			validIdx = []
			for idx in idx_neighbors:
				if self.isValidEdge(v, V[idx], resolution = 0.2):
					validIdx.append(idx) 
	
			self.edges[index_v] = validIdx
		#print(self.edges)
	def shortestPath(self, queries, samples=50, radius=10):
		start_time = time.time()
		self._createVertices(queries, samples)
		self._createEdges(radius)
		graph = self._to_adjacency_matrix()
		n_of_edges = graph.sum()/2
		print(f"NO OF EDGES: {n_of_edges}")
		notused_dist_matrix, predecessors = shortest_path(csgraph=graph, directed=False, indices=0, return_predecessors=True)
		print ("Running DJKSTRA algo")
		visit_indices = self._get_shortest_path_node_indices(0, len(self.vertices) - 1, predecessors)
		end_time = time.time()
		timetaken = end_time - start_time
		print(f"TIME TAKEN : {timetaken}")
		if visit_indices:
			print("SHORTEST PATH FOUND")
			return [self.vertices[ind] for ind in visit_indices]
		else:
			print("PATH NOT FOUND")
			nothing=[]
			return nothing
		
	def _to_adjacency_matrix(self):
		edges_dict = self.edges
		N=len(edges_dict.keys())
		edge_matrix = np.zeros((N,N))
		for row in range(N):
			cols = edges_dict[row]
			if cols:
				edge_matrix[row,cols] = 1 
		indx = np.diag_indices(N)
		edge_matrix[indx] = 0
		return edge_matrix
	def _get_shortest_path_node_indices(self, start, end, previous_nodes):
		visit_nodes = []
		curr = end
		while previous_nodes[curr] != start:
			if previous_nodes[curr] < 0:
				return []
			visit_nodes.insert(0,previous_nodes[curr])
			curr = previous_nodes[curr] 
		return [start] + visit_nodes + [end]	
	def isValidEdge(self, config1, config2, resolution = 0.2):
		intermediate_configs = interpolate(config1, config2, resolution)
		for config in intermediate_configs:
			if self.wspace.IsInCollision(config):
				return False
		return True		

	def Neighbors(self, query_config, radius):
		indexes = self.kdtree.query_ball_point([query_config.x, query_config.y], radius)
		return indexes
	def printEdgeVertices(self):
		print( " Started plotting vertices and Edges")
		V = self.vertices
		E = self.edges
	
		fig= plt.figure()
		ax = fig.add_subplot(111)
		ax.imshow(self.wspace.room_img_numpy)
		# print vertices
		x,y = Point2D_to_x_y_list(V)
		ax.scatter(x, y, color = 'r' )
		# print edges
		for k in E.keys():
			config1 = V[k]
			idx  = E[k]
			for i_ in idx:
				config2 = V[i_]
				x, y = Point2D_to_x_y_list([config1, config2])
				ax.plot(x,y, color = 'b')
		print("Plotting in matplotlin finished !!! ")


			
		plt.show()
		
