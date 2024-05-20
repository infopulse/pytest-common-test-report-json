from pytest import Config, hookimpl, Item, CallInfo, CollectReport, Function, TestReport, fixture, FixtureRequest
from .Report import Report
from collections import OrderedDict


class CTRF:
    def __init__(self, config: Config or None = None):
        self._config = config
        self._report: Report or None = None
        self._json_tests = OrderedDict()

    def pytest_configure(self, config: Config):
        if self._config is None:
            self._config = config
        if not hasattr(config, '_ctrf'):
            self._config._ctrf = self

        if config.option.ctrf:
            self._report = Report(config.option.ctrf)

    @hookimpl(tryfirst=True)
    def pytest_sessionstart(self, session):
        if self._report:
            self._report.start()

    @hookimpl(tryfirst=True)
    def pytest_sessionfinish(self, session):
        if self._report:
            self._report.stop()
            self._report.save()

    def pytest_runtest_logreport(self, report: TestReport):
        self._report.collect(report)

    @fixture(autouse=True)
    def json_metadata(self, request: FixtureRequest):
        node = request.node
        pass
        # try:
        #     return request.node._json_report_extra.setdefault('metadata', {})
        # except AttributeError:
        #     if not request.config.option.json_report:
        #         # The user didn't request a JSON report, so the plugin didn't
        #         # prepare a metadata context. We return a dummy dict, so the
        #         # fixture can be used as expected without causing internal errors.
        #         return {}
        #     raise
