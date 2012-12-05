from SandboxTemplating.Environment import Environment

def toHTML(s, context=None, env=None, **kwargs):
	env = Environment( '/' )
	tpl = env.templateFromString( s )
	context = context or {}
	context.update( kwargs )
	return tpl.render( context )


def test_no_markup():
	assert toHTML('<b>Hello, world!</b>') == '<b>Hello, world!</b>'
	assert toHTML(u'<b>\u2020</b>') == u'<b>\u2020</b>'


def test_substitution():
	assert toHTML(
		'<b>{{ a }}, {{ b }}!</b>',
		a='Hello', b='world'
	) == '<b>Hello, world!</b>'
	
	assert toHTML(
		'<b>{{ a }}, {{ b }}</b>',
		a=1, b=1.2
	) == '<b>1, 1.2</b>'
	
	assert toHTML(
		'<b>{{ c }}, {{ b }}, {{ a }}</b>',
		a=False, b=True, c=None
	) == '<b>None, True, False</b>'


def test_escaping():
	assert toHTML(
		'<b>{{ a }}</b>',
		a='<script>alert(0)</script>',
	) == '<b>&lt;script&gt;alert(0)&lt;/script&gt;</b>'
	
	assert toHTML(
		'''<img src="images/{{ file }}.png" width='{{ width }}'>''',
		file='">lol',
		width="'>lol"
	) == '''<img src="images/&#34;&gt;lol.png" width='&#39;&gt;lol'>'''
	
	assert toHTML(
		'<td>{{ a }}</td>',
		a='&amp;'
	) == '<td>&amp;amp;</td>'


def test_whitespace():
	assert toHTML('{{ a }}', a=' a') == ' a'
	assert toHTML('{{ a }}', a='a ') == 'a '
	assert toHTML('{{ a }}', a='a\nb') == 'a\nb'
	assert toHTML('{{ a }}{{ b }}', a='a ', b=' b') == 'a  b'
	assert toHTML('a ') == 'a '
	
	# Failing:
	assert toHTML(' a') == ' a'
	assert toHTML('{{a}} {{b}}', a=1, b=2) == '1 2'
	assert toHTML('{{a}}\t{{b}}', a=1, b=2) == '1\t2'
	assert toHTML('{{a}}\n{{b}}', a=1, b=2) == '1\n2'
	assert toHTML('<html>\n	   {{ a }}\n</html>', a=1) == '<html>\n	   1\n</html>'
	assert toHTML('{{ a }} {{ b }}', a='a ', b=' b') == 'a   b'


def test_contains():
	# Failing:
	assert toHTML('{{ a in b }}', a=1, b=[1, 2]) == 'True'
	assert toHTML('{{ a in b }}', a=1, b=["1", 2]) == 'False'
	assert toHTML('{{ a in b }}', a=1, b=[]) == 'False'
	assert toHTML('{{ a in b }}', a=None, b=[]) == 'False'
	assert toHTML('{{ a in b }}', a=None, b=[None]) == 'True'


def test_indexing():
	# Failing:
	assert toHTML('{{ a[1] }}', a=['a', 'b', 'c']) == 'b'
	assert toHTML('{{ a[-1] }}', a=['a', 'b', 'c']) == 'c'
	assert toHTML('{{ a[0] }}', a=['a', 'b', 'c']) == 'a'


def test_strings():
	assert toHTML('''{{ '"' + "'" }}''') == '&#34;&#39;'
	assert toHTML('{{ "}}" }}') == '}}'
	assert toHTML(u'{{ "\u2020" }}') == u'\u2020'


def test_if_block():
	assert toHTML('{% if a %}a{% endif %}', a=True) == 'a'
	assert toHTML('{% if a %}a{% endif %}', a=False) == ''
	assert toHTML('{% if True %}a{% endif %}') == 'a'
	assert toHTML('{% if False %}a{% endif %}') == ''
	
	assert toHTML('{% if a %}a{% else %}b{% endif %}', a=True) == 'a'
	assert toHTML('{% if a %}a{% else %}b{% endif %}', a=False) == 'b'
	assert toHTML('{% if True %}a{% else %}b{% endif %}') == 'a'
	assert toHTML('{% if False %}a{% else %}b{% endif %}') == 'b'
	
	assert toHTML('{% if a == 1 %}a{% elif a == 2 %}b{% else %}c{% endif %}', a=1) == 'a'
	assert toHTML('{% if a == 1 %}a{% elif a == 2 %}b{% else %}c{% endif %}', a=2) == 'b'
	assert toHTML('{% if a == 1 %}a{% elif a == 2 %}b{% else %}c{% endif %}', a=3) == 'c'


def test_for_block():
	assert toHTML('{% for i in l %}{{ i }}<br>\n{% endfor %}', l=['a', 'b', 'c']) == 'a<br>\nb<br>\nc<br>\n'
	assert toHTML('{% for i in l %}{{ i }}<br>\n{%empty%}nope{% endfor %}', l=['a', 'b', 'c']) == 'a<br>\nb<br>\nc<br>\n'
	assert toHTML('{% for i in l %}{{ i }}<br>\n{%empty%}nope{% endfor %}', l=[]) == 'nope'
	assert toHTML('{{i}}{% for i in l %}{{i}}{% endfor %}{{i}}', l=['a', 'b', 'c'], i=0) == '0abc0'


def test_attributes():
	assert toHTML('{{ a.a }}, {{ a.b }}, {{ a.c }}', a={'a': 1, 'b': 2, 'c': 3}) == '1, 2, 3'
	assert toHTML('{{ a.a.a }}, {{ a.a.b }}, {{ a.a.c }}', a={'a': {'a': 1, 'b': 2, 'c': 3}}) == '1, 2, 3'
	assert toHTML('{{ a.a["b c"].d["e.f"] }}', a={'a': {'b c': {'d': {'e.f': 1337}}}}) == '1337'

def test_infix():
	# General infix operator test
	for a, b in [(0, 1), (1, 1), (2, 1), (1, 2), (2, 2), (2, 3), (3, 3), (4, 3), (2, 4), (11, 20), (8, 19), (18, 3)]:
			for o in ('+', '-', '/', '%', '|', '&', '^', '<', '>', '<=', '>=', '==', '!='):
				expected = str(eval('%d %s %d' % (a, o, b)))
				assert toHTML('{{ %d %s %d }}' % (a, o, b)) == expected
				assert toHTML('{{ a %s %d }}' % (o, b), a=a) == expected
				assert toHTML('{{ %d %s b }}' % (a, o), b=b) == expected
				assert toHTML('{{ a %s b }}' % o, a=a, b=b) == expected

	# And a few specific ones:
	operations = [
		'"a" + "b"', '"a" * 2',

		'1 + 2 * 3',
		'1 + 2 - 3 * 4 / 2',
		'1 + 2 - 3 * 4 / 2 < 0',

		'1 < 2 and 2 < 3',
		'1 < 2 and 3 < 3',
		'2 < 2 and 2 < 3',
		'2 < 2 and 3 < 3',

		'1 < 2 or 2 < 3',
		'1 < 2 or 3 < 3',
		'2 < 2 or 2 < 3',
		'2 < 2 or 3 < 3',
		'not True',
		'not False',
	]

	for i in operations:
		assert toHTML('{{ %s }}' % i) == str(eval(i))

def test_dict_literals():
	assert toHTML('{{ {"a": "b"}.a }}') == 'b'
	assert toHTML('{{ {"a": "b"}["a"] }}') == 'b'
	assert toHTML('{{ {}.a }}') == 'None'
	assert toHTML('{{ {"b": "c"}.a }}') == 'None'
	assert toHTML('{{ {e: "c"}.alpha }}', e='alpha') == 'c'
	assert toHTML('{{ {e: "c"}.alpha }}', e='beta') == 'None'
	assert toHTML('{{{}}}') == '{}'
	assert toHTML('{{ {"admin": "Administrator", "user": "Basic User"}[userType] }}', userType='admin') == 'Administrator'
	assert toHTML('{{ {"admin": "Administrator", "user": "Basic User"}[userType] }}', userType='user') == 'Basic User'

def test_list_literals():
	assert toHTML('{{[]}}') == '[]'
	assert toHTML('{{ [1][0] }}') == '1'
	assert toHTML('{{ [1,2][0] }}') == '1'
	assert toHTML('{{ [1,2][1] }}') == '2'
