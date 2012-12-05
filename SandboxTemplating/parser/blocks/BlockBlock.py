from ..Block import Block

from ..nodes.NodeListNode import NodeListNode
from ..nodes.InfixOperatorNode import InfixOperatorNode
from ..nodes.ContextVariableNode import ContextVariableNode

class BlockBlock(Block):
	startTagNames = [ 'block' ]
	
	@classmethod
	def parseBlock( cls, startTag, parseUntil ):
		# this is a hack
		arguments = startTag.arguments
		assert len(arguments) == 1
		argument = arguments[0]
		assert isinstance(argument, ContextVariableNode)
		blockName = argument.variableName
		
		# get the contents of the loop
		blockNodes = list( parseUntil( ['endblock'] ) )
		
		blockNodes, endBlock = blockNodes[:-1], blockNodes[-1]
		assert endBlock.name == 'endblock'
		
		return BlockBlock( blockName, blockNodes )
	
	def __init__( self, name, nodes ):
		self.name = name
		self.nodes = NodeListNode( nodes )
	
	def __json__( self ):
		return {
			'nodeType': 'BlockBlock',
			'name': self.name,
			'nodes': self.nodes.__json__( ),
		}
	
	def childrenAccept( self, visitor ):
		self.nodes.accept( visitor )