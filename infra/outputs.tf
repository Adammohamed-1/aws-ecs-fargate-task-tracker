output "ecr_repository_url" {
  value = module.ecr.repository_url
}

output "application_url" {
  value = "http://${module.alb.alb_dns_name}"
}

output "ecs_cluster_name" {
  value = module.ecs.cluster_name
}

output "ecs_service_name" {
  value = module.ecs.service_name
}
