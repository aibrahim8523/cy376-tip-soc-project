# CY376 TIP–SOC Project

**Building a Threat Intelligence Platform (TIP) Integration for a Simulated Security Operations Center (SOC)**

## Student
Ibrahim Abdul Aziz — FCM.41.018.151.23

## Course
CY376 — Network Monitoring, Security and Auditing
Lecturer: Mr. Fredrick Broni

## Summary
A consolidated MISP + Wazuh enrichment prototype. MISP and Wazuh run on a single Ubuntu Server; a custom integration automatically queries the MISP REST API whenever selected Wazuh network or File Integrity Monitoring rules fire, enriching each alert with matching threat-intelligence context.

## Architecture
- **Ubuntu Server** `192.168.18.130` — MISP (HTTPS 443, Docker) + Wazuh (SIEM, Dashboard HTTPS 8443)
- **Kali Linux** `192.168.18.128` — attacker / threat simulator
- Host network: VMware NAT `192.168.18.0/24`

## Key Results
- Custom Wazuh rule **100002** (level 12) detects the MISP-registered Kali IP
- Real-time File Integrity Monitoring rule **554** detects the EICAR file (68 bytes, matching SHA-256)
- Custom `custom-misp` integration queries MISP and returns HTTP 200 with **one matching attribute** for both IP and SHA-256 indicators (Event ID 1, types `ip-dst` and `sha256`)

## Reproduction
1. Install Wazuh on port 8443: `sudo bash wazuh-install.sh -a -o -p 8443`
2. Deploy MISP on port 443 via `misp-docker` Compose stack
3. Create MISP Event ID 1 with three indicators (Kali IP, EICAR SHA-256, test domain)
4. Install the `custom-misp` wrapper + custom rule 100002
5. Run the Kali and EICAR tests and observe enrichment in `integrations.log`

## Repository Layout
```
cy376-tip-soc-project/
├── README.md
├── .gitignore
├── LICENSE
├── report/          → TIP_Integration_Project.pdf (final report)
├── screenshots/     → all figures used in the report
├── evidence/        → original screenshots and reference PDFs
├── configs/         → ossec.conf integration block, custom rule, netplan
├── scripts/         → custom-misp integration wrapper & Python logic
└── docs/            → command reference and guide
```

## Evidence
See `evidence/` and the final report (`report/TIP_Integration_Project.pdf`).

## Security
The lab API key is redacted and must be rotated before the repository is made public. The password `1111` is for the isolated lab administrator account only.
