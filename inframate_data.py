"""This file contains supporting variables for 'run_inframate.py'
"""

import os
import re
import shlex

home = os.environ['HOME']


class Packer(object):
    """Class to contain Packer related dependencies
    """

    # dirs and files
    packer_base_dir = "{}/dev/projects/inframate/packer".format(home)
    packer_tmplt_file = "{}/templates/pckr_tmpl_gcp_centos_nginx.json".format(packer_base_dir)

    # gcp data
    gcp_data = {
        'gcp_cred_file': "{}/.gcp/adept-cascade-216916-a0765ecc09b2.json".format(home),
        'project_id': "adept-cascade-216916",
        'image_name': "sergey-test-$(date' '+%Y%m%d%H%M)",
        'region': "us-east1",
        'zone': "us-east1-b",
        'machine_type': "f1-micro",
        'source_image': "centos-7-v20180911",
        'packer_tmplt_file': "{}/templates/pckr_tmpl_gcp_centos_nginx.json".format(packer_base_dir)
    }

    # cmds and args
    packer_base_cmd = '{}/packer'.format(packer_base_dir)
    packer_base_cmd_verbose = shlex.split(packer_base_cmd + '" "-debug')
    packer_cmd_args = shlex.split(re.sub(' +', ' ', '\
        -var region={region} \
        -var source_image={source_image} \
        -var image_name={image_name} \
        -var machine_type={machine_type} \
        -var zone={zone} \
        -var service_account_json={gcp_cred_file} \
        -var project_id={project_id} {packer_tmplt_file}'.format(**gcp_data)))


class Terraform(object):
    """Class to contain Terraform related dependencies
    """

    terraform_base_dir = '{}/dev/projects/inframate/terraform/gcp_tf_test_deploy".format(home)'.format(home)
