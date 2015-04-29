# configuration file for tcrunner.py

tool = "TestComplete"

configurations = [
    dict(
        suite='AwesomeApp',
        suitepath='C:\\foo\\awesomeApp.pjs',
        subprojects=[
            'UiTests',
            'FunctionalTests',
        ]),
    dict(
        suite='VeryAwesomeApp',
        suitepath='C:\\bar\\veryAwesomeApp.pjs',
        subprojects=[
            'Activities',
            'FunctionalTests',
        ])
]
