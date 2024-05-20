from pytest import Config, Parser
from .CommonTestReportPlugin import CTRF


def pytest_addoption(parser: Parser):
    parser.addoption('--ctrf',
                     action='store',
                     help='generate test report. Report file name is optional')


def pytest_configure(config: Config):
    if not config.option.ctrf:
        return
    if not hasattr(config, 'workerinput'):
        ctrf = CTRF(config)
        config._ctrf = CTRF(config)
        config.pluginmanager.register(ctrf, name='ctrf')


def pytest_unconfigure(config: Config):
    ctrf = getattr(config, '_ctrf', None)
    if ctrf is not None:
        del config._ctrf
    if config.pluginmanager.hasplugin('ctrf'):
        config.pluginmanager.unregister(name='ctrf')
