import pytest

from ast_translator import Lexer, Parser, InfixToPostfixTranslator

to_postfix_notation = [
    ('2 + 2', '2 2 +'),
    ('2 * (2 + 2) * 2', '2 2 2 + * 2 *'),
    ('7 + 3 * (1 / (2 / (3 + 1) - 1))', '7 3 1 2 3 1 + / 1 - / * +')
]


@pytest.mark.parametrize('expression, expected_result', to_postfix_notation)
def test_interpreter(expression, expected_result):
    lexer = Lexer(expression)
    parser = Parser(lexer)
    translator = InfixToPostfixTranslator(parser)

    result = translator.translate()
    assert result == expected_result
