from SandboxTemplating.parser.nodes import *

from parcon import *

VariableStart = Literal( '{{' )
VariableEnd = Literal( '}}' )

TagStart = Literal( '{%' )
TagEnd = Literal( '%}' )

Identifier = Word( alphanum_chars + '_', alpha_chars + '_' )(desc='Identifier')

StringLiteral = (
	('"' + Exact(ZeroOrMore(AnyChar() - CharIn('"'))) + '"')["".join] |
	("'" + Exact(ZeroOrMore(AnyChar() - CharIn("'"))) + "'")["".join]
)[StringLiteralNode]

NumberLiteral = number[float]

Term = (NumberLiteral | StringLiteral | Identifier)

StartTokens = VariableStart | VariableEnd | TagStart | TagEnd
Markup = Exact(Except( Exact(AnyChar()), StartTokens ))[1:](desc='Markup')[MarkupNode]

Expr = Forward()

NoneLiteral = (
	Literal("None") |
	"none" |
	"null"
)[NoneLiteralNode]

BoolLiteral = (
	SignificantLiteral("True") |
	SignificantLiteral("False") |
	SignificantLiteral("true") |
	SignificantLiteral("false")
)[BooleanLiteralNode]

ListLiteral = '[' + Optional( InfixExpr( Expr[ListLiteralNode], [(',', lambda a,b: a.add(b))] ), ListLiteralNode() ) + ']'

DictItem = (Expr + ':' + Expr)
DictLiteral = '{' + Optional( InfixExpr( DictItem[DictLiteralNode], [(',', lambda a,b: a.add(b))] ), DictLiteralNode() ) + '}'

Term = (
	number[NumericLiteralNode] |
	NoneLiteral |
	BoolLiteral |
	ListLiteral |
	DictLiteral |
	Identifier[ContextVariableNode] |
	StringLiteral |
	"(" + Expr + ")"
)( name='Expression' )

Name = (Identifier + ".")[...] + Identifier

def reducePrimary( foo ):
	left, right = foo
	if len(right) == 0:
		return left
	reduceSet = [left] + right
	return reduce( lambda a, b: b.setLeftOperand( a ) or b, reduceSet )

Primary = (Term + (
	("." + Identifier)[GetAttributeNode.withFutureTerm()] |
	('[' + Expr + ']')[GetKeyNode.withFutureTerm()])[...]
)[reducePrimary]

def maybeUnary( args ):
	if isinstance(args, tuple):
		# using the unary operator
		operator, operand = args
		
		# special case to be clean: merge negative unary into numeric constants
		if isinstance(operand, NumericLiteralNode):
			if operator == '-':
				operand.negate( )
				return operand
			elif operator == '+':
				return operand # nop?
		
		return UnaryOperatorNode( operand, operator )
	else:
		# no unary, pass through
		return args

Unary = (-(
	SignificantLiteral('+') |
	SignificantLiteral('-') |
	SignificantLiteral('not') |
	SignificantLiteral('~')
) + Primary)[maybeUnary]

def makeOperators( *operators ):
	return [(op, InfixOperatorNode.withOperator(op)) for op in operators]

MulExpr = InfixExpr( Unary, makeOperators( '*', '/', '%' ) )
AddExpr = InfixExpr( MulExpr, makeOperators( '+', '-' ) )
ShiftExpr = InfixExpr( AddExpr, makeOperators( '<<', '>>' ) )
RelExpr = InfixExpr( ShiftExpr, makeOperators( '<=', '>=', '<', '>' ) )
EqualExpr = InfixExpr( RelExpr, makeOperators( '==', '!=' ) )
AndExpr = InfixExpr( EqualExpr, makeOperators( '&' ) )
XorExpr = InfixExpr( AndExpr, makeOperators( '^' ) )
OrExpr = InfixExpr( XorExpr, makeOperators( '|' ) )
InExpr = InfixExpr( OrExpr, makeOperators( 'in' ) )
CondAndExpr = InfixExpr( InExpr, makeOperators( 'and' ) )
CondOrExpr = InfixExpr( CondAndExpr, makeOperators( 'or' ) )
CondExpr = CondOrExpr # ternary could go here
Expr << CondExpr

Expression = Expr

VariableOutput = Exact( VariableStart + Expression + VariableEnd, space_parser=Whitespace( ) )[VariableOutputNode]

def reduceParameters( left, right ):
	if isinstance( left, list ):
		return left + [right]
	else:
		return [left, right]

def makeTag( tagDefinition ):
	if not isinstance(tagDefinition, tuple):
		tagDefinition = (tagDefinition, [])
	
	tagName, tagArgs = tagDefinition
	
	if not isinstance(tagArgs, list):
		tagArgs = [tagArgs]
	
	tagPositionalArgs = []
	tagKeywordArgs = {}
	
	for arg in tagArgs:
		if isinstance(arg, tuple):
			name, value = arg
			tagKeywordArgs[name] = value
		else:
			assert len(tagKeywordArgs) == 0, "Keyword arguments must appear after all non-keyword arguments"
			tagPositionalArgs.append( arg )
	
	return TagNode( tagName, tagPositionalArgs, tagKeywordArgs )

def wrapInfix( args ):
	# When an infix expression matches only one value, it passes through the whole
	# expression without enclosing it. This function encloses it in a list anyway,
	# since we expect a list of arguments in all cases.
	if not isinstance(args, list):
		args = [args]
	return args

KeywordExpression = (-(Identifier + Except(Literal('='),Literal('=='))) + Expression)
TagParamters = InfixExpr( KeywordExpression, [(',', reduceParameters)] )[wrapInfix]
Tag = Exact( TagStart + Identifier + -TagParamters + TagEnd, space_parser=Whitespace( ) )[makeTag]

ItemList = +( Exact(Markup(name="markup")) | VariableOutput | Tag )

Grammar = ItemList[TemplateNode]