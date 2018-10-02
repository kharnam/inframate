#!/usr/bin/env bash

# Created by Sergey Kharnam

# ------------------------------------------------------------------------------------
# General runtime setup

export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# Exit on error. Append "|| true" if you expect an error.
set -o errexit
# Exit on error inside any functions or subshells.
set -o errtrace
# Do not allow use of undefined vars. Use ${VAR:-} to use an undefined VAR
set -o nounset
# Catch the error in case mysqldump fails (but gzip succeeds) in `mysqldump |gzip`
set -o pipefail
# Turn on traces, useful while debugging but commented out by default
# set -o xtrace
# Produce a trace of every command executed run
# set -o verbose

# Setup working directory
TMPDIR="/tmp/$$"
[[ ! -f ${TMPDIR} ]] && mkdir -p ${TMPDIR} || $( echo "Cannot create TMPDIR ${TMPDIR}" >&2; exit 1 )

# Set magic variables for current file, directory, os, etc.
__dir="$(cd "$(dirname "${BASH_SOURCE[${__tmp_source_idx:-0}]}")" && pwd)"
__file="${__dir}/$(basename "${BASH_SOURCE[${__tmp_source_idx:-0}]}")"
__base="$(basename "${__file}" .sh)"

function sysinfo(){
    level=$1
    echo | tee -a ${LOG_FILE} 2>&1
    info "=====>>  SYSTEM INFORMATION  <<====="
    case "$1" in
        1)
            info "OS Details --> $(uname -a)"
            ;;
        2)
            info "OS Details --> $(uname -a)"
            info "Execution directory --> ${__dir}"
            info "Executed script file path --> ${__file}"
            info "Executed script file name --> ${__base}"
            ;;
        *)
            critical "Wrong system info level!!!"
    esac
}

# ------------------------------------------------------------------------------------
# Logging facility setup

# Define the environment variables (and their defaults) that this script depends on
LOG_LEVEL="${LOG_LEVEL:-7}" # 7 = debug -> 0 = emergency
NO_COLOR="${NO_COLOR:-}"    # true = disable color. otherwise autodetected

# Setup log directory
LOG_DIR="/tmp/logs/"
LOG_FILE="/tmp/logs/inframate.log"

[[ ! -f ${LOG_FILE} ]] && mkdir -p ${LOG_DIR} && $( touch ${LOG_FILE} || $( echo "Cannot write to ${LOG_FILE}" >&2; exit 1 ) )

# Option to play with different streams switchovers
# exec 3>&1 1>>${LOG_FILE} 2>&1

function log () {
    local log_level="${1}"
    shift

    # shellcheck disable=SC2034
    local color_debug="\x1b[35m"
    # shellcheck disable=SC2034
    local color_info="\x1b[32m"
    # shellcheck disable=SC2034
    local color_notice="\x1b[34m"
    # shellcheck disable=SC2034
    local color_warning="\x1b[33m"
    # shellcheck disable=SC2034
    local color_error="\x1b[31m"
    # shellcheck disable=SC2034
    local color_critical="\x1b[1;31m"
    # shellcheck disable=SC2034
    local color_alert="\x1b[1;33;41m"
    # shellcheck disable=SC2034
    local color_emergency="\x1b[1;4;5;33;41m"

    local colorvar="color_${log_level}"

    local color="${!colorvar:-${color_error}}"
    local color_reset="\x1b[0m"

    if [[ "${NO_COLOR:-}" = "true" ]] || ( [[ "${TERM:-}" != "xterm"* ]] && [[ "${TERM:-}" != "screen"* ]] ) || [[ ! -t 2 ]]; then
    if [[ "${NO_COLOR:-}" != "false" ]]; then
      # Don't use colors on pipes or non-recognized terminals
      color=""; color_reset=""
    fi
    fi

    # all remaining arguments are to be printed
    local log_line=""

    while IFS=$'\n' read -r log_line; do
    echo -e "$(date -u +"%Y-%m-%d %H:%M:%S UTC") ${color}$(printf "[%9s]" "${log_level}")${color_reset} ${log_line}" | tee -a ${LOG_FILE} 2>&1
    done <<< "${@:-}"
}

function emergency () {                                  log emergency "${@}"; exit 1; }
function alert ()     { [[ "${LOG_LEVEL:-0}" -ge 1 ]] && log alert "${@}"; true; }
function critical ()  { [[ "${LOG_LEVEL:-0}" -ge 2 ]] && log critical "${@}"; true; }
function error ()     { [[ "${LOG_LEVEL:-0}" -ge 3 ]] && log error "${@}"; true; }
function warning ()   { [[ "${LOG_LEVEL:-0}" -ge 4 ]] && log warning "${@}"; true; }
function notice ()    { [[ "${LOG_LEVEL:-0}" -ge 5 ]] && log notice "${@}"; true; }
function info ()      { [[ "${LOG_LEVEL:-0}" -ge 6 ]] && log info "${@}"; true; }
function debug ()     { [[ "${LOG_LEVEL:-0}" -ge 7 ]] && log debug "${@}"; true; }

# requires `set -o errtrace`
err_report() {
    local error_code
    error_code=${?}
    error "Error in ${__file} in ${1}"
    exit ${error_code}
}

# ------------------------------------------------------------------------------------
# Signal trapping and backtracing

# trap ctrl-c and call ctrl_c()
trap ctrl_c INT
function ctrl_c() {
    echo "** Trapped CTRL-C"
}
# trap script EXIT and call cleanup_before_exit()
# trap cleanup EXIT

# ------------------------------------------------------------------------------------
# Arguments parsing

function show_help(){
    echo
    echo "Usage: ./inframate.sh [-h help] [-v verbose] [-y auto-approve]"
    echo
}

OPTIND=1
VERBOSE=0
YES=0
while getopts "hvy" opt; do
    case "$opt" in
        h)
            show_help
            exit 0
            ;;
        v)  
            VERBOSE=1
            ;;
        y)
            YES=1
            ;;
    esac
done
shift $((OPTIND-1))
[ "${1:-}" = "--" ] && shift


# ====================================================================================
# Core functionality
# ====================================================================================

# ------------------------------------------------------------------------------------
# System functions

function yesno {
    echo
    while true; do
        if [[ "$YES" -eq 1 ]]; then 
            notice "Proceeding in auto-approve mode..."
            break
        fi
        read -p "Continue? [Y]es/[N]o: " yn
        case $yn in
            [Yy]* ) break;;
            [Nn]* ) exit;;
            * ) echo "Please answer [Y]es or [N]o.";;
        esac
    done
    echo
}

function fail {
  echo $1 >&2
  exit 1
}

function retry {
  local n=1
  local max=3
  local delay=10
  while true; do
    "$@" && break || {
      if [[ $n -lt $max ]]; then
        ((n++))
        critical "Failed to restart NGINX! Attempt $n/$max:"
        sleep $delay;
      else
        emergency "NGINX restart failed after $n attempts."
      fi
    }
  done
}


# ------------------------------------------------------------------------------------
# Packer section

PACKER_BASE_DIR="${HOME}/dev/projects/inframate/packer"
PACKER_TMPLT_FILE="/templates/pckr_tmpl_gcp_centos_nginx.json"
TERRAFORM_BASE_DIR="${HOME}/dev/projects/inframate/terraform/gcp_tf_test_deploy"
GCP_CRED_FILE="${HOME}/.gcp/adept-cascade-216916-a0765ecc09b2.json"
PROJECT_ID="adept-cascade-216916"
IMAGE_NAME="sergey-test-$(date +%Y%m%d%H%M)"

function packer_validate(){
    info "Running Packer validation..."
    if [[ "$VERBOSE" -eq 1 ]]; then
        PACKER_LOG=1 $PACKER_BASE_DIR/packer validate \
        -var "region=us-east1" \
        -var "source_image=centos-7-v20180911" \
        -var "image_name=$IMAGE_NAME" \
        -var "machine_type=f1-micro" \
        -var "zone=us-east1-b" \
        -var "service_account_json=$GCP_CRED_FILE" \
        -var "project_id=$PROJECT_ID" \
        $PACKER_BASE_DIR/templates/pckr_tmpl_gcp_centos_nginx.json  \
        | tee -a ${LOG_FILE} 2>&1 > /dev/null || emergency "Failed to validate Packer file!"
    else
        $PACKER_BASE_DIR/packer validate \
        -var "region=us-east1" \
        -var "source_image=centos-7-v20180911" \
        -var "image_name=$IMAGE_NAME" \
        -var "machine_type=f1-micro" \
        -var "zone=us-east1-b" \
        -var "service_account_json=$GCP_CRED_FILE" \
        -var "project_id=$PROJECT_ID" \
        $PACKER_BASE_DIR$PACKER_TMPLT_FILE  \
        | tee -a ${LOG_FILE} 2>&1 > /dev/null || emergency "Failed to validate Packer file < $PACKER_BASE_DIR$PACKER_TMPLT_FILE >!"
    fi
    notice "Packer validation passed successfully."
}

function packer_build() {
    info "Running Packer build..."
    if [[ "$VERBOSE" -eq 1 ]]; then
        PACKER_LOG=1 $PACKER_BASE_DIR/packer build \
        -var "region=us-east1" \
        -var "source_image=centos-7-v20180911" \
        -var "image_name=$IMAGE_NAME" \
        -var "machine_type=f1-micro" \
        -var "zone=us-east1-b" \
        -var "service_account_json=$GCP_CRED_FILE" \
        -var "project_id=$PROJECT_ID" \
        $PACKER_BASE_DIR/templates/pckr_tmpl_gcp_centos_nginx.json  \
        | tee -a ${LOG_FILE} 2>&1 > /dev/null || emergency "Failed to build image < $IMAGE_NAME > with Packer!"
    else
        $PACKER_BASE_DIR/packer build \
        -var "region=us-east1" \
        -var "source_image=centos-7-v20180911" \
        -var "image_name=$IMAGE_NAME" \
        -var "machine_type=f1-micro" \
        -var "zone=us-east1-b" \
        -var "service_account_json=$GCP_CRED_FILE" \
        -var "project_id=$PROJECT_ID" \
        $PACKER_BASE_DIR/templates/pckr_tmpl_gcp_centos_nginx.json  \
        | tee -a ${LOG_FILE} 2>&1 > /dev/null || emergency "Failed to build image < $IMAGE_NAME > with Packer!"
    fi
    notice "Packer build passed successfully."
}

function packer_rollback(){
    critical "Starting Packer rollback procedure..."
    gcloud -q compute images delete $IMAGE_NAME | tee -a ${LOG_FILE} 2>&1 > /dev/null || emergency "Failed to build with Packer!"
    critical "Packer successfully removed created images."
}


# ------------------------------------------------------------------------------------
# Terraform section

function terraform_init() {
    info "Starting Terraform initialization..."
    cd $TERRAFORM_BASE_DIR
    terraform init -input=false -var "image_name=$IMAGE_NAME" | tee -a ${LOG_FILE} 2>&1 > /dev/null || emergency "Failed to initialize Terraform!"
    notice "Terraform initialization passed successfully."
}

function terraform_plan() {
    info "Starting Terraform planning..."
    cd $TERRAFORM_BASE_DIR
    terraform plan -input=false -var "image_name=$IMAGE_NAME" | tee -a ${LOG_FILE} 2>&1 > /dev/null || emergency "Terraform failed to plan!"
    notice "Terraform planning passed successfully."
}

function terraform_rollback(){
    critical "Starting Terraform rollback procedure..."
    cd $TERRAFORM_BASE_DIR
    terraform destroy -auto-approve | tee -a ${LOG_FILE} 2>&1 > /dev/null || emergency "Terraform failed to remove infrastructure!"
    critical "Terraform successfully removed the infrastructure."
}

function terraform_apply() {
    RC=0
    info "Starting Terraform application..."
    cd $TERRAFORM_BASE_DIR
    terraform apply -input=false -auto-approve -var "image_name=$IMAGE_NAME" -auto-approve \
    | tee -a ${LOG_FILE} 2>&1 > /dev/null || RC=1
    if [[ "$RC" -eq 1 ]]; then
        critical "Terraform failed to apply the plan!" 
        rollback
    fi
    notice "Terraform successfully applied the plan."
}


# ------------------------------------------------------------------------------------
# General section

function wait_resource(){
    local rc=1
    local count=1
    local count_max=5
    local delay=30
    local cmd="ping -q -t1 -c1 \"${EXT_IP}\""

    # while [[ "${rc}" -ne 0 ]] && [[ "${count}" -le "${count_max}" ]]; do
    until $(curl --output /dev/null --silent --head --fail http://${EXT_IP}:80); do
        notice "Resource is unreachable. Sleeping ${delay} seconds..."; sleep ${delay}
        notice "Trying to reach out the resource. Attempt "${count}"/"${count_max}"..."
        if [[ ${count} -eq ${count_max} ]]; then
            critical "We've ecxeeded maximum of retry attempts!"
            emergency "Resource is still unreachable. Exiting!"
        fi
        get_external_ip
        count=$((count+1))
    done
    info "Access your web resource on -->  http://${EXT_IP}:80"
}

function get_external_ip(){
    notice "Getting the external IP address..."
    EXT_IP=$(/Users/kharnam/Downloads/google-cloud-sdk/bin/gcloud \
    compute instances list --format="value(networkInterfaces[0].accessConfigs[0].natIP)" \
    --filter="name~'instance-group-manager.*'")
}

function open_chrome(){
    local cmd="/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome http://${EXT_IP}:80 --kiosk"
    eval $cmd | tee -a ${LOG_FILE} 2>&1 > /dev/null || emergency "Failed to open Chrome!"
}

# ------------------------------------------------------------------------------------
# Teardown section

function cleanup(){
	echo | tee -a ${LOG_FILE} 2>&1
    info "=====>>  Starting clean up procedure...  <<====="
}

function rollback(){
    critical "Starting total rollback procedure..."
    terraform_rollback
    packer_rollback
    emergency "Rollback procedure completed!"
}

# ------------------------------------------------------------------------------------
# Main function

function main(){
    echo -e "\n\n\n\n" | tee -a ${LOG_FILE}
    echo -e "====================================================================================================\n\n" | tee -a ${LOG_FILE}
    info "=====   Starting script < ${__base} > execution...   ====="
    sysinfo 2

    packer_validate
    notice "Proceeding to Packer build stage..."
    yesno
    packer_build
    notice "Proceeding to Terraform initialization stage..."
    yesno
    terraform_init
    notice "Proceeding to Terraform plan stage..."
    yesno
    terraform_plan  
    notice "Proceeding to Terraform apply stage..."
    yesno
    terraform_apply

    get_external_ip
    wait_resource
    notice "Would you like to open URL in browser?"
    yesno
    open_chrome

    # system cleanup
    # cleanup

    echo | tee -a ${LOG_FILE}
    info "=====   Congrats! It looks we've done successfully ;)   ====="
    echo -e "\n\n\n" | tee -a ${LOG_FILE}
}
main