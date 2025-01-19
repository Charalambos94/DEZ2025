# No need for that because I added path in .bashrc
# variable "credentials" {
#   description = "My Credentials"
#   default     = "<Path to your Service Account json file>"
# } 


variable "project" {
  description = "Project"
  default     = "dez2025"
}

variable "region" {
  description = "Project Region"
  default     = "europe-north1"
}

variable "location" {
  description = "Project Location"
  default     = "EU"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "dez2025_demo_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "dez2025-demo-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}