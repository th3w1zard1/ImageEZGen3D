job "imageezgen3d" {
  datacenters = ["dc1"]
  type = "service"

  group "app" {
    count = 1

    network {
      port "http" {
        to = 7865
      }
    }

    task "imageezgen3d" {
      driver = "docker"

      config {
        image = "ghcr.io/th3w1zard1/imageezgen3d:latest"
        ports = ["http"]
      }

      service {
        name = "imageezgen3d"
        port = "http"
      }

      resources {
        cpu    = 500
        memory = 1024
      }
    }
  }
}