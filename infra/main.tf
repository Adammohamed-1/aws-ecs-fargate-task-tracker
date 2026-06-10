locals {
  name_prefix = "${var.project_name}-${var.environment}"
}

module "vpc" {
  source      = "./modules/vpc"
  name_prefix = local.name_prefix
  cidr_block  = "10.40.0.0/16"
}

module "ecr" {
  source      = "./modules/ecr"
  name_prefix = local.name_prefix
}

module "alb" {
  source         = "./modules/alb"
  name_prefix    = local.name_prefix
  vpc_id         = module.vpc.vpc_id
  public_subnets = module.vpc.public_subnet_ids
  container_port = var.container_port
}

module "ecs" {
  source                = "./modules/ecs"
  name_prefix           = local.name_prefix
  aws_region            = var.aws_region
  private_subnets       = module.vpc.private_subnet_ids
  alb_security_group_id = module.alb.alb_security_group_id
  target_group_arn      = module.alb.target_group_arn
  repository_url        = module.ecr.repository_url
  image_tag             = var.image_tag
  container_port        = var.container_port
  desired_count         = var.desired_count
}
