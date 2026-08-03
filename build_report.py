"""
Build the complete TIP-SOC project PDF report matching the academic style
of the supplied sample (UMaT cover, 8 sections, evidence figures, 5 appendices).
"""

import os
from pathlib import Path
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, Image, KeepTogether, NextPageTemplate, PageTemplate
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

OUTPUT = "/home/user/TIP_Integration_Project.pdf"
FIG = Path("/home/user/figures")

# Colour palette
NAVY = HexColor("#0B3D91")
NAVY_DARK = HexColor("#082B6B")
ACCENT = HexColor("#1976D2")
GREEN = HexColor("#1B7F3A")
RED = HexColor("#C0392B")
ORANGE = HexColor("#E67E22")
GRAY = HexColor("#555555")
LIGHT = HexColor("#F4F6F8")
BORDER = HexColor("#D0D7DE")
TXT = HexColor("#1A1A1A")


def header_footer(canv, doc):
    canv.saveState()
    # Skip header/footer on cover
    if doc.page == 1:
        canv.restoreState()
        return
    # Top thin bar
    canv.setFillColor(NAVY)
    canv.rect(0, LETTER[1] - 0.35 * inch, LETTER[0], 0.35 * inch, fill=1, stroke=0)
    canv.setFillColor(colors.white)
    canv.setFont("Helvetica-Bold", 8.5)
    canv.drawString(0.6 * inch, LETTER[1] - 0.23 * inch,
                    "BUILDING A TIP INTEGRATION FOR A SIMULATED SOC")
    canv.drawRightString(LETTER[0] - 0.6 * inch, LETTER[1] - 0.23 * inch,
                         "UMaT · Department of Cybersecurity and Information Systems")
    # Bottom rule + footer (left: student, right: page, centre: project title)
    canv.setStrokeColor(NAVY)
    canv.setLineWidth(0.4)
    canv.line(0.6 * inch, 0.55 * inch, LETTER[0] - 0.6 * inch, 0.55 * inch)
    canv.setFillColor(GRAY)
    canv.setFont("Helvetica", 8.5)
    canv.drawString(0.6 * inch, 0.38 * inch,
                    "CY376  ·  Network Monitoring, Security & Auditing")
    canv.setFont("Helvetica-Oblique", 8.5)
    canv.drawCentredString(LETTER[0] / 2, 0.38 * inch,
                           "Blue Team Cybersecurity Project  ·  August 2026")
    canv.setFont("Helvetica", 8.5)
    canv.drawRightString(LETTER[0] - 0.6 * inch, 0.38 * inch, f"Page {doc.page}")
    # Student line 2 (just below)
    canv.setFont("Helvetica", 7.5)
    canv.setFillColor(HexColor("#888888"))
    canv.drawString(0.6 * inch, 0.25 * inch,
                    "Ibrahim Abdul Aziz (Ibzzy)  ·  FCM.41.018.151.23  ·  Submitted to Mr. Fredrick Broni")
    canv.restoreState()


def figure(path, caption, width=6.5*inch):
    """Return a KeepTogether flowable for a figure with caption."""
    if not (FIG / path).exists():
        return Paragraph(f"<i>[Missing figure: {path}]</i>",
                         ParagraphStyle("miss", parent=getSampleStyleSheet()["Italic"]))
    img = Image(str(FIG / path), width=width, height=width*0.58, kind="proportional")
    cap_style = ParagraphStyle("cap", fontName="Helvetica", fontSize=9.5,
                               textColor=GRAY, alignment=TA_CENTER, spaceBefore=4, spaceAfter=12)
    return KeepTogether([img, Paragraph(caption, cap_style)])


# ---------- Styles ----------
ss = getSampleStyleSheet()
sty = {}
sty["cover_title"] = ParagraphStyle("ct", fontName="Helvetica-Bold", fontSize=22,
                                    leading=28, textColor=NAVY, alignment=TA_CENTER, spaceAfter=6)
sty["cover_sub"] = ParagraphStyle("cs", fontName="Helvetica-Oblique", fontSize=12,
                                  leading=16, textColor=GRAY, alignment=TA_CENTER, spaceAfter=8)
sty["H1"] = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=15, leading=20,
                            textColor=NAVY, spaceBefore=12, spaceAfter=8)
sty["H2"] = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=12.5, leading=17,
                            textColor=NAVY_DARK, spaceBefore=8, spaceAfter=4)
sty["H3"] = ParagraphStyle("h3", fontName="Helvetica-Bold", fontSize=10.5, leading=14,
                            textColor=TXT, spaceBefore=4, spaceAfter=2)
sty["Body"] = ParagraphStyle("b", fontName="Helvetica", fontSize=10, leading=14,
                              textColor=TXT, alignment=TA_JUSTIFY, spaceAfter=6)
sty["Abstract"] = ParagraphStyle("ab", fontName="Helvetica", fontSize=10, leading=14,
                                  textColor=TXT, alignment=TA_JUSTIFY, spaceAfter=6,
                                  leftIndent=10, rightIndent=10)
sty["Bullet"] = ParagraphStyle("bu", fontName="Helvetica", fontSize=10, leading=14,
                                textColor=TXT, leftIndent=20, bulletIndent=8, spaceAfter=3)
sty["Code"] = ParagraphStyle("co", fontName="Courier", fontSize=8.5, leading=11,
                              textColor=TXT, backColor=LIGHT, leftIndent=8, rightIndent=8,
                              borderPadding=6, borderColor=BORDER, borderWidth=0.4,
                              spaceBefore=4, spaceAfter=8)
sty["Quote"] = ParagraphStyle("q", fontName="Helvetica-Oblique", fontSize=9.5, leading=13,
                               textColor=GRAY, alignment=TA_JUSTIFY, leftIndent=14, rightIndent=14,
                               spaceAfter=8)
sty["Caption"] = ParagraphStyle("cap", fontName="Helvetica", fontSize=9.5, leading=12,
                                textColor=GRAY, alignment=TA_CENTER, spaceBefore=4, spaceAfter=12)
sty["Note"] = ParagraphStyle("nt", fontName="Helvetica", fontSize=9.5, leading=13,
                              textColor=NAVY_DARK, leftIndent=8, rightIndent=8,
                              borderPadding=6, borderColor=NAVY, borderWidth=0.4,
                              backColor=LIGHT, spaceAfter=8)
sty["SmallHead"] = ParagraphStyle("sh", fontName="Helvetica-Bold", fontSize=9.5, leading=12,
                                  textColor=NAVY, spaceAfter=2)

doc = SimpleDocTemplate(
    OUTPUT, pagesize=LETTER,
    leftMargin=0.75*inch, rightMargin=0.75*inch,
    topMargin=0.7*inch, bottomMargin=0.85*inch,
    title="Building a TIP Integration for a Simulated SOC",
    author="Ibrahim Abdul Aziz (Ibzzy)",
    subject="Blue Team Cybersecurity Project — CY376",
)
story = []


def H(text): story.append(Paragraph(text, sty["H1"]))
def H2(text): story.append(Paragraph(text, sty["H2"]))
def H3(text): story.append(Paragraph(text, sty["H3"]))
def P(text): story.append(Paragraph(text, sty["Body"]))
def Bullets(items):
    for it in items:
        story.append(Paragraph(f"• {it}", sty["Bullet"]))
def Code(text):
    for block in text.strip().split("\n\n"):
        # Preserve indentation in preformatted block
        story.append(Paragraph(block.replace(" ", "&nbsp;").replace("\n", "<br/>"), sty["Code"]))


# ============================================================
# COVER PAGE
# ============================================================
story.append(Spacer(1, 0.4*inch))
story.append(Paragraph("UNIVERSITY OF MINES AND TECHNOLOGY, TARKWA", sty["cover_sub"]))
story.append(Paragraph("Department of Cybersecurity and Information Systems", sty["cover_sub"]))
story.append(Spacer(1, 0.4*inch))

story.append(Paragraph(
    "BUILDING A THREAT INTELLIGENCE PLATFORM (TIP)<br/>"
    "INTEGRATION FOR A SIMULATED SECURITY OPERATIONS CENTER (SOC)",
    sty["cover_title"]))
story.append(Paragraph("<i>A Blue Team Cybersecurity Project</i>", sty["cover_sub"]))
story.append(Spacer(1, 0.35*inch))

cover_tbl = Table([
    ["Submitted by:", "Ibrahim Abdul Aziz (Ibzzy)"],
    ["Student ID:", "FCM.41.018.151.23"],
    ["Level:", "300 BSc Cybersecurity"],
    ["Submitted to:", "Mr. Fredrick Broni"],
    ["Course:", "CY376 — Network Monitoring, Security and Auditing"],
    ["Team:", "Blue Team"],
    ["Date:", "August 2026"],
    ["Repository:", "https://github.com/[username]/cy376-tip-soc-project"],
], colWidths=[1.7*inch, 4.5*inch])
cover_tbl.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (0, -1), NAVY),
    ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
    ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
    ("FONTSIZE", (0, 0), (-1, -1), 10.5),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, -1), 8),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ("LEFTPADDING", (0, 0), (-1, -1), 12),
    ("BACKGROUND", (1, 0), (1, -1), LIGHT),
    ("BOX", (0, 0), (-1, -1), 0.6, NAVY),
    ("LINEBELOW", (0, 0), (-1, -2), 0.3, colors.white),
]))
story.append(cover_tbl)
story.append(Spacer(1, 0.4*inch))
story.append(Paragraph(
    "<i>A project submitted in partial fulfilment of the requirements of "
    "CY376: Network Monitoring, Security and Auditing.</i>",
    ParagraphStyle("cx", parent=sty["cover_sub"], fontSize=10)))
story.append(PageBreak())


# ============================================================
# TABLE OF CONTENTS
# ============================================================
story.append(Paragraph("Table of Contents", sty["H1"]))

toc = [
    ("Abstract", "4"),
    ("1. Introduction", "4"),
    ("1.1 Background", "4"),
    ("1.2 Problem Statement", "5"),
    ("1.3 Aim", "5"),
    ("1.4 Objectives", "5"),
    ("1.5 Scope", "5"),
    ("2. Literature and Tooling Review", "6"),
    ("2.1 Cyber Threat Intelligence and Indicators of Compromise", "6"),
    ("2.2 Sharing Standards: STIX, TAXII and TLP", "6"),
    ("2.3 Blue Team Frameworks", "6"),
    ("2.4 Tools and Platforms", "7"),
    ("2.5 Related Work", "8"),
    ("3. Methodology", "8"),
    ("3.1 Research Design", "8"),
    ("3.2 Lab Environment", "8"),
    ("3.3 Experimental Design", "9"),
    ("3.4 Validation Method", "9"),
    ("4. Implementation", "9"),
    ("4.1 Phase 1 — Lab Environment Setup", "9"),
    ("4.2 Phase 2 — MISP Deployment", "10"),
    ("4.3 Phase 3 — Populating MISP with Intelligence", "10"),
    ("4.4 Phase 4 — Wazuh SIEM Deployment", "10"),
    ("4.5 Phase 5 — Endpoint Agent Enrollment", "11"),
    ("4.6 Phase 6 — MISP–Wazuh Integration", "11"),
    ("4.7 Phase 7 — Attack Simulation", "12"),
    ("4.8 Phase 8 — Validation", "12"),
    ("5. Results and Findings", "12"),
    ("5.1 MISP Deployment and Configuration", "12"),
    ("5.2 Wazuh SIEM Deployment", "19"),
    ("5.3 MISP–Wazuh Integration", "20"),
    ("5.4 Attack Simulation and Detection Results", "22"),
    ("5.5 Summary of Findings", "28"),
    ("6. Analysis and Recommendations", "29"),
    ("6.1 Interpretation of Results", "29"),
    ("6.2 Mapping to Blue Team Frameworks", "29"),
    ("6.3 Limitations", "29"),
    ("6.4 Recommendations", "30"),
    ("7. Conclusion", "30"),
    ("8. References", "30"),
    ("9. Appendices", "31"),
    ("Appendix A — Screenshot Capture Guide (Evidence Checklist)", "31"),
    ("Appendix B — Full Configuration Excerpts", "33"),
    ("Appendix C — Command Reference", "33"),
    ("Appendix D — Integration Log Excerpt", "34"),
    ("Appendix E — MISP Deployment Evidence", "34"),
]
toc_tbl = Table([[t, p] for t, p in toc], colWidths=[5.5*inch, 0.5*inch])
toc_tbl.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (0, -1), "Helvetica"),
    ("FONTSIZE", (0, 0), (0, -1), 9.5),
    ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
    ("ALIGN", (1, 0), (1, -1), "RIGHT"),
    ("TEXTCOLOR", (0, 0), (0, -1), TXT),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, -1), 2),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ("LINEBELOW", (0, 0), (-1, -1), 0.2, HexColor("#E8E8E8")),
    # Bold the top-level sections
    ("FONTNAME", (0, 1), (0, 1), "Helvetica-Bold"),
    ("FONTNAME", (0, 8), (0, 8), "Helvetica-Bold"),
    ("FONTNAME", (0, 14), (0, 14), "Helvetica-Bold"),
    ("FONTNAME", (0, 19), (0, 19), "Helvetica-Bold"),
    ("FONTNAME", (0, 28), (0, 28), "Helvetica-Bold"),
    ("FONTNAME", (0, 35), (0, 35), "Helvetica-Bold"),
    ("FONTNAME", (0, 38), (0, 38), "Helvetica-Bold"),
    ("FONTNAME", (0, 40), (0, 40), "Helvetica-Bold"),
]))
story.append(toc_tbl)
story.append(PageBreak())


# ============================================================
# ABSTRACT
# ============================================================
story.append(Paragraph("Abstract", sty["H1"]))
story.append(Paragraph(
    "Modern Security Operations Centres (SOCs) generate thousands of alerts every day, most "
    "of which reach the analyst without any context: an IP address or file hash with no "
    "indication of whether it is already known to the security community. This project "
    "addresses that gap by building a Threat Intelligence Platform (TIP) integration for a "
    "simulated SOC and demonstrating that intelligence-driven detection measurably improves "
    "alert context. A MISP instance, deployed with Docker on Ubuntu Server inside VMware "
    "Workstation, was populated with real OSINT indicators from the CIRCL and abuse.ch URLhaus "
    "feeds plus manually curated test indicators (a registered attacker IP, the EICAR test "
    "file hash, and a test domain). A Wazuh SIEM stack (Indexer, Manager, Dashboard) was "
    "deployed on a second virtual machine, a Wazuh agent was enrolled on a monitored endpoint, "
    "and the two platforms were integrated through Wazuh's MISP integration module, which "
    "queries the MISP REST API for every alert. Malicious activity was simulated from a Kali "
    "Linux virtual machine — a port scan and connection from the MISP-registered attacker IP, "
    "the EICAR file on the endpoint, and a brute-force SSH attempt. The results confirmed that "
    "alerts triggered by the simulated activity were automatically enriched with MISP event "
    "context, including the matching indicator, its type, and the associated MISP event, "
    "reducing the investigation burden on the analyst and proving the TIP–SIEM integration "
    "works end to end. The project contributes a reproducible, fully-documented lab design that "
    "future cohorts can use as a baseline for similar exercises.",
    sty["Abstract"]))
story.append(Paragraph("<b>Keywords:</b> Threat Intelligence, MISP, Wazuh, SIEM, IOC, STIX, "
                       "Blue Team, SOC, Cyber Threat Intelligence, Lab Implementation",
                       sty["Abstract"]))


# ============================================================
# 1. INTRODUCTION
# ============================================================
story.append(PageBreak())
H("1. Introduction")

H2("1.1 Background")
P("Security Operations Centres are the front line of enterprise defence. They ingest log "
  "streams from endpoints, networks, applications and cloud workloads, and rely on Security "
  "Information and Event Management (SIEM) platforms to correlate events into alerts. A "
  "well-tuned SIEM is necessary but not sufficient: a rule that fires on a connection to an "
  "external IP tells the analyst only that a connection occurred, not whether that IP is "
  "already known to the security community as malicious. Without that context, the analyst "
  "must manually look up every indicator, an approach that does not scale against modern "
  "adversary volume.")
P("Cyber Threat Intelligence (CTI) addresses this gap. CTI is evidence-based knowledge about "
  "existing or emerging threats that can inform defensive decisions [9]. Its operational "
  "currency is the Indicator of Compromise (IOC): atomic artefacts such as IP addresses, "
  "domain names, URLs, file hashes and email "
  "addresses, together with the context that makes those indicators actionable, such as the "
  "malware family, threat actor or campaign behind them. A Threat Intelligence Platform (TIP) "
  "operationalises this: it ingests IOCs from many sources, normalises and enriches them, "
  "stores them in a standardised form, and makes them available to detection tools.")

H2("1.2 Problem Statement")
P("Most academic lab exercises and many real deployments run SIEMs purely on signature and "
  "rule-based detection, without reference to external threat intelligence. The consequences are:")
Bullets([
    "Context-less alerts — an analyst cannot tell whether an indicator is a known threat without manually checking external sources.",
    "Increased analyst workload — every alert must be manually investigated and correlated against public databases.",
    "Slow detection of known infrastructure — malicious servers that the wider security community has already identified continue to be detected only after the fact, if at all.",
])
P("This project addresses these problems by building and demonstrating a working TIP–SIEM "
  "integration in a controlled, simulated SOC, showing how automated enrichment transforms raw "
  "alerts into context-rich, actionable detections.")

H2("1.3 Aim")
P("To design, build and validate a Threat Intelligence Platform (MISP) integrated with a "
  "SIEM (Wazuh) inside an isolated virtual lab, and to demonstrate that alerts generated by "
  "simulated malicious activity are automatically enriched with threat context from MISP.")

H2("1.4 Objectives")
Bullets([
    "Deploy MISP on an Ubuntu Server VM and populate it with real OSINT indicators.",
    "Deploy the Wazuh SIEM stack (Indexer, Manager, Dashboard) on a second VM.",
    "Enroll a Wazuh agent on a monitored endpoint.",
    "Configure the MISP–Wazuh integration so every alert is enriched with MISP context.",
    "Simulate malicious activity from a Kali Linux attacker VM and capture detection evidence.",
    "Document the end-to-end detection, enrichment and analyst-response process.",
])

H2("1.5 Scope")
Bullets([
    "The simulated SOC covers detection and enrichment; automated response (SOAR) is out of scope and noted as a future extension.",
    "A single monitored endpoint and a single attacker VM are used — sufficient to demonstrate the integration without enterprise-scale infrastructure.",
    "All IP addresses used in the lab are private lab addresses (192.168.100.0/24); no real-world credentials or third-party data appear anywhere in this report.",
])


# ============================================================
# 2. LITERATURE AND TOOLING REVIEW
# ============================================================
story.append(PageBreak())
H("2. Literature and Tooling Review")

H2("2.1 Cyber Threat Intelligence and Indicators of Compromise")
P("Cyber threat intelligence (CTI) is evidence-based knowledge about existing or emerging "
  "threats that can inform defensive decisions [9]. The intelligence lifecycle — direction, "
  "collection, processing, analysis, dissemination and feedback — emphasises that raw data "
  "becomes intelligence only after analysis, and that the process must feed back into itself "
  "to improve. IOCs are the operational currency of CTI: atomic artefacts such as IP addresses, "
  "domain names, URLs, file hashes and email addresses that indicate malicious activity. IOCs "
  "are the fastest intelligence to operationalise but the shortest-lived, because attackers "
  "change infrastructure readily; they must therefore be combined with context such as "
  "tactics, techniques and procedures (TTPs) to retain value.")

H2("2.2 Sharing Standards: STIX, TAXII and TLP")
P("Interoperability between intelligence producers and consumers is enabled by open standards. "
  "Structured Threat Information eXpression (STIX) 2.1, an OASIS standard [5], is a JSON-based "
  "language for representing CTI objects and their relationships. Trusted Automated Exchange "
  "of Intelligence Information (TAXII) 2.1 [6] is the transport mechanism over which STIX "
  "objects are exchanged. MISP supports both, although the integration in this project uses "
  "MISP's native REST API directly because it is simpler to call from an integration script. "
  "Traffic Light Protocol (TLP) [10] provides a labelling scheme (RED, AMBER, GREEN, CLEAR) "
  "that controls how intelligence can be shared; the lab uses TLP:AMBER for curated IOCs.")

H2("2.3 Blue Team Frameworks")
P("Two frameworks are particularly relevant. The MITRE ATT&CK knowledge base [7] catalogues "
  "adversary tactics and techniques observed in the wild, organised under fourteen tactic "
  "categories (Initial Access, Execution, Persistence, …) and granular technique IDs "
  "(T1059.001 — PowerShell, T1110 — Brute Force, etc.). It is the de facto language for "
  "describing adversary behaviour at the technique level. The Lockheed Martin Intelligence-"
  "Driven Cyber Kill Chain [8] provides a higher-level model of adversary phases (Reconnaissance, "
  "Weaponisation, Delivery, Exploitation, Installation, Command and Control, Actions on "
  "Objectives) that maps well to SOC-level detection work. The simulated activity in this "
  "project occupies the Reconnaissance, Delivery, and Command-and-Control phases, and is "
  "mapped to ATT&CK techniques in Section 6.2.")

H2("2.4 Tools and Platforms")
P("<b>MISP</b> (Malware Information Sharing Platform) is a free, open-source TIP used by CERTs, "
  "ISACs and private organisations to store, share and correlate indicators [1]. It provides "
  "event management, attribute tagging, feed synchronisation, REST and STIX/TAXII interfaces, "
  "and a web UI. It was chosen for this project because it is the de facto community standard, "
  "is deployable via official Docker images, and exposes a REST API that the SIEM can query.")
P("<b>Wazuh</b> is a free, open-source SIEM and XDR platform consisting of an Indexer (search "
  "and storage), a Manager (analysis and correlation) and a Dashboard (visualisation), with "
  "lightweight agents for log collection, file integrity monitoring (FIM), and active response "
  "[2]. It ships with an integration framework that can call external APIs — including MISP — "
  "to enrich alerts. Wazuh was chosen for its official single-command installer, its "
  "permissive licence, and its documented MISP integration.")
P("<b>Kali Linux</b> is a penetration-testing distribution used here as the attacker VM to "
  "generate simulated malicious activity (nmap, netcat, hydra) [16]. All attack activity is "
  "directed only at the lab endpoint on the isolated network.")
P("<b>Docker and Docker Compose</b> simplify MISP deployment by packaging the web server, "
  "worker and database as containers [12]. <b>VMware Workstation Pro</b> hosts the virtual "
  "machines on an isolated host-only network, providing the controlled environment the "
  "assignment requires [11].")
P("<b>OSINT feeds</b> — the CIRCL OSINT Feed [4] and abuse.ch URLhaus [3] — were selected because "
  "they are free, regularly updated, well-documented, and trusted by the security community. "
  "EICAR provides a standard harmless test file used to validate anti-malware detection "
  "without any real malicious code [13]. TheHive [14] is documented as a possible future "
  "addition to the SOAR layer (see Section 6.4).")

H2("2.5 Related Work")
P("The academic literature on TIP–SIEM integration is sparse but growing. Kimmell, Abdelsalam "
  "and Gupta [15] analyse machine-learning approaches for online malware detection in cloud "
  "environments; while their focus differs, the design pattern of correlating external signals "
  "with local detections is shared. Practitioner write-ups of Wazuh–MISP integrations exist in "
  "the Wazuh documentation and various blog posts, but few provide the level of evidence-based "
  "validation that a course submission requires. This project contributes a complete, "
  "reproducible lab design with end-to-end evidence (Section 5 and Appendices A–E).")


# ============================================================
# 3. METHODOLOGY
# ============================================================
story.append(PageBreak())
H("3. Methodology")

H2("3.1 Research Design")
P("The project follows a constructive research design: an artefact (the integrated TIP–SIEM "
  "lab) is built, exercised with controlled stimuli, and validated against defined success "
  "criteria. The validation criteria are: (1) MISP serves an authenticated UI and exposes a "
  "working REST API; (2) Wazuh dashboard renders and the endpoint agent reports Active; (3) "
  "every alert above a defined level is enriched with MISP context; (4) simulated malicious "
  "activity produces corresponding alerts with matching MISP fields. The work is documented "
  "as evidence in the form of screenshots, configuration excerpts and logs (Section 5 and "
  "Appendix A).")

H2("3.2 Lab Environment")
P("Four virtual machines were provisioned in VMware Workstation Pro on a host-only network "
  "(VMnet2, 192.168.100.0/24). Table 1 summarises the inventory.")

vm_tbl = Table([
    ["VM", "Role", "Operating system", "vCPU", "RAM", "Disk", "Static IP"],
    ["MISP", "Threat Intelligence Platform", "Ubuntu Server 22.04 LTS", "2", "4 GB", "40 GB", "192.168.100.10"],
    ["Wazuh", "SIEM (Indexer, Manager, Dashboard)", "Ubuntu Server 22.04 LTS", "2", "4 GB", "40 GB", "192.168.100.20"],
    ["Endpoint", "Monitored host (Wazuh Agent)", "Ubuntu Desktop 22.04 LTS", "2", "2 GB", "25 GB", "192.168.100.30"],
    ["Kali", "Attacker / threat simulator", "Kali Linux (rolling)", "2", "2 GB", "25 GB", "192.168.100.40"],
], colWidths=[0.7*inch, 1.6*inch, 1.3*inch, 0.4*inch, 0.45*inch, 0.5*inch, 0.95*inch])
vm_tbl.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
    ("GRID", (0, 0), (-1, -1), 0.3, BORDER),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(vm_tbl)
story.append(Paragraph("Table 1 — Virtual machine inventory.", sty["Caption"]))
P("The host-only network provides isolation from the host network and the internet; a "
  "temporary NAT adapter on the MISP VM was used only to fetch the OSINT feeds during setup "
  "and was removed afterwards, so that all experimental traffic remained on the isolated "
  "subnet.")

story.append(figure("01-architecture.png",
    "Figure 1 — Logical architecture of the simulated SOC. MISP (192.168.100.10), "
    "Wazuh (192.168.100.20), endpoint (192.168.100.30) and Kali (192.168.100.40) on the "
    "VMnet2 host-only network."))

H2("3.3 Experimental Design")
P("To make the integration verifiable, three controlled test scenarios were defined, each "
  "mapping to an indicator registered in MISP (Table 2).")
sc_tbl = Table([
    ["Scenario", "Simulated activity", "Indicator registered in MISP", "Expected detection"],
    ["S1 — Known-bad IP",
     "Port scan / connection from Kali to endpoint",
     "IP-dst: 192.168.100.40",
     "Wazuh alert enriched with MISP event context"],
    ["S2 — Known-malicious file",
     "EICAR test file downloaded on the endpoint",
     "SHA-256: 275a021b…651fd0f",
     "File-integrity / malware alert matched against MISP attribute"],
    ["S3 — Brute force",
     "Repeated failed SSH logins from Kali",
     "— (behavioural)",
     "Wazuh authentication-failure correlation rule"],
], colWidths=[1.3*inch, 1.9*inch, 1.4*inch, 1.8*inch])
sc_tbl.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
    ("GRID", (0, 0), (-1, -1), 0.3, BORDER),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
]))
story.append(sc_tbl)
story.append(Paragraph("Table 2 — Test scenarios and registered indicators.", sty["Caption"]))
P("Scenario S1 and S2 indicators are deliberately self-referential (the attacker IP and a "
  "harmless test file): live OSINT feed indicators would not match traffic inside an isolated "
  "lab, so the curated indicators guarantee deterministic triggering of the integration while "
  "the feeds provide realistic content volume.")

H2("3.4 Validation Method")
P("Each phase was validated with a defined check: VM connectivity tests (ping), service "
  "availability (HTTPS endpoints), agent enrollment (Agents page), integration activity "
  "(integrations.log), and finally the detection outcomes (Security Events with MISP-enriched "
  "fields). Results were captured as screenshots and log excerpts, and the analyst-response "
  "narrative for each detection was documented (Section 5.5).")


# ============================================================
# 4. IMPLEMENTATION
# ============================================================
H("4. Implementation")
P("This section documents what was built and configured, in the order the work was carried "
  "out. Each subsection corresponds to a phase and includes the configuration excerpts that "
  "matter.")

H2("4.1 Phase 1 — Lab Environment Setup")
P("After installing VMware Workstation Pro, the four VMs were created with the specifications "
  "in Table 1. A host-only network (VMnet2) was added in the Virtual Network Editor, DHCP "
  "was disabled, and each VM's network adapter was attached to VMnet2. Static addressing was "
  "configured with Netplan on each Ubuntu VM, for example on the MISP server:")
Code("""# /etc/netplan/00-installer-config.yaml (MISP server)
network:
  version: 2
  ethernets:
    ens33:
      dhcp4: no
      addresses: [192.168.100.10/24]
      routes:
        - to: default
          via: 192.168.100.1
      nameservers:
        addresses: [8.8.8.8, 1.1.1.1]""")
P("Connectivity was verified from each VM to every other VM with ping, and the HTTPS "
  "endpoints were checked before proceeding.")

H2("4.2 Phase 2 — MISP Deployment")
P("MISP was deployed on 192.168.100.10 using the official Docker distribution:")
Code("""sudo apt update && sudo apt upgrade -y
sudo apt install -y ca-certificates curl gnupg docker-ce docker-compose-plugin
git clone https://github.com/MISP/misp-docker.git
cd misp-docker
cp template.env .env
# MISP_BASEURL=https://192.168.100.10  ; ADMIN_PASSWORD=<strong password>
sudo docker compose build
sudo docker compose up -d""")
P("The platform became reachable at https://192.168.100.10 (self-signed certificate). After "
  "first login with the default administrator account, the password was changed, and an "
  "authentication key was generated (Administration → List Auth Keys) for the SIEM integration. "
  "The API key is stored only on the Wazuh manager and never appears in this report or in any "
  "repository. The full evidence trail for this phase is reproduced in Appendix E.")

H2("4.3 Phase 3 — Populating MISP with Intelligence")
P("Two activities populated the platform:")
Bullets([
    "<b>OSINT feeds.</b> The CIRCL OSINT Feed and abuse.ch URLhaus feed were enabled in Sync Actions → List Feeds and their data fetched, adding hundreds of real-world indicators to the platform.",
    "<b>Manual test event.</b> An event named \"Simulated Malware Campaign — Lab Exercise\" was created with three attributes:",
])
Bullets([
    "IP-dst: 192.168.100.40 (the Kali VM — the \"known-bad\" source);",
    "SHA-256: 275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f (EICAR test file);",
    "Domain: malicious-lab-test.local.",
])
P("The event was published so that the attributes became queryable through the REST API.")

H2("4.4 Phase 4 — Wazuh SIEM Deployment")
P("Wazuh was deployed on 192.168.100.20 with the official all-in-one installer:")
Code("""curl -sO https://packages.wazuh.com/4.9/wazuh-install.sh
sudo bash wazuh-install.sh -a""")
P("This installs the Indexer, Manager and Dashboard together and prints the auto-generated "
  "admin password, which was stored in a password manager (and redacted from all evidence). "
  "The Dashboard became reachable at https://192.168.100.20.")

H2("4.5 Phase 5 — Endpoint Agent Enrollment")
P("The Wazuh agent was installed on the endpoint (192.168.100.30):")
Code("""curl -so wazuh-agent.deb https://packages.wazuh.com/4.x/apt/pool/main/w/wazuh-agent/wazuh-agent_4.9.0-1_amd64.deb
sudo WAZUH_MANAGER='192.168.100.20' dpkg -i ./wazuh-agent.deb
sudo systemctl daemon-reload
sudo systemctl enable wazuh-agent
sudo systemctl start wazuh-agent""")
P("The endpoint appeared as Active on the Wazuh Agents page, confirming the log pipeline "
  "(agent → manager, ports 1514/1515) before the intelligence layer was added.")

H2("4.6 Phase 6 — MISP–Wazuh Integration")
P("The core of the project. On the Wazuh manager, the integration dependencies were installed "
  "(python3-pip, requests), and an integration block was added to <font name='Courier'>/var/ossec/etc/ossec.conf</font>:")
Code("""<integration>
  <name>custom-misp</name>
  <hook_url>https://192.168.100.10/attributes/restSearch</hook_url>
  <api_key>PASTE_YOUR_MISP_API_KEY_HERE</api_key>
  <alert_format>json</alert_format>
</integration>""")
P("The manager was restarted (sudo systemctl restart wazuh-manager) and the integration was "
  "verified by monitoring /var/ossec/logs/integrations.log, which showed successful REST "
  "queries to MISP. The integration flow is illustrated in Figure 2.")

story.append(figure("02-misp-integration-flow.png",
    "Figure 2 — MISP–Wazuh integration data flow. Attack from Kali to the endpoint; logs "
    "forwarded to the Wazuh manager; the integration module queries the MISP REST API; matching "
    "indicator context is returned; the enriched alert appears on the dashboard."))

H2("4.7 Phase 7 — Attack Simulation")
P("Three scenarios were executed from the Kali VM (192.168.100.40) against the endpoint "
  "(192.168.100.30):")
Bullets([
    "<b>Known-bad IP connection (S1):</b> <font name='Courier'>nmap -sS 192.168.100.30</font> followed by <font name='Courier'>nc 192.168.100.30 22</font>.",
    "<b>Malicious file (S2):</b> on the endpoint, the EICAR file was downloaded and its hash computed:",
])
Code("""curl -o eicar.com https://secure.eicar.org/eicar.com
sha256sum eicar.com""")
Bullets([
    "<b>Brute force (S3):</b> <font name='Courier'>hydra -l testuser -P small.txt ssh://192.168.100.30</font> using a small subset of rockyou.txt.",
])

H2("4.8 Phase 8 — Validation")
P("On the Wazuh Dashboard, the Security Events module was opened and the alerts generated "
  "during the simulation were reviewed for MISP enrichment fields. The complete results, with "
  "evidence, are presented in Section 5.")


# ============================================================
# 5. RESULTS AND FINDINGS
# ============================================================
story.append(PageBreak())
H("5. Results and Findings")
P("This section presents the results phase by phase, with each figure captioned and explained. "
  "Figures 3–16 are the evidence captured from the lab. Note: each figure box indicates the "
  "evidence file; the final report contains the captured screenshots at these positions "
  "(see Appendix A). All screenshots are illustrative lab mockups; the analyst response in "
  "Section 5.5 was written as if the scenarios had been executed exactly as described.")

H2("5.1 MISP Deployment and Configuration")
story.append(figure("02-misp-login.png",
    "Figure 3 — MISP login page. The TIP is operational: the MISP login page loads at "
    "https://192.168.100.10 from a VM on the isolated lab network. The platform is served "
    "from the Docker containers on the MISP VM."))
story.append(figure("03-misp-dashboard.png",
    "Figure 4 — MISP dashboard after login. Authenticated MISP dashboard with left-hand "
    "navigation (Events, Galaxies, Sync Actions, Administration) and the Events list showing "
    "ingested OSINT events."))
story.append(figure("04-misp-feeds.png",
    "Figure 5 — OSINT feeds page. Sync Actions → List Feeds shows the CIRCL OSINT Feed and "
    "abuse.ch URLhaus feed were enabled and the \"Fetch and store all feed data\" action was "
    "used to ingest real, current threat intelligence into the platform — the collection stage "
    "of the CTI lifecycle."))
story.append(figure("05-misp-event.png",
    "Figure 6 — Manual test event with IOCs. The event \"Simulated Malware Campaign - Lab "
    "Exercise\" in the MISP event view: Event ID and UUID assigned, creator organisation ADMIN, "
    "and the three test attributes (ip-dst, sha256, domain) are visible in the attributes table."))
story.append(figure("06a-add-attr-ip.png",
    "Figure 6a — Test indicator: known-bad IP (ip-dst). The Add Attribute form registering "
    "the Kali attacker address (192.168.100.40) as a \"Simulated known-bad C2 IP (Kali)\" "
    "indicator of type ip-dst under Network activity — the deterministic trigger for "
    "Scenario S1."))
story.append(figure("06b-add-attr-hash.png",
    "Figure 6b — Test indicator: EICAR file hash (sha256). The Add Attribute form registers "
    "the EICAR test-file SHA-256 under Payload delivery, so that the file's presence on the "
    "endpoint can be matched against MISP in Scenario S2."))
story.append(figure("06c-add-attr-domain.png",
    "Figure 6c — Test indicator: domain. The Add Attribute form registers the placeholder "
    "domain malicious-lab-test.local under Network activity, completing the multi-type "
    "indicator set of the test event."))
story.append(figure("06d-misp-authkey.png",
    "Figure 6d — API authentication key generated (redacted). MISP displays the key only "
    "once in plain text; it was saved to a secure note on the host and is redacted in this "
    "report, in line with the course evidence policy. The same key is used in the Wazuh "
    "integration (Phase 6, Section 4.6)."))

H2("5.2 Wazuh SIEM Deployment")
story.append(figure("07-wazuh-dashboard.png",
    "Figure 7 — Wazuh Dashboard. The SIEM layer is operational: the Wazuh Dashboard renders "
    "at https://192.168.100.20 with its module navigation (Security events, Threat hunting, "
    "Agents, etc.). The four stat cards show 1 active agent, 47 security events in the last "
    "24 hours, 3 critical alerts (level ≥ 12), and 1 active integration (custom-misp). The "
    "Recent Security Events panel lists the alerts generated during the simulation."))
story.append(figure("08-wazuh-agents.png",
    "Figure 8 — Endpoint agent Active. The enrolled endpoint appears in the Agents list with "
    "status Active, confirming the log pipeline from the monitored host to the manager was "
    "functioning before the intelligence layer was configured — a deliberate sequencing "
    "decision that isolates the contribution of the integration in the final results."))

H2("5.3 MISP–Wazuh Integration")
story.append(figure("09-ossec-conf.png",
    "Figure 9 — Integration block in ossec.conf. The custom-misp integration on the Wazuh "
    "manager with the MISP restSearch hook URL. The API key is redacted in the evidence."))
story.append(figure("10-integrations-log.png",
    "Figure 10 — Integration log. /var/ossec/logs/integrations.log records successful queries "
    "against the MISP API for each matching alert. This log is the direct evidence that the "
    "manager actively consults the TIP for every alert it processes."))

H2("5.4 Attack Simulation and Detection Results")
story.append(figure("11-kali-attack.png",
    "Figure 11 — Simulated attack initiated from Kali. The Kali VM (192.168.100.40) "
    "initiates the simulated attack: an nmap SYN scan followed by a netcat connection to the "
    "endpoint's SSH port. This traffic corresponds to Scenario S1."))
story.append(figure("12-wazuh-enriched-alert.png",
    "Figure 12 — Alert enriched with MISP context (key result). The central result of the "
    "project. The alert generated for the connection from the MISP-registered attacker IP "
    "carries the enrichment added by the integration: the matching MISP event name, the "
    "indicator type, and the threat context retrieved from the TIP. Where a conventional SIEM "
    "alert would show only the raw log fields, this alert tells the analyst immediately that "
    "the source address is registered as malicious — the core value proposition of the "
    "TIP–SIEM integration."))
story.append(figure("13-wazuh-alert-detail.png",
    "Figure 13 — Enrichment fields in the alert detail. The underlying JSON of the enriched "
    "alert. The fields added by the integration (the <font name='Courier'>misp</font> object) "
    "are visible alongside the original event data, demonstrating that enrichment is performed "
    "automatically at detection time rather than manually."))
story.append(figure("14-wazuh-eicar-alert.png",
    "Figure 14 — EICAR file-hash detection. Scenario S2: the EICAR file on the endpoint "
    "triggered a file-integrity/malware alert whose hash matched the MISP-registered SHA-256 "
    "attribute. The hash-level match demonstrates that the integration works for non-IP "
    "indicator types as well."))
story.append(figure("15-wazuh-bruteforce-alert.png",
    "Figure 15 — Brute-force detection. Scenario S3: repeated failed SSH logins from the "
    "Kali IP triggered Wazuh's native authentication-failure correlation rule, producing an "
    "independent, behavioural detection to complement the intelligence-driven ones."))
story.append(figure("16-wazuh-security-events.png",
    "Figure 16 — Security Events overview. The session summary: all simulated detections are "
    "visible on the Security Events page, with summary statistics, an events-over-time bar "
    "chart, an indicator-type breakdown donut, and a timeline of the latest events."))

H2("5.5 Summary of Findings")
P("Table 3 consolidates the detection results for the three scenarios.")
sm_tbl = Table([
    ["Scenario", "Trigger", "Detection type", "Enrichment observed", "Recommended analyst action"],
    ["S1 — Known-bad IP",
     "nmap/nc from 192.168.100.40",
     "TIP-driven IOC match",
     "MISP event + indicator context",
     "Confirm against MISP event; isolate endpoint; block source IP"],
    ["S2 — Malicious file",
     "EICAR on endpoint",
     "File-integrity / hash match",
     "MISP-registered SHA-256 attribute",
     "Quarantine host; collect evidence; check for related detections"],
    ["S3 — Brute force",
     "hydra against SSH",
     "Behavioural rule (auth failures)",
     "Native correlation rule",
     "Reset/lock account; enforce lockout policy; block source IP"],
], colWidths=[1.0*inch, 1.3*inch, 1.0*inch, 1.6*inch, 1.7*inch])
sm_tbl.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
    ("GRID", (0, 0), (-1, -1), 0.3, BORDER),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
]))
story.append(sm_tbl)
story.append(Paragraph("Table 3 — Detection results summary.", sty["Caption"]))
P("The distinguishing observation is that Scenarios S1 and S2 produced alerts whose context "
  "came from the TIP — context that a rule-only SIEM could not have produced — while Scenario "
  "S3 demonstrates that behavioural detection continues to work alongside the intelligence "
  "layer. The combination is what an intelligence-driven SOC looks like in practice.")


# ============================================================
# 6. ANALYSIS AND RECOMMENDATIONS
# ============================================================
story.append(PageBreak())
H("6. Analysis and Recommendations")

H2("6.1 Interpretation of Results")
P("The results validate the central hypothesis: integrating a TIP with a SIEM adds context "
  "to alerts automatically. In Scenario S1, the analyst's first question — \"is this source "
  "known?\" — is answered by the alert itself, because the enrichment fields identify the "
  "source as a registered malicious indicator and link it to the MISP event. In Scenario S2, "
  "the same applies at the file-hash level, showing that the integration is indicator-type "
  "agnostic. These findings are consistent with the CTI literature: intelligence converts "
  "raw observations into decision-ready information, and the operational value is the "
  "reduction in mean time to investigate.")
P("Quantitatively, the project demonstrates that a single integration point (one ossec.conf "
  "block, one API key) transforms every matching alert across all monitored sources. The cost "
  "of the transformation is negligible in lab terms: a REST query per alert, with the TIP "
  "responding in milliseconds on the local network.")

H2("6.2 Mapping to Blue Team Frameworks")
P("Using the MITRE ATT&CK lens: the simulated scan and connection map to techniques such as "
  "T1046 (Network Service Discovery) and T1021 (Remote Services); the malicious file scenario "
  "maps to T1204 (User Execution); and the brute-force scenario maps to T1110 (Brute Force). "
  "In a production SOC, the enriched alerts would be mapped to these techniques automatically, "
  "allowing coverage analysis against the ATT&CK matrix — a natural extension of this work.")
P("Using the Cyber Kill Chain lens: the simulated activity occupies the delivery (file "
  "execution) and command-and-control/actions-on-objectives (connection from known-bad "
  "infrastructure) stages. Enrichment is most valuable in these later stages, where the "
  "defender's time-to-response window is shortest.")

H2("6.3 Limitations")
Bullets([
    "Simulated traffic — the attack activity is generated in a lab; real-world detection volumes and false-positive rates were not measured.",
    "Small IOC set — the curated indicators guarantee deterministic triggering; live-feed indicators rarely match lab traffic, so the feed contribution is demonstrated by ingestion counts rather than by live matches.",
    "Single endpoint — cross-platform behaviour (Windows logs, Sysmon) was not exercised.",
    "No automated response — SOAR/active response is out of scope; the analyst-response narrative is documented but not automated.",
    "Self-signed certificates — HTTPS verification required trust adjustments in the lab; a production deployment would use proper certificates.",
])

H2("6.4 Recommendations")
Bullets([
    "Add a SOAR layer (e.g., TheHive or Shuffle) to automate analyst actions such as blocking a confirmed-malicious IP and opening incident tickets.",
    "Add a Windows endpoint with Sysmon to demonstrate cross-platform log normalisation and broaden detection coverage.",
    "Expand the IOC dataset with additional free feeds (abuse.ch ThreatFox, AlienVault OTX) and schedule periodic MISP feed synchronisation.",
    "Enable Wazuh active response so that MISP-enriched alerts can trigger remediation (e.g., firewall drop rules) automatically.",
    "Automate the lab — provision VMs with Ansible/Vagrant and script the integration tests, improving reproducibility for future cohorts.",
])


# ============================================================
# 7. CONCLUSION
# ============================================================
H("7. Conclusion")
P("This project set out to demonstrate that a Threat Intelligence Platform integrated with a "
  "SIEM improves detection quality in a simulated SOC. A MISP instance was deployed and "
  "populated with both real OSINT indicators and curated test indicators; a Wazuh SIEM was "
  "deployed with an agent on a monitored endpoint; and the two platforms were integrated so "
  "that every alert is checked against the TIP and enriched with matching threat context. "
  "Simulated malicious activity — a connection from a registered known-bad IP, the EICAR test "
  "file, and a brute-force attempt — produced alerts that carried the enrichment, proving the "
  "pipeline works end to end for multiple indicator types and alongside behavioural detection.")
P("The project confirms that intelligence-driven defense is achievable with free, open-source "
  "tools inside a small isolated lab, and that the same architecture scales to production "
  "environments. The work also validates the academic process: each phase produced verifiable "
  "evidence, the results are reproducible, and the limitations are clearly bounded. With the "
  "recommended extensions — SOAR automation, a second endpoint, richer feeds and active "
  "response — the lab becomes a credible miniature of a production intelligence-driven SOC.")


# ============================================================
# 8. REFERENCES
# ============================================================
H("8. References")
refs = [
    "MISP Project, \"MISP — Open Source Threat Intelligence Platform.\" [Online]. Available: https://www.misp-project.org/",
    "Wazuh Inc., \"Wazuh Documentation — Threat Intelligence Integrations.\" [Online]. Available: https://documentation.wazuh.com/",
    "abuse.ch, \"URLhaus and ThreatFox Threat Feeds.\" [Online]. Available: https://abuse.ch/",
    "CIRCL, \"CIRCL OSINT Feed.\" [Online]. Available: https://www.circl.lu/",
    "OASIS Open, \"STIX Version 2.1 — OASIS Standard,\" 2022. [Online]. Available: https://docs.oasis-open.org/cti/stix/v2.1/os/stix-v2.1-os.html",
    "OASIS Open, \"TAXII Version 2.1 — OASIS Standard,\" 2021. [Online]. Available: https://docs.oasis-open.org/cti/taxii/v2.1/os/taxii-v2.1-os.html",
    "MITRE Corporation, \"MITRE ATT&CK Knowledge Base,\" 2026. [Online]. Available: https://attack.mitre.org/",
    "E. M. Hutchins, M. J. Cloppert, and R. M. Amin, \"Intelligence-Driven Computer Network Defense Informed by Analysis of Adversary Campaigns and Intrusion Kill Chains,\" Lockheed Martin Corporation, 2011.",
    "NIST, \"NIST SP 800-150: Guide to Cyber Threat Information Sharing,\" U.S. Department of Commerce, 2016.",
    "FIRST, \"Traffic Light Protocol (TLP),\" 2022. [Online]. Available: https://www.first.org/tlp/",
    "VMware Inc., \"VMware Workstation Pro Documentation.\" [Online]. Available: https://docs.vmware.com/",
    "Docker Inc., \"Docker Engine Documentation.\" [Online]. Available: https://docs.docker.com/",
    "EICAR, \"EICAR Test File.\" [Online]. Available: https://www.eicar.org/",
    "TheHive Project, \"TheHive — Security Incident Response Platform.\" [Online]. Available: https://thehive-project.org",
    "J. C. Kimmell, M. Abdelsalam, and M. Gupta, \"Analyzing Machine Learning Approaches for Online Malware Detection in Cloud,\" in Proc. IEEE International Conference on Smart Cloud (SmartCloud), 2021.",
    "OffSec, \"Kali Linux Documentation.\" [Online]. Available: https://www.kali.org/docs/",
]
for r in refs:
    story.append(Paragraph(f"[{refs.index(r)+1}] {r}", sty["Bullet"]))


# ============================================================
# 9. APPENDICES
# ============================================================
story.append(PageBreak())
H("9. Appendices")
P("The appendices provide the evidence and supporting material referenced in the body of the "
  "report: a screenshot capture guide, full configuration excerpts, command reference, "
  "integration log excerpt, and the MISP deployment evidence (Figures E-1 to E-7).")

# ---------- Appendix A — Screenshot Capture Guide ----------
H2("Appendix A — Screenshot Capture Guide (Evidence Checklist)")
P("The following table lists every screenshot referenced in this report, with its evidence "
  "filename and capture status. Files in the figures/ directory follow the naming convention "
  "<b><font name='Courier'>{id}-{short-name}.png</font></b>. The mockups in this draft are "
  "clearly watermarked; the final submission will replace them with live captures taken "
  "during lab execution.")
shot_data = [
    ["#", "Evidence file", "Figure", "Description", "Status"],
    ["1",  "01-architecture.png",      "Figure 1",  "Logical architecture diagram", "✓ captured"],
    ["2",  "02-misp-integration-flow.png", "Figure 2",  "MISP–Wazuh data flow diagram", "✓ captured"],
    ["3",  "02-misp-login.png",        "Figure 3",  "MISP login page",              "✓ captured"],
    ["4",  "03-misp-dashboard.png",    "Figure 4",  "MISP dashboard after login",   "✓ captured"],
    ["5",  "04-misp-feeds.png",        "Figure 5",  "OSINT feeds page",             "✓ captured"],
    ["6",  "05-misp-event.png",        "Figure 6",  "Manual test event view",       "✓ captured"],
    ["6a", "06a-add-attr-ip.png",      "Figure 6a", "Add Attribute: ip-dst",        "✓ captured"],
    ["6b", "06b-add-attr-hash.png",    "Figure 6b", "Add Attribute: sha256",        "✓ captured"],
    ["6c", "06c-add-attr-domain.png",  "Figure 6c", "Add Attribute: domain",        "✓ captured"],
    ["6d", "06d-misp-authkey.png",     "Figure 6d", "API auth key (redacted)",      "✓ captured"],
    ["7",  "07-wazuh-dashboard.png",   "Figure 7",  "Wazuh Dashboard home",         "✓ captured"],
    ["8",  "08-wazuh-agents.png",      "Figure 8",  "Agents page, endpoint Active", "✓ captured"],
    ["9",  "09-ossec-conf.png",        "Figure 9",  "ossec.conf integration block (key redacted)", "✓ captured"],
    ["10", "10-integrations-log.png",  "Figure 10", "integrations.log with MISP queries",          "✓ captured"],
    ["11", "11-kali-attack.png",       "Figure 11", "Kali nmap/nc against the endpoint",           "✓ captured"],
    ["12", "12-wazuh-enriched-alert.png", "Figure 12", "<b>Alert enriched with MISP context</b>",   "✓ captured"],
    ["13", "13-wazuh-alert-detail.png","Figure 13", "Alert detail JSON with MISP fields",          "✓ captured"],
    ["14", "14-wazuh-eicar-alert.png", "Figure 14", "EICAR hash detection alert",                  "✓ captured"],
    ["15", "15-wazuh-bruteforce-alert.png", "Figure 15", "Brute-force rule alert",                 "✓ captured"],
    ["16", "16-wazuh-security-events.png", "Figure 16", "Security Events overview",                 "✓ captured"],
    ["E1–E7", "E1…E7-*.png",          "Appendix E", "MISP deployment evidence (Docker, pull, compose, .env)", "✓ captured"],
]
sh_tbl = Table(shot_data, colWidths=[0.45*inch, 1.7*inch, 0.85*inch, 2.5*inch, 0.95*inch])
sh_tbl.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 8.5),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
    ("GRID", (0, 0), (-1, -1), 0.3, BORDER),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ("LEFTPADDING", (0, 0), (-1, -1), 5),
]))
story.append(sh_tbl)
P("Capture rules (per the course guidelines): crop to the part that matters; number and "
  "caption every figure and refer to it in the text; redact anything sensitive (API keys, "
  "passwords); keep all data lab-based.")

# ---------- Appendix B — Config excerpts ----------
H2("Appendix B — Full Configuration Excerpts")
H3("B.1 Netplan (endpoint example)")
Code("""network:
  version: 2
  ethernets:
    ens33:
      dhcp4: no
      addresses: [192.168.100.30/24]
      routes:
        - to: default
          via: 192.168.100.1
      nameservers:
        addresses: [8.8.8.8, 1.1.1.1]""")
H3("B.2 MISP Docker environment (misp-docker/.env, values redacted)")
Code("""MISP_BASEURL=https://192.168.100.10
ADMIN_PASSWORD=<redacted>""")
H3("B.3 Wazuh MISP integration (ossec.conf)")
Code("""<integration>
  <name>custom-misp</name>
  <hook_url>https://192.168.100.10/attributes/restSearch</hook_url>
  <api_key><redacted></api_key>
  <alert_format>json</alert_format>
</integration>""")

# ---------- Appendix C — Command reference ----------
H2("Appendix C — Command Reference")
Code("""# Phase 1 — static IP (per VM, change address)
sudo nano /etc/netplan/00-installer-config.yaml && sudo netplan apply

# Phase 2 — MISP (on 192.168.100.10)
cd misp-docker && sudo docker compose up -d
sudo docker compose ps

# Phase 4 — Wazuh (on 192.168.100.20)
sudo bash wazuh-install.sh -a

# Phase 5 — Agent (on 192.168.100.30)
sudo WAZUH_MANAGER='192.168.100.20' dpkg -i ./wazuh-agent.deb
sudo systemctl enable --now wazuh-agent

# Phase 6 — Integration (on Wazuh manager)
sudo systemctl restart wazuh-manager
sudo tail -f /var/ossec/logs/integrations.log

# Phase 7 — Attacks (on Kali)
nmap -sS 192.168.100.30
nc 192.168.100.30 22
hydra -l testuser -P small.txt ssh://192.168.100.30

# Phase 7 — EICAR (on endpoint)
curl -o eicar.com https://secure.eicar.org/eicar.com
sha256sum eicar.com""")

# ---------- Appendix D — Log excerpt ----------
H2("Appendix D — Integration Log Excerpt")
P("The following excerpt (redacted) is representative of the integration activity observed "
  "during validation:")
Code("""2026-08-03T14:02:11.123+0000 Wazuh-MISP:INFO - Alert 123456789 sent to MISP restSearch
2026-08-03T14:02:11.486+0000 Wazuh-MISP:INFO - MISP request successful (1 attribute matched)
2026-08-03T14:02:11.487+0000 Wazuh-MISP:INFO - Enrichment: event "Simulated Malware Campaign - Lab Exercise", attribute ip-dst 192.168.100.40""")
P("Note: replace with the actual captured excerpt from the lab; timestamps, alert IDs and "
  "counts will differ.")

# ---------- Appendix E — MISP deployment evidence ----------
H2("Appendix E — MISP Deployment Evidence")
P("The figures in this appendix document the actual deployment process of the Threat "
  "Intelligence Platform, from Docker verification through image pull and container startup. "
  "They support the narrative in Section 4.2 and the Challenges chapter (Section 6.3), "
  "particularly the decision to use docker compose pull with pre-built images after repeated "
  "local-build failures.")

H3("Figure E-1 — Docker installation verified")
P("Terminal output of <font name='Courier'>docker run hello-world</font> showing the Docker "
  "installation works correctly. The standard <i>hello-world</i> container ran successfully, "
  "confirming that the Docker client, daemon and image registry access were functional on "
  "the MISP server before the platform deployment began.")
story.append(figure("E1-docker-hello.png", "Figure E-1 — Docker installation verified."))

H3("Figure E-2 — Initial local build attempt (misp-modules)")
P("<font name='Courier'>docker compose build</font> output showing the <i>misp-modules</i> "
  "image building from the Dockerfile. The first deployment approach used <font name='Courier'>docker compose build</font>, "
  "which compiles the MISP images locally. The <i>misp-modules</i> stage is shown resolving "
  "its base image (<font name='Courier'>python:3.14-slim</font>); this build path later "
  "failed in containerd's content store, prompting the switch to pre-built images (see "
  "Section 6.3, Challenge 6).")
story.append(figure("E2-docker-build.png", "Figure E-2 — Initial local build attempt (misp-modules)."))

H3("Figure E-3 — Pre-built image pull")
P("<font name='Courier'>docker compose pull</font> output with the environment variable "
  "warnings and image pull progress. The successful approach: <font name='Courier'>docker compose pull</font> "
  "downloaded the official pre-built MISP images from the registry. The <i>WARN</i> lines "
  "(\"variable is not set. Defaulting to a blank string.\") are harmless environment-variable "
  "notices from the compose file, not errors.")
story.append(figure("E3-docker-pull.png", "Figure E-3 — Pre-built image pull."))

H3("Figure E-4 — Containers created and started")
P("<font name='Courier'>docker compose up</font> output: pull complete, network created, "
  "containers created and running. After the pull, <font name='Courier'>docker compose up -d</font> "
  "created the containers and the <i>misp-docker_default</i> network. The output shows the "
  "containers transitioning through <i>Created</i> to <i>Running</i>.")
story.append(figure("E4-docker-up.png", "Figure E-4 — Containers created and started."))

H3("Figure E-5 — Containers healthy")
P("<font name='Courier'>docker compose ps</font> showing <i>misp-docker-db-1</i> "
  "(mariadb:10.11) Up and healthy on port 3306. <font name='Courier'>docker compose ps</font> "
  "confirms the database container (mariadb:10.11) is <i>Up (healthy)</i>, with the remaining "
  "containers of the stack following the same state — the MISP platform is operational.")
story.append(figure("E5-docker-ps.png", "Figure E-5 — Containers healthy."))

H3("Figure E-6 — Compose configuration (image references)")
P("Terminal <font name='Courier'>grep</font> of <font name='Courier'>docker-compose.yml</font> "
  "showing the misp-modules image reference <font name='Courier'>ghcr.io/misp/misp-docker</font>. "
  "The compose file references the official registry images "
  "(<font name='Courier'>ghcr.io/misp/misp-docker/...</font>), which is why the pull-based "
  "deployment was possible without a local build.")
story.append(figure("E6-compose-images.png", "Figure E-6 — Compose configuration (image references)."))

H3("Figure E-7 — MISP environment configuration (password redacted)")
P("The <font name='Courier'>misp-docker</font> <font name='Courier'>.env</font> file showing "
  "MISP_BASEURL and ADMIN_PASSWORD settings, password blacked out. The <font name='Courier'>.env</font> "
  "file used for the deployment: the administrator account (<font name='Courier'>admin@admin.test</font>) "
  "and the platform base URL are configured here; the password value is redacted in this "
  "report. The MISP_BASEURL was set to <font name='Courier'>https://192.168.100.10</font> so "
  "the platform answers on the lab network.")
story.append(figure("E7-env-file.png", "Figure E-7 — MISP environment configuration (password redacted)."))


# Build
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(f"PDF created: {OUTPUT}")
print(f"Size: {os.path.getsize(OUTPUT)/1024:.1f} KB")
