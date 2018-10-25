#!/usr/bin/env python3

"""
Usage:
    inframate.py -h | --help
    inframate.py scenario <name>
    inframate.py packer (validate | inspect | build | rollback)
    inframate.py terraform (init | plan | apply | destroy) [-y | --yes]

CLI to control Inframate (Infrastructure Automation Tool).

Arguments:
    scenario    Run predefined scenario
    packer      Invoke Packer module
    terraform   Invoke Terraform module
    init        Execute 'terraform init'
    plan        Execute 'terraform plan'
    apply       Execute 'terraform apply'
    destroy     Execute 'terraform destroy'
    validate    Execute 'packer validate'
    inspect     Execute 'packer inspect'
    build       Execute 'packer build'
    rollback    Execute 'packer rollback'

Options:
    -h --help
    -v --verbose  verbose mode
    -q --quiet    quiet mode
    -y --yes      auto-assume 'Yes' on approval
"""

__author__ = "sergey kharnam"
__version__ = "0.1.0"

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



def packer_handler(host):
    """
    Function to control Packer flows
    :param host: host to run from
    :return:
    """
    if arg['validate']:
        ia.packer_validate(host)
    if arg['inspect']:
        ia.packer_inspect(host)
    if arg['build']:
        ia.packer_build(host)


def terraform_handler(host):
    """
    Function to control Terraform flows
    :param host: host to run from
    :return:
    """
    if arg['init']:
        ia.terraform_init(host)
    if arg['plan']:
        ia.terraform_plan(host)
    if arg['apply']:
        if arg['--yes']:
            ia.terraform_apply(host, auto_approve=True)
        else:
            ia.terraform_apply(host)
    if arg['destroy']:
        if arg['--yes']:
            ia.terraform_destroy(host, auto_approve=True)
        else:
            ia.terraform_destroy(host)


# ---------------------
# Main

def main(arg):
    """
    Main function
    :param arg: user input arguments
    :return:
    """
    host = host_base.HostBase('localhost')

    if arg['scenario']:
        log.debug('execute scenario < {} >'.format('scenario_{}'.format(arg['<name>'])))
        eval('scenario_{}'.format(arg['<name>']))
    if arg['packer']:
        log.debug('call Packer handler...')
        packer_handler(host=host)
    if arg['terraform']:
        log.debug('call Terraform handler...')
        terraform_handler(host=host)


# Execution
if __name__ == '__main__':
    arg = docopt(__doc__)
    log = logger.set_logger('Inframate')
    log.debug('received arguments:\n{}'.format(arg))
    main(arg)
