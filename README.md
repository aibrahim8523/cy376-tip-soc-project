# Building a Threat Intelligence Platform (TIP) Integration for a Simulated SOC

A Blue Team cybersecurity project that demonstrates how a Threat Intelligence Platform
(**MISP**) can be integrated with a SIEM (**Wazuh**) to automatically enrich security
alerts with threat-intelligence context inside an isolated, virtualised SOC.

> **Course:** CY376 — Network Monitoring, Security and Auditing
> **Programme:** BSc Cybersecurity, Level 300
> **Author:** Ibrahim Abdul Aziz (Ibzzy) — FCM.41.018.151.23
> **Submitted to:** Mr. Fredrick Broni
> **Date:** August 2026

---

## 📂 Repository Layout

```
cy376-tip-soc-project/
├── README.md                  ← you are here
├── .gitignore                 ← excludes secrets, build artefacts
├── LICENSE                    ← MIT
├── report/
│   └── TIP_Integration_Project.pdf   ← full project report (read this)
├── screenshots/               ← all 24 figures embedded in the report
│   ├── 01-architecture.png
│   ├── 02-misp-login.png
│   ├── …
│   └── E7-env-file.png
├── configs/                   ← configuration excerpts referenced in the report
│   ├── netplan-endpoint.yaml
│   ├── misp-docker.env
│   └── wazuh-ossec.conf
├── docs/
│   └── command-reference.md   ← all commands used in the lab, copy-paste-ready
├── build_report.py            ← regenerates the PDF (requires reportlab)
└── make_figures.py            ← regenerates the screenshot mockups (requires cairosvg)
```

---

## 🎯 What This Project Shows

1. **Deploying a TIP** — MISP runs as a Docker stack on Ubuntu Server, populated with
   real OSINT feeds (CIRCL, abuse.ch URLhaus) and curated test indicators.
2. **Deploying a SIEM** — Wazuh (Indexer + Manager + Dashboard) on a second VM, with an
   agent enrolled on a monitored endpoint.
3. **Integrating them** — a single `custom-misp` integration block in `ossec.conf`
   makes every Wazuh alert query MISP's REST API for known-bad IOCs and attach the
   matching threat context automatically.
4. **Validating end-to-end** — three attack scenarios (known-bad IP, EICAR file, SSH
   brute force) generate alerts that are automatically enriched and shown on the
   dashboard.

**The key result** (see Figure 12 in `report/TIP_Integration_Project.pdf`): an alert
for a connection from a MISP-registered attacker IP carries the matching IOC, the
threat event name, and the indicator type — context that a rule-only SIEM cannot
produce.

---

## 🚀 Reproducing the Lab

The full, step-by-step procedure is in Section 4 of the report. In brief:

| VM         | Role                       | OS                          | IP                |
|------------|----------------------------|-----------------------------|-------------------|
| MISP       | Threat Intelligence        | Ubuntu Server 22.04 LTS     | 192.168.100.10    |
| Wazuh      | SIEM (all-in-one)          | Ubuntu Server 22.04 LTS     | 192.168.100.20    |
| Endpoint   | Monitored host (agent)     | Ubuntu Desktop 22.04 LTS    | 192.168.100.30    |
| Kali       | Attacker / threat simulator| Kali Linux (rolling)        | 192.168.100.40    |

All four VMs run on an isolated host-only network (VMware VMnet2 / VirtualBox
Host-Only). See `docs/command-reference.md` for the full command list.

---

## 🛠️ Regenerating the Report and Figures

The PDF and screenshots in this repository were generated with the included Python
scripts. To rebuild them:

```bash
# 1. Install dependencies
pip install reportlab pymupdf cairosvg

# 2. Regenerate all 24 screenshot mockups (writes to ./screenshots/)
python3 make_figures.py

# 3. Regenerate the PDF (writes to ./report/TIP_Integration_Project.pdf)
python3 build_report.py
```

The screenshot mockups in this repository are clearly watermarked
"**ILLUSTRATIVE LAB MOCKUP — for report layout purposes only**". To submit the
final report with real lab captures, replace the PNGs in `screenshots/` with files
of the same name taken from your live environment, then re-run `build_report.py`.

---

## 🔒 Security & Academic Integrity Notes

* **No real secrets are committed.** API keys, passwords and tokens in the report
  are redacted (`<redacted>` / `•••••••`) — see `configs/wazuh-ossec.conf` and
  `screenshots/06d-misp-authkey.png`.
* All IP addresses are private lab addresses on `192.168.100.0/24`. No production
  data, real credentials, or third-party assets appear anywhere in this repository.
* The MISP `.env` and `ossec.conf` excerpts in `configs/` are sanitised templates
  suitable for sharing.

---

## 📚 References

The full bibliography is in Section 8 of the report. Key sources:

* MISP Project — https://www.misp-project.org/
* Wazuh Documentation — https://documentation.wazuh.com/
* MITRE ATT&CK — https://attack.mitre.org/
* abuse.ch (URLhaus) — https://abuse.ch/
* CIRCL OSINT Feed — https://www.circl.lu/

---

## 📜 License

This project is released under the **MIT License** (see `LICENSE`). You are free to
use, modify, and redistribute the code and documentation with attribution.
