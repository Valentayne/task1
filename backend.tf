resource "docker_image" "backend" {
  name = "flask-python:latest"

  build {
    context    = "${path.module}"
    dockerfile = "Dockerfile"
  }
}

resource "docker_container" "backend" {
  name  = "flask-python"
  image = docker_image.backend.image_id

  env = [
    "DATABASE_URL=postgresql+psycopg2://postgres:1111@db:5432/task1"
  ]

  ports {
    internal = 5000
    external = 8080
  }

  networks_advanced {
    name = docker_network.backend_network.name
  }

  mounts {
    target = "/app/static/uploads"
    source = "/Users/valushka/Documents/python/hometask1/static/uploads"
    type   = "bind"
  }

  depends_on = [
    docker_container.postgres
  ]
}
