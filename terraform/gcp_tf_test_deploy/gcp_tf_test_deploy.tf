// The below code will create XXXXXXX

// This part is implemented using native Terraform resources (not modules)
resource "google_compute_instance_template" "compute_instance" {
  name_prefix    = "tf-test-instance-"
  description    = "App instance creation template."
  can_ip_forward = false
  machine_type   = "${var.machine_type}"
  region         = "${var.region}"

  // boot disk from img
  disk {
    source_image = "https://www.googleapis.com/compute/v1/projects/adept-cascade-216916/global/images/${var.image_name}"
    auto_delete  = true
    boot         = true
  }

  network_interface {
    network = "default"
    access_config {} // Ephimeral IP
  }

  service_account {
    scopes = ["userinfo-email", "compute-ro", "storage-ro"]
  }
  
  tags = ["web-srv"]

  metadata {
    service     = "web-srv"
    environment = "sandbox"
  }

  metadata_startup_script = "echo 'This is a test...' > /test.txt"
}

resource "google_compute_target_pool" "target_pool" {
  name = "target-pool"
}

resource "google_compute_instance_group_manager" "instance_group_manager" {
  name               = "tf-test-inst-grp-mngr"
  instance_template  = "${google_compute_instance_template.compute_instance.self_link}"
  target_pools       = ["${google_compute_target_pool.target_pool.self_link}"]
  base_instance_name = "instance-group-manager"
  zone               = "${var.region}-${var.zones[0]}"
}

resource "google_compute_autoscaler" "autoscaler" {
  name   = "autoscaler"
  zone   = "${var.region}-${var.zones[0]}"
  target = "${google_compute_instance_group_manager.instance_group_manager.self_link}"

  autoscaling_policy = {
    max_replicas    = 5
    min_replicas    = 1
    cooldown_period = 60

    cpu_utilization {
      target = 0.5
    }
  }
}

output "ip" {
  value = "${google_compute_instance_template.compute_instance.network_interface.0.address}"
}