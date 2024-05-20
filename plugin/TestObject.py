from enum import Enum
from pytest import TestReport


class TestStatus(Enum):
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    PENDING = "pending"
    OTHER = "other"


class TestObject:
    name: str = None
    status: TestStatus = TestStatus.PENDING
    raw_status: str = None
    duration: float = 0
    start: float = None
    stop: float = None
    retries: int = 0

    worker_id: str = None
    file_path: str = None
    tags: list[str] = None
    browser: str = None
    trace: str = None

    def set_status(self, report: TestReport) -> None:
        if self.status in (TestStatus.SKIPPED, TestStatus.FAILED):
            return
        elif report.skipped:
            self.status = TestStatus.SKIPPED
        elif report.failed:
            self.status = TestStatus.FAILED
            self.raw_status = f"{report.when}_{report.outcome}"
        elif report.passed:
            self.status = TestStatus.PASSED
        else:
            self.status = TestStatus.OTHER

    def update(self, report: TestReport, worker_id: str = None) -> None:
        self.name = report.head_line.split('[')[0]
        self.set_status(report)
        self.duration += report.duration
        if report.when == "setup" and not self.start:
            self.start = report.start
        if report.when == "teardown" and not self.stop:
            self.stop = report.stop
        self.file_path = report.location[0]
        if report.longrepr and len(report.longreprtext) > 0:
            self.trace = report.longreprtext
        if hasattr(report, '_ctrf_metadata'):
            self.tags = report._ctrf_metadata.get('tags')
            self.browser = report._ctrf_metadata.get('browser')
        self.worker_id = worker_id

    def serialize(self) -> dict:
        result = {
            'name': self.name,
            'status': self.status.value,
            'raw_status': self.raw_status,
            'duration': self.duration,
            'start': self.start,
            'stop': self.stop,
            'retries': None if self.retries == 1 else self.retries,
            'file_path': self.file_path,
            'tags': self.tags,
            'browser': self.browser,
            'trace': self.trace
        }
        if self.worker_id:
            result['extra'] = {'worker': self.worker_id}
        return {key: value for key, value in result.items() if value not in [None, '', []]}
