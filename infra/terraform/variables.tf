variable "resource_group_name" {
  description = "Назва Resource Group в Azure"
  type        = string
  default     = "open-data-analytics-rg"
}

variable "location" {
  description = "Azure регіон"
  type        = string
  default     = "northeurope"
}

variable "prefix" {
  description = "Префікс для всіх ресурсів"
  type        = string
  default     = "oda"
}

variable "vm_size" {
  description = "Розмір VM (Standard_B1s — найдешевший для студентів)"
  type        = string
  default     = "Standard_D2s_v3"
}

variable "admin_username" {
  description = "Ім'я адміністратора VM"
  type        = string
  default     = "azureuser"
}

variable "ssh_public_key_path" {
  description = "Шлях до публічного SSH-ключа"
  type        = string
  default     = "~/.ssh/id_rsa.pub"
}

variable "web_port" {
  description = "Порт веб-інтерфейсу"
  type        = string
  default     = "5000"
}

variable "grafana_port" {
  description = "Порт Grafana"
  type        = string
  default     = "3000"
}

variable "prometheus_port" {
  description = "Порт Prometheus"
  type        = string
  default     = "9090"
}

variable "repo_url" {
  description = "URL GitHub-репозиторію для git clone"
  type        = string
  default     = "https://github.com/vorobmaks/open-data-ai-analytics"
}
