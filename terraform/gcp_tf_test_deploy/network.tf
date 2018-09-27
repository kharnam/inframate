// Networking setup

resource "google_compute_network" "network" {
  name                    = "${var.name}"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "subnetwork" {
  name          = "${var.name}"
  ip_cidr_range = "${var.cidr}"
  network       = "${google_compute_network.network.self_link}"
  region        = "${var.region}"
}

resource "google_compute_firewall" "fw_allow_admin" {
  name    = "${var.name}-allow-admin"
  network = "${google_compute_network.network.name}"

  allow {
    protocol = "tcp"
    ports = [
      22,
    ]
  }
  allow {
    protocol = "icmp"
  }

  source_ranges = [
    "${var.trusted_network}",
  ]
}

resource "google_compute_firewall" "servers" {
  name    = "${var.name}-allow-servers"
  network = "${google_compute_network.network.name}"

  allow {
    protocol = "tcp"
    ports = [
      80,
    ]
  }
  allow {
    protocol = "icmp"
  }

  source_ranges = [
    "0.0.0.0/0",
  ]
}

resource "google_compute_firewall" "internal" {
  name    = "${var.name}-allow-internal"
  network = "${google_compute_network.network.name}"

  allow {
    protocol = "all"
  }

  source_ranges = [
    "${var.cidr}",
  ]
}