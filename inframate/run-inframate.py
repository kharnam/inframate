#!/usr/bin/env python3

"""
Usage:
    inframate_api.py [-h] [-y] [-v | -q ] [-m <all> | <packer> | \
<terraform> ] [ -a <plan> | <apply> | <destroy> | <build> | <rollback> ]
    inframate_api.py [ -m <all> ]
    inframate_api.py [ -m <packer> | <terraform> ]
    inframate_api.py [ -m <packer> ] [ -a <build> | <rollback> ]
    inframate_api.py [ -m <terraform> ] [ -a <plan> | <apply> | \
<destroy> ]

CLI to control Infrastructure Automation.

Arguments:
    all         All modules
    packer      Packer module
    terraform   Terraform
    plan        Execute 'terraform plan'
    apply       Execute 'terraform apply'
    destroy     Execute 'terraform destroy'
    build       Execute 'packer build'
    rollback    Execute 'packer rollback'

Options:
    -h --help
    -v --verbose  verbose mode
    -q --quiet    quiet mode
    -m    Module to call
    -a    Action to execute by module
    -y    Auto-assume 'Yes' on approval
"""

__author__ = "sergey kharnam"
__version__ = "0.0.1"

"""
Inframate scenarios runner architecture:
  - run-inframate -- module to implement only high-level scenarios (procedural level)
  - inframate_api -- module to provide building blocks for inframate runner/s (functional level)
  - devopsipy     -- package to implement low-level framework (core level)
"""


import sys
import os
fw_env = os.getenv('FW', '/Users/kharnam/dev/projects')
sys.path.append(fw_env + '/devopsipy/devopsipy')

# stdlib
import shlex

# PyPi
from python_terraform import *
from docopt import docopt

# Inframate
import inframate_data as id
from inframate_data import Packer as pckr
from inframate_data import Terraform as terra
import inframate_api as ia

# DevOpsiPy
import logger
import host_base
import pstate
import exceptions as pe
import host_base_const as hbc





def packer_handler(host, action):
    """
    Function to control Packer flows
    :param action: action to perform
    :return:
    """
    ia.packer_validate(host)
    log.info('------------------------------------')
    ia.packer_inspect(host)
    # log.info('------------------------------------')
    # ia.packer_build(host)


def terraform_handler(host, action):
    """
    Function to control Terraform flows
    :param action: action to perform
    :return:
    """
    ia.terraform_init(host)
    ia.terraform_plan(host)
    ia.terraform_apply(host)
    # terraform_destroy(host)


# ---------------------
# Main

def main(arg):
    """
    Main function
    :param arg: user input arguments
    :return:
    """

    log = logger.set_logger('Inframate')
    host = host_base.HostBase('localhost')
    packer_handler(host=host, action=None)
    # terraform_handler(host=host, action=None)


# Execution
if __name__ == '__main__':
    arg = docopt(__doc__)
    main(arg)
