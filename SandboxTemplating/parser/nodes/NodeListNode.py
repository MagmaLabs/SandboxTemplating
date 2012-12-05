from ..Node import Node

class NodeListNode(Node):
	def __init__( self, nodes ):
		self.nodes = nodes
		
	def __json__( self ):
		return {
			'nodeType': self.__class__.__name__,
			'nodes': [node.__json__( ) for node in self.nodes],
		}
	
	def childrenAccept( self, visitor ):
		for node in self.nodes:
			node.accept( visitor )