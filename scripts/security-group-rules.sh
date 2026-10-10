#!/bin/bash
# Lab 4 — Security Group Audit & Ingress Rule Management Script
set -e

REGION="eu-west-1"
SG_NAME="cloudlab-sg"

SG_ID=$(aws ec2 describe-security-groups --region $REGION --filters "Name=group-name,Values=$SG_NAME" --query "SecurityGroups[0].GroupId" --output text)
echo "Auditing Security Group ID: $SG_ID"

MY_IP=$(curl -s ifconfig.me)
echo "Current Public IP: $MY_IP"

echo "=== Current Inbound Rules ==="
aws ec2 describe-security-groups --region $REGION --group-ids $SG_ID --query "SecurityGroups[0].IpPermissions" --output json

# Revoke 0.0.0.0/0 if present on SSH port 22
ANYWHERE_RULE=$(aws ec2 describe-security-groups --region $REGION --group-ids $SG_ID --query "SecurityGroups[0].IpPermissions[?ToPort==\`22\`].IpRanges[?CidrIp==\`0.0.0.0/0\`]" --output text)

if [ -n "$ANYWHERE_RULE" ]; then
    echo "WARNING: Open 0.0.0.0/0 rule detected on port 22. Revoking..."
    aws ec2 revoke-security-group-ingress --region $REGION --group-id $SG_ID --protocol tcp --port 22 --cidr 0.0.0.0/0
    echo "Open 0.0.0.0/0 rule revoked successfully!"
else
    echo "Check passed: No insecure 0.0.0.0/0 rule found."
fi

# Ensure user's current IP is authorized
aws ec2 authorize-security-group-ingress --region $REGION --group-id $SG_ID --protocol tcp --port 22 --cidr "$MY_IP/32" 2>/dev/null || echo "My IP rule already active."
