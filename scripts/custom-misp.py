#!/usr/bin/env python3
"""
custom-misp.py — Wazuh integration component.
Reads the temporary alert file passed by wazuh-integratord, extracts an IP
(data.srcip / data.dstip) or a SHA-256 (syscheck.sha256_after), queries the
MISP restSearch API, and logs the result.

Arguments (as passed by wazuh-integratord):
  argv[1] = path to the temporary alert JSON file
  argv[2] = MISP API key
  argv[3] = MISP hook URL (restSearch endpoint)
"""
import json
import sys
import requests
import urllib3

urllib3.disable_warnings()


def main():
    if len(sys.argv) < 4:
        print("ERROR: expected argv[1]=alert_file argv[2]=api_key argv[3]=hook_url", flush=True)
        return

    alert_file = sys.argv[1]
    api_key = sys.argv[2]
    hook_url = sys.argv[3]

    try:
        with open(alert_file, "r", encoding="utf-8") as fh:
            alert = json.load(fh)
    except Exception as exc:
        print("ERROR: cannot read/parse alert file: %s" % exc, flush=True)
        return

    data = alert.get("data", {}) or {}
    syscheck = alert.get("syscheck", {}) or {}
    rule = alert.get("rule", {}) or {}

    # Select an indicator: prefer an IP, else a file hash
    value = data.get("srcip") or data.get("dstip")
    indicator_source = "ip"
    if not value:
        value = syscheck.get("sha256_after")
        indicator_source = "sha256"

    if not value:
        print("INFO: no IP or SHA-256 indicator to query", flush=True)
        return

    headers = {"Authorization": api_key, "Accept": "application/json"}
    params = {"value": value, "returnFormat": "json"}

    print("INFO: Rule %s; querying MISP for %s value=%s"
          % (rule.get("id"), indicator_source, value), flush=True)
    try:
        response = requests.get(hook_url, headers=headers, params=params,
                                verify=False, timeout=15)
        print("INFO: MISP response code=%s" % response.status_code, flush=True)
        if response.status_code == 200:
            attributes = response.json().get("response", {}).get("Attribute", [])
            print("INFO: MISP returned %s matching attribute(s)" % len(attributes), flush=True)
            if attributes:
                attr = attributes[0]
                print("MATCH: Enrichment attached: event_id=%s, type=%s, value=%s"
                      % (attr.get("event_id"), attr.get("type"), attr.get("value")), flush=True)
        else:
            print("ERROR: MISP returned HTTP %s" % response.status_code, flush=True)
    except Exception as exc:
        print("ERROR: MISP request failed: %s" % exc, flush=True)


if __name__ == "__main__":
    main()
