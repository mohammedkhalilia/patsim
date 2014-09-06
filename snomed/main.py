import MySQLdb
from patsim import snomed

#create database connection
dbconn = MySQLdb.connect(host="localhost",user="root",passwd="",db="snomed_ct")

#Clinical finding hierarchy parent concept ID: 404684003 (starting point)
#  testing: 73211009 (diabetes)
#  testing: 199223000 (Diabetes mellitus during pregnancy)

#build snomed network starting with a specific concept id and pass the db connection
print "Building the SNOMED tree"
t = snomed.Network(dbconn, 404684003)

#save path length to redis key-value database
#only save the pairwise distances for those concepts that are mapped to ICD9 codes
#that will reduce the number redis keys from 5 billion to only 2 million keys 
c = dbconn.cursor()
query = "select d.dx_code, concept_id "\
		"from (select distinct dx_code from choa.asthma_dx) d, snomed_ct.dx_mapping m " \
		"where m.dx_code = d.dx_code and d.dx_code not like 'E%' and d.dx_code not like 'V%' and in_core = 1";
c.execute(query)
rows = c.fetchall()
keys = [row[1] for row in rows]

print "Computing and saving path length to redis database"
t.compute_shortest_path(keys)

#write the network g to a GML file
print "Save tree to GML file"
t.save("/tmp/snomed_clinical_finding.gml")

#clean up
del sn
