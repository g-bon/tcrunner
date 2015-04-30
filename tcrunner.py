# usage: tcrunner.py [-h] [--conf CONF] [--tool TOOL] [--path PATH]
#                    [--project PROJECT] [--test TEST] [--silent SILENT]
#                    [--exit EXIT]
#
# examples: python tcrunner.py --conf neo --test 42
#           python tcrunner.py --tool TestComplete --path C:\foo\awesomeApp.pjs --project UiTests --test 42
#           python tcrunner.py --tool TestExecute --path C:\foo\awesomeApp.pjs --project UiTests
#
# optional arguments:
#   -h, --help         show this help message and exit
#   --conf CONF        Name of the configuration specified in tcrunner.config.py
#   --tool TOOL        TestComplete | TestExecute
#   --path PATH        Full path to the project suite (.pjs) file
#   --project PROJECT  The project to run in the project suite
#   --test TEST        The test case to run
#   --silent SILENT    Run test in silent mode
#   --exit EXIT        Exit after the execution is completed

import sys
import win32com.client
import argparse
import time
import tcconfig


def Stop(message):
    sys.exit("{}. Exiting...".format(message))


def CreateNewInstance(objectName):
    try:
        appInstance = win32com.client.Dispatch(objectName)
        return appInstance
    except:
        return None


def CheckForInstance(objectName):
    try:
        appInstance = win32com.client.GetActiveObject(objectName)
        return appInstance
    except:
        return None


def GetCOMObject(tool):
    TC_OLE_PATH = "TestComplete.TestCompleteApplication"
    TE_OLE_PATH = "TestExecute.TestExecuteApplication"
    tcObject = CheckForInstance(TC_OLE_PATH)
    teObject = CheckForInstance(TE_OLE_PATH)

    if tool == "TestComplete":
        if teObject:
            Stop("TestExecute is already running")

        if tcObject:
            return tcObject

        tcObject = CreateNewInstance(TC_OLE_PATH)
        if tcObject:
            return tcObject

        Stop("Cannot start TestComplete")
    else:
        if tcObject:
            Stop("TestComplete is already running")

        if teObject:
            return teObject

        teObject = CreateNewInstance(TC_OLE_PATH)
        if teObject:
            return teObject

        Stop("Cannot start TestExecute")


# Get an instance of TestComplete | TestExecute and open the project suite.
def Initialize(tool, silent, path):
    appInstance = GetCOMObject(tool)
    if not appInstance:
        Stop(tool + " COM object not found")

    if silent:
        appInstance.Manager.RunMode = 0
        appInstance.Visible = 1
    else:
        appInstance.Manager.RunMode = 3

    integration = appInstance.Integration

    if integration.IsRunning():
        print("The test is already running. Stop it manually or click 'OK' to force the test to be terminated.")
        integration.Stop()
        while appInstance.Integration.IsRunning():
            time.sleep(0.5)

    if integration.OpenProjectSuite(path) == False:
        appInstance.Quit()
        Stop("Cannot open the project")

    return appInstance


# Run a test or a entire project If a test is not specified.
def run(appInstance, subProject, test):
    if test:
        try:
            appInstance.Integration.RunProjectTestItem(subProject, test)
            print("Executing test {}".format(test))
            while appInstance.Integration.IsRunning():
                time.sleep(0.5)
        except:
            return False
    else:
        try:
            appInstance.Integration.RunProject(subProject)
            print("Executing project {}".format(subProject))
            while appInstance.Integration.IsRunning():
                time.sleep(0.5)
        except:
            return False

    return True


def main():
    argParser = argparse.ArgumentParser(description="A python test runner for SmartBear TestComplete and TestExecute")
    argParser.add_argument("--conf", help="Name of the configuration specified in tcrunner.config.py")
    argParser.add_argument("--tool", help="TestComplete | TestExecute")
    argParser.add_argument("--path", help="Full path to the project suite (.pjs) file")
    argParser.add_argument("--project", help="The project to run in the project suite")
    argParser.add_argument("--test", help="The test case to run")
    argParser.add_argument("--silent", help="Run test in silent mode")
    argParser.add_argument("--exit", help="Exit after the execution is completed")

    if len(sys.argv) == 1:
        argParser.print_help()
    exit(1)

    args = argParser.parse_args()

    # If a configured project is specified get configuration and run on
    # every project so that just the ticket number has to be specified.
    appInstance = None
    isExecuted = False
    if args.conf:
        if not args.test:
            Stop("No test specified")
        projectSuite = (conf for conf in tcconfig.configurations if conf["suite"] == args.conf).next()
        if projectSuite:
            args.tool = tcconfig.tool
            args.path = projectSuite["suitepath"]
            appInstance = Initialize(args.tool, args.silent, args.path)
            for subProject in projectSuite["subprojects"]:
                args.project = subProject
                isExecuted = run(appInstance, args.project, args.test)
                if isExecuted:
                    break
        else:
            Stop("Project suite not found in configuration file")
    else:
        appInstance = Initialize(args.tool, args.silent, args.path)
        isExecuted = run(appInstance, args.project, args.test)

    if not isExecuted:
        print("No tests executed")

    if appInstance and args.exit:
        appInstance.Quit()

if __name__ == "__main__":
    main()
