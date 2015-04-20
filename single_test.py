# usage: single_test.py [-h] --tool TOOL --path PATH --project PROJECT
#                       [--test TEST] [--silent SILENT] [--exit EXIT]
#
# A python test runner for SmartBear TestComplete and TestExecute
#
# Arguments:
#   -h, --help         show this help message and exit
#   --tool TOOL        TestComplete | TestExecute
#   --path PATH        Full path to the .pjs file
#   --project PROJECT  The project to run, if running a project suite
#   --test TEST        The test case to run
#   --silent SILENT    Run test in silent mode
#   --exit EXIT        Exit after the execution is completed

import sys
import win32com.client
import argparse
import time

def Stop(message):
    sys.exit(message)

def CreateNewInstance(ObjectName):
    try:
        AppObject = win32com.client.Dispatch(ObjectName)
        return AppObject
    except:
        return None

def CheckForInstance(ObjectName):
    try:
        AppObject = win32com.client.GetActiveObject(ObjectName)
        return AppObject
    except:
        return None

def GetCOMObject(ToolToRun):
    TC_OLE_PATH = "TestComplete.TestCompleteApplication"
    TE_OLE_PATH = "TestExecute.TestExecuteApplication"
    tcObject = CheckForInstance(TC_OLE_PATH)
    teObject = CheckForInstance(TE_OLE_PATH)

    if ToolToRun == "TestComplete":
        if teObject:
            Stop("TestExecute is already running. Exiting...")

        if tcObject:
            return tcObject

        tcObject = CreateNewInstance(TC_OLE_PATH)
        if tcObject:
            return tcObject

        Stop("Cannot start TestComplete. Exiting...")
    else:
        if tcObject:
            Stop("TestComplete is already running. Exiting...")

        if teObject:
            return teObject

        teObject = CreateNewInstance(TC_OLE_PATH)
        if teObject:
            return teObject

        Stop("Cannot start TestExecute. Exiting...")

    return False

def main():
    argParser = argparse.ArgumentParser(description="A python test runner for SmartBear TestComplete and TestExecute")
    argParser.add_argument("--tool", help="TestComplete | TestExecute", required=True)
    argParser.add_argument("--path", help="Full path to the .pjs file", required=True)
    argParser.add_argument("--project", help="The project to run, if running a project suite", required=True)
    argParser.add_argument("--test", help="The test case to run")
    argParser.add_argument("--silent", help="Run test in silent mode", default=False)
    argParser.add_argument("--exit", help="Exit after the execution is completed")
    args = argParser.parse_args()

    AppObject = GetCOMObject(args.tool)
    if AppObject is None:
        Stop(args.tool + " COM object not found")

    AppObject.Visible = 1
    if args.silent:
        AppObject.Manager.RunMode = 0
        AppObject.Visible = True
    else:
        AppObject.Manager.RunMode = 3

    integration = AppObject.Integration

    if integration.IsRunning():
        print("The test is already running. Stop it manually or click 'OK' to force the test to be terminated.")
        integration.Stop()
        while AppObject.Integration.IsRunning():
            time.sleep(0.1)

    if integration.OpenProjectSuite(args.path) == False:
        AppObject.Quit()
        Stop("Cannot open the project (project suite). Please check the path.")

    if args.test != "":
        AppObject.Integration.RunProjectTestItem(args.project, args.test)
    else:
        AppObject.Integration.RunProject(args.project)

    while AppObject.Integration.IsRunning():
        time.sleep(0.5)

    if args.exit is not None:
        AppObject.Quit()

if __name__ == "__main__":
    main()

