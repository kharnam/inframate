#!/usr/bin/env python3

"""
Usage:
    inframate.py -h | --help
    inframate.py scenario <name> <input_file>
    inframate.py packer (validate | inspect | build | rollback) <input_file>
    inframate.py terraform (init | plan | apply | destroy) [-y | --yes] <input_file>

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
  - inframate       -- runner module to implement only high-level scenarios (procedural level)
  - inframate_api   -- module to provide building blocks for inframate runner/s (functional level)
  - devopsipy       -- package to implement low-level framework (core level)
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
import data_provider
import api

# DevOpsiPy
import logger
import host_base
import pstate
import exceptions as pe
import host_base_const as hbc


# --------
# Handlers

def packer_handler(host, data_prov):
    """
    Function to control Packer flows
    :param host: host to run from
    :return:
    """
    if arg['validate']:
        api.packer_validate(host, data_prov)
    if arg['inspect']:
        api.packer_inspect(host, data_prov)
    if arg['build']:
        api.packer_build(host, data_prov)


def terraform_handler(host, data_prov):
    """
    Function to control Terraform flows
    :param host: host to run from
    :return:
    """
    if arg['init']:
        api.terraform_init(host, data_prov)
    if arg['plan']:
        api.terraform_plan(host, data_prov)
    if arg['apply']:
        if arg['--yes']:
            api.terraform_apply(host, data_prov, auto_approve=True)
        else:
            api.terraform_apply(host, data_prov)
    if arg['destroy']:
        if arg['--yes']:
            api.terraform_destroy(host, data_prov, auto_approve=True)
        else:
            api.terraform_destroy(host, data_prov)


# ---------------------
# Scenarios

def scenario_full():
    pass


# ---------------------
# Main

def main(arg):
    """
    Main function
    :param arg: user input arguments
    :return:
    """
    host = host_base.HostBase('localhost')
    log.debug('HostBase:\n{}'.format(host.__repr__()))
    dp = data_provider.DataProvider(arg['<input_file>'])
    log.debug('DataProvider:\n{}'.format(dp.__repr__()))

    if arg['scenario']:
        log.debug('execute scenario < {} >'.format('scenario_{}'.format(arg['<name>'])))
        eval('scenario_{}'.format(arg['<name>']))
    if arg['packer']:
        log.debug('call Packer handler...')
        packer_handler(host, data_prov=dp)
    if arg['terraform']:
        log.debug('call Terraform handler...')
        terraform_handler(host, data_prov=dp)


# Execution
if __name__ == '__main__':
    arg = docopt(__doc__)
    log = logger.set_logger('Inframate')
    log.debug('received arguments:\n{}'.format(arg))
    main(arg)
