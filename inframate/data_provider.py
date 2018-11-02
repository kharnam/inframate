"""
This file contains variables used as input for 'api.py'
"""

__author__ = 'sergey kharnam'

import os
import datetime
import re
import yaml
import logging

log = logging.getLogger(__name__)
home = os.environ['HOME']


class DataProvider(object):

    def __init__(self, file):

        with open(file, 'rb') as f:
            try:
                self.config = yaml.load(f)
            except FileNotFoundError as e:
                log.exception('Cannot open file < {} >'.format(file, e))
        self.image_name = '{}-{}'.format(self.config['general']['image_name_prefix'],
                                         datetime.datetime.now().strftime('%Y%m%d%H%M'))

        # TODO: Implement dynamic zone (fetch available from region)
        self.gcp_data = {
            'gcp_cred_file': self.config['gcp_data']['gcp_cred_file'],
            'project_id': self.config['gcp_data']['project_id'],
            'image_name': self.image_name,
            'region': self.config['gcp_data']['region'],
            'zone': self.config['gcp_data']['zone'],
            'machine_type': self.config['gcp_data']['machine_type'],
            'source_image': self.config['gcp_data']['source_image'],
            'packer_tmplt_file': self.config['packer']['packer_tmplt_file']
        }

        self.packer_cmd_args = re.sub(' +', ' ', '\
            -var region={region} \
            -var source_image={source_image} \
            -var image_name={image_name} \
            -var machine_type={machine_type} \
            -var zone={zone} \
            -var service_account_json={gcp_cred_file} \
            -var project_id={project_id} {packer_tmplt_file}'.format(**self.gcp_data))

        self.packer_base_dir = self.config['packer']['packer_base_dir']
        self.packer_cmd_base = self.config['packer']['packer_cmd_base']
        self.packer_tmplt_file = self.config['packer']['packer_tmplt_file']

        self.terraform_cmd_init = 'terraform init'
        self.terraform_cmd_plan = 'terraform plan'
        self.terraform_cmd_apply = 'terraform apply'
        self.terraform_cmd_destroy = 'terraform destroy'

    def __str__(self):
        return vars(self)

    def __repr__(self):
        return vars(self)

