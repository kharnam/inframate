# Inframate

#### Description:
This is a demo project orchestrating resources over IaaS platforms GCP and AWS.

---
#### High-level perspective   
- Orchestrated by custom CLI application -- 'Inframate' (implemented in Python and Shell) 
- Employs Packer for template image creation:
    * CentOS 7
    * CPU 1vCore
    * RAM 0.5GB
    * Disk 10GB
- Employs Ansible for template image creation provisioning: 
    * Installs and configure NGINX
    * Installs and configure NTP
    * Installs and configure ...
- Employs Terraform for infrastructure 
    * Creates VPC and subnet
    * Creates bunch of firewall rules for internal and external communication
    * Creates Instance Template based on above generated image
    * Creates Target Pool
    * Creates Instance Group Manager
    * Creates Autoscaler and attach it to above Group Manager

---
#### Present functionality
**Inframate**
* Shell version capabilities:
_Built to employ wide range of shell scripting capabilities: functions, logging, 
signal handlers, error tracing etc._
```text
./inframate-bash.sh -h

Usage: ./inframate.sh [-h help] [-v verbose] [-y auto-approve]
```

* Python version capabilities:  
_Built as a grown CLI application with abstract data tier, logging facility etc. 
It operates from virtual environment to be easily Dockerized_.
```text
./inframate.py --help
Usage:
    inframate.py [-h] [-y] [-v | -q ] [-m <all> | <packer> | <terraform> ] [ -a <plan> | <apply> | <destroy> | <build> | <rollback> ]
    inframate.py [ -m <all> ]
    inframate.py [ -m <packer> | <terraform> ]
    inframate.py [ -m <packer> ] [ -a <build> | <rollback> ]
    inframate.py [ -m <terraform> ] [ -a <plan> | <apply> | <destroy> ]

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
```

**Packer**  
_Extendable and well-structured Packer project with verity of builders, 
provisioners and templates in mind..._

**Terraform**  
_Extendable and well-structured Terraform project with verity of providers, 
infrastructure levels and templates in mind..._

**Ansible**  
_Extendable and well-structured Ansible project with verity of inventories, 
roles, modules and playbooks in mind..._


---
#### Roadmap
**Functional**
- Implement flows for AWS provider
- Dockerize Inframate
- Build CI/CD pipes with GCP and Jenkins X
- Migrate to micro-service design: API server, CLI client, web client

**Project**
- Add unit-tests
- Add tox
