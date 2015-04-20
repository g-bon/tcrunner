# usage: single_test.py [-h] --tool TOOL --path PATH --project PROJECT
#                       [--test TEST] [--silent SILENT] [--exit EXIT]

import sys
import win32com.client
import argparse
import time

AppObject = ""

def Stop(message):
    sys.exit(message)


def CreateNewInstance(ObjectName):
    try:
        global AppObject
        AppObject = win32com.client.Dispatch(ObjectName)
        return True
    except:
        return False

def CheckForInstance(ObjectName):
    try:
        global AppObject
        AppObject = win32com.client.GetActiveObject(ObjectName)
        return True
    except:
        return False

def GetCOMObject(ToolToRun):
    tcActive = CheckForInstance("TestComplete.TestCompleteApplication")
    teActive = CheckForInstance("TestExecute.TestExecuteApplication")

    if ToolToRun == "TestComplete":
        if (teActive):
            Stop("TestExecute is already running. Exiting...")
        else:
            if (tcActive):
                return True
            if CreateNewInstance("TestComplete.TestCompleteApplication"):
                return True
            Stop("Cannot start TestComplete. Exiting...")
    else:
        if (tcActive):
            Stop("TestComplete is already running. Exiting...")
        else:
            if (teActive):
                return True
            if CreateNewInstance("TestExecute.TestExecuteApplication"):
                return True
            Stop("Cannot start TestComplete. Exiting...")

    return False


def main():
    argParser = argparse.ArgumentParser(description="A python test executor for testcomplete")
    argParser.add_argument("--tool", required=True)
    argParser.add_argument("--path", required=True)
    argParser.add_argument("--project", required=True)
    argParser.add_argument("--test")
    argParser.add_argument("--silent", default=False)
    argParser.add_argument("--exit")
    args = argParser.parse_args()

    global AppObject
    GetCOMObject(args.tool)
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

    if args.exit != "":
        AppObject.Quit()

if __name__ == "__main__":
    main()

