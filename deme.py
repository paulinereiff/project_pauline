

class Deme:

	def __init__(self, id=0, size = 5): 
		
		self.id = id
		self.size = size
		self.select = False
		self.migrate_to = list() #id
		self.join_to = list()
		self.is_joined_by = list()