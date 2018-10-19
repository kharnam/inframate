// GCP Provider setup

provider "google" {
  region      = "${var.region}"
  project     = "${var.project}"
  credentials = "${var.cred_file}"
}

terraform {
  required_version = "0.11.8"
}