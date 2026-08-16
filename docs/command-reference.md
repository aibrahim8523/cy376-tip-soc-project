# Command Reference — TIP–SOC Lab

All commands run inside the student-controlled VMware lab environment
(Ubuntu Server `192.168.18.130`, Kali `192.168.18.128`).

## Wazuh installation
```bash
curl -sO https://packages.wazuh.com/4.9/wazuh-install.sh
sudo bash wazuh-install.sh -a -o -p 8443
# Dashboard: https://192.168.18.130:8443
```

## Wazuh service health
```bash
sudo systemctl is-active wazuh-manager wazuh-indexer wazuh-dashboard filebeat
sudo /var/ossec/bin/wazuh-control status
```

## Docker / containerd
```bash
sudo systemctl stop docker docker.socket containerd
sudo rm -rf /var/lib/containerd
sudo mkdir -p /var/lib/containerd
sudo systemctl start containerd docker
sudo docker run hello-world
```

## MISP deployment (Docker Compose)
```bash
cd ~/misp-docker
sudo docker compose up -d
sudo docker compose ps
```

## MISP base-URL correction
```bash
# .env:  BASE_URL=https://192.168.18.130
#        MISP_BASEURL=https://192.168.18.130
# config.php: 'baseurl' => 'https://192.168.18.130',
sudo docker compose up -d --force-recreate misp-core
```

## Wazuh custom-misp integration
```bash
# /var/ossec/integrations/custom-misp.py  (Python component)
# /var/ossec/integrations/custom-misp    (executable wrapper, mode 750 root:wazuh)
sudo systemctl restart wazuh-manager
sudo tail -f /var/ossec/logs/integrations.log
```

## Custom rule (local_rules.xml)
```xml
<rule id="100002" level="12">
  <match>192.168.18.128</match>
  <description>Connection from MISP-registered known-bad IP (Kali)</description>
</rule>
```

## FIM database repair
```bash
sudo systemctl stop wazuh-manager
sudo rm -f /var/ossec/queue/fim/db/fim.db*
sudo systemctl start wazuh-manager
```

## Kali attack tests
```bash
nmap -sS 192.168.18.130
ssh kali@192.168.18.130
```

## EICAR test
```bash
curl -L -o /tmp/eicar.com https://secure.eicar.org/eicar.com
sha256sum /tmp/eicar.com
```

## Swap (added because the indexer was OOM-killed)
```bash
sudo fallocate -l 2G /swapfile && sudo chmod 600 /swapfile
sudo mkswap /swapfile && sudo swapon /swapfile
```
