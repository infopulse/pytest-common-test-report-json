from pytest import Config, Parser, FixtureRequest, fixture
from ctrf.CommonTestReportPlugin import CTRF
from ctrf.BaseMetadataReport import BaseMetadataReport


def pytest_addoption(parser: Parser):
    group = parser.getgroup('ctrf', 'generate test report in CTR format')
    group.addoption('--ctrf',
                    action='store',
                    help='generate test report. Report file name is optional')


def pytest_configure(config: Config):
    if not config.option.ctrf:
        return
    if hasattr(config, 'workerinput'):
        plugin = BaseMetadataReport()
    else:
        plugin = CTRF()
    setattr(config, '_ctrf', plugin)
    config.pluginmanager.register(plugin, name='ctrf_plugin')
    pass


def pytest_unconfigure(config: Config):
    ctrf = getattr(config, '_ctrf', None)
    if ctrf is not None:
        delattr(config, '_ctrf')
    if config.pluginmanager.hasplugin('ctrf_plugin'):
        config.pluginmanager.unregister(name='ctrf_plugin')


@fixture(autouse=True)
def ctrf_json_metadata(request: FixtureRequest):
    if not request.config.option.ctrf:
        return
    tags = [mark.name for mark in request.node.iter_markers()]
    request.node._ctrf_metadata.setdefault('tags', tags)
    if hasattr(request.node, 'callspec'):
        browser = request.node.callspec.params.get('browser_name')
        if browser:
            request.node._ctrf_metadata.setdefault('browser', browser)
    return request.node._ctrf_metadata
