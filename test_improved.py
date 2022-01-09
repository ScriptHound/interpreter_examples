import pytest

from improved_interpreter import Interpreter, Lexer

test_data = [
    ('2 + 2', 4),
    ('2 - 2', 0),
    ('3 * 3', 9),
    ('9 / 3', 3),
    ('2 + 2 * 2', 6),
    ('2 + 2 * 2 + 2 * 2', 10),
    ('(2 + 2) * 2', 8),
    ('2 * (2 + 2) * 2', 16),
    ('7 + 3 * (1 / (2 / (3 + 1) - 1))', 1),
]


@pytest.mark.parametrize('expression, expected_result', test_data)
def test_interpreter(expression, expected_result):
    lexer = Lexer(expression)
    interpreter = Interpreter(lexer)

    result = interpreter.expr()
    assert result == expected_result
