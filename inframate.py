#!/usr/bin/env python3
"""
Usage:
    run_infra_automation.py [-h] [-y] [-v | -q ] [-m <all> | <packer> | \
<terraform> ] [ -a <plan> | <apply> | <destroy> | <build> | <rollback> ]
    run_infra_automation.py [ -m <all> ]
    run_infra_automation.py [ -m <packer> | <terraform> ]
    run_infra_automation.py [ -m <packer> ] [ -a <build> | <rollback> ]
    run_infra_automation.py [ -m <terraform> ] [ -a <plan> | <apply> | \
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

# -------------------
# Imports

import logging
import re
import subprocess
import sys

from docopt import docopt
from python_terraform import *

from inframate_data import Packer as pckr
from inframate_data import Terraform as terra


__author__ = "sergey kharnam"
__version__ = "0.0.1"


# Setup logging
log = logging.getLogger('InfraAutomation')
log.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('/tmp/logs/infra_automation.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
log.addHandler(ch)
log.addHandler(fh)

# -------------------
# System generics


def execute(*command):
    next_input = None
    for cmd in command:
        p = subprocess.Popen(cmd, stdin=next_input, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, universal_newlines=True)
        next_input = p.stdout
        for stdout_line in iter(p.stdout.readline, ""):
            yield stdout_line
        p.stdout.close()
        return_code = p.wait()
        if return_code:
            raise subprocess.CalledProcessError(return_code, cmd)


def run_command(*command):
    """
    Function to execute arbitrary series of shell commands.
    Support pipe in format: (['cmd1','args'],['cmd2', 'args'],..)
        :param *command: tupple of lists (see above)
        :return 1: if stderr has a value
    """
    if not command:
        return
    for cmd in command:
        log.debug('executing command    < {0} >'.format(cmd))
        ignored = ['\n']
        for line in execute(cmd):
            if line and line not in ignored:
                log.info(line)


# ---------------------
# Packer


def packer_validate():
    """Function to validate Packer templates.
    """
    log.info("Starting Packer template validation...")
    cmd = list([pckr.packer_base_cmd, 'validate'])
    cmd.extend(pckr.packer_cmd_args)
    run_command(cmd)


def packer_inspect():
    """ Function to inspect Packer template.
    """
    log.info('Starting Packer template inspection...')
    cmd = list([pckr.packer_base_cmd, 'inspect'])
    cmd.append(pckr.packer_cmd_args[-1])
    run_command(cmd)


def packer_build():
    """ Function to execute 'packer build'
    """
    log.info('Starting Packer image build process...')
    cmd = list([pckr.packer_base_cmd_verbose if arg['--verbose']
                else pckr.packer_base_cmd, 'build'])
    cmd.extend(pckr.packer_cmd_args)
    try:
        run_command(cmd)
    except subprocess.CalledProcessError as e:
        pass


# TODO: implement packer_destroy()
def packer_destroy():
    """Function to destroy Packer applied plan.
    """
    pass


# ---------------------
# Terraform


def terraform_init():
    pass


def terraform_plan():
    pass


def terraform_apply():
    pass


def terraform_destroy():
    pass


# ---------------------
# Main


def main(arg):
    """ Main function
    """
    packer_validate()
    log.info('------------------------------------')
    packer_inspect()
    log.info('------------------------------------')
    packer_build()
    print(arg)


# Execution
if __name__ == '__main__':
    arg = docopt(__doc__)
    main(arg)
