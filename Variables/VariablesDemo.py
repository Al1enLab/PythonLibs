from Variables import *
import configparser
import argparse
import os
from types import SimpleNamespace

from pprint import pprint

demo_config_content = """
[System]
HomeDir = /ConfigFileHomeDir
AppDir = /ConfigFileAppDir
WorkDir = /ConfigFileWorkDir
"""

configfile = configparser.ConfigParser()
configfile.read_string(demo_config_content)

parsedargs = argparse.Namespace()
setattr(parsedargs, 'work-dir', 'CmdArgWorkdir')

config = SimpleNamespace(
    homedir=PreferredVariable(
        CommandArgument(parsedargs, 'home-dir'),
        EnvironmentVariable('USERPROFILE'),
        EnvironmentVariable('HOME'),
        ConfigFileVariable(configfile, 'System', 'HomeDir'),
        DefaultValue(value='DefaultValueHomeDir')
    ),
    workdir=PreferredVariable(
        CommandArgument(parsedargs, 'work-dir'),
        EnvironmentVariable('CWD'),
        ConfigFileVariable(configfile, 'System', 'WorkDir'),
        DefaultValue('/DefaultWorkDir')
    ),
    appdir=PreferredVariable(
        CommandArgument(parsedargs, 'app-dir'),
        EnvironmentVariable('APPDIR'),
        ConfigFileVariable(configfile, 'System', 'AppDir'),
        DefaultValue(value='/DefaulAppDir')
    ),
    tmpdir=PreferredVariable(
        CommandArgument(parsedargs, 'tmp-dir'),
        EnvironmentVariable('FAKETMPDIR'),
        ConfigFileVariable(configfile, 'System', 'TmpDir'),
        DefaultValue('/DefaultTmpDir')
    )
)
pprint(config)
