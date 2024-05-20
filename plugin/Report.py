import os
import pytest
import time
import json
from pytest import Item, CallInfo, TestReport, Mark
from enum import Enum
from collections import OrderedDict


class TestStatus(Enum):
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    PENDING = "pending"
    OTHER = "other"


class Report:
    def __init__(self, report_file: str):
        self.test_items = OrderedDict()
        self.start_time = None
        self.stop_time = None
        self.report_file = report_file

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.stop_time = time.time()

    @staticmethod
    def _get_tool():
        return {
            "name": "pytest",
            "version": str(pytest.__version__)
        }

    def _get_summary(self):
        return {
            'tests': len(self.test_items),
            'passed': len([test for test in self.test_items.values() if test['status'] == TestStatus.PASSED]),
            'failed': len([test for test in self.test_items.values() if test['status'] == TestStatus.FAILED]),
            'skipped': len([test for test in self.test_items.values() if test['status'] == TestStatus.SKIPPED]),
            'pending': len([test for test in self.test_items.values() if test['status'] == TestStatus.PENDING]),
            'other': 0,
            'start': self.start_time,
            'stop': self.stop_time
        }

    @staticmethod
    def _get_test_status(report: TestReport) -> TestStatus:
        if report.skipped:
            return TestStatus.SKIPPED
        elif report.failed:
            return TestStatus.FAILED
        elif report.passed:
            return TestStatus.PASSED
        else:
            return TestStatus.OTHER

    def _add(self, nodeid: str, test_report: TestReport):
        worker = None
        if hasattr(test_report, 'worker_id'):
            worker = test_report.worker_id
        if nodeid not in self.test_items.keys():
            self.test_items[nodeid] = {
                "name": test_report.head_line,
                "status": self._get_test_status(test_report),
                "duration": 0,
                'extra': {'worker': worker if worker else 'controller'}
            }

    def _list_tests(self):
        for test in self.test_items.values():
            test['status'] = test['status'].value
            yield test

    def collect(self, report: TestReport):
        nodeid = report.nodeid
        if nodeid not in self.test_items.keys():
            self._add(nodeid, report)
        else:
            test_details = self.test_items.get(nodeid)
            if test_details["status"] not in (TestStatus.SKIPPED, TestStatus.FAILED):
                test_details["status"] = self._get_test_status(report)
                if test_details["status"] == TestStatus.FAILED:
                    test_details['rawStatus'] = f"{report.when}_{report.outcome}"

            test_details["duration"] += report.duration
            if report.when == "call":
                test_details["start"] = report.start
            if report.when == "teardown":
                test_details["stop"] = report.stop
            # metadata
            test_details["filePath"] = report.location[0]
            # extra
            if report.longrepr and len(report.longreprtext) > 0:
                test_details["extra"]["stackTrace"] = report.longreprtext

    def get_report(self):
        return {'results':
            {
                "tool": self._get_tool(),
                "summary": self._get_summary(),
                "tests": list(self._list_tests())
            }
        }

    def save(self):
        dirname = os.path.dirname(self.report_file)
        if dirname:
            try:
                os.makedirs(dirname)
            except Exception as e:
                print(e)
                raise Exception(f"Can't create directory {dirname}")
        with open(self.report_file, 'w') as file:
            json.dump(self.get_report(), file, default=str, indent=4)
