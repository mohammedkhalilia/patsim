import MySQLdb
from snomedtools.net import net

#create database connection
dbconn = MySQLdb.connect(host="localhost",user="root",passwd="C0msc29.gatech",db="snomed_ct")

#Clinical finding hierarchy parent concept ID: 404684003 (starting point)
#  testing: 73211009 (diabetes)
#  testing: 199223000 (Diabetes mellitus during pregnancy)

#build snomed network starting with a specific concept id and pass the db connection
sn = net(dbconn, 199223000)

#network stats
print "Number of nodes %d, number of edges %d" % (len(sn.graph.nodes()), len(sn.graph.edges()))

#write the network g to a GML file
sn.save("/tmp/snomed_clinical_finding.gml")

#clean up
del sn
