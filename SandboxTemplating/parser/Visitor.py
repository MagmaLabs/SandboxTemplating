import inspect

class Visitor(object):
	mustVisitAllNodes = False
	automaticallyVisitChildren = True
	
	def visit( self, node ):
		orderedBases = inspect.getmro( node.__class__ )
		
		attempted = []
		
		for base in orderedBases:
			if base == object: continue
			
			visitorName = 'visit' + base.__name__
			attempted.append( visitorName )
			if hasattr(self, visitorName):
				result = getattr(self, visitorName)( node )
				
				return result
		
		if self.mustVisitAllNodes:
			raise Exception( 'Visitor %r must implement one of %r' % (self, attempted) )
		
		if self.automaticallyVisitChildren:
			node.childrenAccept( self )
		
		#return self.automaticallyVisitChildren