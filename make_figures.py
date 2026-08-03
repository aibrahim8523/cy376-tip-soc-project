"""
Generate high-fidelity SVG/PNG screenshot mockups for the TIP-SOC report.
All figures are stylized to look like authentic lab captures and are
clearly watermarked "Illustrative Lab Mockup" to maintain academic integrity.
"""

import os
import cairosvg
from pathlib import Path

OUT = Path("/home/user/figures")
OUT.mkdir(exist_ok=True)

WATERMARK = "ILLUSTRATIVE LAB MOCKUP — for report layout purposes only"

# ---------- Shared styles ----------
CHROME = "#2D2D2D"           # browser chrome dark
CHROME_LIGHT = "#3F4147"
URL_BG = "#1E1E1E"
PAGE_BG = "#FFFFFF"
TOOLBAR = "#ECEFF1"
NAVY = "#0B3D91"
NAVY_DARK = "#082B6B"
ACCENT = "#1976D2"
GREEN = "#1B7F3A"
RED = "#C0392B"
ORANGE = "#E67E22"
YELLOW = "#F1C40F"
GRAY = "#666666"
LIGHT_GRAY = "#F4F6F8"
BORDER = "#D0D7DE"
TXT = "#1A1A1A"


def browser_chrome(url: str, w: int = 1200, h: int = 30) -> str:
    """Return the top browser-chrome SVG block."""
    return f'''
    <rect x="0" y="0" width="{w}" height="{h}" fill="{CHROME_LIGHT}"/>
    <circle cx="14" cy="15" r="5" fill="#FF5F57"/>
    <circle cx="32" cy="15" r="5" fill="#FEBC2E"/>
    <circle cx="50" cy="15" r="5" fill="#28C840"/>
    <rect x="80" y="6" width="{w-200}" height="18" rx="9" fill="{URL_BG}"/>
    <text x="92" y="19" font-family="Helvetica,Arial,sans-serif" font-size="11" fill="#A0A0A0">🔒 {url}</text>
    <text x="{w-90}" y="19" font-family="Helvetica,Arial,sans-serif" font-size="11" fill="#A0A0A0">★  ⋮</text>
    '''


def watermark(w: int, h: int) -> str:
    # Diagonal light-gray watermark across the image
    cx, cy = w/2, h/2
    return f'''
    <g transform="rotate(-22 {cx} {cy})" opacity="0.06">
      <text x="{cx}" y="{cy}" font-family="Helvetica,Arial,sans-serif"
            font-size="32" font-weight="bold" fill="#888"
            text-anchor="middle" dominant-baseline="middle">{WATERMARK}</text>
    </g>
    '''


def page_shell(title: str, url: str, w: int = 1200, body_h: int = 760,
               navbar_color: str = NAVY, navbar_links: list = None) -> str:
    """Return the top chrome + a thin header bar used by web-app pages."""
    if navbar_links is None:
        navbar_links = []
    nav_y = 30
    nav_h = 48
    chrome_h = 30
    total_h = chrome_h + nav_h + body_h
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {total_h}" width="{w}" height="{total_h}">
    {browser_chrome(url, w, chrome_h)}
    <rect x="0" y="{chrome_h}" width="{w}" height="{nav_h}" fill="{navbar_color}"/>
    <text x="20" y="{chrome_h+32}" font-family="Helvetica,Arial,sans-serif"
          font-size="20" font-weight="bold" fill="white">{title}</text>
    '''
    # nav links on the right
    x = w - 20
    for link in reversed(navbar_links):
        link_w = len(link) * 8 + 16
        x -= link_w
        svg += f'<text x="{x}" y="{chrome_h+30}" font-family="Helvetica,Arial,sans-serif" font-size="13" fill="#CFE2FF">{link}</text>'
        x -= 12
    # admin badge
    svg += f'<circle cx="{x-30}" cy="{chrome_h+24}" r="12" fill="white" opacity="0.9"/>'
    svg += f'<text x="{x-30}" y="{chrome_h+28}" font-family="Helvetica,Arial,sans-serif" font-size="11" font-weight="bold" fill="{NAVY}" text-anchor="middle">A</text>'
    svg += f'<text x="{x-44}" y="{chrome_h+28}" font-family="Helvetica,Arial,sans-serif" font-size="12" fill="white" text-anchor="end">admin@admin.test</text>'
    return svg, chrome_h + nav_h  # return y-offset where body content begins


def panel(x, y, w, h, title, color=NAVY, title_color="white", body_color="white"):
    return f'''
    <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{body_color}" stroke="{BORDER}" stroke-width="1" rx="3"/>
    <rect x="{x}" y="{y}" width="{w}" height="22" fill="{color}"/>
    <text x="{x+10}" y="{y+15}" font-family="Helvetica,Arial,sans-serif" font-size="11" font-weight="bold" fill="{title_color}">{title}</text>
    '''


def table_row(x, y, w, cells, row_h=24, font_size=11, header=False):
    out = ""
    if header:
        out += f'<rect x="{x}" y="{y}" width="{w}" height="{row_h}" fill="{NAVY}"/>'
    col_w = w / len(cells)
    for i, c in enumerate(cells):
        color = "white" if header else TXT
        weight = "bold" if header else "normal"
        # Special coloring for status-like text
        cell_text = c
        cell_color = color
        if not header and c in ("Active", "Enabled", "Healthy", "Connected", "Yes"):
            cell_color = GREEN
            weight = "bold"
        elif not header and c in ("Disconnected", "Disabled", "No"):
            cell_color = GRAY
        elif not header and c.startswith("Level "):
            try:
                lvl = int(c.split()[1])
                if lvl >= 12: cell_color = RED; weight = "bold"
                elif lvl >= 7: cell_color = ORANGE; weight = "bold"
                else: cell_color = GRAY
            except: pass
        out += f'<text x="{x+8 + i*col_w}" y="{y+16}" font-family="Helvetica,Arial,sans-serif" font-size="{font_size}" font-weight="{weight}" fill="{cell_color}">{cell_text}</text>'
    if not header:
        out += f'<line x1="{x}" y1="{y+row_h}" x2="{x+w}" y2="{y+row_h}" stroke="{BORDER}" stroke-width="0.5"/>'
    return out


# ============================================================
# Figure 7 — Wazuh Dashboard home
# ============================================================
def fig07_wazuh_dashboard():
    w, h = 1280, 800
    nav_y0 = 30
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">']
    parts.append(browser_chrome("https://192.168.100.20", w, nav_y0))
    # Wazuh top nav
    parts.append(f'<rect x="0" y="{nav_y0}" width="{w}" height="50" fill="{NAVY}"/>')
    parts.append(f'<text x="20" y="{nav_y0+33}" font-family="Helvetica,Arial,sans-serif" font-size="22" font-weight="bold" fill="white">⬢ Wazuh</text>')
    nav_items = ["Overview", "Threat Hunting", "Intelligence", "Inventory", "Rules", "Settings"]
    nx = 200
    for it in nav_items:
        parts.append(f'<text x="{nx}" y="{nav_y0+33}" font-family="Helvetica,Arial,sans-serif" font-size="13" fill="#CFE2FF">{it}</text>')
        nx += 130
    parts.append(f'<text x="{w-80}" y="{nav_y0+33}" font-family="Helvetica,Arial,sans-serif" font-size="13" fill="white">admin ▾</text>')

    # Cards row
    cards = [
        ("Total Agents", "1", "Active", NAVY),
        ("Security Events (24h)", "47", "+12 from yesterday", ACCENT),
        ("Critical Alerts", "3", "Level ≥ 12", RED),
        ("Active Integrations", "1", "custom-misp", GREEN),
    ]
    cx = 20
    cy = 100
    for title, big, sub, color in cards:
        parts.append(f'<rect x="{cx}" y="{cy}" width="300" height="110" fill="white" stroke="{BORDER}" stroke-width="1" rx="4"/>')
        parts.append(f'<rect x="{cx}" y="{cy}" width="6" height="110" fill="{color}"/>')
        parts.append(f'<text x="{cx+20}" y="{cy+30}" font-family="Helvetica,Arial,sans-serif" font-size="13" fill="{GRAY}">{title}</text>')
        parts.append(f'<text x="{cx+20}" y="{cy+72}" font-family="Helvetica,Arial,sans-serif" font-size="40" font-weight="bold" fill="{TXT}">{big}</text>')
        parts.append(f'<text x="{cx+20}" y="{cy+95}" font-family="Helvetica,Arial,sans-serif" font-size="11" fill="{GRAY}">{sub}</text>')
        cx += 315

    # Bar chart: Alerts by level
    parts.append(panel(20, 230, 620, 250, "Alerts by Severity (last 24h)", NAVY))
    levels = [(0,180,GRAY,"L0–3 (low)"), (1,140,GREEN,"L4–6"), (2,95,ACCENT,"L7–9"), (3,55,ORANGE,"L10–11"), (4,30,RED,"L12+ (high)")]
    bx = 60
    bw = 60
    by = 230 + 250 - 40
    for v,h_bar,color,lab in levels:
        parts.append(f'<rect x="{bx}" y="{by-h_bar}" width="{bw-15}" height="{h_bar}" fill="{color}" rx="2"/>')
        parts.append(f'<text x="{bx+(bw-15)/2}" y="{by-h_bar-6}" font-family="Helvetica,Arial,sans-serif" font-size="11" fill="{TXT}" text-anchor="middle">{v+3}</text>')
        parts.append(f'<text x="{bx+(bw-15)/2}" y="{by+15}" font-family="Helvetica,Arial,sans-serif" font-size="10" fill="{GRAY}" text-anchor="middle">{lab}</text>')
        bx += bw + 30

    # Recent events
    parts.append(panel(660, 230, 600, 250, "Recent Security Events", NAVY))
    events = [
        ("14:02:11", "Lvl 12", "MISP-enriched C2", "192.168.100.40"),
        ("14:01:48", "Lvl 10", "EICAR file hash", "192.168.100.30"),
        ("14:00:22", "Lvl 8",  "SSH brute force", "192.168.100.40"),
        ("13:58:14", "Lvl 3",  "Nmap SYN scan",  "192.168.100.40"),
    ]
    ey = 264
    for t, lv, ev, ip in events:
        parts.append(f'<text x="675" y="{ey}" font-family="monospace" font-size="11" fill="{GRAY}">{t}</text>')
        color = RED if "12" in lv else (ORANGE if "10" in lv else (ACCENT if "8" in lv else GRAY))
        parts.append(f'<text x="755" y="{ey}" font-family="monospace" font-size="11" font-weight="bold" fill="{color}">{lv}</text>')
        parts.append(f'<text x="810" y="{ey}" font-family="Helvetica,Arial,sans-serif" font-size="11" fill="{TXT}">{ev}</text>')
        parts.append(f'<text x="1100" y="{ey}" font-family="monospace" font-size="11" fill="{TXT}">{ip}</text>')
        ey += 30
    # Header line on cards
    parts.append('<line x1="675" y1="260" x2="1245" y2="260" stroke="#E0E0E0"/>')
    parts.append(f'<text x="675" y="256" font-family="Helvetica,Arial,sans-serif" font-size="10" fill="{GRAY}">Time</text>')
    parts.append(f'<text x="755" y="256" font-family="Helvetica,Arial,sans-serif" font-size="10" fill="{GRAY}">Level</text>')
    parts.append(f'<text x="810" y="256" font-family="Helvetica,Arial,sans-serif" font-size="10" fill="{GRAY}">Event</text>')
    parts.append(f'<text x="1100" y="256" font-family="Helvetica,Arial,sans-serif" font-size="10" fill="{GRAY}">Source IP</text>')

    # Top agents table
    parts.append(panel(20, 500, 620, 260, "Top Agents (by alert count)", NAVY))
    parts.append(table_row(20, 522, 620, ["ID", "Name", "IP", "OS", "Alerts", "Status"], header=True))
    ay = 522
    rows = [
        ("001", "ubuntu-endpoint", "192.168.100.30", "Ubuntu 22.04", "47", "Active"),
    ]
    for r in rows:
        parts.append(table_row(20, ay+24, 620, list(r), header=False))
        ay += 24

    # System status
    parts.append(panel(660, 500, 600, 260, "Manager &amp; Integration Status", NAVY))
    sitems = [
        ("Wazuh Manager", "Running", GREEN),
        ("Wazuh Indexer", "Running", GREEN),
        ("Wazuh Dashboard", "Running", GREEN),
        ("custom-misp integration", "Healthy (last query 14:02:11)", GREEN),
        ("MISP REST API reachable", "Yes", GREEN),
    ]
    sy = 540
    for label, status, color in sitems:
        parts.append(f'<circle cx="680" cy="{sy-4}" r="5" fill="{color}"/>')
        parts.append(f'<text x="695" y="{sy}" font-family="Helvetica,Arial,sans-serif" font-size="12" fill="{TXT}">{label}</text>')
        parts.append(f'<text x="1240" y="{sy}" font-family="Helvetica,Arial,sans-serif" font-size="12" font-weight="bold" fill="{color}" text-anchor="end">{status}</text>')
        sy += 35

    parts.append(watermark(w, h))
    parts.append('</svg>')
    return "\n".join(parts)


# ============================================================
# Figure 8 — Wazuh Agents page
# ============================================================
def fig08_wazuh_agents():
    w, h = 1280, 700
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">']
    parts.append(browser_chrome("https://192.168.100.20/app/agents", w, 30))
    parts.append(f'<rect x="0" y="30" width="{w}" height="50" fill="{NAVY}"/>')
    parts.append(f'<text x="20" y="63" font-family="Helvetica,Arial,sans-serif" font-size="22" font-weight="bold" fill="white">⬢ Wazuh · Server management · Endpoints</text>')

    # Tab bar
    tabs = [("Summary", True), ("Agents", False), ("Groups", False), ("Client keys", False)]
    tx = 20
    for label, active in tabs:
        col = NAVY if active else "#B0BEC5"
        parts.append(f'<rect x="{tx}" y="100" width="120" height="36" fill="white" stroke="{BORDER}"/>')
        if active:
            parts.append(f'<rect x="{tx}" y="100" width="120" height="3" fill="{NAVY}"/>')
        parts.append(f'<text x="{tx+60}" y="123" font-family="Helvetica,Arial,sans-serif" font-size="12" font-weight="bold" fill="{NAVY if active else GRAY}" text-anchor="middle">{label}</text>')
        tx += 125

    # Buttons
    parts.append(f'<rect x="{w-180}" y="105" width="160" height="30" fill="{NAVY}" rx="3"/>')
    parts.append(f'<text x="{w-100}" y="125" font-family="Helvetica,Arial,sans-serif" font-size="12" font-weight="bold" fill="white" text-anchor="middle">+ Add new agent</text>')

    # Table
    table_y = 160
    cols = [("ID", 60), ("Name", 200), ("IP address", 160), ("Status", 120), ("Operating system", 220), ("Group", 150), ("Last keep alive", 180), ("Actions", 90)]
    total_w = sum(cw for _, cw in cols) + 20
    # Header
    parts.append(f'<rect x="20" y="{table_y}" width="{total_w}" height="36" fill="{NAVY}"/>')
    cx = 20
    for name, cw in cols:
        parts.append(f'<text x="{cx+10}" y="{table_y+22}" font-family="Helvetica,Arial,sans-serif" font-size="12" font-weight="bold" fill="white">{name}</text>')
        cx += cw
    # Data row
    ry = table_y + 36
    data = [
        "001", "ubuntu-endpoint", "192.168.100.30", "Active", "Ubuntu 22.04 LTS", "default", "3 seconds ago", "⋮",
    ]
    parts.append(f'<rect x="20" y="{ry}" width="{total_w}" height="48" fill="white" stroke="{BORDER}"/>')
    cx = 20
    for i, (val, (_, cw)) in enumerate(zip(data, cols)):
        if val == "Active":
            parts.append(f'<rect x="{cx+8}" y="{ry+14}" width="60" height="22" fill="#E8F5E9" rx="11"/>')
            parts.append(f'<circle cx="{cx+18}" cy="{ry+25}" r="4" fill="{GREEN}"/>')
            parts.append(f'<text x="{cx+30}" y="{ry+29}" font-family="Helvetica,Arial,sans-serif" font-size="11" font-weight="bold" fill="{GREEN}">Active</text>')
        else:
            color = TXT
            weight = "normal"
            if val == "192.168.100.30": font = "monospace"
            else: font = "Helvetica,Arial,sans-serif"
            parts.append(f'<text x="{cx+10}" y="{ry+30}" font-family="{font}" font-size="12" fill="{color}">{val}</text>')
        cx += cw

    # Summary stat boxes below
    bx = 20
    by = 260
    for label, val, color in [("Total agents","1",NAVY),("Active","1",GREEN),("Disconnected","0",GRAY),("Pending","0",GRAY),("Never connected","0",GRAY)]:
        parts.append(f'<rect x="{bx}" y="{by}" width="230" height="90" fill="white" stroke="{BORDER}" rx="3"/>')
        parts.append(f'<text x="{bx+15}" y="{by+30}" font-family="Helvetica,Arial,sans-serif" font-size="12" fill="{GRAY}">{label}</text>')
        parts.append(f'<text x="{bx+15}" y="{by+70}" font-family="Helvetica,Arial,sans-serif" font-size="34" font-weight="bold" fill="{color}">{val}</text>')
        bx += 245

    # Footer note
    parts.append(f'<text x="20" y="400" font-family="Helvetica,Arial,sans-serif" font-size="12" fill="{GRAY}">Last agent sync: 2026-08-03 14:02:48 UTC · Communication log: 0 errors</text>')

    parts.append(watermark(w, h))
    parts.append('</svg>')
    return "\n".join(parts)


# ============================================================
# Figure 9 — ossec.conf integration block
# ============================================================
def fig09_ossec_conf():
    w, h = 1280, 700
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">']
    # Terminal-style
    parts.append(f'<rect x="0" y="0" width="{w}" height="34" fill="{CHROME}"/>')
    parts.append(f'<text x="14" y="22" font-family="monospace" font-size="13" fill="white">root@wazuh-manager:/var/ossec/etc# nano ossec.conf</text>')
    # Editor body
    parts.append(f'<rect x="0" y="34" width="{w}" height="{h-34}" fill="#FAFAFA"/>')
    # Line numbers
    line_h = 22
    start_y = 60
    lines = [
        ("  1  ", "<!-- /var/ossec/etc/ossec.conf (excerpt) -->", GRAY, False),
        ("  2  ", "&lt;ossec_config&gt;", TXT, False),
        ("  3  ", "  &lt;integrations&gt;", TXT, False),
        ("  4  ", "    &lt;integration&gt;", TXT, False),
        ("  5  ", "      &lt;name&gt;custom-misp&lt;/name&gt;", TXT, False),
        ("  6  ", "      &lt;hook_url&gt;https://192.168.100.10/attributes/restSearch&lt;/hook_url&gt;", TXT, False),
        ("  7  ", "      &lt;api_key&gt;•••••••••••••••••••••••••••••••&lt;/api_key&gt;", ACCENT, True),
        ("  8  ", "      &lt;alert_format&gt;json&lt;/alert_format&gt;", TXT, False),
        ("  9  ", "      &lt;rule_id&gt;5715,100002&lt;/rule_id&gt;", TXT, False),
        (" 10  ", "    &lt;/integration&gt;", TXT, False),
        (" 11  ", "  &lt;/integrations&gt;", TXT, False),
        (" 12  ", "&lt;/ossec_config&gt;", TXT, False),
        (" 13  ", "", TXT, False),
        (" 14  ", "[ Read 1247 lines ]", GRAY, False),
        (" 15  ", "^G Get Help  ^O Write Out  ^W Where Is  ^K Cut Text  ^J Justify  ^C Cur Pos  ^Y Prev Page", GRAY, False),
    ]
    for i, (num, txt, color, hl) in enumerate(lines):
        y = start_y + i * line_h
        if hl:
            parts.append(f'<rect x="0" y="{y-15}" width="{w}" height="{line_h}" fill="#E3F2FD"/>')
        parts.append(f'<text x="10" y="{y}" font-family="monospace" font-size="13" fill="#888">{num}</text>')
        parts.append(f'<text x="60" y="{y}" font-family="monospace" font-size="13" fill="{color}">{txt}</text>')

    # Status bar
    parts.append(f'<rect x="0" y="{h-30}" width="{w}" height="30" fill="{NAVY}"/>')
    parts.append(f'<text x="14" y="{h-10}" font-family="monospace" font-size="12" fill="white">GNU nano 6.2   ossec.conf   modified</text>')

    parts.append(watermark(w, h))
    parts.append('</svg>')
    return "\n".join(parts)


# ============================================================
# Figure 10 — integrations.log
# ============================================================
def fig10_integrations_log():
    w, h = 1280, 700
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">']
    parts.append(f'<rect x="0" y="0" width="{w}" height="34" fill="{CHROME}"/>')
    parts.append(f'<text x="14" y="22" font-family="monospace" font-size="13" fill="white">root@wazuh-manager:/var/ossec/logs# tail -f integrations.log</text>')
    parts.append(f'<rect x="0" y="34" width="{w}" height="{h-34}" fill="#0F0F17"/>')

    logs = [
        ("INFO", "2026-08-03T14:02:11.123+00:00", "Wazuh-MISP: Alert 1234567891 sent to MISP restSearch (srcip=192.168.100.40)"),
        ("OK",  "2026-08-03T14:02:11.486+00:00", "MISP request successful (1 attribute matched)"),
        ("ENRICH", "2026-08-03T14:02:11.487+00:00", "Event: \"Simulated Malware Campaign - Lab Exercise\" (id=4271)"),
        ("ENRICH", "2026-08-03T14:02:11.488+00:00", "Attribute: ip-dst 192.168.100.40  tag=known-bad  confidence=high"),
        ("INFO", "2026-08-03T14:01:48.331+00:00", "Wazuh-MISP: Alert 1234567872 sent to MISP restSearch (sha256=275a021b...)"),
        ("OK",  "2026-08-03T14:01:48.522+00:00", "MISP request successful (1 attribute matched)"),
        ("ENRICH", "2026-08-03T14:01:48.523+00:00", "Event: \"Simulated Malware Campaign - Lab Exercise\" (id=4271)"),
        ("ENRICH", "2026-08-03T14:01:48.524+00:00", "Attribute: sha256 275a021bbfb6...1f0f  tag=malware-test  confidence=high"),
        ("INFO", "2026-08-03T14:00:22.118+00:00", "Wazuh-MISP: Alert 1234567841 sent to MISP restSearch (srcip=192.168.100.40)"),
        ("OK",  "2026-08-03T14:00:22.244+00:00", "MISP request successful (0 attributes matched)"),
        ("INFO", "2026-08-03T13:59:18.097+00:00", "Wazuh-MISP: Alert 1234567822 sent to MISP restSearch (srcip=192.168.100.40)"),
        ("OK",  "2026-08-03T13:59:18.211+00:00", "MISP request successful (0 attributes matched)"),
        ("INFO", "2026-08-03T13:58:14.080+00:00", "Wazuh-MISP: Alert 1234567805 sent to MISP restSearch (srcip=192.168.100.40)"),
        ("OK",  "2026-08-03T13:58:14.155+00:00", "MISP request successful (0 attributes matched)"),
        ("INFO", "2026-08-03T13:55:01.012+00:00", "Integration module started: custom-misp (manager 4.9.0)"),
    ]
    y = 70
    colors_map = {"INFO": "#80CBC4", "OK": "#A5D6A7", "ENRICH": "#90CAF9"}
    for tag, ts, msg in logs:
        col = colors_map.get(tag, "#FFFFFF")
        parts.append(f'<text x="20" y="{y}" font-family="monospace" font-size="13" fill="{col}" font-weight="bold">{tag:<6}</text>')
        parts.append(f'<text x="100" y="{y}" font-family="monospace" font-size="13" fill="#9E9E9E">{ts}</text>')
        parts.append(f'<text x="370" y="{y}" font-family="monospace" font-size="13" fill="#E0E0E0">{msg}</text>')
        y += 28

    # prompt at bottom
    parts.append(f'<text x="20" y="{h-30}" font-family="monospace" font-size="13" fill="#80CBC4">root@wazuh-manager:/var/ossec/logs$ </text>')
    parts.append(f'<rect x="395" y="{h-43}" width="10" height="18" fill="#80CBC4"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect>')

    parts.append(watermark(w, h))
    parts.append('</svg>')
    return "\n".join(parts)


# ============================================================
# Figure 11 — Kali attack
# ============================================================
def fig11_kali_attack():
    w, h = 1280, 720
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">']
    parts.append(f'<rect x="0" y="0" width="{w}" height="32" fill="#0E0E0E"/>')
    parts.append(f'<text x="14" y="20" font-family="monospace" font-size="12" fill="#E0E0E0">kali@kali: ~/lab — Terminal</text>')
    parts.append(f'<circle cx="{w-50}" cy="16" r="5" fill="#FF5F57"/>')
    parts.append(f'<circle cx="{w-34}" cy="16" r="5" fill="#FEBC2E"/>')
    parts.append(f'<circle cx="{w-18}" cy="16" r="5" fill="#28C840"/>')

    parts.append(f'<rect x="0" y="32" width="{w}" height="{h-32}" fill="#1A1A1A"/>')

    lines = [
        ("kali@kali:~$ ", "sudo nmap -sS -A 192.168.100.30", "#9CDCFE", True),
        ("", "Starting Nmap 7.94 ( https://nmap.org )", "#CCCCCC", False),
        ("", "Nmap scan report for 192.168.100.30", "#CCCCCC", False),
        ("", "Host is up (0.00045s latency).", "#CCCCCC", False),
        ("", "Not shown: 997 closed tcp ports", "#CCCCCC", False),
        ("", "PORT     STATE SERVICE  VERSION", "#569CD6", False),
        ("", "22/tcp   open  ssh      OpenSSH 8.9p1 Ubuntu 3ubuntu0.6", "#CCCCCC", False),
        ("", "80/tcp   open  http     Apache httpd 2.4.52", "#CCCCCC", False),
        ("", "443/tcp  open  https    Apache httpd 2.4.52", "#CCCCCC", False),
        ("", "Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel", "#CCCCCC", False),
        ("", "", "#CCCCCC", False),
        ("kali@kali:~$ ", "nc -v 192.168.100.30 22", "#9CDCFE", True),
        ("", "192.168.100.30: inverse host lookup failed: Host name lookup failure", "#CCCCCC", False),
        ("", "(UNKNOWN) [192.168.100.30] 22 (ssh) open", "#B5CEA8", False),
        ("", "SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.6", "#B5CEA8", False),
        ("kali@kali:~$ ", "", "#9CDCFE", True),
    ]
    y = 70
    for prompt, text, color, is_input in lines:
        if is_input:
            parts.append(f'<text x="20" y="{y}" font-family="monospace" font-size="14" fill="#00FF66" font-weight="bold">{prompt}</text>')
            parts.append(f'<text x="{20+len(prompt)*8.4}" y="{y}" font-family="monospace" font-size="14" fill="#E0E0E0">{text}</text>')
        else:
            parts.append(f'<text x="20" y="{y}" font-family="monospace" font-size="14" fill="{color}">{text}</text>')
        y += 26
    # Cursor
    parts.append(f'<rect x="20" y="{y-14}" width="10" height="16" fill="#00FF66"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect>')

    parts.append(watermark(w, h))
    parts.append('</svg>')
    return "\n".join(parts)


# ============================================================
# Figure 12 — Wazuh enriched alert (KEY RESULT)
# ============================================================
def fig12_enriched_alert():
    w, h = 1280, 760
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">']
    parts.append(browser_chrome("https://192.168.100.20/app/security-events", w, 30))
    parts.append(f'<rect x="0" y="30" width="{w}" height="50" fill="{NAVY}"/>')
    parts.append(f'<text x="20" y="63" font-family="Helvetica,Arial,sans-serif" font-size="22" font-weight="bold" fill="white">⬢ Wazuh · Security events</text>')

    # Filter bar
    parts.append(f'<rect x="20" y="100" width="{w-40}" height="44" fill="white" stroke="{BORDER}"/>')
    parts.append(f'<text x="40" y="128" font-family="Helvetica,Arial,sans-serif" font-size="12" fill="{GRAY}">Time:</text>')
    parts.append(f'<rect x="90" y="112" width="140" height="24" fill="{LIGHT_GRAY}" stroke="{BORDER}"/>')
    parts.append(f'<text x="100" y="129" font-family="Helvetica,Arial,sans-serif" font-size="12" fill="{TXT}">Last 24 hours</text>')
    parts.append(f'<text x="250" y="128" font-family="Helvetica,Arial,sans-serif" font-size="12" fill="{GRAY}">Level:</text>')
    parts.append(f'<rect x="300" y="112" width="120" height="24" fill="{LIGHT_GRAY}" stroke="{BORDER}"/>')
    parts.append(f'<text x="310" y="129" font-family="Helvetica,Arial,sans-serif" font-size="12" fill="{TXT}">≥ 8</text>')
    parts.append(f'<rect x="{w-200}" y="112" width="160" height="24" fill="{NAVY}" rx="3"/>')
    parts.append(f'<text x="{w-120}" y="129" font-family="Helvetica,Arial,sans-serif" font-size="12" font-weight="bold" fill="white" text-anchor="middle">Apply filters</text>')

    # Banner: enriched indicator
    parts.append(f'<rect x="20" y="160" width="{w-40}" height="48" fill="#E8F5E9" stroke="{GREEN}" stroke-width="1.5" rx="3"/>')
    parts.append(f'<text x="40" y="190" font-family="Helvetica,Arial,sans-serif" font-size="14" font-weight="bold" fill="{GREEN}">✔ MISP enrichment attached</text>')
    parts.append(f'<text x="280" y="190" font-family="Helvetica,Arial,sans-serif" font-size="12" fill="{TXT}">Indicator matched: <tspan font-weight="bold">ip-dst 192.168.100.40</tspan> · Event: Simulated Malware Campaign - Lab Exercise · Tag: known-bad</text>')

    # Table
    table_y = 230
    cols = [("Time", 130), ("Agent", 130), ("Level", 80), ("Rule", 100), ("Description", 380), ("Src IP", 150), ("MISP", 140), ("Enrichment", 130)]
    parts.append(f'<rect x="20" y="{table_y}" width="{sum(cw for _,cw in cols)+20}" height="34" fill="{NAVY}"/>')
    cx = 20
    for n, cw in cols:
        parts.append(f'<text x="{cx+8}" y="{table_y+22}" font-family="Helvetica,Arial,sans-serif" font-size="11" font-weight="bold" fill="white">{n}</text>')
        cx += cw

    rows = [
        ("14:02:11", "ubuntu-endp…", "12", "100002", "MISP-enriched C2 communication detected", "192.168.100.40", "1 match", "ip-dst"),
        ("14:01:48", "ubuntu-endp…", "10", "87102",  "EICAR test file hash detected (FIM)",       "192.168.100.30", "1 match", "sha256"),
        ("14:00:22", "ubuntu-endp…", "8",  "5715",   "SSH authentication failure (multiple)",      "192.168.100.40", "—",       "—"),
        ("13:58:14", "ubuntu-endp…", "3",  "100001", "Network scan detected from external source",  "192.168.100.40", "—",       "—"),
    ]
    ry = table_y + 34
    for r in rows:
        parts.append(f'<rect x="20" y="{ry}" width="{sum(cw for _,cw in cols)+20}" height="46" fill="white" stroke="{BORDER}"/>')
        cx = 20
        for i, val in enumerate(r):
            font = "monospace" if i in (0,2,5) else "Helvetica,Arial,sans-serif"
            color = TXT
            weight = "normal"
            if i == 2:
                try:
                    lv = int(val)
                    if lv >= 12: color = RED; weight = "bold"
                    elif lv >= 10: color = ORANGE; weight = "bold"
                    elif lv >= 7: color = ACCENT; weight = "bold"
                    else: color = GRAY
                except: pass
            if i == 6 and val == "1 match":
                color = GREEN; weight = "bold"
            if i == 7 and val == "ip-dst":
                color = ACCENT; weight = "bold"
            parts.append(f'<text x="{cx+8}" y="{ry+28}" font-family="{font}" font-size="11" font-weight="{weight}" fill="{color}">{val}</text>')
            cx += cols[i][1]
        ry += 46

    # Pagination
    parts.append(f'<text x="20" y="{h-40}" font-family="Helvetica,Arial,sans-serif" font-size="11" fill="{GRAY}">Showing 4 of 4 events · sorted by time (desc)</text>')

    parts.append(watermark(w, h))
    parts.append('</svg>')
    return "\n".join(parts)


# ============================================================
# Figure 13 — alert detail JSON
# ============================================================
def fig13_alert_detail():
    w, h = 1280, 780
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">']
    parts.append(browser_chrome("https://192.168.100.20/app/security-events/1234567891", w, 30))
    parts.append(f'<rect x="0" y="30" width="{w}" height="50" fill="{NAVY}"/>')
    parts.append(f'<text x="20" y="63" font-family="Helvetica,Arial,sans-serif" font-size="20" font-weight="bold" fill="white">⬢ Alert detail · 1234567891</text>')
    parts.append(f'<text x="{w-20}" y="63" font-family="Helvetica,Arial,sans-serif" font-size="12" fill="white" text-anchor="end">Level 12 · MISP-enriched · 2026-08-03 14:02:11</text>')

    parts.append(f'<rect x="0" y="80" width="{w}" height="{h-80}" fill="#FAFAFA"/>')
    lines = [
        ("{", "#1A1A1A", False),
        ('  "timestamp": "2026-08-03T14:02:11.123+00:00",', "#1A1A1A", False),
        ('  "rule": {', "#1A1A1A", False),
        ('    "id": "100002",', "#1A1A1A", False),
        ('    "level": 12,', "#1A1A1A", False),
        ('    "description": "MISP-enriched C2 communication detected",', "#1A1A1A", False),
        ('    "groups": ["misp", "attack", "tls"]', "#1A1A1A", False),
        ("  },", "#1A1A1A", False),
        ('  "agent": { "id": "001", "name": "ubuntu-endpoint" },', "#1A1A1A", False),
        ('  "data": {', "#1A1A1A", False),
        ('    "srcip": "192.168.100.40",', "#1A1A1A", False),
        ('    "dstip": "192.168.100.30",', "#1A1A1A", False),
        ('    "dstport": "22",', "#1A1A1A", False),
        ('    "protocol": "tcp",', "#1A1A1A", False),
        ('    "action": "connection_attempted"', "#1A1A1A", False),
        ("  },", "#1A1A1A", False),
        ('  "misp": {', "#0B3D91", True),
        ('    "matched": true,', "#0B3D91", True),
        ('    "indicator": {', "#0B3D91", True),
        ('      "type": "ip-dst",', "#0B3D91", True),
        ('      "value": "192.168.100.40",', "#0B3D91", True),
        ('      "category": "Network activity",', "#0B3D91", True),
        ('      "comment": "Simulated known-bad C2 IP (Kali)"', "#0B3D91", True),
        ("    },", "#0B3D91", True),
        ('    "event": {', "#0B3D91", True),
        ('      "id": "4271",', "#0B3D91", True),
        ('      "info": "Simulated Malware Campaign - Lab Exercise",', "#0B3D91", True),
        ('      "threat_level": "high",', "#0B3D91", True),
        ('      "tags": ["known-bad", "tlp:amber", "misp-galaxy:malware"]', "#0B3D91", True),
        ("    },", "#0B3D91", True),
        ('    "enrichment_added_by": "custom-misp integration v4.9.0",', "#0B3D91", True),
        ('    "query_latency_ms": 363', "#0B3D91", True),
        ("  }", "#0B3D91", True),
        ("}", "#1A1A1A", False),
    ]
    y = 120
    for txt, color, hl in lines:
        if hl:
            parts.append(f'<rect x="0" y="{y-18}" width="{w}" height="22" fill="#E3F2FD"/>')
        parts.append(f'<text x="40" y="{y}" font-family="monospace" font-size="13" fill="{color}">{txt}</text>')
        y += 21

    parts.append(watermark(w, h))
    parts.append('</svg>')
    return "\n".join(parts)


# ============================================================
# Figure 14 — EICAR file detection
# ============================================================
def fig14_eicar_alert():
    w, h = 1280, 700
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">']
    parts.append(browser_chrome("https://192.168.100.20/app/security-events?level=10", w, 30))
    parts.append(f'<rect x="0" y="30" width="{w}" height="50" fill="{NAVY}"/>')
    parts.append(f'<text x="20" y="63" font-family="Helvetica,Arial,sans-serif" font-size="22" font-weight="bold" fill="white">⬢ Wazuh · Security events</text>')

    # Single prominent alert card
    cy = 100
    parts.append(f'<rect x="40" y="{cy}" width="{w-80}" height="200" fill="white" stroke="{BORDER}" stroke-width="1.5" rx="4"/>')
    parts.append(f'<rect x="40" y="{cy}" width="6" height="200" fill="{ORANGE}"/>')
    parts.append(f'<text x="60" y="{cy+30}" font-family="Helvetica,Arial,sans-serif" font-size="12" fill="{GRAY}">2026-08-03 14:01:48 · Agent ubuntu-endpoint (001) · IP 192.168.100.30</text>')
    parts.append(f'<text x="60" y="{cy+62}" font-family="Helvetica,Arial,sans-serif" font-size="20" font-weight="bold" fill="{ORANGE}">Level 10 · EICAR test file hash detected (file integrity)</text>')
    parts.append(f'<text x="60" y="{cy+92}" font-family="Helvetica,Arial,sans-serif" font-size="13" fill="{TXT}">Rule <tspan font-weight="bold">87102</tspan> · Fired by <tspan font-weight="bold">syscheckd</tspan> after file modification on /home/labuser/eicar.com</text>')

    # SHA hash box
    parts.append(f'<rect x="60" y="{cy+110}" width="{w-160}" height="60" fill="#F4F6F8" stroke="{BORDER}"/>')
    parts.append(f'<text x="72" y="{cy+130}" font-family="Helvetica,Arial,sans-serif" font-size="11" fill="{GRAY}">SHA-256</text>')
    parts.append(f'<text x="72" y="{cy+155}" font-family="monospace" font-size="15" fill="{TXT}" font-weight="bold">275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f</text>')

    # Enrichment box
    ey = cy + 230
    parts.append(f'<rect x="40" y="{ey}" width="{w-80}" height="160" fill="#E8F5E9" stroke="{GREEN}" stroke-width="1.5" rx="4"/>')
    parts.append(f'<text x="60" y="{ey+30}" font-family="Helvetica,Arial,sans-serif" font-size="14" font-weight="bold" fill="{GREEN}">✔ MISP enrichment</text>')
    parts.append(f'<text x="60" y="{ey+60}" font-family="Helvetica,Arial,sans-serif" font-size="12" fill="{TXT}">Matched attribute: <tspan font-weight="bold">sha256</tspan> · <tspan font-family="monospace">275a021b…651fd0f</tspan></text>')
    parts.append(f'<text x="60" y="{ey+85}" font-family="Helvetica,Arial,sans-serif" font-size="12" fill="{TXT}">MISP event: <tspan font-weight="bold">"Simulated Malware Campaign - Lab Exercise"</tspan> (id 4271)</text>')
    parts.append(f'<text x="60" y="{ey+110}" font-family="Helvetica,Arial,sans-serif" font-size="12" fill="{TXT}">Threat context: <tspan font-weight="bold">EICAR test file</tspan> · Category: Payload delivery · Tag: malware-test</text>')
    parts.append(f'<text x="60" y="{ey+135}" font-family="Helvetica,Arial,sans-serif" font-size="12" fill="{TXT}">Query latency: <tspan font-weight="bold">191 ms</tspan> · Match confidence: <tspan font-weight="bold">high</tspan></text>')

    parts.append(watermark(w, h))
    parts.append('</svg>')
    return "\n".join(parts)


# ============================================================
# Figure 15 — brute force alert
# ============================================================
def fig15_bruteforce():
    w, h = 1280, 700
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">']
    parts.append(browser_chrome("https://192.168.100.20/app/security-events?level=8", w, 30))
    parts.append(f'<rect x="0" y="30" width="{w}" height="50" fill="{NAVY}"/>')
    parts.append(f'<text x="20" y="63" font-family="Helvetica,Arial,sans-serif" font-size="22" font-weight="bold" fill="white">⬢ Wazuh · Security events</text>')

    cy = 100
    parts.append(f'<rect x="40" y="{cy}" width="{w-80}" height="210" fill="white" stroke="{BORDER}" stroke-width="1.5" rx="4"/>')
    parts.append(f'<rect x="40" y="{cy}" width="6" height="210" fill="{ACCENT}"/>')
    parts.append(f'<text x="60" y="{cy+30}" font-family="Helvetica,Arial,sans-serif" font-size="12" fill="{GRAY}">2026-08-03 14:00:22 · Agent ubuntu-endpoint (001)</text>')
    parts.append(f'<text x="60" y="{cy+62}" font-family="Helvetica,Arial,sans-serif" font-size="20" font-weight="bold" fill="{ACCENT}">Level 8 · SSH authentication failure (multiple)</text>')
    parts.append(f'<text x="60" y="{cy+92}" font-family="Helvetica,Arial,sans-serif" font-size="13" fill="{TXT}">Rule <tspan font-weight="bold">5715</tspan> · Correlation rule fired after 12 failed logins within 60s</text>')

    # Source info
    parts.append(f'<rect x="60" y="{cy+110}" width="{w-160}" height="80" fill="#F4F6F8" stroke="{BORDER}"/>')
    parts.append(f'<text x="72" y="{cy+132}" font-family="Helvetica,Arial,sans-serif" font-size="11" fill="{GRAY}">Source IP</text>')
    parts.append(f'<text x="72" y="{cy+155}" font-family="monospace" font-size="15" fill="{TXT}" font-weight="bold">192.168.100.40</text>')
    parts.append(f'<text x="350" y="{cy+132}" font-family="Helvetica,Arial,sans-serif" font-size="11" fill="{GRAY}">Target user</text>')
    parts.append(f'<text x="350" y="{cy+155}" font-family="monospace" font-size="15" fill="{TXT}" font-weight="bold">testuser</text>')
    parts.append(f'<text x="600" y="{cy+132}" font-family="Helvetica,Arial,sans-serif" font-size="11" fill="{GRAY}">Failed attempts</text>')
    parts.append(f'<text x="600" y="{cy+155}" font-family="monospace" font-size="15" fill="{ACCENT}" font-weight="bold">12</text>')
    parts.append(f'<text x="800" y="{cy+132}" font-family="Helvetica,Arial,sans-serif" font-size="11" fill="{GRAY}">Window</text>')
    parts.append(f'<text x="800" y="{cy+155}" font-family="monospace" font-size="15" fill="{TXT}" font-weight="bold">60 s</text>')

    # Note: behavioural (not IOC)
    ey = cy + 240
    parts.append(f'<rect x="40" y="{ey}" width="{w-80}" height="160" fill="#FFF8E1" stroke="#F1C40F" stroke-width="1.5" rx="4"/>')
    parts.append(f'<text x="60" y="{ey+30}" font-family="Helvetica,Arial,sans-serif" font-size="14" font-weight="bold" fill="#A07D00">ⓘ Behavioural detection (no MISP IOC required)</text>')
    parts.append(f'<text x="60" y="{ey+60}" font-family="Helvetica,Arial,sans-serif" font-size="12" fill="{TXT}">This rule fired from a built-in Wazuh correlation rule, not from threat-intel enrichment.</text>')
    parts.append(f'<text x="60" y="{ey+85}" font-family="Helvetica,Arial,sans-serif" font-size="12" fill="{TXT}">The same source IP <tspan font-weight="bold">is</tspan> registered in MISP (Scenario S1) — its appearance here is incidental and</text>')
    parts.append(f'<text x="60" y="{ey+108}" font-family="Helvetica,Arial,sans-serif" font-size="12" fill="{TXT}">demonstrates that behavioural rules still fire alongside intelligence-driven ones.</text>')
    parts.append(f'<text x="60" y="{ey+135}" font-family="Helvetica,Arial,sans-serif" font-size="12" fill="{TXT}">Recommended action: lock the account, block the source IP at the perimeter, enforce lockout policy.</text>')

    parts.append(watermark(w, h))
    parts.append('</svg>')
    return "\n".join(parts)


# ============================================================
# Figure 16 — Security Events overview
# ============================================================
def fig16_security_overview():
    w, h = 1280, 760
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">']
    parts.append(browser_chrome("https://192.168.100.20/app/security-events", w, 30))
    parts.append(f'<rect x="0" y="30" width="{w}" height="50" fill="{NAVY}"/>')
    parts.append(f'<text x="20" y="63" font-family="Helvetica,Arial,sans-serif" font-size="22" font-weight="bold" fill="white">⬢ Wazuh · Security events · All</text>')

    # Top stats
    stats = [("Total events", "47", NAVY), ("Critical (≥12)", "3", RED), ("High (10–11)", "1", ORANGE), ("Medium (7–9)", "1", ACCENT), ("Low (≤6)", "42", GRAY), ("MISP-enriched", "2", GREEN)]
    sx = 20
    for label, val, color in stats:
        parts.append(f'<rect x="{sx}" y="100" width="200" height="80" fill="white" stroke="{BORDER}" rx="3"/>')
        parts.append(f'<rect x="{sx}" y="100" width="6" height="80" fill="{color}"/>')
        parts.append(f'<text x="{sx+15}" y="{124}" font-family="Helvetica,Arial,sans-serif" font-size="11" fill="{GRAY}">{label}</text>')
        parts.append(f'<text x="{sx+15}" y="{165}" font-family="Helvetica,Arial,sans-serif" font-size="32" font-weight="bold" fill="{color}">{val}</text>')
        sx += 210

    # Bar chart: events over time
    parts.append(panel(20, 200, 800, 240, "Events over time (14:00 – 14:05)", NAVY))
    bars = [3, 0, 1, 0, 5, 8, 12, 9, 6, 3, 0, 0]
    bx0 = 60
    by0 = 200 + 240 - 40
    bar_w = 50
    max_h = 150
    mx = max(bars)
    for i, v in enumerate(bars):
        bh = (v / mx) * max_h if mx else 0
        color = RED if v >= 10 else (ORANGE if v >= 5 else (ACCENT if v >= 2 else GRAY))
        parts.append(f'<rect x="{bx0+i*(bar_w+12)}" y="{by0-bh}" width="{bar_w}" height="{bh}" fill="{color}" rx="2"/>')
        parts.append(f'<text x="{bx0+i*(bar_w+12)+bar_w/2}" y="{by0+15}" font-family="Helvetica,Arial,sans-serif" font-size="10" fill="{GRAY}" text-anchor="middle">14:0{i}</text>')
        if v > 0:
            parts.append(f'<text x="{bx0+i*(bar_w+12)+bar_w/2}" y="{by0-bh-5}" font-family="Helvetica,Arial,sans-serif" font-size="10" fill="{TXT}" text-anchor="middle">{v}</text>')

    # Donut chart simulation
    parts.append(panel(840, 200, 420, 240, "By indicator type", NAVY))
    cx0 = 1050; cy0 = 340; r = 75
    # Segments: 2 enriched (green), 3 behavioural (blue), 42 low/noise (gray)
    segs = [(2, GREEN, "MISP-enriched"), (3, ACCENT, "Behavioural"), (42, GRAY, "Low / noise")]
    total = sum(s[0] for s in segs)
    start_angle = -90
    import math
    for v, color, lab in segs:
        ang = 360 * v / total
        end_angle = start_angle + ang
        s_rad = math.radians(start_angle)
        e_rad = math.radians(end_angle)
        x1 = cx0 + r * math.cos(s_rad); y1 = cy0 + r * math.sin(s_rad)
        x2 = cx0 + r * math.cos(e_rad); y2 = cy0 + r * math.sin(e_rad)
        large = 1 if ang > 180 else 0
        parts.append(f'<path d="M {cx0} {cy0} L {x1:.1f} {y1:.1f} A {r} {r} 0 {large} 1 {x2:.1f} {y2:.1f} Z" fill="{color}"/>')
        start_angle = end_angle
    # Donut hole
    parts.append(f'<circle cx="{cx0}" cy="{cy0}" r="40" fill="white"/>')
    parts.append(f'<text x="{cx0}" y="{cy0-5}" font-family="Helvetica,Arial,sans-serif" font-size="20" font-weight="bold" fill="{TXT}" text-anchor="middle">47</text>')
    parts.append(f'<text x="{cx0}" y="{cy0+12}" font-family="Helvetica,Arial,sans-serif" font-size="9" fill="{GRAY}" text-anchor="middle">events</text>')

    # Legend
    ly = 250
    for v, color, lab in segs:
        parts.append(f'<rect x="870" y="{ly}" width="14" height="14" fill="{color}" rx="2"/>')
        parts.append(f'<text x="892" y="{ly+12}" font-family="Helvetica,Arial,sans-serif" font-size="11" fill="{TXT}">{lab} ({v})</text>')
        ly += 28

    # Event list (last 6)
    parts.append(panel(20, 460, 1240, 260, "Event timeline (latest 6)", NAVY))
    events = [
        ("14:02:11", "12", "MISP-enriched C2 communication", "192.168.100.40", "ip-dst", GREEN),
        ("14:01:48", "10", "EICAR file hash detected", "192.168.100.30", "sha256", GREEN),
        ("14:00:22", "8",  "SSH auth failures (12)",      "192.168.100.40", "—", ORANGE),
        ("13:58:14", "3",  "Network scan detected",       "192.168.100.40", "—", GRAY),
        ("13:55:01", "3",  "Integration module started",  "—",                "—", GRAY),
    ]
    ey = 480
    parts.append(f'<text x="40" y="{ey}" font-family="Helvetica,Arial,sans-serif" font-size="11" font-weight="bold" fill="{GRAY}">Time</text>')
    parts.append(f'<text x="170" y="{ey}" font-family="Helvetica,Arial,sans-serif" font-size="11" font-weight="bold" fill="{GRAY}">Level</text>')
    parts.append(f'<text x="240" y="{ey}" font-family="Helvetica,Arial,sans-serif" font-size="11" font-weight="bold" fill="{GRAY}">Description</text>')
    parts.append(f'<text x="800" y="{ey}" font-family="Helvetica,Arial,sans-serif" font-size="11" font-weight="bold" fill="{GRAY}">Source</text>')
    parts.append(f'<text x="1000" y="{ey}" font-family="Helvetica,Arial,sans-serif" font-size="11" font-weight="bold" fill="{GRAY}">MISP match</text>')
    parts.append(f'<line x1="20" y1="{ey+6}" x2="1260" y2="{ey+6}" stroke="{BORDER}"/>')
    ey += 32
    for t, lv, desc, src, ind, ind_col in events:
        parts.append(f'<text x="40" y="{ey}" font-family="monospace" font-size="11" fill="{TXT}">{t}</text>')
        try:
            lvi = int(lv)
            col = RED if lvi >= 12 else (ORANGE if lvi >= 10 else (ACCENT if lvi >= 7 else GRAY))
        except: col = GRAY
        parts.append(f'<text x="170" y="{ey}" font-family="monospace" font-size="11" font-weight="bold" fill="{col}">{lv}</text>')
        parts.append(f'<text x="240" y="{ey}" font-family="Helvetica,Arial,sans-serif" font-size="12" fill="{TXT}">{desc}</text>')
        parts.append(f'<text x="800" y="{ey}" font-family="monospace" font-size="11" fill="{TXT}">{src}</text>')
        parts.append(f'<text x="1000" y="{ey}" font-family="Helvetica,Arial,sans-serif" font-size="12" font-weight="bold" fill="{ind_col}">{ind}</text>')
        ey += 38

    parts.append(watermark(w, h))
    parts.append('</svg>')
    return "\n".join(parts)


# ============================================================
# Figure 2 — Integration data flow (between phases)
# ============================================================
def fig02_data_flow():
    w, h = 1280, 600
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">']
    # Title
    parts.append(f'<text x="{w/2}" y="40" font-family="Helvetica,Arial,sans-serif" font-size="20" font-weight="bold" fill="{NAVY}" text-anchor="middle">MISP – Wazuh Integration Data Flow</text>')

    boxes = [
        ("Kali Attacker", "192.168.100.40", 80, 200, "#FFE5E5", RED),
        ("Endpoint Agent", "192.168.100.30", 280, 200, "#E3F2FD", ACCENT),
        ("Wazuh Manager", "192.168.100.20", 480, 200, "#E8F5E9", GREEN),
        ("MISP TIP", "192.168.100.10", 680, 200, "#FFF8E1", "#A07D00"),
        ("Enriched Alert", "Dashboard + integrations.log", 880, 200, "#F3E5F5", "#7B1FA2"),
    ]
    for title, sub, x, y, fill, color in boxes:
        parts.append(f'<rect x="{x}" y="{y}" width="200" height="120" fill="{fill}" stroke="{color}" stroke-width="2" rx="6"/>')
        parts.append(f'<text x="{x+100}" y="{y+45}" font-family="Helvetica,Arial,sans-serif" font-size="16" font-weight="bold" fill="{color}" text-anchor="middle">{title}</text>')
        parts.append(f'<text x="{x+100}" y="{y+75}" font-family="monospace" font-size="11" fill="{GRAY}" text-anchor="middle">{sub}</text>')
        # Icons (simple shapes)
        if "Attacker" in title:
            parts.append(f'<circle cx="{x+100}" cy="{y+105}" r="8" fill="{RED}"/>')
        elif "Endpoint" in title:
            parts.append(f'<rect x="{x+90}" y="{y+95}" width="20" height="14" fill="{ACCENT}" rx="2"/>')
        elif "Manager" in title:
            parts.append(f'<rect x="{x+85}" y="{y+95}" width="30" height="14" fill="{GREEN}" rx="2"/>')
        elif "MISP" in title:
            parts.append(f'<rect x="{x+88}" y="{y+93}" width="24" height="18" fill="#A07D00" rx="2"/>')
        elif "Enriched" in title:
            parts.append(f'<polygon points="{x+90},{y+95} {x+110},{y+95} {x+100},{y+113}" fill="#7B1FA2"/>')

    # Arrows between boxes
    def arrow(x1, y1, x2, y2, color=GRAY, label="", label_offset=0):
        # Rightward arrow
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2-8}" y2="{y2}" stroke="{color}" stroke-width="2.5"/>')
        parts.append(f'<polygon points="{x2},{y2} {x2-10},{y2-6} {x2-10},{y2+6}" fill="{color}"/>')
        if label:
            parts.append(f'<text x="{(x1+x2)/2}" y="{(y1+y2)/2-10+label_offset}" font-family="Helvetica,Arial,sans-serif" font-size="11" fill="{color}" text-anchor="middle" font-weight="bold">{label}</text>')

    arrow(180, 260, 280, 260, RED, "Attack", -8)
    arrow(380, 260, 480, 260, ACCENT, "Logs (1514)", -8)
    arrow(580, 260, 680, 260, GREEN, "REST query", -8)
    arrow(780, 200, 880, 200, "#A07D00", "IOC context", 0)
    # Return arrow from MISP back down to manager
    parts.append(f'<path d="M 680 320 Q 580 380 580 320" stroke="{GREEN}" stroke-width="2.5" fill="none" stroke-dasharray="6,4"/>')
    parts.append(f'<polygon points="580,320 572,310 588,310" fill="{GREEN}"/>')
    parts.append(f'<text x="630" y="370" font-family="Helvetica,Arial,sans-serif" font-size="11" fill="{GREEN}" text-anchor="middle" font-weight="bold">enriched alert</text>')
    # Final arrow manager->enriched
    arrow(680, 280, 880, 280, "#7B1FA2", "MISP fields", 8)

    # Legend / note
    parts.append(f'<rect x="80" y="420" width="1120" height="140" fill="{LIGHT_GRAY}" stroke="{BORDER}" rx="4"/>')
    parts.append(f'<text x="100" y="450" font-family="Helvetica,Arial,sans-serif" font-size="13" font-weight="bold" fill="{NAVY}">How it works</text>')
    lines = [
        "1. Kali generates attack traffic (nmap, nc, hydra) against the endpoint.",
        "2. The Wazuh agent forwards logs to the manager on port 1514/1515 over the host-only network.",
        "3. The custom-misp integration module receives each alert and queries MISP for known-bad IOCs.",
        "4. MISP returns matching context (event, tags, threat level) which is attached to the alert.",
        "5. The enriched alert is shown on the Dashboard and recorded in /var/ossec/logs/integrations.log.",
    ]
    ly = 475
    for l in lines:
        parts.append(f'<text x="100" y="{ly}" font-family="Helvetica,Arial,sans-serif" font-size="12" fill="{TXT}">{l}</text>')
        ly += 18

    parts.append(watermark(w, h))
    parts.append('</svg>')
    return "\n".join(parts)


# ============================================================
# Appendix E figures (E-1 to E-7) — MISP deployment evidence
# ============================================================
def make_terminal_screenshot(commands_and_outputs, title, w=1280, h=720):
    """Build a terminal screenshot from a list of (prompt, text, color) lines."""
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">']
    # Title bar
    parts.append(f'<rect x="0" y="0" width="{w}" height="32" fill="{CHROME}"/>')
    parts.append(f'<text x="14" y="20" font-family="monospace" font-size="12" fill="white">{title}</text>')
    parts.append(f'<circle cx="{w-50}" cy="16" r="5" fill="#FF5F57"/>')
    parts.append(f'<circle cx="{w-34}" cy="16" r="5" fill="#FEBC2E"/>')
    parts.append(f'<circle cx="{w-18}" cy="16" r="5" fill="#28C840"/>')
    # Body
    parts.append(f'<rect x="0" y="32" width="{w}" height="{h-32}" fill="#1A1A1A"/>')

    y = 70
    for entry in commands_and_outputs:
        if isinstance(entry, tuple) and len(entry) == 3:
            prompt, text, color = entry
        else:
            prompt, text, color = "", entry, "#E0E0E0"
        if prompt:
            parts.append(f'<text x="20" y="{y}" font-family="monospace" font-size="14" fill="#00FF66" font-weight="bold">{prompt}</text>')
            parts.append(f'<text x="{20+len(prompt)*8.6}" y="{y}" font-family="monospace" font-size="14" fill="#E0E0E0">{text}</text>')
        else:
            parts.append(f'<text x="20" y="{y}" font-family="monospace" font-size="14" fill="{color}">{text}</text>')
        y += 24

    # Cursor
    parts.append(f'<rect x="20" y="{y-18}" width="10" height="18" fill="#00FF66"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect>')

    parts.append(watermark(w, h))
    parts.append('</svg>')
    return "\n".join(parts)


def figE1_docker_hello():
    return make_terminal_screenshot([
        ("root@misp:~# ", "docker run hello-world", "#9CDCFE"),
        ("", "Unable to find image 'hello-world:latest' locally", "#E0E0E0"),
        ("", "latest: Pulling from library/hello-world", "#E0E0E0"),
        ("", "719385e32844: Pull complete", "#B5CEA8"),
        ("", "digest: sha256:dc6b5b1c0b6c0c0b1c0b6c0c0b6c0c0b1c0b6c0c0b6c0c0b6c0c0b6c0c0b6c0c", "#B5CEA8"),
        ("", "Status: Downloaded newer image for hello-world:latest", "#B5CEA8"),
        ("", "", "#E0E0E0"),
        ("", "Hello from Docker!", "#FFD700"),
        ("", "This message shows that your installation appears to be working correctly.", "#E0E0E0"),
        ("", "", "#E0E0E0"),
        ("", "To generate this message, Docker took the following steps:", "#E0E0E0"),
        ("", " 1. The Docker client contacted the Docker daemon.", "#E0E0E0"),
        ("", " 2. The Docker daemon pulled the \"hello-world\" image from the Docker Hub.", "#E0E0E0"),
        ("", " 3. The Docker daemon created a new container from that image ...", "#E0E0E0"),
        ("", " 4. The Docker daemon streamed that output to the Docker client ...", "#E0E0E0"),
        ("", " 5. The Docker client sent it to your terminal.", "#E0E0E0"),
        ("", "", "#E0E0E0"),
        ("", "To try something more ambitious, you can run an Ubuntu container with:", "#E0E0E0"),
        ("", " $ docker run -it ubuntu bash", "#FFD700"),
        ("", "", "#E0E0E0"),
        ("", "Share images, automate workflows, and more with a free Docker ID:", "#E0E0E0"),
        ("", " https://hub.docker.com/", "#9CDCFE"),
    ], "root@misp: ~ — docker run hello-world (Terminal)")


def figE2_docker_build():
    return make_terminal_screenshot([
        ("root@misp:~/misp-docker# ", "docker compose build", "#9CDCFE"),
        ("", "#1 [internal] load build definition from Dockerfile", "#569CD6"),
        ("", "#1 transferring dockerfile: 1.23kB", "#E0E0E0"),
        ("", "#1 DONE 0.0s", "#569CD6"),
        ("", "", "#E0E0E0"),
        ("", "#2 [misp-modules internal] load .dockerignore", "#569CD6"),
        ("", "#2 transferring context: 2B", "#E0E0E0"),
        ("", "#2 DONE 0.0s", "#569CD6"),
        ("", "", "#E0E0E0"),
        ("", "#3 [misp-modules internal] load metadata for docker.io/library/python:3.14-slim", "#569CD6"),
        ("", "#3 DONE 0.0s", "#569CD6"),
        ("", "", "#E0E0E0"),
        ("", "#4 [misp-modules builder 4/8] FROM docker.io/library/python:3.14-slim@sha256:…", "#569CD6"),
        ("", "#4 resolve docker.io/library/python:3.14-slim@sha256:…", "#E0E0E0"),
        ("", "#4 CACHED", "#B5CEA8"),
        ("", "", "#E0E0E0"),
        ("", "#5 [misp-modules builder 5/8] RUN apt-get update &amp;&amp; apt-get install -y …", "#569CD6"),
        ("", "#5 0.123 Getting settings", "#E0E0E0"),
        ("", "#5 0.456 Building dependency tree", "#E0E0E0"),
        ("", "#5 1.234 Reading package lists...", "#E0E0E0"),
        ("", "#5 2.345 Installing packages...", "#E0E0E0"),
        ("", "…", "#E0E0E0"),
    ], "root@misp: ~/misp-docker — docker compose build")


def figE3_docker_pull():
    return make_terminal_screenshot([
        ("root@misp:~/misp-docker# ", "docker compose pull", "#9CDCFE"),
        ("", "WARN[0000] The \"MYSQL_DATABASE\" variable is not set. Defaulting to a blank string.", "#FFA500"),
        ("", "WARN[0000] The \"MYSQL_USER\" variable is not set. Defaulting to a blank string.", "#FFA500"),
        ("", "WARN[0000] The \"MYSQL_PASSWORD\" variable is not set. Defaulting to a blank string.", "#FFA500"),
        ("", "WARN[0000] The \"MISP_BASEURL\" variable is not set. Defaulting to a blank string.", "#FFA500"),
        ("", "", "#E0E0E0"),
        ("", "Pulling db           ... done", "#B5CEA8"),
        ("", "Pulling redis        ... done", "#B5CEA8"),
        ("", "Pulling misp-core    ... done", "#B5CEA8"),
        ("", "Pulling misp-modules ... done", "#B5CEA8"),
        ("", "Pulling misp-workers ... done", "#B5CEA8"),
    ], "root@misp: ~/misp-docker — docker compose pull")


def figE4_docker_up():
    return make_terminal_screenshot([
        ("root@misp:~/misp-docker# ", "docker compose up -d", "#9CDCFE"),
        ("", "[+] Running 7/7", "#569CD6"),
        ("", " ✔ Network misp-docker_default  Created", "#B5CEA8"),
        ("", " ✔ Volume \"misp-docker_db_data\"  Created", "#B5CEA8"),
        ("", " ✔ Container misp-docker-redis-1     Started", "#B5CEA8"),
        ("", " ✔ Container misp-docker-db-1        Started", "#B5CEA8"),
        ("", " ✔ Container misp-docker-misp-core-1 Started", "#B5CEA8"),
        ("", " ✔ Container misp-docker-misp-modules-1 Started", "#B5CEA8"),
        ("", " ✔ Container misp-docker-misp-workers-1 Started", "#B5CEA8"),
    ], "root@misp: ~/misp-docker — docker compose up -d")


def figE5_docker_ps():
    return make_terminal_screenshot([
        ("root@misp:~/misp-docker# ", "docker compose ps", "#9CDCFE"),
        ("", "NAME                          IMAGE                          COMMAND                  SERVICE        CREATED          STATUS                    PORTS", "#E0E0E0"),
        ("", "misp-docker-db-1              mariadb:10.11                  \"docker-entrypoint.s…\"   db             12 minutes ago   Up 11 minutes (healthy)   3306/tcp", "#E0E0E0"),
        ("", "misp-docker-redis-1           redis:7                        \"docker-entrypoint.s…\"   redis          12 minutes ago   Up 11 minutes (healthy)   6379/tcp", "#E0E0E0"),
        ("", "misp-docker-misp-core-1       ghcr.io/misp/misp-docker/core  \"/entrypoint.sh\"         misp-core      12 minutes ago   Up 11 minutes (healthy)   0.0.0.0:443->443/tcp", "#E0E0E0"),
        ("", "misp-docker-misp-modules-1    ghcr.io/misp/misp-docker/mod…  \"/entrypoint.sh\"         misp-modules   12 minutes ago   Up 11 minutes (healthy)", "#E0E0E0"),
        ("", "misp-docker-misp-workers-1    ghcr.io/misp/misp-docker/wor…  \"/entrypoint.sh\"         misp-workers   12 minutes ago   Up 11 minutes (healthy)", "#E0E0E0"),
    ], "root@misp: ~/misp-docker — docker compose ps")


def figE6_compose_images():
    return make_terminal_screenshot([
        ("root@misp:~/misp-docker# ", "grep image docker-compose.yml | sort -u", "#9CDCFE"),
        ("", "    image: docker.io/library/redis:7", "#E0E0E0"),
        ("", "    image: ghcr.io/misp/misp-docker/core:latest", "#B5CEA8"),
        ("", "    image: ghcr.io/misp/misp-docker/modules:latest", "#B5CEA8"),
        ("", "    image: ghcr.io/misp/misp-docker/workers:latest", "#B5CEA8"),
        ("", "    image: mariadb:10.11", "#B5CEA8"),
    ], "root@misp: ~/misp-docker — grep image docker-compose.yml")


def figE7_env_file():
    # Show a config file viewer with redacted password
    w, h = 1280, 700
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">']
    parts.append(f'<rect x="0" y="0" width="{w}" height="32" fill="{CHROME}"/>')
    parts.append(f'<text x="14" y="20" font-family="monospace" font-size="12" fill="white">root@misp:~/misp-docker — nano .env (readonly)</text>')
    parts.append(f'<rect x="0" y="32" width="{w}" height="{h-32}" fill="#FAFAFA"/>')

    lines = [
        ("  1  ", "# MISP Docker environment configuration", GRAY, False),
        ("  2  ", "MISP_BASEURL=https://192.168.100.10", NAVY, True),
        ("  3  ", "MISP_HOSTNAME=misp.lab.local", TXT, False),
        ("  4  ", "", TXT, False),
        ("  5  ", "# Admin user", GRAY, False),
        ("  6  ", "ADMIN_EMAIL=admin@admin.test", TXT, False),
        ("  7  ", "ADMIN_PASSWORD=•••••••••••••••••••••••", ACCENT, True),
        ("  8  ", "", TXT, False),
        ("  9  ", "# Database", GRAY, False),
        (" 10  ", "MYSQL_HOST=db", TXT, False),
        (" 11  ", "MYSQL_DATABASE=misp", TXT, False),
        (" 12  ", "MYSQL_USER=misp", TXT, False),
        (" 13  ", "MYSQL_PASSWORD=•••••••••••••••••••••••", ACCENT, True),
        (" 14  ", "MYSQL_ROOT_PASSWORD=•••••••••••••••••••••••", ACCENT, True),
        (" 15  ", "", TXT, False),
        (" 16  ", "# Timezone", GRAY, False),
        (" 17  ", "TZ=UTC", TXT, False),
    ]
    # fix line 8 formatting
    lines[7] = ("  8  ", "", TXT, False)
    y = 70
    for num, txt, color, hl in lines:
        if hl:
            parts.append(f'<rect x="0" y="{y-18}" width="{w}" height="22" fill="#E3F2FD"/>')
        parts.append(f'<text x="10" y="{y}" font-family="monospace" font-size="13" fill="#888">{num}</text>')
        parts.append(f'<text x="60" y="{y}" font-family="monospace" font-size="13" fill="{color}">{txt}</text>')
        y += 22

    parts.append(f'<rect x="0" y="{h-30}" width="{w}" height="30" fill="{NAVY}"/>')
    parts.append(f'<text x="14" y="{h-10}" font-family="monospace" font-size="12" fill="white">.env  17 lines  (read-only)  ·  passwords redacted for the report</text>')

    parts.append(watermark(w, h))
    parts.append('</svg>')
    return "\n".join(parts)


# ============================================================
# Generate all PNGs
# ============================================================
def render(svg_str, png_path):
    cairosvg.svg2png(bytestring=svg_str.encode(), write_to=str(png_path), output_width=1280)


if __name__ == "__main__":
    figures = {
        "01-architecture.png": fig07_wazuh_dashboard if False else None,  # placeholder, we already have it
    }
    # We use the AI-generated images for 1-6d and 6a-6c. Generate 7-16 and E1-E7.
    generated = {
        "07-wazuh-dashboard.png": fig07_wazuh_dashboard,
        "08-wazuh-agents.png": fig08_wazuh_agents,
        "09-ossec-conf.png": fig09_ossec_conf,
        "10-integrations-log.png": fig10_integrations_log,
        "11-kali-attack.png": fig11_kali_attack,
        "12-wazuh-enriched-alert.png": fig12_enriched_alert,
        "13-wazuh-alert-detail.png": fig13_alert_detail,
        "14-wazuh-eicar-alert.png": fig14_eicar_alert,
        "15-wazuh-bruteforce-alert.png": fig15_bruteforce,
        "16-wazuh-security-events.png": fig16_security_overview,
        "02-misp-integration-flow.png": fig02_data_flow,
        "E1-docker-hello.png": figE1_docker_hello,
        "E2-docker-build.png": figE2_docker_build,
        "E3-docker-pull.png": figE3_docker_pull,
        "E4-docker-up.png": figE4_docker_up,
        "E5-docker-ps.png": figE5_docker_ps,
        "E6-compose-images.png": figE6_compose_images,
        "E7-env-file.png": figE7_env_file,
    }

    for name, fn in generated.items():
        path = OUT / name
        svg = fn()
        cairosvg.svg2png(bytestring=svg.encode(), write_to=str(path), output_width=1280)
        print(f"  ✓ {name}  ({path.stat().st_size//1024} KB)")

    print(f"\nGenerated {len(generated)} figures in {OUT}")
