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
    def fromPytestItem(cls, item: pytest.Item):
        test_kind = ""
        if MARKER_CASE_NORMAL in item.keywords:
            # print(dir(item.module))#, item)
            test_kind = TEST_KIND_NORMAL
        elif MARKER_CASE_ABNORMAL in item.keywords:
            test_kind = TEST_KIND_ABNORMAL
        elif MARKER_CASE_LIMITATION in item.keywords:
            test_kind = TEST_KIND_LIMITATION

        pkg = ""
        mdl = item.module.__name__
        cls = item.cls if item.cls else ""
        fnc = item.name
        doc = ""
        print(item)
        print(dir(item))
        return TestReportEx(pkg, mdl, cls, fnc, test_kind, doc)


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
        break
    to_csv(reports)
    print("**** end")
