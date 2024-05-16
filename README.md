# CTRF for pytest

Pytest implementation of Common Test Report Format (CTRF) for test results.  
Test report will be generated in JSON format.

## Installation

```bash
pip install ctrf-pytest
```

## Usage

generate report.json file in the root directory of the project

```bash
pytest --ctrf
```

generate report file in the specified directory

```bash
pytest --ctrf=results/test-report.json
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

## Credits

- https://ctrf.io/
- https://github.com/numirias/pytest-json-report
- https://github.com/testomatio/pytestomatio

