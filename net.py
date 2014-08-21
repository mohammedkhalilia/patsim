import networkx as nx

class net:

	# __init__: constructor
	# Creates a cursor to the database and adds the provided 
	# parent nodes to a new graph
	#
	# Arguments:
	# 	dbconn - connection to the database
	#  	parent - parent node ID (concept ID)
	def __init__(self, dbconn, parent):
		self.dbconn = dbconn
		self.db = dbconn.cursor()

		#start the graph
		g = nx.Graph()

		#add parent to graph
		g.add_node(parent)

		#recursively add nodes to the graph starting by the parent 
		self.build(g,parent)
		
	# build()
	# Given a concept ID and a starting graph recursively add nodes
	# tot he graph by finding the children of the given node (concept)
	#
	# Arguments:
	# 	g 			- the current graph
	#   concept_id	- concept_id for which will find its children
	def build(self, g, concept_id):
		#get the child nodes for concept_id
		children = self.getconceptchildren(concept_id)
	
		#for every child node
		for child in children:
			#add the node to the graph
			g.add_node(child[0])

			#add an edge that connects the parent concept_id to the child
			g.add_edge(child[0],concept_id)

			#for that child, find its children
			self.build(g,child[0])
		
		self.graph = g
	
	# getconceptchildren()
	# For some concept find its child concepts
	#
	# Arguments:
	# 	concept_id - concept_id for which we will find its children
	#
	def getconceptchildren(self, concept_id):
		query = "SELECT r.source_id, d.term " \
				"FROM relationship r, description d " \
				"WHERE r.source_id=d.concept_id AND d.active = 1 "\
				"AND r.active = 1 AND d.type_id = 900000000000003001 "\
				"AND r.type_id = 116680003 AND r.destination_id = '%s'"
			
		self.db.execute(query, concept_id)
		return self.db.fetchall()

	# save()
	# Save the network to GML file
	#
	# Arguments:
	# 	filename - destination file
	def save(self, filename):
		nx.write_gml(self.graph, filename)	
 
	# destructor
	# Free resources and do clean up
	#
	# Argument:
	#	None
	def __del__(self):
		#close database cursor
		self.db.close()

		#delete cursor
		del self.db

		#close database connection
		self.dbconn.close()
