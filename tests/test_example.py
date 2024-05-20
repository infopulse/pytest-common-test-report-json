from pytest import mark, fixture


@fixture
def pre_fail():
    raise Exception("This is a test exception")


@fixture
def post_fail():
    yield
    raise Exception("This is a test exception")


def test_do_calculations_1_pass():
    assert 2 + 2 == 4


@mark.regression
def test_do_calculations_2_pass():
    assert 3 + 3 == 6


@mark.skip
def test_do_calculations_3_skip():
    assert 4 + 4 == 8


@mark.smoke
def test_do_calculations_4_smoke():
    assert 5 + 5 == 10


def test_do_calculations_5_fail():
    assert 6 + 6 == 13


def test_do_calculations_6_error():
    raise Exception("This is a test exception")


def test_do_calculations_7_pre_error(pre_fail):
    assert 7 + 7 == 14


def test_do_calculations_8_post_error(post_fail):
    assert 8 + 8 == 16


@mark.parametrize('param', [1, 2, 3, 4, 5])
def test_parametrized(param):
    assert param < 10
