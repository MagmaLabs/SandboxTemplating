from SandboxTemplating.Environment import Environment

def toJSON(s, env=None):
    env = env or Environment( '/' )
    tpl = env.templateFromString( s )
    return tpl.doc.__json__( )



def test_no_markup():
    assert toJSON('Hello, world!')['nodes'] == \
        [{'markup': u'Hello, world!', 'nodeType': 'MarkupNode'}]


def test_if_block():
    assert toJSON('{% if magic %}magic{% endif %}')['nodes'] == \
        [{'condition': {'nodeType': 'ContextVariableNode', 'variableName': 'magic'},
          'elseNodes': {'nodeType': 'NodeListNode', 'nodes': []},
          'ifNodes': {'nodeType': 'NodeListNode',
                      'nodes': [{'markup': u'magic', 'nodeType': 'MarkupNode'}]},
          'nodeType': 'IfBlock'}]

    assert toJSON('{% if magic %}more magic{% else %}magic{% endif %}')['nodes'] == \
        [{'condition': {'nodeType': 'ContextVariableNode', 'variableName': 'magic'},
          'elseNodes': {'nodeType': 'NodeListNode',
                        'nodes': [{'markup': u'magic', 'nodeType': 'MarkupNode'}]},
          'ifNodes': {'nodeType': 'NodeListNode',
                      'nodes': [{'markup': u'more magic', 'nodeType': 'MarkupNode'}]},
          'nodeType': 'IfBlock'}]

    assert toJSON('{% if magic %}magic{% elif evil %}evil{% endif %}')['nodes'] == \
        [{'condition': {'nodeType': 'ContextVariableNode', 'variableName': 'magic'},
          'elseNodes': {'nodeType': 'NodeListNode',
                        'nodes': [{'condition': {'nodeType': 'ContextVariableNode',
                                                 'variableName': 'evil'},
                                   'elseNodes': {'nodeType': 'NodeListNode',
                                                 'nodes': []},
                                   'ifNodes': {'nodeType': 'NodeListNode',
                                               'nodes': [{'markup': u'evil',
                                                          'nodeType': 'MarkupNode'}]},
                                   'nodeType': 'IfBlock'}]},
          'ifNodes': {'nodeType': 'NodeListNode',
                      'nodes': [{'markup': u'magic', 'nodeType': 'MarkupNode'}]},
          'nodeType': 'IfBlock'}]

    assert toJSON('{% if magic %}magic{% elif evil %}evil{% else %}neither{% endif %}')['nodes'] == \
        [{'condition': {'nodeType': 'ContextVariableNode', 'variableName': 'magic'},
          'elseNodes': {'nodeType': 'NodeListNode',
                        'nodes': [{'condition': {'nodeType': 'ContextVariableNode',
                                                 'variableName': 'evil'},
                                   'elseNodes': {'nodeType': 'NodeListNode',
                                                 'nodes': [{'markup': u'neither',
                                                            'nodeType': 'MarkupNode'}]},
                                   'ifNodes': {'nodeType': 'NodeListNode',
                                               'nodes': [{'markup': u'evil',
                                                          'nodeType': 'MarkupNode'}]},
                                   'nodeType': 'IfBlock'}]},
          'ifNodes': {'nodeType': 'NodeListNode',
                      'nodes': [{'markup': u'magic', 'nodeType': 'MarkupNode'}]},
          'nodeType': 'IfBlock'}]


def test_for_block():
    assert toJSON('{% for person in people %}{{ person.name }}<br>{% endfor %}')['nodes'] == \
        [{'emptyNodes': {'nodeType': 'NodeListNode', 'nodes': []},
          'haystack': {'nodeType': 'ContextVariableNode', 'variableName': 'people'},
          'loopNodes': {'nodeType': 'NodeListNode',
                        'nodes': [{'expression': {'attributeName': 'name',
                                                  'nodeType': 'GetAttributeNode',
                                                  'term': {'nodeType': 'ContextVariableNode',
                                                           'variableName': 'person'}},
                                   'nodeType': 'VariableOutputNode'},
                                  {'markup': u'<br>', 'nodeType': 'MarkupNode'}]},
          'needle': 'person',
          'nodeType': 'ForLoopBlock'}]

    assert toJSON('{% for person in people %}{{ person.name }}<br>{% empty %}no people!{% endfor %}')['nodes'] == \
        [{'emptyNodes': {'nodeType': 'NodeListNode',
                         'nodes': [{'markup': u'no people!',
                                    'nodeType': 'MarkupNode'}]},
          'haystack': {'nodeType': 'ContextVariableNode', 'variableName': 'people'},
          'loopNodes': {'nodeType': 'NodeListNode',
                        'nodes': [{'expression': {'attributeName': 'name',
                                                  'nodeType': 'GetAttributeNode',
                                                  'term': {'nodeType': 'ContextVariableNode',
                                                           'variableName': 'person'}},
                                   'nodeType': 'VariableOutputNode'},
                                  {'markup': u'<br>', 'nodeType': 'MarkupNode'}]},
          'needle': 'person',
          'nodeType': 'ForLoopBlock'}]


def test_expressions():
    assert toJSON('{{ "string" }}')['nodes'] == \
        [{'expression': {'literal': u'string', 'nodeType': 'StringLiteralNode'},
          'nodeType': 'VariableOutputNode'}]

    assert toJSON('{{ 1 }}')['nodes'] == \
        [{'expression': {'literal': 1, 'nodeType': 'NumericLiteralNode'},
          'nodeType': 'VariableOutputNode'}]

    assert toJSON('{{ 1.2 }}')['nodes'] == \
        [{'expression': {'literal': 1.2, 'nodeType': 'NumericLiteralNode'},
          'nodeType': 'VariableOutputNode'}]

    assert toJSON('{{ -1 }}')['nodes'] == \
        [{'expression': {'literal': -1, 'nodeType': 'NumericLiteralNode'},
          'nodeType': 'VariableOutputNode'}]

    assert toJSON('{{ a }}')['nodes'] == \
        [{'expression': {'nodeType': 'ContextVariableNode', 'variableName': 'a'},
          'nodeType': 'VariableOutputNode'}]

    assert toJSON('{{ -a }}')['nodes'] == \
        [{'expression': {'nodeType': 'UnaryOperatorNode',
                         'operand': {'nodeType': 'ContextVariableNode',
                                     'variableName': 'a'},
                         'operator': '-'},
          'nodeType': 'VariableOutputNode'}]

    assert toJSON('{{ True }}')['nodes'] == \
        [{'expression': {'nodeType': 'BooleanLiteralNode', 'value': True},
          'nodeType': 'VariableOutputNode'}]

    assert toJSON('{{ False }}')['nodes'] == \
        [{'expression': {'nodeType': 'BooleanLiteralNode', 'value': False},
          'nodeType': 'VariableOutputNode'}]

    assert toJSON('{{ None }}')['nodes'] == \
        [{'expression': {'nodeType': 'NoneLiteralNode'},
          'nodeType': 'VariableOutputNode'}]

    assert toJSON('{{ true }}')['nodes'] == \
        [{'expression': {'nodeType': 'BooleanLiteralNode', 'value': True},
          'nodeType': 'VariableOutputNode'}]

    assert toJSON('{{ false }}')['nodes'] == \
        [{'expression': {'nodeType': 'BooleanLiteralNode', 'value': False},
          'nodeType': 'VariableOutputNode'}]

    assert toJSON('{{ null }}')['nodes'] == \
        [{'expression': {'nodeType': 'NoneLiteralNode'},
          'nodeType': 'VariableOutputNode'}]


def test_tags():
    assert toJSON('{% some_tag %}')['nodes'] == \
        [{'arguments': [], 'keywordArguments': {}, 'name': 'some_tag', 'nodeType': 'TagNode'}]

    assert toJSON('{% some_tag argument %}')['nodes'] == \
        [{'arguments': [{'nodeType': 'ContextVariableNode',
                         'variableName': 'argument'}], 'keywordArguments': {},
          'name': 'some_tag',
          'nodeType': 'TagNode'}]

    assert toJSON('{% some_tag argument,another %}')['nodes'] == \
        [{'arguments': [{'nodeType': 'ContextVariableNode',
                         'variableName': 'argument'},
                        {'nodeType': 'ContextVariableNode',
                         'variableName': 'another'}], 'keywordArguments': {},
          'name': 'some_tag',
          'nodeType': 'TagNode'}]

    assert toJSON('{% some_tag argument, "a string", 42, -123, -+123, +-123, --123, 1--1, and_another %}')['nodes'] == \
        [{'arguments': [{'nodeType': 'ContextVariableNode',
                         'variableName': 'argument'},
                        {'literal': u'a string', 'nodeType': 'StringLiteralNode'},
                        {'literal': 42, 'nodeType': 'NumericLiteralNode'},
                        {'literal': -123, 'nodeType': 'NumericLiteralNode'},
                        {'literal': -123, 'nodeType': 'NumericLiteralNode'},
                        {'literal': -123, 'nodeType': 'NumericLiteralNode'},
                        {'literal': 123, 'nodeType': 'NumericLiteralNode'},
                        {'leftOperand': {'literal': 1,
                                         'nodeType': 'NumericLiteralNode'},
                         'nodeType': 'InfixOperatorNode',
                         'operator': '-',
                         'rightOperand': {'literal': -1,
                                          'nodeType': 'NumericLiteralNode'}},
                        {'nodeType': 'ContextVariableNode',
                         'variableName': 'and_another'}], 'keywordArguments': {},
          'name': 'some_tag',
          'nodeType': 'TagNode'}]

    assert toJSON('{% some_tag 1.2, None, null, True, False, true, false %}')['nodes'] == \
        [{'arguments': [{'literal': 1.2, 'nodeType': 'NumericLiteralNode'},
                        {'nodeType': 'NoneLiteralNode'},
                        {'nodeType': 'NoneLiteralNode'},
                        {'nodeType': 'BooleanLiteralNode', 'value': True},
                        {'nodeType': 'BooleanLiteralNode', 'value': False},
                        {'nodeType': 'BooleanLiteralNode', 'value': True},
                        {'nodeType': 'BooleanLiteralNode', 'value': False}], 'keywordArguments': {},
          'name': 'some_tag',
          'nodeType': 'TagNode'}]


def test_attributes():
    assert toJSON("{{ foo['aasd'].bar[BBB][CCC].aaa.baz }}")['nodes'] == \
        [{'expression': {'attributeName': 'baz',
                         'nodeType': 'GetAttributeNode',
                         'term': {'attributeName': 'aaa',
                                  'nodeType': 'GetAttributeNode',
                                  'term': {'keyExpression': {'nodeType': 'ContextVariableNode',
                                                             'variableName': 'CCC'},
                                           'nodeType': 'GetKeyNode',
                                           'term': {'keyExpression': {'nodeType': 'ContextVariableNode',
                                                                      'variableName': 'BBB'},
                                                    'nodeType': 'GetKeyNode',
                                                    'term': {'attributeName': 'bar',
                                                             'nodeType': 'GetAttributeNode',
                                                             'term': {'keyExpression': {'literal': u'aasd',
                                                                                        'nodeType': 'StringLiteralNode'},
                                                                      'nodeType': 'GetKeyNode',
                                                                      'term': {'nodeType': 'ContextVariableNode',
                                                                               'variableName': 'foo'}}}}}}},
          'nodeType': 'VariableOutputNode'}]
