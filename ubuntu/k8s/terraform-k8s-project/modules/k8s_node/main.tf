
resource "aws_instance" "node" {
  ami           = var.ami_id
  instance_type = var.instance_type
  key_name      = var.key_name
  vpc_security_group_ids = [var.security_group_id]

  root_block_device {
    volume_size = 20
    volume_type = "gp2"
    delete_on_termination = true
  }

  tags = {
    Name = var.server_name
  }

# VITAL: Set the hostname on first boot
  user_data = <<-EOF
#!/bin/bash
# 1. Set the hostname immediately
hostnamectl set-hostname ${var.server_name}

# 2. Update /etc/hosts to ensure persistence and self-reference
# Use the local IP address if available, but setting the hostname is key.
# For simplicity and correctness, rely on hostnamectl for modern Ubuntu.
EOF
}

output "public_ip" {
  value = aws_instance.node.public_ip
}
