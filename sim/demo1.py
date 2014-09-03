import MySQLdb
import redis

#create db connection
dbconn = MySQLdb.connect(host="localhost",user="root",passwd="",db="choa")
db = dbconn.cursor()

#check the Redis database
r = redis.Redis("localhost")
	
#Get list of patients and append patients to the network
patient = {}
query = "select kids_pat_id, concept_id "\
		"from asthma_dx d, asthma_core c, snomed_ct.dx_mapping m "\
		"where d.kids_visit_id = c.kids_visit_id and m.dx_code = d.dx_code  "\
		"and d.dx_code not like 'E%' and d.dx_code not like 'V%' and in_core = 1 "\
		"group by kids_pat_id, concept_id limit 100";
		
db.execute(query)
rows = db.fetchall()

#transform patient data to dictionary
for row in rows:
	pat_id = row[0]
	
	if pat_id not in patient:
		patient[pat_id] = []
	
	patient[pat_id].append(row[1])
	
#Example redis query
#to get the distance between concept ID 209557005 and 70070008
d = r.get("%d:%d" % (209557005, 70070008))
print d

#Example patient similarity compute
#to get the distance between patient ID 332322 and 566556
pat_cncpt1 = patient[332322]
pat_cncpt2 = patient[566556]

#compute distance matrix for the 2 patients' concepts
dis_matrix = []

for cncpt1 in pat_cncpt1:
	dis_cncpt = []
		
	for cncpt2 in pat_cncpt2:
		d = r.get("%d:%d" % (cncpt1, cncpt2))
		dis_cncpt.append(d) 
	
	dis_matrix.append(dis_cncpt)

#get the transposed matrix of the distance matrix
trans_dis_matrix = []
for i in range(len(dis_matrix[0])):
	trans_dis_matrix.append([row[i] for row in dis_matrix])

#Method 1: Average for all the shortest distance

d_avg_st = 0

for row in dis_matrix:
	d_avg_st = d_avg_st + min(row)

for row in trans_dis_matrix:
	d_avg_st = d_avg_st + min(row)

d_avg_st = 1.0 * d_avg_st / (len(dis_matrix) + len(trans_dis_matrix))
print d_avg_st


#Method 2: Multiply every concept distance compared with Longest distance

#Assume that the longest distance is 111
d_lgst = 111

d_mul_lgst = 1.0

for row in dis_matrix:
	for d in row:
		d_mul_lgst = d_mul_lgst * d / d_lgst

print d_mul_lgst

#Method 3: Multiply every concept distance compared with Average distance

#Assume that the average distance is 55
d_avg = 55

d_mul_avg = 1.0

for row in dis_matrix:
	for d in row:
		d_mul_avg = d_mul_lgst * d / d_avg

print d_mul_avg



