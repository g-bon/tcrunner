# tcrunner

*tcrunner* is a python test runner for SmartBear [TestComplete](http://smartbear.com/product/testcomplete/overview/) and TestExecute.

## Why && Features
I created this script to overcome some of issues I found using the standard TestExecute interface as the impossibility to run single test cases insted of projects, and to have a tool that is easy to use and easier to integrate with other test automation scripts.

Here are some of the features:
- Run single scripts
- Run project
- Run suite (In progress)
- Run in silent mode
- Configuration file (In progress)
- Simplified run of single testcase using the testcase name only (In progress, requires configuration file)

## Usage
````
## Usage
Usage: single_test.py [-h] [--test TEST] [--silent SILENT] [--exit EXIT] tool path project

required arguments:
   tool             TestComplete | TestExecute
   path             Full path to the project suite (.pjs) file
   project          The project to run in the project suite

optional arguments:
   -h, --help       show help message and exit
   --test TEST      The test case to run
   --silent SILENT  Run test in silent mode
   --exit EXIT      Exit after the execution is completed
````

## Authors and contributing

tcrunner has been initially written and is maintained by Gabriele Bonetti but you are very welcome to submit a [pull request](https://help.github.com/articles/using-pull-requests/) for any improvement you might like.
