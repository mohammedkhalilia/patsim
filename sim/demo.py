import MySQLdb
import redis
from patsim.sim import snomed_distance

#create db connection
dbconn = MySQLdb.connect(host="localhost",user="root",passwd="",db="choa")
db = dbconn.cursor()

#check the Redis database
r = redis.Redis("localhost")
	
#Get list of patients and append patients to the network
patient = {}
query = "select kids_pat_id, concept_id "\
		"from asthma_dx d, asthma_core c, snomed_ct.dx_mapping m "\
		"where d.kids_visit_id = c.kids_visit_id and m.dx_code = d.dx_code "\
		"and d.dx_code not like 'E%' and d.dx_code not like 'V%' and in_core = 1 "\
		"group by kids_pat_id, concept_id limit 20";
		
db.execute(query)
rows = db.fetchall()

#transform patient data to dictionary
for row in rows:
	pat_id = row[0]
	
	if pat_id not in patient:
		patient[pat_id] = {'diagnosis':[]}
	
	patient[pat_id]['diagnosis'].append(row[1])

print patient

#Compute the distance between two patients
patient1 = patient[patient.keys()[1]]
patient2 = patient[patient.keys()[2]]
sd = snomed_distance.SnomedDistance(patient1, patient2)
print sd.compute("nmax")
