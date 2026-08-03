# Command Reference

A copy-paste-ready list of every command used in the lab. Run as indicated in
the phase headers. See `report/TIP_Integration_Project.pdf` Section 4 for the
contextual walkthrough.

---

## Phase 1 — Static IP (each Ubuntu VM)

```bash
# Edit the file (replace 192.168.100.X with the right address)
sudo nano /etc/netplan/00-installer-config.yaml
sudo netplan apply

# Verify
ip a
ping -c 2 192.168.100.10   # from every other VM
```

## Phase 2 — MISP deployment (on 192.168.100.10)

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y ca-certificates curl gnupg docker-ce docker-compose-plugin
git clone https://github.com/MISP/misp-docker.git
cd misp-docker
cp template.env .env
# Edit .env: set MISP_BASEURL and ADMIN_PASSWORD
sudo docker compose pull
sudo docker compose up -d
sudo docker compose ps
```

## Phase 3 — Populate MISP with intelligence

* **Web UI:** browse to `https://192.168.100.10`, log in, **change the admin
  password immediately**.
* **OSINT feeds:** Sync Actions → List Feeds → enable CIRCL OSINT Feed and
  abuse.ch URLhaus → "Fetch and store all feed data".
* **Auth key for SIEM:** Administration → List Users → your user → Auth Keys →
  Add auth key. **Copy and store safely — MISP only shows it once.**

## Phase 4 — Wazuh SIEM (on 192.168.100.20)

```bash
curl -sO https://packages.wazuh.com/4.9/wazuh-install.sh
sudo bash wazuh-install.sh -a
# SAVE THE PASSWORD PRINTED AT THE END
```

Browse to `https://192.168.100.20`, log in with `admin` and the saved password.

## Phase 5 — Endpoint agent (on 192.168.100.30)

```bash
curl -so wazuh-agent.deb \
  https://packages.wazuh.com/4.x/apt/pool/main/w/wazuh-agent/wazuh-agent_4.9.0-1_amd64.deb
sudo WAZUH_MANAGER='192.168.100.20' dpkg -i ./wazuh-agent.deb
sudo systemctl daemon-reload
sudo systemctl enable --now wazuh-agent
sudo systemctl status wazuh-agent
```

The endpoint should now appear as **Active** in the Wazuh Dashboard →
Server management → Endpoints Summary.

## Phase 6 — MISP ↔ Wazuh integration (on Wazuh manager)

```bash
# Install the integration dependencies
sudo apt install -y python3-pip
pip3 install requests pymisp --break-system-packages

# Edit /var/ossec/etc/ossec.conf and add the integration block
# (see configs/wazuh-ossec.conf for the exact XML)

sudo systemctl restart wazuh-manager
sudo tail -f /var/ossec/logs/integrations.log
# You should see "Wazuh-MISP: Alert ... sent to MISP restSearch" lines
```

## Phase 7 — Attack simulation (on Kali, 192.168.100.40)

```bash
# Scenario S1: known-bad IP scan + connection
nmap -sS -A 192.168.100.30
nc -v 192.168.100.30 22

# Scenario S3: SSH brute force
hydra -l testuser -P /usr/share/wordlists/rockyou.txt ssh://192.168.100.30
```

## Phase 7 — EICAR file (on endpoint, 192.168.100.30)

```bash
curl -o eicar.com https://secure.eicar.org/eicar.com
sha256sum eicar.com
# Expected: 275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f
```

## Phase 8 — Validate

In the Wazuh Dashboard → Security events, look for the four alerts from the
simulation window. The two IP/hash scenarios should show a "MISP enrichment
attached" banner; the brute-force scenario is a behavioural detection and
should still fire alongside the intelligence-driven ones.
