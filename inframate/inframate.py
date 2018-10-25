#!/usr/bin/env python3

"""
Usage:
    inframate.py [-h] [-y] [-v | -q ] [-m <all> | <packer> | \
<terraform> ] [ -a <plan> | <apply> | <destroy> | <build> | <rollback> ]
    inframate.py [ -m <all> ]
    inframate.py [ -m <packer> | <terraform> ]
    inframate.py [ -m <packer> ] [ -a <build> | <rollback> ]
    inframate.py [ -m <terraform> ] [ -a <plan> | <apply> | \
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

# DevOpsiPy
import logger
import host_base
import pstate
import exceptions as pe
import host_base_const as hbc


# -------------------
# System generics


def execute(*command, cwd=None):
    next_input = None
    print(cwd)
    for cmd in command:
        p = subprocess.Popen(cmd, cwd, stdin=next_input, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)  # , universal_newlines=True)
        next_input = p.stdout
        for stdout_line in iter(p.stdout.readline, ""):
            yield stdout_line
        p.stdout.close()
        return_code = p.wait()
        if return_code:
            raise subprocess.CalledProcessError(return_code, cmd)


def run_command(*command, cwd=None):
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
        for line in execute(cmd, cwd):
            if line and line not in ignored:
                log.info(line)


# TODO: implement rollback()
def rollback():
    pass

# ---------------------
# Packer


def packer_validate(host):
    """
    Function to validate Packer templates.
    """
    log.info("Starting Packer template validation...")
    cmd = pckr.packer_cmd_base + ' validate ' + pckr.packer_cmd_args
    log.info('cmd: < {} >'.format(cmd))
    host.run(cmd, print_stdout=True)


def packer_inspect(host):
    """
    Function to inspect Packer template.
    """
    log.info('Starting Packer template inspection...')
    cmd = pckr.packer_cmd_base + ' inspect ' + pckr.packer_tmplt_file
    log.info('cmd: < {} >'.format(cmd))
    host.run(cmd, print_stdout=True)


def packer_build(host):
    """
    Function to execute 'packer build'
    """
    log.info('Starting Packer image build process...')
    cmd = pckr.packer_cmd_base + ' build -debug ' if arg['--verbose'] else pckr.packer_cmd_base + ' build '
    cmd += pckr.packer_cmd_args
    log.info('cmd: < {} >'.format(cmd))
    host.run(cmd, print_stdout=True)


# TODO: implement get_packer_images()
def get_packer_images(host):
    cmd = "gcloud compute images list --filter='sergey' --format=json"


# TODO: implement packer_destroy()
def packer_destroy(host):
    """
    Function to destroy Packer applied plan.
    """
    pass


def packer_handler(host, action):
    """
    Function to control Packer flows
    :param action: action to perform
    :return:
    """
    packer_validate(host)
    log.info('------------------------------------')
    packer_inspect(host)
    log.info('------------------------------------')
    packer_build(host)


# ---------------------
# Terraform

# TODO: terraform_init
def terraform_init(host):
    log.info('Run Terraform initialization...')
    log.debug('initializing for dir -- < {} >'.format(terra.terraform_base_dir_gcp))
    cmd = terra.cmd_terraform_init + ' {}'.format(terra.terraform_base_dir_gcp)
    log.debug('init cmd to exec -- < {} >'.format(cmd))
    p = host.run(commands=[cmd], print_stdout=True)


# TODO: terraform_plan
def terraform_plan(host, plan_file='.terraform/terraform.tfplan'):
    log.info('Run Terraform planning...')
    log.debug('save output to file -- < {} >'.format(plan_file))
    cmd = '{0} -out {2}/{1} {2}'.format(terra.cmd_terraform_plan, plan_file, terra.terraform_base_dir_gcp)
    log.debug('init cmd to exec -- < {} >'.format(cmd))
    p = host.run(commands=[cmd], print_stdout=True)


# TODO: terraform_apply
def terraform_apply(host, plan_file='.terraform/terraform.tfplan'):
    log.info('Run Terraform plan application...')
    cmd = terra.cmd_terraform_apply + ' {}/{}'.format(terra.terraform_base_dir_gcp, plan_file)
    log.debug('init cmd to exec -- < {} >'.format(cmd))
    p = host.run(commands=[cmd], print_stdout=True)


# TODO: terraform_destroy
def terraform_destroy(host, auto_approve=True):
    log.info('Run Terraform latest plan destruction...')
    if auto_approve:
        cmd = terra.cmd_terraform_destroy + ' -auto-approve' + ' {}'.format(terra.terraform_base_dir_gcp)
    else:
        cmd = terra.cmd_terraform_destroy + ' {}'.format(terra.terraform_base_dir_gcp)
    log.debug('init cmd to exec -- < {} >'.format(cmd))
    p = host.run(commands=[cmd], print_stdout=True)


def terraform_handler(host, action):
    """
    Function to control Terraform flows
    :param action: action to perform
    :return:
    """
    terraform_init(host)
    terraform_plan(host)
    terraform_apply(host)
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
