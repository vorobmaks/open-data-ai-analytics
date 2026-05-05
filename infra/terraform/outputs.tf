output "public_ip" {
  description = "Public IP адреса VM"
  value       = azurerm_public_ip.pip.ip_address
}

output "web_url" {
  description = "URL веб-інтерфейсу"
  value       = "http://${azurerm_public_ip.pip.ip_address}:${var.web_port}"
}

output "grafana_url" {
  description = "URL Grafana"
  value       = "http://${azurerm_public_ip.pip.ip_address}:${var.grafana_port}"
}

output "prometheus_url" {
  description = "URL Prometheus"
  value       = "http://${azurerm_public_ip.pip.ip_address}:${var.prometheus_port}"
}

output "ssh_command" {
  description = "SSH команда для підключення до VM"
  value       = "ssh ${var.admin_username}@${azurerm_public_ip.pip.ip_address}"
}
