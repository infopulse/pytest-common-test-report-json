from pytest import Item, CallInfo, TestReport, Mark
from enum import Enum


class TestStatus(Enum):
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    PENDING = "pending"


class Report:
    def __init__(self):
        self.test_items = dict()

    def _add(self, item: Item, call: CallInfo, report: TestReport):
        self.test_items[item.nodeid] = {
            "status": TestStatus.PENDING,
            "rawStatus": None,
            "duration": 0,
            "start": None,
            "stop": None,
            "tags": [],
            "filePath": None,
            "browser": None,
            "extra": {}
        }

    def update(self, item: Item, call: CallInfo, report: TestReport):
        if item.nodeid not in self.test_items.keys():
            self._add(item, call, report)
        else:
            # status
            test_details = self.test_items.get(item.nodeid)
            if report.skipped:
                test_details["status"] = TestStatus.SKIPPED
            elif report.failed:
                test_details["status"] = TestStatus.FAILED
                test_details['rawStatus'] = f"{report.when}_{report.outcome}"
            else:
                test_details["status"] = TestStatus.PASSED

            test_details["duration"] += report.duration
            if report.when == "call":
                test_details["start"] = report.start
            if report.when == "teardown":
                test_details["stop"] = report.stop
            # metadata
            test_details["tags"] = [mark.name for mark in item.iter_markers()]
            test_details["filePath"] = item.fspath.strpath
            # pytest-playwright only
            if hasattr(item, 'callspec'):
                test_details["browser"] = item.callspec.params.get('browser_name')
            # extra
            if len(report.longrepr) > 0:
                test_details["extra"]["stackTrace"] = report.longreprtext


