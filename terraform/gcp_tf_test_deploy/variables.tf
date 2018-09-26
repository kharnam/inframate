// Variables
variable "cred_file" {
  type        = "string"
  description = "Path to credentials file."
  default     = "/Users/kharnam/.gcp/adept-cascade-216916-a0765ecc09b2.json"
}

variable "image_name" {
  type        = "string"
  description = "The name of the image for the deployment."
  default     = "centos-cloud/centos-7-v20180911"
}

variable "machine_type" {
  type        = "string"
  description = "The type of the machine for deployment."
  default     = "f1-micro"
}

variable "region" {
  type        = "string"
  description = "The region to use for the deployment."
  default     = "us-east1"
}

variable "zones" {
  type        = "list"
  description = "List of available zones for the region."
  default     = ["b", "c", "d"]
}

variable "project" {
  type        = "string"
  description = "Project ID."
  default     = "adept-cascade-216916"
}

variable "trusted_network" {
  type        = "string"
  description = "Network ranges will be enabled for access"
  default = "66.207.203.61"
}

variable "name" {
  type        = "string"
  description = "An idenfitying name used for names of cloud resources"
  default      = "sergey-tf-test"
}

variable "cidr" {
  type        = "string"
  description = "CIDR"
  default     = "10.142.10.0/24"
}

variable "user_data" {
  default = "user_data.sh"
}

variable "remote_user" {
  default = "ansible"
}

variable "public_key" {
  default = "~/.ssh/id_rsa.pub"
}
