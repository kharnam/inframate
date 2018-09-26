// GCP Provider
provider "google" {
    credentials = "${var.gcp_cred_file}"
}
