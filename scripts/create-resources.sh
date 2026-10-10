#!/bin/bash
# Lab 4 — AWS Cloud Lab: Resource Creation Script
set -e

REGION="eu-west-1"
KEY_NAME="cloudlab-key"
SG_NAME="cloudlab-sg"
INSTANCE_NAME="ec2-cloudlab-01"

echo "=== 1. Fetching Default VPC ID ==="
VPC_ID=$(aws ec2 describe-vpcs --region $REGION --filters "Name=is-default,Values=true" --query "Vpcs[0].VpcId" --output text)
echo "Default VPC ID: $VPC_ID"

echo "=== 2. Fetching Subnet ID ==="
SUBNET_ID=$(aws ec2 describe-subnets --region $REGION --filters "Name=vpc-id,Values=$VPC_ID" --query "Subnets[0].SubnetId" --output text)
echo "Subnet ID: $SUBNET_ID"

echo "=== 3. Creating SSH Key Pair ==="
if [ ! -f "cloudlab-key.pem" ]; then
  aws ec2 create-key-pair --region $REGION --key-name $KEY_NAME --query "KeyMaterial" --output text > cloudlab-key.pem
  chmod 400 cloudlab-key.pem
  echo "Key pair created: cloudlab-key.pem"
else
  echo "Key pair cloudlab-key.pem already exists locally."
fi

echo "=== 4. Creating Security Group ==="
SG_ID=$(aws ec2 create-security-group --region $REGION --group-name $SG_NAME --description "Cloud lab SG" --vpc-id $VPC_ID --query "GroupId" --output text 2>/dev/null || aws ec2 describe-security-groups --region $REGION --filters "Name=group-name,Values=$SG_NAME" --query "SecurityGroups[0].GroupId" --output text)
echo "Security Group ID: $SG_ID"

echo "=== 5. Detecting Public IP & Authorizing SSH Ingress ==="
MY_IP=$(curl -s ifconfig.me)
echo "Your Public IP: $MY_IP"
aws ec2 authorize-security-group-ingress --region $REGION --group-id $SG_ID --protocol tcp --port 22 --cidr "$MY_IP/32" || echo "Ingress rule already exists."

echo "=== 6. Finding latest Ubuntu 22.04 AMI ==="
AMI_ID=$(aws ec2 describe-images --region $REGION --owners 099720109477 \
  --filters "Name=name,Values=ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*" "Name=state,Values=available" \
  --query "sort_by(Images, &CreationDate)[-1].ImageId" --output text)
echo "Ubuntu 22.04 AMI ID: $AMI_ID"

echo "=== 7. Launching EC2 Instance ==="
INSTANCE_ID=$(aws ec2 run-instances \
  --region $REGION \
  --image-id $AMI_ID \
  --instance-type t2.micro \
  --key-name $KEY_NAME \
  --subnet-id $SUBNET_ID \
  --security-group-ids $SG_ID \
  --associate-public-ip-address \
  --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=$INSTANCE_NAME}]" \
  --query "Instances[0].InstanceId" --output text)

echo "EC2 Instance launched! ID: $INSTANCE_ID"
echo "Waiting for instance to be in running state..."
aws ec2 wait instance-running --region $REGION --instance-ids $INSTANCE_ID

PUBLIC_IP=$(aws ec2 describe-instances --region $REGION --instance-ids $INSTANCE_ID --query "Reservations[0].Instances[0].PublicIpAddress" --output text)
echo "=== Setup Complete! ==="
echo "Instance ID: $INSTANCE_ID"
echo "Public IP: $PUBLIC_IP"
echo "SSH Command: ssh -i cloudlab-key.pem ubuntu@$PUBLIC_IP"
