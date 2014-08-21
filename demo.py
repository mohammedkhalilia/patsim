import MySQLdb, sys
import networkx as nx
from snomed.net import net

dbconn = MySQLdb.connect(host="localhost",user="root",passwd="",db="snomed_ct")

#Clinical finding hierarchy parent concept ID: 404684003 (starting point)
#  testing: 73211009 (diabetes)
#  testing: 199223000 (Diabetes mellitus during pregnancy)
sn = net(dbconn, 199223000)
nx.write_gml(sn.graph,"snomed_clinical_finding.gml")
del sn
