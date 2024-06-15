from pytest import Config, hookimpl, Item
from .Report import Report

metadata = '_ctrf_metadata'


class BaseMetadataReport:
    '''This class needed only to get metadata
    from test nodes from different workers and
    transfer it the report objects'''

    def __init__(self):
        self._report = Report()

    def pytest_configure(self, config: Config):
        if not hasattr(config, '_ctrf'):
            setattr(config, '_ctrf', self)

        if config.option.ctrf and not self._report:
            self._report = Report()

    @hookimpl(hookwrapper=True)
    def pytest_runtest_protocol(self, item: Item, nextitem: Item):
        setattr(item, metadata, {})
        yield
        delattr(item, metadata)

    @hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        report = (yield).get_result()
        meta = getattr(item, metadata)
        if meta:
            setattr(report, metadata, meta)
