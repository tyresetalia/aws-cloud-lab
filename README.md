# AWS Cloud Lab

Segmentatie, beveiliging en monitoring van een cloudomgeving in AWS, opgezet en getest vanaf nul.

## Doel

Aantonen dat ik een beveiligde cloudomgeving kan opzetten in AWS: netwerktoegang (Security Groups), least-privilege toegangsbeheer (IAM), en logging/monitoring (CloudWatch) — dezelfde principes als in mijn Azure-lab, maar met een andere cloud-leverancier, om te tonen dat de kennis overdraagbaar is.

## Omgeving

- AWS Free Tier account
- AWS CLI
- Regio: eu-west-1 (Ierland)

## Wat is gedaan

*(vul ik aan zodra je de stappen doorloopt)*

1. IAM-gebruiker aangemaakt voor CLI-gebruik (niet met root gewerkt)
2. EC2-instance gedeployed in de default VPC
3. Security Group geconfigureerd: enkel eigen IP toegelaten voor SSH
4. IAM: least-privilege gebruiker (ReadOnlyAccess) aangetoond
5. CloudWatch-logging van SSH-pogingen ingesteld
6. Troubleshooting-scenario: [titel]
7. Resources opgeruimd om kosten te vermijden

## Skills aangetoond

- AWS-infrastructuur opzetten (CLI + Console)
- Netwerkbeveiliging in de cloud (Security Groups)
- Identity & Access Management (IAM, least privilege)
- Logging en monitoring (CloudWatch Logs Insights)
- Kostenbewust cloudbeheer (Free Tier, budget-alerts)

## Screenshots

Zie map `screenshots/`.

## Documentatie

Zie `documentatie/` voor het volledige voortgangsverslag met screenshots per stap.
