from pytest import hookimpl, TestReport
from collections import OrderedDict
from .BaseMetadataReport import metadata, BaseMetadataReport


class CTRF(BaseMetadataReport):
    def __init__(self):
        super().__init__()
        self._json_tests = OrderedDict()

    @hookimpl(tryfirst=True)
    def pytest_sessionstart(self, session):
        if self._report:
            self._report.start()

    @hookimpl(tryfirst=True)
    def pytest_sessionfinish(self, session):
        if self._report:
            self._report.stop()
            self._report.save(session.config.option.ctrf)

    def pytest_runtest_logreport(self, report: TestReport):
        if not hasattr(report, metadata):
            setattr(report, metadata, {})
        self._report.collect(report)
