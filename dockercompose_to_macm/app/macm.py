from networkx import *




class Node(DiGraph):
	def __init__(self, secondary, primary, namee, type_node, atype,dtype,ctype):
		self.primary=primary
		self.secondary=secondary
		self.namee=namee
		self.type_node=type_node
		self.atype=atype
		self.dtype=dtype
		self.ctype=ctype
		
	def get_primary(self):
		return self.primary

	def get_secondary(self):
		return self.secondary

	def get_name(self):
		return self.namee
	
	def get_type(self):
		return self.type_node

	def get_atype(self):
		return self.atype

	def get_dtype(self):
		return self.dtype

	def get_ctype(self):
		return self.ctype

	def set_atype(self,value):
		self.atype=value

	def set_dtype(self,value):
		self.dtype=value

	def set_ctype(self,value):
		self.ctype=value

class Edge(DiGraph):
	def __init__(self, by_node , to_node, type_connect):
		self.by_node=by_node
		self.to_node=to_node
		self.type_connect=type_connect
		
	def get_bynode(self):
		return self.by_node
	
	def get_tonode(self):
		return self.to_node
	
	def get_type_connect(self):
		return self.type_connect







