# AWS Cloud Lab — Amazon Web Services (AWS)

Opzetten van een beveiligde cloudomgeving met VPC-architectuur, EC2-deployment, netwerkbeveiliging (Security Groups), toegangsbeheer (IAM Least Privilege) en security-monitoring met CloudWatch Logs Insights.

---

## Doel

Aantonen dat ik een realistische AWS-cloudomgeving kan ontwerpen, via CLI/Console configureren en beveiligen: VPC- en subnet-architectuur, virtuele machines (EC2), strikte netwerkbeveiliging met Security Group IP-whitelisting op beheerpoorten, Identity & Access Management volgens het **least privilege** principe, en security event audit monitoring via CloudWatch Logs Insights.

Dit lab toont dezelfde security- en beheerprincipes aan als in mijn **Azure Cloud Lab (Lab 2)**, waarmee bewezen wordt dat de opgedane cloudkennis provider-onafhankelijk en universeel overdraagbaar is.

---

## Architectuur & Netwerkontwerp

```
                                  [Internet]
                                      |
                         [Security Group: cloudlab-sg]
                 (Allow SSH Port 22 ONLY from 94.110.212.107/32)
                                      |
                     [VPC: vpc-04f383bde656b42e8 (Default)]
                                      |
                [Subnet: subnet-0210306b5bd658670 (172.31.16.0/20)]
                                      |
                 [EC2: ec2-cloudlab-01 (Ubuntu 22.04 LTS)]
                         (Public IP: 52.214.147.254)
                                      |
                   [IAM Role: EC2-CloudWatch-Role]
                                      |
                 [CloudWatch Log Group: cloudlab-auth-log]
```

| Component | Naam | Details / Specificaties | IP / Bereik |
|---|---|---|---|
| **Virtual Private Cloud** | `vpc-04f383bde656b42e8` | AWS Default VPC (eu-west-1 Ierland) | 172.31.0.0/16 |
| **Subnet** | `subnet-0210306b5bd658670` | Publiek Subnet in eu-west-1a | 172.31.16.0/20 |
| **Virtual Machine** | `ec2-cloudlab-01` | Linux Ubuntu 22.04 LTS (`t3.micro`) | Publiek: 52.214.147.254 / Privé: 172.31.19.243 |
| **Security Group** | `cloudlab-sg` | Inbound SSH (22) restricted to owner IP | 94.110.212.107/32 |
| **IAM Beheerder** | `cli-cloudlab` | Programmatic Access (CLI) i.p.v. Root | AdministratorAccess |
| **IAM Auditor** | `reader-cloudlab` | Least Privilege controle-account | ReadOnlyAccess |
| **Monitoring Workspace** | `cloudlab-auth-log` | CloudWatch Log Group & Agent (`auth.log`) | OS-level SSH Audit Streaming |

---

## Wat is gedaan

1. **Budget- & Kostenbeheer ingesteld** — Gratis AWS-account geactiveerd met $200 promo-krediet en direct een budget-alert geconfigureerd (*Zero-Spend Budget*) met e-mailnotificaties bij verbruik om onverwachte kosten uit te sluiten.
2. **Scheiding van Root & Programmatic IAM CLI-gebruiker** — Conform de CIS AWS Benchmark het root-account ontzien voor beheer; een dedicated IAM-gebruiker `cli-cloudlab` aangemaakt met CLI access keys en gekoppeld aan de lokale terminal in regio `eu-west-1`.
3. **VPC-architectuur & Key Pair generatie** — Default VPC en publieke subnets in kaart gebracht. Een RSA key pair `cloudlab-key` (`cloudlab-key.pem`) gegenereerd en beveiligd voor wachtwoordloze SSH-authenticatie.
4. **Netwerkbeveiliging & Security Group Ingress Hardening** — Dedicated firewall `cloudlab-sg` geconfigureerd. In plaats van SSH open te stellen voor de hele wereld (`0.0.0.0/0`), is poort 22 via dynamische IP-detectie strikt beperkt tot enkel mijn eigen beheerder-IP (`94.110.212.107/32`). Geverifieerd dat er geen open Anywhere-regels aanwezig zijn.
5. **Compute Deployment (EC2)** — Uitrol van `ec2-cloudlab-01` (Ubuntu 22.04 LTS, `t3.micro`) binnen de AWS Free Tier met publiek IPv4-adres en gekoppeld aan de hardened Security Group.
6. **IAM Least Privilege Demonstratie** — Een aparte audit-gebruiker `reader-cloudlab` aangemaakt met uitsluitend de AWS-managed policy `ReadOnlyAccess`. Hiermee is aangetoond dat medewerkers uitsluitend de minimaal benodigde permissies krijgen en geen destructieve acties kunnen uitvoeren.
7. **CloudWatch Agent & Security Incident Monitoring** — IAM-servicerol `EC2-CloudWatch-Role` gekoppeld aan de server via een Instance Profile. De Amazon CloudWatch Agent geïnstalleerd op de server om Linux authenticatielogs (`/var/log/auth.log`) real-time te streamen naar CloudWatch.
8. **Aanvalssimulatie & Forensische Loganalyse** — Mislukte brute-force inlogpogingen gesimuleerd (`hacker`, `admin`, `malicious_bot`, `testuser`) en in CloudWatch Logs Insights geanalyseerd:
   ```sql
   fields @timestamp, @message
   | filter @message like /Failed/ or @message like /Invalid user/
   | sort @timestamp desc
   ```
9. **Geautomatiseerd Opschonen (FinOps)** — Na succesvolle verificatie van alle doelen de EC2-instance beëindigd (`terminated`), de Security Group verwijderd en het sleutelpaar opgeruimd om onnodige compute-kosten te voorkomen.

---

## Troubleshooting & Incident Response

Tijdens het lab zijn reële cloud-incidenten methodisch gediagnosticeerd en opgelost (*Symptoom → Diagnose → Oorzaak → Oplossing*):

- **Incident 1: EC2 Free Tier Quota & Instance Type Incompatibiliteit (`t2.micro` vs `t3.micro`)**
  - *Symptoom*: Foutmelding `InvalidParameterCombination: The specified instance type is not eligible for Free Tier` bij aanvraag van een `t2.micro`.
  - *Oorzaak*: In nieuwere AWS-accounts en Availability Zones in `eu-west-1` is de oudere T2-generatie uitgefaseerd voor Free Tier ten gunste van moderne Nitro-architectuur.
  - *Oplossing*: Beschikbare Free Tier instance types opgevraagd via de CLI en de VM succesvol gelanceerd als **`t3.micro`**.
- **Incident 2: Security Group Naming Convention Restrictie (`sg-*`)**
  - *Symptoom*: Foutmelding `InvalidParameterValue: Value (sg-cloudlab) for parameter GroupName is invalid. Group names may not be in the format sg-*`.
  - *Oorzaak*: AWS reserveert het prefix `sg-*` uitsluitend voor door het platform gegenereerde Security Group ID's.
  - *Oplossing*: De security group hernoemd naar **`cloudlab-sg`**.
- **Incident 3: OpenSSH Private Key Encoding & Windows BOM Incompatibiliteit**
  - *Symptoom*: SSH-verbinding vanaf Windows gaf `Load key cloudlab-key.pem: invalid format` gevolgd door `Permission denied (publickey)`.
  - *Oorzaak*: De PowerShell output-redirection operator (`>`) sloeg het bestand standaard op als UTF-16 LE met Byte Order Mark (BOM). OpenSSH vereist zuivere ASCII/UTF-8 zonder BOM.
  - *Oplossing*: Sleutelbestand geconverteerd naar pure ASCII zonder BOM en bestandspermissies vastgezet met `icacls` (alleen leesrechten voor de huidige eigenaar).
- **Incident 4: CloudWatch Agent JSON Parsing Syntaxis**
  - *Symptoom*: CloudWatch Agent startte niet en logde `unable to parse json, error: invalid character l looking for beginning of object key string`.
  - *Oorzaak*: Door shell escape-gedrag ontbraken de vereiste dubbele aanhalingstekens om JSON keys (`"logs"`).
  - *Oplossing*: Geldige JSON-configuratie geschreven en de CloudWatch Agent herstart via `amazon-cloudwatch-agent-ctl`.

---

## Vergelijking & Overdraagbaarheid: Azure vs. AWS

Dit lab toont aan dat de fundamentele concepten van cloud security, netwerkinsluiting, identiteitsbeheer en incident response universeel toepasbaar zijn:

| Concept / Beveiligingsdoel | Microsoft Azure (Lab 2) | Amazon Web Services (Lab 4) |
| :--- | :--- | :--- |
| **Netwerksegmentatie** | Virtual Network (VNet) & Subnet (`vnet-homelab`) | Virtual Private Cloud (VPC) & Subnet (`eu-west-1a`) |
| **Stateful Firewalling** | Network Security Group (NSG) poort 22 `/32` | Security Group (`cloudlab-sg`) poort 22 `/32` |
| **Least Privilege IAM** | Azure RBAC Reader-rol op Resource Group | AWS IAM User (`reader-cloudlab`) met `ReadOnlyAccess` |
| **Compute Deployment** | Azure VM (Ubuntu 24.04 / `Standard_B1s`) | EC2 Instance (Ubuntu 22.04 / `t3.micro`) |
| **Logging & Incident Querying** | Log Analytics Workspace (`law-homelab`) met KQL | CloudWatch Logs Insights met query filter `/Failed\|Invalid/` |
| **Kostenbeheer** | Budget Alert (€5 drempel) | Zero-Spend Budget Alert ($1 drempel) |

---

## Wat is geleerd / Skills aangetoond

- **Cloud Infrastructure Management**: AWS CLI & Management Console automatisering, VPC/Subnet adressering, EC2 provisioning.
- **Cloud Security & Hardening**: Security Group inbound/outbound firewall rules, port 22 restriction, Zero Trust Ingress.
- **Identity & Access Management (IAM)**: Scheiding van Root en CLI, IAM Users, Policies, Roles, Instance Profiles, Least Privilege enforcement (`ReadOnlyAccess`).
- **Security Observability**: Amazon CloudWatch Agent deployment, OS-level `/var/log/auth.log` log streaming, CloudWatch Logs Insights queries.
- **Troubleshooting & Problem Solving**: Diagnose van AWS API errors, instance type quota's, OpenSSH encoding en JSON syntaxis.
- **Kostenbewust Cloudbeheer (FinOps)**: Zero-Spend Budget alerts, compute lifecycle management, resource teardown.

---

## Documentatie & Screenshots

Alle bewijslast en stappen zijn volledig gedocumenteerd:
- 📄 **Word Document:** [`documentatie/Lab4_Voortgangsverslag.docx`](file:///c:/Users/talia/Desktop/aws-cloud-lab/documentatie/Lab4_Voortgangsverslag.docx) *(Compleet officieel rapport met alle 10 screenshots ingebed)*
- 📝 **Markdown Verslag:** [`documentatie/Lab4_Voortgangsverslag.md`](file:///c:/Users/talia/Desktop/aws-cloud-lab/documentatie/Lab4_Voortgangsverslag.md)
- 📸 **Screenshots Map:** [`screenshots/`](file:///c:/Users/talia/Desktop/aws-cloud-lab/screenshots) *(10 genummerde bewijsscreenshots)*
