from ..Node import Node

from functools import partial

class GetAttributeNode(Node):
	@classmethod
	def withFutureTerm( cls ):
		return partial( GetAttributeNode, None )
	
	def __init__( self, term, attributeName ):
		self.term = term
		self.attributeName = attributeName
	
	def setLeftOperand( self, operand ):
		self.term = operand
	
	def __json__( self ):
		return {
			'nodeType': 'GetAttributeNode',
			'term': self.term.__json__( ),
			'attributeName': self.attributeName,
		}