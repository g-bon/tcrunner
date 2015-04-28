# usage: single_test.py [-h] [--test TEST] [--silent SILENT] [--exit EXIT] tool path project
#
# A python test runner for SmartBear TestComplete and TestExecute
#
# positional arguments:
#   tool             TestComplete | TestExecute
#   path             Full path to the project suite (.pjs) file
#   project          The project to run in the project suite
#
# optional arguments:
#   -h, --help       show this help message and exit
#   --test TEST      The test case to run
#   --silent SILENT  Run test in silent mode
#   --exit EXIT      Exit after the execution is completed

import sys
import win32com.client
import argparse
import time


def Stop(message):
    sys.exit("{} . Exiting...".format(message))


def CreateNewInstance(ObjectName):
    try:
        AppInstance = win32com.client.Dispatch(ObjectName)
        return AppInstance
    except:
        return None


def CheckForInstance(ObjectName):
    try:
        AppInstance = win32com.client.GetActiveObject(ObjectName)
        return AppInstance
    except:
        return None


def GetCOMObject(ToolToRun):
    TC_OLE_PATH = "TestComplete.TestCompleteApplication"
    TE_OLE_PATH = "TestExecute.TestExecuteApplication"
    tcObject = CheckForInstance(TC_OLE_PATH)
    teObject = CheckForInstance(TE_OLE_PATH)

    if ToolToRun == "TestComplete":
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

    return False


def main():
    argParser = argparse.ArgumentParser(description="A python test runner for SmartBear TestComplete and TestExecute")
    argParser.add_argument("tool", help="TestComplete | TestExecute")
    argParser.add_argument("path", help="Full path to the project suite (.pjs) file")
    argParser.add_argument("project", help="The project to run in the project suite")
    argParser.add_argument("--test", help="The test case to run")
    argParser.add_argument("--silent", help="Run test in silent mode")
    argParser.add_argument("--exit", help="Exit after the execution is completed")
    args = argParser.parse_args()

    AppInstance = GetCOMObject(args.tool)  # TestComplete or TestExecute instance

    if AppInstance is None:
        Stop(args.tool + " COM object not found")

    if args.silent is None:
        AppInstance.Manager.RunMode = 0
        AppInstance.Visible = 1
    else:
        AppInstance.Manager.RunMode = 3

    integration = AppInstance.Integration

    if integration.IsRunning():
        print("The test is already running. Stop it manually or click 'OK' to force the test to be terminated.")
        integration.Stop()
        while AppInstance.Integration.IsRunning():
            time.sleep(0.5)

    if integration.OpenProjectSuite(args.path) == False:
        AppInstance.Quit()
        Stop("Cannot open the project")

    if args.test is not None:
        AppInstance.Integration.RunProjectTestItem(args.project, args.test)
    else:
        AppInstance.Integration.RunProject(args.project)

    while AppInstance.Integration.IsRunning():
        time.sleep(0.5)

    if args.exit is not None:
        AppInstance.Quit()

if __name__ == "__main__":
    main()
