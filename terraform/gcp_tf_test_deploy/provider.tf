// GCP Provider setup

provider "google" {
  region      = "${var.region}"
  project     = "${var.project}"
  credentials = "${var.cred_file}"
}

provider "template" {
  version = "1.0.0"
}

terraform {
  required_version = "0.11.8"
}