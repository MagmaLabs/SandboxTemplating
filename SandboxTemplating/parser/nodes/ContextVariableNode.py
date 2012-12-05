from ..Node import Node

class ContextVariableNode(Node):
	def __init__( self, variableName ):
		self.variableName = variableName
	
	def __json__( self ):
		return {
			'nodeType': 'ContextVariableNode',
			'variableName': self.variableName,
		}