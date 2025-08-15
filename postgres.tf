resource "docker_container" "postgres" {
  name  = "db"
  image = docker_image.postgres.image_id

  env = [
    "POSTGRES_USER=postgres",
    "POSTGRES_PASSWORD=1111",
    "POSTGRES_DB=task1"
  ]

  ports {
    internal = 5432
    external = 8000
  }

  networks_advanced {
    name = docker_network.backend_network.name
  }

  mounts {
    target = "/var/lib/postgresql/data"
    source = docker_volume.db_data.name
    type   = "volume"
  }
}

resource "docker_image" "postgres" {
  name = "postgres:15"
}
