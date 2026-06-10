variable "aws_region" {
  type    = string
  default = "eu-west-2"
}

variable "project_name" {
  type    = string
  default = "ecs-service-dashboard"
}

variable "environment" {
  type    = string
  default = "dev"
}

variable "container_port" {
  type    = number
  default = 8080
}

variable "image_tag" {
  type    = string
  default = "latest"
}

variable "desired_count" {
  type    = number
  default = 2
}
