resource "aws_eks_cluster" "rancor-eks" {
  name     = var.cluster_name
  role_arn = ""

  vpc_config {
    subnet_ids = []
  }

  depends_on = []
}