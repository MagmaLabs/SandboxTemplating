from ..Block import Block

from ..nodes.NodeListNode import NodeListNode
from ..nodes.InfixOperatorNode import InfixOperatorNode
from ..nodes.ContextVariableNode import ContextVariableNode

class IfBlock(Block):
	startTagNames = [ 'if' ]
	
	@classmethod
	def parseBlock( cls, startTag, parseUntil ):
		assert startTag.name in ( 'if', 'elif' )
		
		assert len(startTag.arguments) == 1
		argument = startTag.arguments[0]
		
		# get the contents of the condition
		ifNodes = list( parseUntil( ['elif', 'else', 'endif'] ) )
		
		ifNodes, endIf = ifNodes[:-1], ifNodes[-1]
		
		if endIf.name == 'elif':
			elseNodes = [ IfBlock.parseBlock( endIf, parseUntil ) ]
		elif endIf.name == 'else':
			elseNodes = list( parseUntil( ['endif'] ) )
			elseNodes, endIf = elseNodes[:-1], elseNodes[-1]
			assert endIf.name == 'endif'
		else:
			assert endIf.name == 'endif'
			elseNodes = []
		
		return IfBlock( argument, ifNodes, elseNodes )
	
	def __init__( self, condition, ifNodes, elseNodes ):
		self.condition = condition
		self.ifNodes = NodeListNode( ifNodes )
		self.elseNodes = NodeListNode( elseNodes )
	
	def __json__( self ):
		return {
			'nodeType': 'IfBlock',
			'condition': self.condition.__json__( ),
			'ifNodes': self.ifNodes.__json__( ),
			'elseNodes': self.elseNodes.__json__( ),
		}