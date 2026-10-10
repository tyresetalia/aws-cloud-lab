import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DOC_PATH = r"c:\Users\talia\Desktop\aws-cloud-lab\documentatie\Lab4_Voortgangsverslag.docx"
SCREENSHOTS_DIR = r"c:\Users\talia\Desktop\aws-cloud-lab\screenshots"

def create_report():
    doc = docx.Document()

    # Page Margins: 1 inch
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Styles
    # AWS Colors: Deep Navy #232F3E, AWS Orange #FF9900, Text #222222
    navy = RGBColor(0x23, 0x2F, 0x3E)
    orange = RGBColor(0xEC, 0x72, 0x11)
    gray = RGBColor(0x55, 0x55, 0x55)

    # Title
    p_title = doc.add_paragraph()
    r_title = p_title.add_run("☁️ Lab 4 — AWS Cloud Security & Infrastructure Lab")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(22)
    r_title.font.bold = True
    r_title.font.color.rgb = navy
    p_title.paragraph_format.space_after = Pt(4)

    # Subtitle
    p_sub = doc.add_paragraph()
    r_sub = p_sub.add_run("Stapsgewijze Uitvoering, Netwerksegmentatie (VPC & Security Groups), IAM Least Privilege, CloudWatch Logging & Incident Response")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(13)
    r_sub.font.italic = True
    r_sub.font.color.rgb = gray
    p_sub.paragraph_format.space_after = Pt(18)

    # Meta table
    table = doc.add_table(rows=4, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Student / Beheerder:", "Talia"),
        ("Cloud Provider & Regio:", "Amazon Web Services (AWS) — eu-west-1 (Ierland)"),
        ("Lab Doel:", "Segmentatie, hardening, least-privilege toegangsbeheer en monitoring"),
        ("Status:", "In Uitvoering — Stap 0 voltooid")
    ]
    for i, (k, v) in enumerate(meta_data):
        row = table.rows[i]
        r0 = row.cells[0].paragraphs[0].add_run(k)
        r0.font.name = "Calibri"
        r0.font.bold = True
        r0.font.size = Pt(10.5)
        r1 = row.cells[1].paragraphs[0].add_run(v)
        r1.font.name = "Calibri"
        r1.font.size = Pt(10.5)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Section 1: Inleiding & Overdracht van principes
    h1 = doc.add_heading(level=1)
    r_h1 = h1.add_run("1. Doel & Overzicht van het Lab")
    r_h1.font.name = "Calibri"
    r_h1.font.color.rgb = navy

    p_intro = doc.add_paragraph()
    p_intro.add_run(
        "Het doel van dit lab is het opzetten, beveiligen, monitoren en beheren van een professionele cloudomgeving binnen Amazon Web Services (AWS) volgens industriestandaarden (Well-Architected Framework) en het principe van Least Privilege. "
        "Dit lab bouwt direct voort op de kennis opgedaan in Lab 2 (Microsoft Azure). Door dezelfde beveiligings- en beheerprincipes toe te passen op een ander cloudplatform (AWS), wordt bewezen dat de security-concepten provider-onafhankelijk en universeel overdraagbaar zijn."
    )
    
    p_bullets = [
        ("Netwerksegmentatie & VPC: ", "In plaats van een Azure VNet/Subnet wordt gebruikgemaakt van de AWS Default VPC en bijbehorende publieke subnets in regio eu-west-1."),
        ("Compute Deployment: ", "Uitrol van een kostenbewuste Ubuntu 22.04 LTS EC2-instance (t2.micro binnen de Free Tier)."),
        ("Netwerkbeveiliging & Firewalling: ", "Configuratie van AWS Security Groups (SG) met strikte IP-whitelisting voor SSH (poort 22 /32), vergelijkbaar met NSG's in Azure."),
        ("Identity & Access Management (IAM): ", "Toepassing van Least Privilege door een programmatic beheerder te scheiden van het root-account en een audit-gebruiker te voorzien van strikte ReadOnlyAccess."),
        ("Monitoring & Incident Response: ", "Installatie van de Amazon CloudWatch Agent voor OS-niveau logverzameling (auth.log) en analyse via CloudWatch Logs Insights ter detectie van verdachte login-pogingen."),
        ("Kostenbeheer & Troubleshooting: ", "Implementatie van een Zero Spend Budget-alert en gestructureerde documentatie van incidentdiagnoses.")
    ]
    for b_title, b_desc in p_bullets:
        bp = doc.add_paragraph(style='List Bullet')
        r_bt = bp.add_run(b_title)
        r_bt.bold = True
        bp.add_run(b_desc)

    # Section 2: Stap 0
    h2 = doc.add_heading(level=1)
    r_h2 = h2.add_run("2. Stap 0 — AWS Account Setup, Regio & Budget-Alert")
    r_h2.font.name = "Calibri"
    r_h2.font.color.rgb = navy

    p_s0 = doc.add_paragraph()
    p_s0.add_run(
        "Er is een nieuw AWS Free Tier account aangemaakt. Hierbij is gekozen voor het gratis plan (6 maanden gratis met $200 promo-credits) met automatische stopzetting bij overschrijding ter bescherming tegen onverwachte kosten. "
        "Direct na activatie is de beheeromgeving geopend in de AWS Management Console. De doelregio voor alle lab-activiteiten is vastgesteld op Europe (Ireland) / eu-west-1."
    )

    # Insert Screenshot 01
    img01_path = os.path.join(SCREENSHOTS_DIR, "01-aws-dashboard.png")
    if os.path.exists(img01_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(img01_path, width=Inches(6.0))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("📸 Screenshot 01: AWS Management Console Home na succesvolle accountactivatie")
        r_cap.font.italic = True
        r_cap.font.size = Pt(9.5)
        r_cap.font.color.rgb = gray

    p_budget = doc.add_paragraph()
    p_budget.add_run(
        "Kostenbeheersing & FinOps Alerting: "
    ).bold = True
    p_budget.add_run(
        "Om strikte kostencontrole te garanderen en onvoorziene uitgaven te elimineren, is direct via AWS Billing and Cost Management een 'Zero-Spend Budget' geconfigureerd (My Zero-Spend Budget). "
        "Dit budget stuurt direct geautomatiseerde waarschuwingsmails zodra de geschatte of actuele uitgaven de drempelwaarde overschrijden. Hiermee wordt voldaan aan het cloud governance principe van continue budgetbewaking."
    )

    # Insert Screenshot 02
    img02_path = os.path.join(SCREENSHOTS_DIR, "02-budget-zero-spend.png")
    if os.path.exists(img02_path):
        p_img2 = doc.add_paragraph()
        p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(img02_path, width=Inches(6.0))
        p_cap2 = doc.add_paragraph()
        p_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap2 = p_cap2.add_run("📸 Screenshot 02: Geactiveerd 'Zero-Spend Budget' met gezonde status (Healthy) in Billing & Cost Management")
        r_cap2.font.italic = True
        r_cap2.font.size = Pt(9.5)
        r_cap2.font.color.rgb = gray

    # Section 3: Stap 1 — IAM Gebruiker voor CLI-gebruik
    h3 = doc.add_heading(level=1)
    r_h3 = h3.add_run("3. Stap 1 — IAM-gebruiker & Programmatic Access (Niet werken met Root)")
    r_h3.font.name = "Calibri"
    r_h3.font.color.rgb = navy

    p_s1 = doc.add_paragraph()
    p_s1.add_run(
        "Security Best Practice: Scheiding van Root en Beheer: "
    ).bold = True
    p_s1.add_run(
        "Het AWS root-account heeft onbeperkte rechten binnen de cloud tenant. Volgens de AWS Security Best Practices en het CIS AWS Foundations Benchmark mag het root-account nooit worden gebruikt voor dagelijks operationeel beheer of scripting. "
        "Daarom is een specifieke IAM-gebruiker genaamd 'cli-cloudlab' aangemaakt. Voor deze gebruiker is console-toegang expliciet uitgeschakeld om het aanvalsoppervlak te verkleinen; de gebruiker functioneert uitsluitend via programmatic access (AWS CLI)."
    )

    # Insert Screenshot 03
    img03_path = os.path.join(SCREENSHOTS_DIR, "03-iam-user-cli-cloudlab.png")
    if os.path.exists(img03_path):
        p_img3 = doc.add_paragraph()
        p_img3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(img03_path, width=Inches(6.0))
        p_cap3 = doc.add_paragraph()
        p_cap3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap3 = p_cap3.add_run("📸 Screenshot 03: Overzicht van aangemaakte IAM-gebruiker 'cli-cloudlab' in de AWS IAM Console")
        r_cap3.font.italic = True
        r_cap3.font.size = Pt(9.5)
        r_cap3.font.color.rgb = gray

    p_s1_keys = doc.add_paragraph()
    p_s1_keys.add_run(
        "Aanmaak en Beheer van CLI Access Keys: "
    ).bold = True
    p_s1_keys.add_run(
        "Binnen de Security Credentials van 'cli-cloudlab' is een nieuw sleutelpaar (Access Key ID en Secret Access Key) gegenereerd met de use case 'Command Line Interface (CLI)'. "
        "De gegenereerde sleutels zijn veilig opgeslagen via de CLI-configuratie (~/.aws/credentials) en gekoppeld aan de doelregio eu-west-1."
    )

    # Insert Screenshot 04
    img04_path = os.path.join(SCREENSHOTS_DIR, "04-iam-cli-access-key.png")
    if os.path.exists(img04_path):
        p_img4 = doc.add_paragraph()
        p_img4.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(img04_path, width=Inches(6.0))
        p_cap4 = doc.add_paragraph()
        p_cap4.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap4 = p_cap4.add_run("📸 Screenshot 04: Generatie van de CLI Access Key voor 'cli-cloudlab' met eenmalige Secret weergave")
        r_cap4.font.italic = True
        r_cap4.font.size = Pt(9.5)
        r_cap4.font.color.rgb = gray

    # Section 4: Stap 2 & 3 — VPC, Subnet & Key Pair
    h4 = doc.add_heading(level=1)
    r_h4 = h4.add_run("4. Stap 2 & 3 — Netwerkbasis (VPC, Subnet) & SSH Key Pair")
    r_h4.font.name = "Calibri"
    r_h4.font.color.rgb = navy

    p_s2 = doc.add_paragraph()
    p_s2.add_run(
        "Default VPC en Publieke Subnets: "
    ).bold = True
    p_s2.add_run(
        "In AWS beschikt elke regio standaard over een Default VPC (Virtual Private Cloud) voorzien van een Internet Gateway en publieke subnets in verschillende Availability Zones. "
        "Via de AWS CLI is de Default VPC (vpc-04f383bde656b42e8) opgevraagd, inclusief het publieke subnet subnet-0210306b5bd658670 in eu-west-1a (172.31.16.0/20).\n\n"
        "SSH Key Pair Generatie & Hardening: "
    )
    p_s2.add_run(
        "Voor veilige remote toegang tot Linux-servers zonder wachtwoorden is een RSA-sleutelpaar genaamd 'cloudlab-key' gegenereerd. "
        "De private key (cloudlab-key.pem) is lokaal beveiligd met strikte bestandsrechten (alleen leesrechten voor de huidige gebruiker) conform de vereisten van OpenSSH."
    )

    # Section 5: Stap 4, 5, 6 & 8 — Security Group & IP Whitelisting
    h5 = doc.add_heading(level=1)
    r_h5 = h5.add_run("5. Stap 4, 5, 6 & 8 — Netwerkbeveiliging & Ingress Firewalling")
    r_h5.font.name = "Calibri"
    r_h5.font.color.rgb = navy

    p_s4 = doc.add_paragraph()
    p_s4.add_run(
        "Stateful Firewalling met Security Groups: "
    ).bold = True
    p_s4.add_run(
        "Binnen de VPC fungeert een Security Group als een virtuele stateful firewall op instance-niveau. Er is een specifieke security group 'cloudlab-sg' (ID: sg-0cb659a04f2914e27) geconfigureerd.\n\n"
        "Principe van IP-Whitelisting (Zero Trust / Ingress Restriction): "
    )
    p_s4.add_run(
        "In plaats van poort 22 (SSH) open te stellen voor het internet (0.0.0.0/0) — een van de meest voorkomende misconfiguraties die leidt tot continue brute-force aanvallen — "
        "is via automatische IP-detectie strikt het eigen publieke IP-adres (94.110.212.107/32) geautoriseerd. "
        "Er is geverifieerd dat er geen open 'Anywhere'-regels aanwezig zijn."
    )

    # Insert Screenshot 06
    img06_path = os.path.join(SCREENSHOTS_DIR, "06-security-group-inbound-rules.png")
    if os.path.exists(img06_path):
        p_img6 = doc.add_paragraph()
        p_img6.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(img06_path, width=Inches(6.0))
        p_cap6 = doc.add_paragraph()
        p_cap6.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap6 = p_cap6.add_run("📸 Screenshot 06: Inbound rules van 'cloudlab-sg' — poort 22 strikt beperkt tot het beheerder IP (94.110.212.107/32)")
        r_cap6.font.italic = True
        r_cap6.font.size = Pt(9.5)
        r_cap6.font.color.rgb = gray

    # Section 6: Stap 7 — EC2 Instance Deployment
    h6 = doc.add_heading(level=1)
    r_h6 = h6.add_run("6. Stap 7 — EC2 Virtual Machine Deployment (Ubuntu 22.04 LTS)")
    r_h6.font.name = "Calibri"
    r_h6.font.color.rgb = navy

    p_s7 = doc.add_paragraph()
    p_s7.add_run(
        "Compute Uitrol & Free Tier Specificatie: "
    ).bold = True
    p_s7.add_run(
        "Met behulp van de AWS CLI is een EC2-instance genaamd 'ec2-cloudlab-01' (ID: i-08e9f043c289a384f) gelanceerd op basis van de officiële Canonical Ubuntu 22.04 LTS AMI (ami-0f2f23fa3c4a98b7f). "
        "De instance is gekoppeld aan het subnet in eu-west-1a, voorzien van de 'cloudlab-sg' firewall en heeft een publiek IPv4-adres (52.214.147.254) toegewezen gekregen. "
        "Als instance-type is gekozen voor t3.micro (geactiveerd binnen de Free Tier voor moderne accounts)."
    )

    # Insert Screenshot 05
    img05_path = os.path.join(SCREENSHOTS_DIR, "05-ec2-instance-running.png")
    if os.path.exists(img05_path):
        p_img5 = doc.add_paragraph()
        p_img5.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(img05_path, width=Inches(6.0))
        p_cap5 = doc.add_paragraph()
        p_cap5.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap5 = p_cap5.add_run("📸 Screenshot 05: EC2 Dashboard toont 'ec2-cloudlab-01' in actieve 'Running' status met 3/3 checks passed")
        r_cap5.font.italic = True
        r_cap5.font.size = Pt(9.5)
        r_cap5.font.color.rgb = gray

    # Section 7: Stap 9 — IAM Least Privilege Demonstratie
    h7 = doc.add_heading(level=1)
    r_h7 = h7.add_run("7. Stap 9 — IAM Least Privilege & Rolgebaseerde Scheiding")
    r_h7.font.name = "Calibri"
    r_h7.font.color.rgb = navy

    p_s9 = doc.add_paragraph()
    p_s9.add_run(
        "Demonstratie van het Least-Privilege Principe: "
    ).bold = True
    p_s9.add_run(
        "Binnen een enterprise cloudomgeving krijgt personeel uitsluitend de minimaal benodigde permissies om hun taak uit te voeren. "
        "Om dit principe concreet te demonstreren, is een aparte IAM-gebruiker genaamd 'reader-cloudlab' aangemaakt. "
        "Deze gebruiker heeft uitsluitend de AWS-managed job-function policy 'ReadOnlyAccess' toegekend gekregen. "
        "Hiermee kan een auditor alle resources en logs inspecteren, zonder de bevoegdheid om configuraties te wijzigen, instances te stoppen of security groups aan te passen."
    )

    # Insert Screenshot 07
    img07_path = os.path.join(SCREENSHOTS_DIR, "07-iam-least-privilege-reader.png")
    if os.path.exists(img07_path):
        p_img7 = doc.add_paragraph()
        p_img7.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(img07_path, width=Inches(6.0))
        p_cap7 = doc.add_paragraph()
        p_cap7.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap7 = p_cap7.add_run("📸 Screenshot 07: IAM Details van 'reader-cloudlab' met exclusieve toekenning van de ReadOnlyAccess policy")
        r_cap7.font.italic = True
        r_cap7.font.size = Pt(9.5)
        r_cap7.font.color.rgb = gray

    # Section 8: Stap 10 — IAM Rol voor EC2
    h8 = doc.add_heading(level=1)
    r_h8 = h8.add_run("8. Stap 10 — IAM Service Role voor EC2 CloudWatch Logging")
    r_h8.font.name = "Calibri"
    r_h8.font.color.rgb = navy

    p_s10 = doc.add_paragraph()
    p_s10.add_run(
        "Instance Profile & Service-to-Service Rechten: "
    ).bold = True
    p_s10.add_run(
        "Om een virtuele machine in staat te stellen OS-niveau logs veilig naar Amazon CloudWatch door te sturen zonder statische credentials op de schijf te bewaren, "
        "is een IAM-rol genaamd 'EC2-CloudWatch-Role' aangemaakt met de 'CloudWatchAgentServerPolicy'. "
        "Deze rol is via een Instance Profile 'EC2-CloudWatch-Profile' direct gekoppeld aan de EC2-instance via de AWS Security metadata service."
    )

    # Section 9: Stap 11 & 12 — CloudWatch Agent & Aanvalssimulatie
    h9 = doc.add_heading(level=1)
    r_h9 = h9.add_run("9. Stap 11 & 12 — OS-niveau Logging & Incident Generatie")
    r_h9.font.name = "Calibri"
    r_h9.font.color.rgb = navy

    p_s11 = doc.add_paragraph()
    p_s11.add_run(
        "CloudWatch Agent Deployment: "
    ).bold = True
    p_s11.add_run(
        "Op de Ubuntu 22.04 LTS instance is de officiële Amazon CloudWatch Agent geïnstalleerd via het Debian-pakket (amazon-cloudwatch-agent.deb). "
        "De agent is geconfigureerd met een JSON-specificatie (/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json) om het Linux authenticatielogbestand (/var/log/auth.log) continu te monitoren en te streamen naar de CloudWatch Log Group 'cloudlab-auth-log' met log stream ID {instance_id}.\n\n"
        "Generatie van Verdachte Inlogactiviteit: "
    )
    p_s11.add_run(
        "Vanaf de externe beheermachine zijn meerdere gesimuleerde brute-force/onbevoegde SSH-inlogpogingen uitgevoerd met fictieve gebruikersaccounts (waaronder 'malicious_bot', 'testuser', 'hacker', 'admin', 'intruder'). "
        "Omdat OpenSSH op de doelserver geconfigureerd is met publickey authenticatie, resulteerden deze pogingen direct in 'Invalid user' en 'Failed publickey' events in /var/log/auth.log."
    )

    # Section 10: Stap 13 — CloudWatch Logs Insights Analyse
    h10 = doc.add_heading(level=1)
    r_h10 = h10.add_run("10. Stap 13 — Monitoring & Log Analytics met CloudWatch Logs Insights")
    r_h10.font.name = "Calibri"
    r_h10.font.color.rgb = navy

    p_s13 = doc.add_paragraph()
    p_s13.add_run(
        "Forensische Loganalyse & Querying: "
    ).bold = True
    p_s13.add_run(
        "In de AWS Management Console is de CloudWatch Logs Insights (Log Analytics) interface geopend. "
        "Om verdachte activiteit en ongeautoriseerde toegangspogingen direct inzichtelijk te maken, is de volgende query uitgevoerd op log group 'cloudlab-auth-log':"
    )

    p_query = doc.add_paragraph()
    r_q = p_query.add_run(
        "fields @timestamp, @message\n"
        "| filter @message like /Failed/ or @message like /Invalid user/\n"
        "| sort @timestamp desc"
    )
    r_q.font.name = "Consolas"
    r_q.font.size = Pt(9.5)
    r_q.font.color.rgb = navy

    # Insert Screenshot 08
    img08_path = os.path.join(SCREENSHOTS_DIR, "08-cloudwatch-insights-query.png")
    if os.path.exists(img08_path):
        p_img8 = doc.add_paragraph()
        p_img8.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(img08_path, width=Inches(6.0))
        p_cap8 = doc.add_paragraph()
        p_cap8.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap8 = p_cap8.add_run("📸 Screenshot 08: Geconfigureerde zoekquery in CloudWatch Logs Insights gericht op mislukte SSH-inlogpogingen")
        r_cap8.font.italic = True
        r_cap8.font.size = Pt(9.5)
        r_cap8.font.color.rgb = gray

    # Insert Screenshot 09
    img09_path = os.path.join(SCREENSHOTS_DIR, "09-cloudwatch-insights-results.png")
    if os.path.exists(img09_path):
        p_img9 = doc.add_paragraph()
        p_img9.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(img09_path, width=Inches(6.0))
        p_cap9 = doc.add_paragraph()
        p_cap9.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap9 = p_cap9.add_run("📸 Screenshot 09: Queryresultaten in CloudWatch Logs Insights tonen 5/5 gedetecteerde pogingen ('Invalid user malicious_bot', 'testuser') inclusief bron-IP")
        r_cap9.font.italic = True
        r_cap9.font.size = Pt(9.5)
        r_cap9.font.color.rgb = gray

    # Section 11: Stap 14 — Troubleshooting Scenario's
    h11 = doc.add_heading(level=1)
    r_h11 = h11.add_run("11. Stap 14 — Troubleshooting Incidentanalyse")
    r_h11.font.name = "Calibri"
    r_h11.font.color.rgb = navy

    p_tb_intro = doc.add_paragraph()
    p_tb_intro.add_run(
        "Tijdens de implementatie zijn meerdere reële incidenten en configuratiebeperkingen opgetreden die methodisch zijn gediagnosticeerd en opgelost volgens het principe: Symptoom → Diagnose → Oorzaak → Oplossing."
    )

    troubleshoot_items = [
        ("Incident 1: EC2 Free Tier Quota & Instance Type Incompatibiliteit",
         "Symptoom: RunInstances foutmelding 'InvalidParameterCombination: The specified instance type is not eligible for Free Tier' bij t2.micro.\n"
         "Diagnose: Uitvoeren van 'aws ec2 describe-instance-types --region eu-west-1 --filters Name=free-tier-eligible,Values=true'.\n"
         "Oorzaak: In recente AWS accounts en specifieke Availability Zones in eu-west-1 is de oudere t2-generatie uitgefaseerd ten gunste van modernere Nitro-instances.\n"
         "Oplossing: Instance type omgezet naar t3.micro, waardoor de VM succesvol en gratis startte."),
        
        ("Incident 2: Security Group Naming Convention Restrictie",
         "Symptoom: CreateSecurityGroup fout 'InvalidParameterValue: Value (sg-cloudlab) for parameter GroupName is invalid. Group names may not be in the format sg-*'.\n"
         "Diagnose: AWS API documentatie voor EC2 Security Groups geraadpleegd.\n"
         "Oorzaak: AWS reserveert het prefix 'sg-*' exclusief voor door het platform gegenereerde Security Group ID's.\n"
         "Oplossing: Groepsnaam hernoemd naar 'cloudlab-sg'."),

        ("Incident 3: OpenSSH Private Key Encoding & Windows BOM Incompatibiliteit",
         "Symptoom: SSH-verbinding vanaf Windows gaf 'Load key cloudlab-key.pem: invalid format' gevolgd door Permission Denied.\n"
         "Diagnose: Inspectie van de byte-structuur toonde een UTF-16 Byte Order Mark (0xFF 0xFE) gegenereerd door de PowerShell redirection operator (>).\n"
         "Oorzaak: OpenSSH vereist strikte ASCII / UTF-8 codering zonder BOM en exclusieve bestandsrechten.\n"
         "Oplossing: Sleutelbestand gehercodeerd naar pure ASCII zonder BOM en bestandsrechten vergrendeld via icacls (alleen leesrechten voor de huidige eigenaar)."),

        ("Incident 4: CloudWatch Agent JSON Parsing Syntaxis",
         "Symptoom: CloudWatch Agent rapporteerde 'unable to parse json, error: invalid character l looking for beginning of object key string'.\n"
         "Diagnose: Logbestand /opt/aws/amazon-cloudwatch-agent/logs/amazon-cloudwatch-agent.log geanalyseerd op de server.\n"
         "Oorzaak: Door string interpolation waren dubbele aanhalingstekens rond de keys in het JSON-configuratiebestand weggevallen.\n"
         "Oplossing: Configuratiebestand opnieuw gegenereerd met valide JSON-syntaxis en de service herstart via amazon-cloudwatch-agent-ctl.")
    ]

    for title, desc in troubleshoot_items:
        p_t = doc.add_paragraph()
        r_t = p_t.add_run(f"• {title}\n")
        r_t.bold = True
        p_t.add_run(desc)

    # Section 12: Stap 15 — Kostenbeheer & Resources Opruimen
    h12 = doc.add_heading(level=1)
    r_h12 = h12.add_run("12. Stap 15 — Kostenbeheer & Lifecycle Cleanup Verantwoording")
    r_h12.font.name = "Calibri"
    r_h12.font.color.rgb = navy

    p_s15 = doc.add_paragraph()
    p_s15.add_run(
        "Kostenbewust Cloudbeheer: "
    ).bold = True
    p_s15.add_run(
        "Een cruciaal onderdeel van professioneel cloudbeheer is het tijdig de-provisionen van tijdelijke resources. "
        "Zolang een EC2-instance draait, verbruikt deze compute hours en EBS-opslagruimte. "
        "Om onnodige kosten te voorkomen, worden de actieve resources systematisch opgeruimd via de AWS CLI zodra de verificatie is voltooid:\n\n"
        "1. EC2 Instance beëindigen: aws ec2 terminate-instances --instance-ids i-08e9f043c289a384f\n"
        "2. Security Group verwijderen: aws ec2 delete-security-group --group-id sg-0cb659a04f2914e27\n"
        "3. Key Pair opruimen: aws ec2 delete-key-pair --key-name cloudlab-key\n"
        "4. Lokaal sleutelbestand verwijderen: rm -f cloudlab-key.pem\n\n"
        "De IAM-rollen, gebruikers en de Default VPC genereren geen kosten en kunnen blijven bestaan voor audit- en portfoliodoeleinden."
    )

    # Insert Screenshot 10
    img10_path = os.path.join(SCREENSHOTS_DIR, "10-ec2-instance-terminated.png")
    if os.path.exists(img10_path):
        p_img10 = doc.add_paragraph()
        p_img10.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(img10_path, width=Inches(6.0))
        p_cap10 = doc.add_paragraph()
        p_cap10.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap10 = p_cap10.add_run("📸 Screenshot 10: Succesvolle beëindiging (Shutting-down / Terminated) van 'ec2-cloudlab-01' in de EC2 Console")
        r_cap10.font.italic = True
        r_cap10.font.size = Pt(9.5)
        r_cap10.font.color.rgb = gray

    # Section 13: Vergelijking Azure Lab 2 vs AWS Lab 4
    h13 = doc.add_heading(level=1)
    r_h13 = h13.add_run("13. Vergelijking & Overdraagbaarheid: Azure vs. AWS")
    r_h13.font.name = "Calibri"
    r_h13.font.color.rgb = navy

    p_cmp = doc.add_paragraph()
    p_cmp.add_run(
        "Dit lab toont aan dat de fundamentele concepten van cloud security, netwerkinsluiting, identiteitsbeheer en incident response universeel toepasbaar zijn. "
        "Onderstaande tabel toont de directe equivalentie tussen Microsoft Azure (Lab 2) en Amazon Web Services (Lab 4):"
    )

    cmp_table = doc.add_table(rows=6, cols=3)
    cmp_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Concept / Beveiligingsdoel", "Microsoft Azure (Lab 2)", "Amazon Web Services (Lab 4)"]
    for col_idx, h in enumerate(headers):
        hdr_cell = cmp_table.rows[0].cells[col_idx]
        run_h = hdr_cell.paragraphs[0].add_run(h)
        run_h.bold = True
        run_h.font.color.rgb = navy

    comparisons = [
        ("Netwerksegmentatie", "Virtual Network (VNet) & Subnet (vnet-homelab)", "Virtual Private Cloud (VPC) & Subnet (eu-west-1a)"),
        ("Stateful Firewalling", "Network Security Group (NSG) poort 22 /32", "Security Group (cloudlab-sg) poort 22 /32"),
        ("Least Privilege IAM", "Azure RBAC Reader-rol op Resource Group", "AWS IAM User (reader-cloudlab) met ReadOnlyAccess"),
        ("Compute Deployment", "Azure VM (Ubuntu 22.04 / Standard_B1s)", "EC2 Instance (Ubuntu 22.04 / t3.micro)"),
        ("Logging & Incident Querying", "Log Analytics Workspace (law-homelab) met KQL", "CloudWatch Logs Insights met filter /Failed|Invalid/"),
    ]

    for row_idx, row_data in enumerate(comparisons, start=1):
        row = cmp_table.rows[row_idx]
        for col_idx, text in enumerate(row_data):
            cell = row.cells[col_idx]
            r_c = cell.paragraphs[0].add_run(text)
            r_c.font.size = Pt(9.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    os.makedirs(os.path.dirname(DOC_PATH), exist_ok=True)
    doc.save(DOC_PATH)
    print("Full report successfully updated at:", DOC_PATH)

if __name__ == "__main__":
    create_report()
