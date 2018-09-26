// Variables
variable "gcp_cred_file" {
  default = "~/.gcp/adept-cascade-216916-85d23caa1778.json"
}
variable "gcp_image_name" {
  type        = "string"
  description = "The name of the image for the deployment."
  default     = "happy_randomizer"
}

variable "gcp_image_version" {
  type        = "string"
  description = "The version of the image for the deployment."
  default     = "1.0.0"
}

variable "gcp_image_type" {
  type        = "string"
  description = "The type of the image for the deployment."
  default     = "lx-dataset"
}

variable "gcp_package_name" {
  type        = "string"
  description = "The package to use when making a deployment."
  default     = "g4-highcpu-128M"
}

variable "gcp_service_name" {
  type        = "string"
  description = "The name of the service in CNS."
  default     = "happiness"
}

variable "gcp_service_networks" {
  type        = "list"
  description = "The name or ID of one or more networks the service will operate on."
  default     = ["Joyent-SDC-Public"]
}