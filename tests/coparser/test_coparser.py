import pytest

from coparser.parser import CoParser, TokenKind
from coparser.models import Line, Node, Summary


@pytest.mark.parametrize(
    "line, token_kind, exp",
    [
        ("<Package foo>", TokenKind.PACKAGE, Line(content="foo")),
        ("<Module bar>", TokenKind.MODULE, Line(content="bar")),
        ("<Class baz>", TokenKind.CLASS, Line(content="baz")),
        ("<Function qux>", TokenKind.FUNCTION, Line(content="qux")),
        ("docstring", TokenKind.OTHER, Line(content="docstring")),
    ],
)
def test_coparser_parse_line(line, token_kind, exp):
    # prepare
    coparser = CoParser()

    # execute
    actual = coparser.parse_line(line)
    # verify
    assert actual == (token_kind, exp)


def test_coparser_parse_file():
    # prepare
    coparser = CoParser()

    # execute
    content = """<Package foo>
  <Module bar>
    <Class baz>
      <Function qux>
        title

        detail description
      <Function hoge>
        aaa
"""
    actual = coparser.parse_file(content)

    # verify
    exp = Summary(children=[
        Node(kind=TokenKind.PACKAGE, value="foo", children=[
            Node(kind=TokenKind.MODULE, value="bar", children=[
                Node(kind=TokenKind.CLASS, value="baz", children=[
                    Node(kind=TokenKind.FUNCTION, value="qux", children=[
                        Node(kind=TokenKind.OTHER, value="        title", children=[]),
                        Node(kind=TokenKind.OTHER, value="", children=[]),
                        Node(kind=TokenKind.OTHER, value="        detail description", children=[]),
                    ]),
                ]),
            ]),
        ])
    ])
    print(actual)
    assert exp == actual
