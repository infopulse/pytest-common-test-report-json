# CTRF for pytest

Pytest implementation of Common Test Report Format (CTRF) for test results.  
Test report will be generated in JSON format.  
Test report can be used to prettify the report in GitHub Actions with [github-actions-ctrf](https://github.com/ctrf-io/github-actions-ctrf).  
Do not worry if report in GitHub does not appear immediately. It takes some time to process the report. 

## Features
- Generates JSON report
- Tested to work correctly with and without [pytest-xdist](https://pypi.org/project/pytest-xdist/)
- Tested to get browser name from [pytest-playwright](https://pypi.org/project/pytest-playwright/)
- Parametrized tests are supported and reported as 1 test with multiple retries

## Installation

```bash
pip install pytest-json-ctrf
```

## Usage

generate report.json file in the root directory of the project. File path is mandatory

```bash
pytest --ctrf report.json
```

## Json exampe

More info here: https://ctrf.io/docs/schema/examples

```json
{
  "results": {
    "tool": {
      "name": "jest"
    },
    "summary": {
      "tests": 3,
      "passed": 1,
      "failed": 1,
      "pending": 0,
      "skipped": 1,
      "other": 0,
      "start": 1706644023,
      "stop": 1706644043
    },
    "tests": [
      {
        "name": "User should be able to login",
        "status": "passed",
        "duration": 1200
      },
      {
        "name": "User profile information should be correct",
        "status": "failed",
        "duration": 800
      },
      {
        "name": "User should be able to logout",
        "status": "skipped",
        "duration": 0
      }
    ]
  }
}
```

## Report Example
![Example Image](./assets/report_example.png)

## Credits

- https://ctrf.io/ -> nice data format
- https://github.com/numirias/pytest-json-report -> Source of inspiration and dealing with xdist sync
- https://github.com/testomatio/pytestomatio -> Source of inspiration for creating pytest plugins
- https://github.com/infopulse/Playwright-course-python -> The report will be used in the demo project as +1 report option

