import networkx as nx
import redis

class Network:

	def __init__(self, dbconn, parent):
		""" constructor
		Creates a cursor to the database and adds the provided 
		parent nodes to a new graph
	
		Arguments:
	 		dbconn - connection to the database
			parent - parent node ID (concept ID)
		"""
		self.dbconn = dbconn
		self.db = dbconn.cursor()

		#start the graph
		g = nx.Graph()

		#add parent to graph
		g.add_node(parent)

		#recursively add nodes to the graph starting by the parent 
		self.build(g,parent)
		
	def build(self, g, concept_id):
		""" Recursively build SNOMED network
		Given a concept ID and a starting graph recursively add nodes
		to the graph by finding the children of the given node (concept)
	
		Arguments:
			g -- the current graph
			concept_id -- concept_id for which will find its children
		"""
		
		#get the child nodes for concept_id
		children = self.get_concept_children(concept_id)
	
		#for every child node
		for child in children:
			#add the node to the graph
			g.add_node(child[0])

			#add an edge that connects the parent concept_id to the child
			g.add_edge(child[0],concept_id)

			#for that child, find its children
			self.build(g,child[0])
		
		self.graph = g
	
	def get_concept_children(self, concept_id):
		""" Get concept children
		For some concept find its child concepts
	
		Arguments:
			concept_id - concept_id for which we will find its children
		"""
		query = "SELECT r.source_id, d.term " \
				"FROM snomed_ct.relationship r, snomed_ct.description d " \
				"WHERE r.source_id=d.concept_id AND d.active = 1 "\
				"AND r.active = 1 AND d.type_id = 900000000000003001 "\
				"AND r.type_id = 116680003 AND r.destination_id = '%s'"
			
		self.db.execute(query, concept_id)
		return self.db.fetchall()

	def save(self, filename):
		""" Save network to GML file
		Arguments:
	 		filename -- destination file
		"""
		nx.write_gml(self.graph, filename)		
	
 	def compute_shortest_path(self, keys):
 		""" Save the shortest path distance to key-value database
 			We will avoid computing the pairwise shortest path among all
 			SNOMED concepts as this will be a huge number of pairwise distances.
 			Instead we will only store the SNOMED codes that are referenced in the 
 			keys argument passed to this method.
 			
 		Arguments:
 			keys -- the keys for which we are interested in storing the 
 					pairwise distances for
 		"""
 		r = redis.Redis("localhost")
 		r.flushdb()

 		#only use the keys that are referenced in the argument "keys"
 		concepts = list(set(self.graph.nodes()).intersection(keys))
 		num_concepts = len(concepts)
		
 		for i in range(0,num_concepts):
 			r.set("%d:%d" % (concepts[i], concepts[i]), 0)
 			
 			for j in range(i+1,num_concepts):
 				r.set("%d:%d" % (concepts[j], concepts[j]), 0)
				p = nx.shortest_path(self.graph, concepts[i], concepts[j])
				r.set("%d:%d" % (concepts[i], concepts[j]),len(p))
				
	def __del__(self):
		""" destructor
		Free resources and do clean up
	
		Argument:
			None
		"""
		#close database cursor
		self.db.close()

		#delete cursor
		del self.db

		#close database connection
		self.dbconn.close()
