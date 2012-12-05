
class Node(object):
	def __json__( self ):
		return None
	
	def __repr__( self ):
		return '<Node: %r>' % self.__json__( )
	
	def childrenAccept( self, visitor ):
		pass
	
	def accept( self, visitor ):
		result = visitor.visit( self )
		
		#if visitor.automaticallyVisitChildren:
		#	self.childrenAccept( visitor )
		
		return result