import networkx as nx

class net:

	def __init__(self, dbconn, parent):
		self.dbconn = dbconn
		self.db = dbconn.cursor()

		g = nx.Graph()
		g.add_node(parent)
		self.build(g,parent)
		
	def build(self, g, concept_id):
		children = self.getconceptchildren(concept_id)
	
		for child in children:
			g.add_node(child[0])
			g.add_edge(child[0],concept_id)
			self.build(g,child[0])
		
		self.graph = g
	
	def getconceptchildren(self, concept_id):
		query = "SELECT r.source_id, d.term " \
				"FROM relationship r, description d " \
				"WHERE r.source_id=d.concept_id AND d.active = 1 "\
				"AND r.active = 1 AND d.type_id = 900000000000003001 "\
				"AND r.type_id = 116680003 AND r.destination_id = '%s'"
			
		self.db.execute(query, concept_id)
		return self.db.fetchall()

	def __del__(self):
		self.db.close()
		del self.db
		self.dbconn.close()
