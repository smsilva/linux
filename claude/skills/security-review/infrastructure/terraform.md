# Terraform Security Reference

## Overview

Infrastructure as Code (IaC) security covers misconfigurations that lead to overly permissive IAM, exposed resources, unencrypted data, hardcoded secrets, and insecure network policies. Terraform issues are often high severity because they define the security posture of entire environments.

---

## Secrets and Credentials

### Hardcoded Secrets

```hcl
# VULNERABLE: Secrets hardcoded in resource definitions
resource "aws_db_instance" "db" {
  username = "admin"
  password = "supersecret123"  # FLAG: Hardcoded password
}

resource "aws_iam_access_key" "key" {
  user = aws_iam_user.user.name
}
output "secret" {
  value = aws_iam_access_key.key.secret  # FLAG: Secret in output (may end up in state)
}

# SAFE: Use variables with no default, or secrets manager
variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}

resource "aws_db_instance" "db" {
  password = var.db_password
}

# SAFE: Reference secrets manager
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "prod/db/password"
}

resource "aws_db_instance" "db" {
  password = data.aws_secretsmanager_secret_version.db_password.secret_string
}
```

### Secrets in State File

```hcl
# FLAG: Sensitive values without sensitive = true end up in plain text in state
output "db_connection_string" {
  value = "postgres://admin:${var.db_password}@${aws_db_instance.db.endpoint}/mydb"
  # Missing: sensitive = true
}

# SAFE: Mark sensitive outputs
output "db_connection_string" {
  value     = "postgres://admin:${var.db_password}@${aws_db_instance.db.endpoint}/mydb"
  sensitive = true
}

# FLAG: State file stored insecurely
terraform {
  backend "local" {}  # CHECK: Local state leaks secrets to disk unencrypted
}

# SAFE: Remote backend with encryption
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    kms_key_id     = "arn:aws:kms:us-east-1:123456789012:key/..."
    dynamodb_table = "terraform-state-lock"
  }
}
```

---

## IAM and Access Control

### Overly Permissive IAM Policies

```hcl
# CRITICAL: Wildcard actions and resources
resource "aws_iam_policy" "policy" {
  policy = jsonencode({
    Statement = [{
      Effect   = "Allow"
      Action   = "*"          # FLAG: All actions
      Resource = "*"          # FLAG: All resources
    }]
  })
}

# CRITICAL: Allow all on sensitive services
resource "aws_iam_policy" "policy" {
  policy = jsonencode({
    Statement = [{
      Effect   = "Allow"
      Action   = ["iam:*", "s3:*", "ec2:*"]  # FLAG: Wildcard on sensitive services
      Resource = "*"
    }]
  })
}

# SAFE: Least privilege - specific actions and resources
resource "aws_iam_policy" "policy" {
  policy = jsonencode({
    Statement = [{
      Effect   = "Allow"
      Action   = ["s3:GetObject", "s3:PutObject"]
      Resource = "arn:aws:s3:::my-bucket/*"
    }]
  })
}
```

### Trust Policies (Role Assumption)

```hcl
# CRITICAL: Any principal can assume the role
resource "aws_iam_role" "role" {
  assume_role_policy = jsonencode({
    Statement = [{
      Effect    = "Allow"
      Principal = "*"   # FLAG: Anyone can assume this role
      Action    = "sts:AssumeRole"
    }]
  })
}

# SAFE: Restrict to specific principals
resource "aws_iam_role" "role" {
  assume_role_policy = jsonencode({
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}
```

### Inline Policies

```hcl
# FLAG: Inline policies are harder to audit than managed policies
resource "aws_iam_role_policy" "inline" {
  role   = aws_iam_role.role.id
  policy = jsonencode({
    Statement = [{
      Effect   = "Allow"
      Action   = "*"
      Resource = "*"
    }]
  })
}

# SAFE: Use managed policies with attachment
resource "aws_iam_policy" "managed" { ... }
resource "aws_iam_role_policy_attachment" "attach" {
  role       = aws_iam_role.role.name
  policy_arn = aws_iam_policy.managed.arn
}
```

---

## Network Security

### Security Groups

```hcl
# CRITICAL: Open to entire internet
resource "aws_security_group_rule" "ingress" {
  type        = "ingress"
  from_port   = 22
  to_port     = 22
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]  # FLAG: SSH open to internet
}

resource "aws_security_group_rule" "all" {
  type        = "ingress"
  from_port   = 0
  to_port     = 65535
  protocol    = "-1"
  cidr_blocks = ["0.0.0.0/0"]  # FLAG: All ports open to internet
}

# SAFE: Restrict to specific CIDRs or security groups
resource "aws_security_group_rule" "ingress" {
  type                     = "ingress"
  from_port                = 22
  to_port                  = 22
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.bastion.id  # Restrict to bastion
}
```

### Ports Commonly Flagged

```hcl
# Always flag if exposed to 0.0.0.0/0 or ::/0:
# 22    - SSH
# 3389  - RDP
# 3306  - MySQL
# 5432  - PostgreSQL
# 6379  - Redis
# 27017 - MongoDB
# 9200  - Elasticsearch
# 2379  - etcd
# 445   - SMB
```

### Public Subnets and IP Assignment

```hcl
# FLAG: Auto-assigning public IPs to instances
resource "aws_subnet" "public" {
  map_public_ip_on_launch = true  # CHECK: Intentional?
}

resource "aws_instance" "server" {
  associate_public_ip_address = true  # CHECK: Should this be public-facing?
}

# FLAG: Database in public subnet
resource "aws_db_subnet_group" "db" {
  subnet_ids = [aws_subnet.public.id]  # FLAG: DB should be in private subnet
}
```

### VPC Flow Logs

```hcl
# FLAG: No VPC flow logs (no network visibility)
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  # Missing: flow log resource
}

# SAFE: Enable VPC flow logs
resource "aws_flow_log" "main" {
  vpc_id          = aws_vpc.main.id
  traffic_type    = "ALL"
  iam_role_arn    = aws_iam_role.flow_logs.arn
  log_destination = aws_cloudwatch_log_group.flow_logs.arn
}
```

---

## Encryption

### Storage Encryption

```hcl
# FLAG: Unencrypted S3 bucket
resource "aws_s3_bucket" "bucket" {
  bucket = "my-bucket"
  # Missing: server-side encryption configuration
}

# SAFE: S3 with encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "bucket" {
  bucket = aws_s3_bucket.bucket.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.key.arn
    }
  }
}

# FLAG: Unencrypted EBS volume
resource "aws_ebs_volume" "data" {
  availability_zone = "us-east-1a"
  size              = 100
  encrypted         = false  # FLAG
}

# SAFE: Encrypted EBS
resource "aws_ebs_volume" "data" {
  availability_zone = "us-east-1a"
  size              = 100
  encrypted         = true
  kms_key_id        = aws_kms_key.key.arn
}

# FLAG: Unencrypted RDS
resource "aws_db_instance" "db" {
  storage_encrypted = false  # FLAG
}

# FLAG: Unencrypted EKS secrets
resource "aws_eks_cluster" "cluster" {
  # Missing: encryption_config for secrets
}
```

### In-Transit Encryption

```hcl
# FLAG: TLS not enforced on load balancer
resource "aws_lb_listener" "http" {
  port     = "80"
  protocol = "HTTP"
  # Missing: redirect to HTTPS
  default_action {
    type = "forward"
    target_group_arn = aws_lb_target_group.app.arn
  }
}

# SAFE: Redirect HTTP to HTTPS
resource "aws_lb_listener" "http" {
  port     = "80"
  protocol = "HTTP"
  default_action {
    type = "redirect"
    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}

# FLAG: Outdated TLS policy
resource "aws_lb_listener" "https" {
  ssl_policy = "ELBSecurityPolicy-2015-05"  # FLAG: Outdated policy
}

# SAFE: Current TLS policy
resource "aws_lb_listener" "https" {
  ssl_policy = "ELBSecurityPolicy-TLS13-1-2-2021-06"
}
```

---

## S3 Bucket Security

### Public Access

```hcl
# CRITICAL: Public ACL
resource "aws_s3_bucket_acl" "bucket" {
  acl = "public-read"       # FLAG: Publicly readable
}

resource "aws_s3_bucket_acl" "bucket" {
  acl = "public-read-write" # CRITICAL: Publicly writable
}

# CRITICAL: Block public access disabled
resource "aws_s3_bucket_public_access_block" "bucket" {
  block_public_acls       = false  # FLAG
  block_public_policy     = false  # FLAG
  ignore_public_acls      = false  # FLAG
  restrict_public_buckets = false  # FLAG
}

# SAFE: Block all public access
resource "aws_s3_bucket_public_access_block" "bucket" {
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

### Bucket Policies

```hcl
# CRITICAL: Bucket policy allows public access
resource "aws_s3_bucket_policy" "bucket" {
  policy = jsonencode({
    Statement = [{
      Effect    = "Allow"
      Principal = "*"    # FLAG: Anyone
      Action    = "s3:GetObject"
      Resource  = "${aws_s3_bucket.bucket.arn}/*"
    }]
  })
}
```

### Versioning and Logging

```hcl
# FLAG: No versioning on critical data buckets
resource "aws_s3_bucket" "critical_data" {
  # Missing: versioning
}

# FLAG: No access logging
resource "aws_s3_bucket" "bucket" {
  # Missing: logging configuration
}

# SAFE: Versioning + logging
resource "aws_s3_bucket_versioning" "bucket" {
  bucket = aws_s3_bucket.bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_logging" "bucket" {
  bucket        = aws_s3_bucket.bucket.id
  target_bucket = aws_s3_bucket.logs.id
  target_prefix = "s3-access-logs/"
}
```

---

## Logging and Monitoring

### CloudTrail

```hcl
# FLAG: CloudTrail not enabled or incomplete
resource "aws_cloudtrail" "trail" {
  include_global_service_events = false  # FLAG: Misses IAM, STS events
  is_multi_region_trail         = false  # FLAG: Only one region
  log_file_validation_enabled   = false  # FLAG: No tamper detection
  enable_log_file_validation    = false  # FLAG
}

# SAFE: Comprehensive CloudTrail
resource "aws_cloudtrail" "trail" {
  name                          = "all-regions-trail"
  s3_bucket_name                = aws_s3_bucket.cloudtrail.id
  include_global_service_events = true
  is_multi_region_trail         = true
  enable_log_file_validation    = true

  event_selector {
    read_write_type           = "All"
    include_management_events = true
    data_resource {
      type   = "AWS::S3::Object"
      values = ["arn:aws:s3:::"]
    }
  }
}
```

### GuardDuty and Security Hub

```hcl
# FLAG: GuardDuty not enabled
# (absence of this resource in an AWS account is a finding)
resource "aws_guardduty_detector" "main" {
  enable = false  # FLAG: Threat detection disabled
}

# SAFE
resource "aws_guardduty_detector" "main" {
  enable = true
}
```

---

## Kubernetes (EKS) Security

```hcl
# FLAG: Public API endpoint with no CIDR restriction
resource "aws_eks_cluster" "cluster" {
  vpc_config {
    endpoint_public_access  = true
    public_access_cidrs     = ["0.0.0.0/0"]  # FLAG: Anyone can reach API
    endpoint_private_access = false
  }
}

# SAFE: Private endpoint or restrict public CIDRs
resource "aws_eks_cluster" "cluster" {
  vpc_config {
    endpoint_public_access  = true
    public_access_cidrs     = ["10.0.0.0/8"]  # Restrict to corporate IPs
    endpoint_private_access = true
  }
}

# FLAG: EKS nodes with admin IAM role
resource "aws_iam_role_policy_attachment" "nodes" {
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"  # FLAG: Node group shouldn't have admin
  role       = aws_iam_role.nodes.name
}

# SAFE: Minimum required managed policies for nodes
resource "aws_iam_role_policy_attachment" "nodes_worker" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.nodes.name
}
```

---

## Provider and Module Security

### Provider Configuration

```hcl
# FLAG: No version constraints on providers (unpredictable updates)
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      # Missing: version constraint
    }
  }
}

# FLAG: Credentials hardcoded in provider
provider "aws" {
  access_key = "AKIAIOSFODNN7EXAMPLE"  # FLAG: Hardcoded
  secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"  # FLAG
}

# SAFE: Use IAM roles / environment variables / AWS profiles
provider "aws" {
  region = "us-east-1"
  # Credentials from environment or instance role
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"  # Pinned major version
    }
  }
}
```

### Third-Party Modules

```hcl
# FLAG: Unversioned module from public registry (unpredictable)
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  # Missing: version
}

# FLAG: Module from untrusted source
module "custom" {
  source = "github.com/random-user/terraform-magic"  # CHECK: Untrusted source
}

# SAFE: Pinned version from verified source
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.2"
}
```

---

## Grep Patterns for Terraform

```bash
# Hardcoded secrets
grep -rn 'password\s*=\s*"' . --include="*.tf" | grep -v 'var\.\|data\.'
grep -rn 'secret\s*=\s*"' . --include="*.tf" | grep -v 'var\.\|data\.'
grep -rn 'api_key\s*=\s*"' . --include="*.tf"
grep -rn 'BEGIN.*PRIVATE KEY' . --include="*.tf"

# Open security groups
grep -rn '"0\.0\.0\.0/0"\|"::/0"' . --include="*.tf"

# Public S3 access
grep -rn 'public-read\|public-read-write' . --include="*.tf"
grep -rn 'block_public_acls\s*=\s*false\|restrict_public_buckets\s*=\s*false' . --include="*.tf"

# Unencrypted storage
grep -rn 'encrypted\s*=\s*false\|storage_encrypted\s*=\s*false' . --include="*.tf"

# Wildcard IAM actions/resources
grep -rn '"Action":\s*"\*"\|"Resource":\s*"\*"' . --include="*.tf"
grep -rn '"Principal":\s*"\*"' . --include="*.tf"

# Sensitive outputs without sensitive = true
grep -rn -A5 'output "' . --include="*.tf" | grep -B3 '"password\|"secret\|"key' | grep -v 'sensitive = true'

# Missing TLS validation
grep -rn 'skip_credentials_validation\|ssl_verify\s*=\s*false\|insecure\s*=\s*true' . --include="*.tf"
```

---

## Testing Checklist

- [ ] No hardcoded credentials, passwords, or API keys in `.tf` files
- [ ] All sensitive outputs marked `sensitive = true`
- [ ] Remote backend with encryption enabled for state
- [ ] IAM policies follow least privilege (no `Action: "*"` or `Resource: "*"`)
- [ ] No `Principal: "*"` in trust/resource policies
- [ ] Security groups do not open SSH/RDP/DB ports to `0.0.0.0/0`
- [ ] S3 buckets block all public access (unless intentionally public)
- [ ] Storage encrypted at rest (EBS, RDS, S3, EKS secrets)
- [ ] In-transit encryption enforced (TLS listeners, no HTTP)
- [ ] CloudTrail enabled with multi-region, log validation, global events
- [ ] VPC flow logs enabled
- [ ] GuardDuty enabled
- [ ] EKS API server not public or CIDR-restricted
- [ ] Provider and module versions pinned
- [ ] No modules from untrusted or unversioned sources

---

## References

- [OWASP IaC Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Infrastructure_as_Code_Security_Cheat_Sheet.html)
- [CIS Amazon Web Services Foundations Benchmark](https://www.cisecurity.org/benchmark/amazon_web_services)
- [Terraform Security Best Practices - HashiCorp](https://developer.hashicorp.com/terraform/cloud-docs/recommended-practices)
- [tfsec - Static analysis for Terraform](https://github.com/aquasecurity/tfsec)
- [Checkov - Policy-as-code for IaC](https://www.checkov.io/)
