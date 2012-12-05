from ..Node import Node

class DictLiteralNode(Node):
	def __init__( self, literal=None ):
		if literal:
			self.literal = [(literal[0], literal[1])]
		else:
			self.literal = []
	
	def add( self, other ):
		self.literal += other.literal
		return self
	
	def __json__( self ):
		return {
			'nodeType': 'ListLiteralNode',
			'literal': [(a.__json__(), b.__json__()) for a,b in self.literal]
		}