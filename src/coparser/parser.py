import re
from typing import Tuple, Union
from collections import deque
from functools import total_ordering
from enum import Enum

from .models import Line, Node, Summary, MyStack


@total_ordering
class TokenKind(Enum):
    PACKAGE = 1
    MODULE = 2
    CLASS = 3
    FUNCTION = 4
    OTHER = 5

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


# TOKENS = {
#     TokenKind.PACKAGE: "<Package",
#     TokenKind.MODULE: "<Module",
#     TokenKind.CLASS: "<Class",
#     TokenKind.FUNCTION: "<Function",
#     TokenKind.OTHER: "",
# }
TOKENS = {
    "<Package": TokenKind.PACKAGE,
    "<Module": TokenKind.MODULE,
    "<Class": TokenKind.CLASS,
    "<Function": TokenKind.FUNCTION,
}


class CoParser:
    def __init__(self):
        pass

    def parse_line(self, line: str) -> Tuple[TokenKind, Line]:
        """1行をパースして、トークン種別と内容を返す

        Args:
            line (str): ファイルから読んだ1行

        Returns:
            Tuple[TokenKind, Line]: トークン種別と内容の組
        """
        # いずれかのトークンで始まっているかをチェック
        for token in TOKENS.keys():
            pattern = re.compile(r"^\s*({})".format(token))
            result = re.match(pattern, line)
            if result:
                # トークン種別を返す
                token_kind = TOKENS[result.group(1)]  # 空白を除いたトークン
                # トークンの内容を返す
                content = line.replace(token, "").strip(" >")

                return token_kind, Line(content=content)
        return TokenKind.OTHER, Line(content=line)

    def parse_file(self, content: str) -> Summary:
        """ファイル全体をパースして、Summaryを返す

        Args:
            content (str): ファイル全体の文字列

        Returns:
            Summary: サマリー
        """
        # ファイルを行ごとに分割
        lines = content.splitlines()

        stack: MyStack[Node] = MyStack()

        summary = Summary(children=[])
        # 1行ずつパースして、トークン種別と内容を取得
        # for line in lines:
        #     token_kind, line = self.parse_line(line)
        #     node = Node(kind=token_kind, value=line.content, children=[])

        #     if stack.is_empty():
        #         stack.push(node)
        #         continue

        #     pre_node = stack.peek()
        #     if pre_node.kind <= token_kind:
        #         # より深い階層になった場合はスタックに積む
        #         stack.push(node)
        #     else:
        #         # より浅い階層になった場合はスタックから取り出す
        #         while not stack.is_empty():# and stack.peek().kind > token_kind:
        #             pre_node = stack.pop()
        #             print(pre_node)
        #             pre_node.children.append(node)
        #             node = pre_node
        #             if pre_node.kind == TokenKind.PACKAGE:
        #                 summary.children.append(pre_node)

        # return summary

        pkg = None
        mdl = None
        cls = None
        func = None
        docstring = ""
        for line in lines:
            token_kind, line = self.parse_line(line)
            if token_kind == TokenKind.PACKAGE:
                pkg = line.content
            elif token_kind == TokenKind.MODULE:
                mdl = line.content
            elif token_kind == TokenKind.CLASS:
                cls = line.content
            elif token_kind == TokenKind.FUNCTION:
                func = line.content
            else:
                docstring += line.content + "\n"
