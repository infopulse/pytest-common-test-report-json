import os
import pytest
import time
import json
from pytest import Item, CallInfo, TestReport, Mark
from collections import OrderedDict
from .TestObject import TestObject, TestStatus


class Report:
    def __init__(self):
        self.test_items = OrderedDict()
        self.prepared_tests = dict()
        self.start_time = None
        self.stop_time = None

    def start(self) -> None:
        self.start_time = time.time()

    def stop(self) -> None:
        self.stop_time = time.time()

    @staticmethod
    def _get_tool() -> dict:
        return {
            "name": "pytest",
            "version": str(pytest.__version__)
        }

    def _get_summary(self) -> dict:
        return {
            'tests': len(self.prepared_tests),
            'passed': len([test for test in self.prepared_tests.values() if test.status == TestStatus.PASSED]),
            'failed': len([test for test in self.prepared_tests.values() if test.status == TestStatus.FAILED]),
            'skipped': len([test for test in self.prepared_tests.values() if test.status == TestStatus.SKIPPED]),
            'pending': len([test for test in self.prepared_tests.values() if test.status == TestStatus.PENDING]),
            'other': 0,
            'start': self.start_time,
            'stop': self.stop_time
        }

    def collect(self, report: TestReport) -> None:
        if report.nodeid not in self.test_items.keys():
            test = TestObject()
        else:
            test = self.test_items.get(report.nodeid)
        test.update(report, getattr(report, 'worker_id', None))
        self.test_items[report.nodeid] = test

    def process_retries(self) -> None:
        for test_id, test_data in self.test_items.items():
            name = test_id.split('[')[0]
            test = self.prepared_tests.get(name)
            if test:
                test.retries += 1
            else:
                self.prepared_tests[name] = test_data

    def get_report(self) -> dict:
        self.process_retries()
        return {'results':
            {
                "tool": self._get_tool(),
                "summary": self._get_summary(),
                "tests": [test.serialize() for test in self.prepared_tests.values()]
            }
        }

    def save(self, report_file: str) -> None:
        dirname = os.path.dirname(report_file)
        if dirname:
            try:
                os.makedirs(dirname)
            except Exception as e:
                print(e)
                raise Exception(f"Can't create directory {dirname}")
        with open(report_file, 'w') as file:
            json.dump(self.get_report(), file, default=str, indent=4)
