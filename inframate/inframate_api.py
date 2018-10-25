"""
Module to implement functional level for Inframate.
Inframate scenarios runner architecture:
  - run-inframate -- module to implement only high-level scenarios (procedural level)
  - inframate_api -- module to provide building blocks for inframate runner/s (functional level)
  - devopsipy     -- package to implement low-level framework (core level)
"""

__author__ = "sergey kharnam"

import logging
log = logging.getLogger(__name__)

import sys
import os
fw_env = os.getenv('FW', '/Users/kharnam/dev/projects')
sys.path.append(fw_env + '/devopsipy/devopsipy')

# PyPi
from python_terraform import *

# Inframate
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
    log.info('--------------------------------------')
    log.info("Run Packer template validation...")
    cmd = pckr.packer_cmd_base + ' validate ' + pckr.packer_cmd_args
    log.debug('cmd: < {} >'.format(cmd))
    host.run(cmd, print_stdout=True)


def packer_inspect(host):
    """
    Function to inspect Packer template.
    """
    log.info('--------------------------------------')
    log.info('Run Packer template inspection...')
    cmd = pckr.packer_cmd_base + ' inspect ' + pckr.packer_tmplt_file
    log.debug('cmd: < {} >'.format(cmd))
    host.run(cmd, print_stdout=True)


def packer_build(host, verbose=False):
    """
    Function to execute 'packer build'
    """
    log.info('--------------------------------------')
    log.info('Run Packer image build process...')
    cmd = pckr.packer_cmd_base + ' build -debug ' if verbose else pckr.packer_cmd_base + ' build '
    cmd += pckr.packer_cmd_args
    log.debug('cmd: < {} >'.format(cmd))
    host.run(cmd, print_stdout=True)


# TODO: implement get_packer_images()
def get_packer_images(host):
    cmd = "gcloud compute images list --filter='sergey' --format=json"


# TODO: implement packer_destroy()
def packer_destroy(host):
    """
    Function to destroy Packer applied plan.
    """
    log.info('--------------------------------------')
    pass


# ---------------------
# Terraform

# TODO: terraform_init
def terraform_init(host):
    log.info('-------------------------------')
    log.info('Run Terraform initialization...')
    log.debug('initializing for dir -- < {} >'.format(terra.terraform_base_dir_gcp))
    cmd = terra.cmd_terraform_init + ' {}'.format(terra.terraform_base_dir_gcp)
    log.debug('init cmd to exec -- < {} >'.format(cmd))
    p = host.run(commands=[cmd], print_stdout=True)


# TODO: terraform_plan
def terraform_plan(host, plan_file='.terraform/terraform.tfplan'):
    log.info('-------------------------')
    log.info('Run Terraform planning...')
    log.debug('save output to file -- < {} >'.format(plan_file))
    cmd = '{0} -out {2}/{1} {2}'.format(terra.cmd_terraform_plan, plan_file, terra.terraform_base_dir_gcp)
    log.debug('plan cmd to exec -- < {} >'.format(cmd))
    p = host.run(commands=[cmd], print_stdout=True)


# TODO: terraform_apply
def terraform_apply(host, auto_approve=False, plan_file='.terraform/terraform.tfplan'):
    log.info('---------------------------------')
    log.info('Run Terraform plan application...')
    if auto_approve:
        cmd = terra.cmd_terraform_apply + ' -auto-approve' + ' {}/{}'.format(terra.terraform_base_dir_gcp, plan_file)
    else:
        cmd = terra.cmd_terraform_apply + ' {}/{}'.format(terra.terraform_base_dir_gcp, plan_file)
    log.debug('apply cmd to exec -- < {} >'.format(cmd))
    p = host.run(commands=[cmd], print_stdout=True)


# TODO: terraform_destroy
def terraform_destroy(host, auto_approve=False):
    log.info('----------------------------------------')
    log.info('Run Terraform latest plan destruction...')
    if auto_approve:
        cmd = terra.cmd_terraform_destroy + ' -auto-approve' + ' {}'.format(terra.terraform_base_dir_gcp)
    else:
        cmd = terra.cmd_terraform_destroy + ' {}'.format(terra.terraform_base_dir_gcp)
    log.debug('destroy cmd to exec -- < {} >'.format(cmd))
    p = host.run(commands=[cmd], print_stdout=True)
