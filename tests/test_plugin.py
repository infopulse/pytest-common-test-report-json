import json
from pytest import Pytester, fixture

pytest_plugins = ["pytester", "xdist", "ctrf"]
test_file = "tests/test_example.py"
basic_test_args = ["-k", "test_example"]


@fixture
def ctrf_report_sync(pytester: Pytester):
    pytester.copy_example(test_file)
    pytester.runpytest(*[*basic_test_args, "--ctrf", "report.json"])
    with open(pytester.path / "report.json") as file:
        yield json.load(file)


@fixture
def ctrf_report_xdist(pytester: Pytester):
    pytester.copy_example(test_file)
    pytester.runpytest(*[*basic_test_args, "--ctrf", "report.json", "-n", "3"])
    with open(pytester.path / "report.json") as file:
        yield json.load(file)


def test_without_plugin_no_xdist(pytester: Pytester):
    pytester.copy_example(test_file)
    result = pytester.runpytest(*basic_test_args)
    result.assert_outcomes(passed=9, skipped=1, failed=2, errors=2)


def test_without_plugin_with_xdist(pytester: Pytester):
    pytester.copy_example(test_file)
    result = pytester.runpytest(*[*basic_test_args, "-n", "3"])
    result.assert_outcomes(passed=9, skipped=1, failed=2, errors=2)
    assert "created: 3/3 workers" in result.stdout.str()


def test_with_markers(pytester: Pytester):
    pytester.copy_example(test_file)
    args = [*basic_test_args, "--ctrf", "report.json", "-m smoke"]
    pytester.runpytest(*args)
    with open(pytester.path / "report.json") as file:
        report = json.load(file)
    assert report["results"]["summary"]["tests"] == 1
    assert report["results"]["summary"]["passed"] == 1
    assert report["results"]["summary"]["failed"] == 0
    assert report["results"]["summary"]["skipped"] == 0


def test_with_plugin_no_xdist(ctrf_report_sync):
    assert ctrf_report_sync["results"]["summary"]["tests"] == 9
    assert ctrf_report_sync["results"]["summary"]["passed"] == 4
    assert ctrf_report_sync["results"]["summary"]["failed"] == 4
    assert ctrf_report_sync["results"]["summary"]["skipped"] == 1


def test_with_plugin_failed_details(ctrf_report_sync):
    for test in ctrf_report_sync["results"]["tests"]:
        if test["status"] == "failed" and test.get("raw_status") == "call_failed":
            assert test.get('trace') is not None
            assert test.get("message") is not None
            assert test.get("raw_status") is not None


def test_any_test_has_timestamps(ctrf_report_sync):
    for test in ctrf_report_sync["results"]["tests"]:
        assert test.get("start") is not None
        assert test.get("stop") is not None
        assert test.get("duration") is not None


def test_with_plugin_with_xdist(ctrf_report_xdist):
    assert ctrf_report_xdist["results"]["summary"]["tests"] == 9
    assert ctrf_report_xdist["results"]["summary"]["passed"] == 4
    assert ctrf_report_xdist["results"]["summary"]["failed"] == 4
    assert ctrf_report_xdist["results"]["summary"]["skipped"] == 1


def test_with_plugin_failed_details_xdist(ctrf_report_xdist):
    for test in ctrf_report_xdist["results"]["tests"]:
        if test["status"] == "failed" and test.get("raw_status") == "call_failed":
            assert test.get('trace') is not None
            assert test.get("message") is not None
            assert test.get("raw_status") is not None


def test_any_test_has_timestamps_xdist(ctrf_report_xdist):
    for test in ctrf_report_xdist["results"]["tests"]:
        assert test.get("start") is not None
        assert test.get("stop") is not None
        assert test.get("duration") is not None
