"""This file contains supporting variables for 'inframate.py'
"""
import datetime
import os
import re
import shlex

home = os.environ['HOME']
image_name = 'sergey-test-{}'.format(datetime.datetime.now().strftime('%Y%m%d%H%M'))


class Packer(object):
    """
    Class to contain Packer related dependencies
    """

    # dirs and files
    packer_base_dir = "{}/dev/projects/inframate/modules/packer".format(home)
    packer_tmplt_file = "{}/templates/pckr_tmpl_gcp_centos_nginx.json".format(packer_base_dir)

    # gcp data
    gcp_data = {
        'gcp_cred_file': "{}/.gcp/adept-cascade-216916-a0765ecc09b2.json".format(home),
        'project_id': "adept-cascade-216916",
        'image_name': image_name,
        'region': "us-east1",
        'zone': "us-east1-b",
        'machine_type': "f1-micro",
        'source_image': "centos-7-v20181011",
        'packer_tmplt_file': "{}/templates/pckr_tmpl_gcp_centos_nginx.json".format(packer_base_dir)
    }

    # cmds and args
    packer_cmd_base = '{}/packer'.format(packer_base_dir)
    packer_cmd_args = re.sub(' +', ' ', '\
        -var region={region} \
        -var source_image={source_image} \
        -var image_name={image_name} \
        -var machine_type={machine_type} \
        -var zone={zone} \
        -var service_account_json={gcp_cred_file} \
        -var project_id={project_id} {packer_tmplt_file}'.format(**gcp_data))


class Terraform(object):
    """
    Class to contain Terraform related dependencies
    """

    # paths
    terraform_base_dir = '{}/dev/projects/inframate/modules/terraform'.format(home)
    terraform_base_dir_gcp = '{}/gcp_tf_test_deploy'.\
        format(terraform_base_dir)
    terraform_base_dir_aws = '{}/aws_tf_test_deploy'.\
        format(terraform_base_dir)

    # cmds and args
    cmd_terraform_init = 'terraform init'
    cmd_terraform_plan = 'terraform plan'
    cmd_terraform_apply = 'terraform apply'
    cmd_terraform_destroy = 'terraform destroy'
