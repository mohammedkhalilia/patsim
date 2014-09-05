import redis
import numpy as np

class SnomedDistance:

	def __init__(self, patient1, patient2):
		""" set the patients for whom the distance will be computed
		
		Arguments:
			patient1 -- the first patient
			patient2 -- the second patient
		"""
		self.patient1 = patient1
		self.patient2 = patient2
		
		#compute the distance matrix among the concept that both patients has
		self.compute_distance_matrix()
		
	def compute_distance_matrix(self):
		""" compute the distance matrix among concepts
			
			This will fetch the pairwise distances from the Redis database
			and store the distance in a NxM matrix
			
			Arguments:
				None
				
			Return:
				None
		"""
		r = redis.Redis("localhost")
		dx1 = self.patient1['diagnosis']
		dx2 = self.patient2['diagnosis']
		num_dx1 = len(dx1)
		num_dx2 = len(dx2)
		
		dist_mat = np.zeros((num_dx1, num_dx2))
		
		for i in range(0, num_dx1):
			for j in range(0, num_dx2):
				d = r.get("%d:%d" % (dx1[i], dx2[j])) or r.get("%d:%d" % (dx2[j], dx1[i]))
				dist_mat[i][j] = d

		self.dist_mat = dist_mat
		
	def compute(self, dist_type = "avg"):
		""" Compute the distance between the two patients
			
			Arguments:
				dist_type -- the type of distance, possible values are:
							 avg: average shortest path (default)
							 
			Return:
				None
		"""
		if dist_type == "avg":
			return self.compute_avg_distance()
		elif dist_type == "nmax":
			return self.compute_distance_normalized_by_max()
		elif dist_type == "navg":
			return self.compute_distance_normalized_by_avg()
					
	def compute_avg_distance(self):
		""" compute the 
			
			Given the distance matrix we can use average the shortest paths
			distance among the two patients
		
			Arguments:
				None
				
			Return:
				d -- distance
		"""
		d = np.mean(self.dist_mat.min(1) + self.dist_mat.min(0))
		return d
		
	def compute_distance_normalized_by_max(self):
		d_lgst = 5

		normalized_d = np.divide(self.dist_mat + 1, d_lgst)
		d = np.prod(normalized_d)
		return d
		
	def compute_distance_normalized_by_avg(self):
		d_avg = 55
		normalized_d = np.divide(self.dist_mat + 1, d_avg)
		d = np.prod(normalized_d)
		return d
		
	
	
	
