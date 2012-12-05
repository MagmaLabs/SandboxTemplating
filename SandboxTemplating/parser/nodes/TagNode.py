from ..Node import Node

class TagNode(Node):
	def __init__( self, name, arguments, keywordArguments ):
		self.name = name
		self.arguments = arguments
		self.keywordArguments = keywordArguments
	
	def __json__( self ):
		return {
			'nodeType': 'TagNode',
			'name': self.name,
			'arguments': [ arg.__json__( ) for arg in self.arguments ],
			'keywordArguments': dict( (n,v.__json__( )) for n,v in self.keywordArguments.iteritems() )
		}