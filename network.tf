resource "docker_network" "backend_network" {
  name   = "backend_network"
  driver = "bridge"
}
resource "docker_volume" "db_data" {
  name = "hometask1_db-data"
}
