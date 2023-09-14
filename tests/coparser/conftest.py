from typing import List
from collections import namedtuple

import pytest


MARKER_CASE_NORMAL = "case_normal"
MARKER_CASE_ABNORMAL = "case_abnormal"
MARKER_CASE_LIMITATION = "case_limit"

TEST_KIND_NORMAL = "N"
TEST_KIND_ABNORMAL = "A"
TEST_KIND_LIMITATION = "L"


TestReport = namedtuple(
    "TestReport", ["package", "module", "cls", "function", "test_kind", "docstring"]
)


class TestReportEx(TestReport):
    def __str__(self):
        msg = "{},{},{},{},{},{}".format(
            self.package,
            self.module,
            self.cls,
            self.function,
            self.test_kind,
            self.docstring,
        )
        return msg

    @classmethod
    def get_docstring(cls, item):
        func_name = item.originalname
        try:
            if item.cls:
                func = getattr(item.cls, func_name)
            else:
                func = getattr(item.module, func_name)
        except AttributeError as e:
            raise e

        return func.__doc__

    @classmethod
    def fromPytestItem(cls, item: pytest.Item):
        test_kind = ""
        if MARKER_CASE_NORMAL in item.keywords:
            test_kind = TEST_KIND_NORMAL
        elif MARKER_CASE_ABNORMAL in item.keywords:
            test_kind = TEST_KIND_ABNORMAL
        elif MARKER_CASE_LIMITATION in item.keywords:
            test_kind = TEST_KIND_LIMITATION
        else:
            test_kind = "未分類"

        pkg = item.module.__package__
        mdl = item.module.__name__
        clz = item.cls.__name__ if item.cls else ""
        fnc = item.name
        # NOTE: 以下だとdocstringが取得できない
        # doc = item.__doc__
        doc = cls.get_docstring(item)
        return TestReportEx(pkg, mdl, clz, fnc, test_kind, doc)


def to_csv(reports: List[TestReportEx]):
    reports = sorted(reports)
    for rep in reports:
        print(rep)


def pytest_collection_modifyitems(
    session: pytest.Session, config: pytest.Config, items: List[pytest.Item]
):
    """pytestがテストの収集を終えたタイミングで呼び出されるhook"""

    print("**** start")
    reports = []
    for item in items:
        test_report = TestReportEx.fromPytestItem(item)
        reports.append(test_report)
    to_csv(reports)
    print("**** end")
