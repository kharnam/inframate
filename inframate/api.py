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

import subprocess

# Inframate
import data_provider

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


def packer_validate(host, data_prov):
    """
    Function to validate Packer templates.
    """
    log.info('--------------------------------------')
    log.info("Run Packer template validation...")
    cmd = data_prov.packer_cmd_base + ' validate ' + data_prov.packer_cmd_args
    log.debug('cmd: < {} >'.format(cmd))
    host.run(cmd, print_stdout=True)


def packer_inspect(host, data_prov):
    """
    Function to inspect Packer template.
    """
    log.info('--------------------------------------')
    log.info('Run Packer template inspection...')
    cmd = data_prov.packer_cmd_base + ' inspect ' + data_prov.packer_tmplt_file
    log.debug('cmd: < {} >'.format(cmd))
    host.run(cmd, print_stdout=True)


def packer_build(host, data_prov, verbose=False):
    """
    Function to execute 'packer build'
    """
    log.info('--------------------------------------')
    log.info('Run Packer image build process...')
    cmd = data_prov.packer_cmd_base + ' build -debug ' if verbose else data_prov.packer_cmd_base + ' build '
    cmd += data_prov.packer_cmd_args
    log.debug('cmd: < {} >'.format(cmd))
    host.run(cmd, print_stdout=True)


# TODO: implement get_packer_images()
def get_packer_images(host, data_prov):
    cmd = "gcloud compute images list --filter='sergey' --format=json"


# TODO: implement packer_destroy()
def packer_destroy(host, data_prov):
    """
    Function to destroy Packer applied plan.
    """
    log.info('--------------------------------------')
    pass


# ---------------------
# Terraform

# TODO: terraform_init
def terraform_init(host, data_prov):
    log.info('-------------------------------')
    log.info('Run Terraform initialization...')
    log.debug('initializing for dir -- < {} >'.format(data_prov.terraform_base_dir_gcp))
    cmd = data_prov.terraform_cmd_init + ' {}'.format(data_prov.terraform_base_dir_gcp)
    log.debug('init cmd to exec -- < {} >'.format(cmd))
    p = host.run(commands=[cmd], print_stdout=True)


# TODO: terraform_plan
def terraform_plan(host, data_prov, plan_file='.terraform/terraform.tfplan'):
    log.info('-------------------------')
    log.info('Run Terraform planning...')
    log.debug('save output to file -- < {} >'.format(plan_file))
    cmd = '{0} -out {2}/{1} {2}'.format(data_prov.terraform_cmd_plan, plan_file, data_prov.terraform_base_dir_gcp)
    log.debug('plan cmd to exec -- < {} >'.format(cmd))
    p = host.run(commands=[cmd], print_stdout=True)


# TODO: terraform_apply
def terraform_apply(host, data_prov, auto_approve=False, plan_file='.terraform/terraform.tfplan'):
    log.info('---------------------------------')
    log.info('Run Terraform plan application...')
    if auto_approve:
        cmd = data_prov.terraform_cmd_apply + ' -auto-approve' + ' {}/{}'.format(data_prov.terraform_base_dir_gcp, plan_file)
    else:
        cmd = data_prov.terraform_cmd_apply + ' {}/{}'.format(data_prov.terraform_base_dir_gcp, plan_file)
    log.debug('apply cmd to exec -- < {} >'.format(cmd))
    p = host.run(commands=[cmd], print_stdout=True)


# TODO: terraform_destroy
def terraform_destroy(host, data_prov, auto_approve=False):
    log.info('----------------------------------------')
    log.info('Run Terraform latest plan destruction...')
    if auto_approve:
        cmd = data_prov.terraform_cmd_destroy + ' -auto-approve' + ' {}'.format(data_prov.terraform_base_dir_gcp)
    else:
        cmd = data_prov.terraform_cmd_destroy + ' {}'.format(data_prov.terraform_base_dir_gcp)
    log.debug('destroy cmd to exec -- < {} >'.format(cmd))
    p = host.run(commands=[cmd], print_stdout=True)
