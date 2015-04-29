# tcrunner
*tcrunner* is a python test runner for SmartBear [TestComplete](http://smartbear.com/product/testcomplete/overview/) and TestExecute.

## Why && Features
I created this script to overcome some of issues I found using the standard TestExecute interface as the impossibility to run single test cases insted of projects, and to have a tool that is easy to use and easier to integrate with other test automation scripts.

Here are some of the features:
- Run single scripts
- Run project
- Run suite (In progress)
- Run in silent mode
- Configuration file
- Simplified run of single testcase using the testcase name only

## Usage
````
usage: tcrunner.py [-h] [--conf CONF] [--tool TOOL] [--path PATH]
                   [--project PROJECT] [--test TEST] [--silent SILENT]
                   [--exit EXIT]

examples: python tcrunner.py --conf neo --test 42
          python tcrunner.py --tool TestComplete --path C:\foo\awesomeApp.pjs --project UiTests --test 42
          python tcrunner.py --tool TestComplete --path C:\foo\awesomeApp.pjs --project UiTests

optional arguments:
  -h, --help         show this help message and exit
  --conf CONF        Name of the configuration specified in tcrunner.config.py
  --tool TOOL        TestComplete | TestExecute
  --path PATH        Full path to the project suite (.pjs) file
  --project PROJECT  The project to run in the project suite
  --test TEST        The test case to run
  --silent SILENT    Run test in silent mode
  --exit EXIT        Exit after the execution is completed
````

## Contributing
tcrunner has been initially written and is maintained by Gabriele Bonetti but you are very welcome to submit a [pull request](https://help.github.com/articles/using-pull-requests/) for any improvement you might like.
