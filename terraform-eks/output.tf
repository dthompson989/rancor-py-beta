output "eks-endpoint" {
  value = aws_eks_cluster.rancor-eks.endpoint
}

output "eks-kubeconfig-cert-authority-data" {
  value = aws_eks_cluster.rancor-eks.certificate_authority.0.data
}