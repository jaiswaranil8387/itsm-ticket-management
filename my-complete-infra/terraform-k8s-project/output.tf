output "master_public_ip" {
  value       = module.k8s_master.public_ip
  description = "Public IP of the Master Node"
}

output "worker_public_ip" {
  #value       = module.k8s_worker.public_ip
  value = [for worker in module.k8s_worker : worker.public_ip]
  description = "Public IP of the Worker Node"
}
