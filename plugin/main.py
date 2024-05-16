from pytest import hookimpl, Config, Item, CallInfo


class CTRF:
    def __init__(self, config: Config or None = None):
        self._config = config

    @staticmethod
    def _test_report(item: Item, call: CallInfo) -> dict:
        result = {
            "name": item.name,
            "status": None,
            "duration": None,
            "start": None,
            "stop": None,
            "suite": None,
            "tags": [],
            "filePath": None,
            "retries": 0,
            "browser": None,
            "extra":  {
                "stackTrace": None,
            }
        }
        return result

    def pytest_configure(self, config):
        '''
        Failsafe method to set config object
        :param config: pytest.Config
        :return: None
        '''
        if self._config is None:
            self._config = config
        if not hasattr(config, '_ctrf'):
            self._config._ctrf = self

    @hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item: Item, call: CallInfo):
        report = (yield).get_result()
        if not self._must_omit('streams'):
            streams = {key: val for when_, key, val in item._report_sections if
                       when_ == report.when and key in ['stdout', 'stderr']}
            item._json_report_extra[call.when].update(streams)
        for dict_ in self._config.hook.pytest_json_runtest_metadata(item=item,
                                                                    call=call):
            if not dict_:
                continue
            item._json_report_extra.setdefault('metadata', {}).update(dict_)
        self._validate_metadata(item)
        # Attach the JSON details to the report. If this is an xdist worker,
        # the details will be serialized and relayed with the other attributes
        # of the report.
        report._json_report_extra = item._json_report_extra

    # def pytest_addhooks(self, pluginmanager):
    #     pluginmanager.add_hookspecs(Hooks)


# class Hooks:
#
#     def pytest_json_modify_report(self, json_report):
#         """Called after building JSON report and before saving it.
#         Plugins can use this hook to modify the report before it's saved.
#         """
#
#     def pytest_add_test_metadata(self, item, call):
#         """Return a dict which will be added to the current test item's JSON
#         metadata.
#         Called from `pytest_runtest_makereport`. Plugins can use this hook to
#         add metadata based on the current test run.
#         """

def pytest_addoption(parser):
    group = parser.getgroup('CTRF', 'collecting test results in JSON format')
    group.addoption('--ctrf',
                    help='generate test report. Report file name is optional',
                    type=str,
                    nargs='?',
                    const='report.json',
                    default=None)


def pytest_configure(config):
    if not config.option.ctrf:
        return
    ctrf = CTRF(config)
    config._ctrf = CTRF(config)
    config.pluginmanager.register(ctrf)


def pytest_unconfigure(config):
    ctrf = getattr(config, '_ctrf', None)
    if ctrf is not None:
        del config.ctrf
        config.pluginmanager.unregister(ctrf)
