output "public_ip" {
  description = "Public IP адреса VM"
  value       = azurerm_public_ip.pip.ip_address
}

output "web_url" {
  description = "URL веб-інтерфейсу"
  value       = "http://${azurerm_public_ip.pip.ip_address}:5000"
}

output "ssh_command" {
  description = "SSH команда для підключення до VM"
  value       = "ssh azureuser@${azurerm_public_ip.pip.ip_address}"
}
