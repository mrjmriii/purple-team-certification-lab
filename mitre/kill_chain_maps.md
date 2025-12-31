# Kill-Chain Maps by Posture

Executive-ready MITRE ATT&CK kill-chain views for each of the 12 social-engineering postures.
Each map shows the ordered phases, ATT&CK techniques, and planned scripts (one technique per
script). Scripts are safe simulations and not yet implemented.

## Visual options
- **Inline previews (GitHub-friendly):** SVG previews generated from the Navigator layers live under
  `mitre/navigator/previews/` and render directly in GitHub. Each shows the ordered steps, tactic,
  ATT&CK ID, and planned script.
- **ATT&CK Navigator layers:** Import the posture-specific JSON layers from `mitre/navigator/*.json`
  into https://mitre-attack.github.io/attack-navigator/ to see tactic-aligned tiles with ordering
  metadata.
- **Mermaid flow diagrams:** Inline flowcharts illustrate the kill-chain order for quick review.

## Legend
- Phases follow MITRE ATT&CK.
- Techniques include ATT&CK IDs.
- Scripts are planned names matching `labs/postures/*.yaml` manifests.
- Order is the execution sequence within each posture.

---

## 01 Reduced MFA coverage
```mermaid
flowchart LR
    A[Initial Access\nT1078\ninitial_access_valid_creds.py] --> B[Execution\nT1059\nexec_follow_on.py]
    B --> C[Persistence\nT1053\npersistence_temp_cron.py]
    C --> D[C2\nT1071.001\nc2_http_localhost.py]
```

![Navigator preview](navigator/previews/01_reduced_mfa_coverage.svg)

| Order | Phase              | Technique (ATT&CK)                  | Planned Script                |
|-------|--------------------|-------------------------------------|-------------------------------|
| 1     | Initial Access     | Valid Accounts (T1078)              | initial_access_valid_creds.py |
| 2     | Execution          | Command Execution (T1059)           | exec_follow_on.py             |
| 3     | Persistence        | Scheduled Task/Job (T1053)          | persistence_temp_cron.py      |
| 4     | Command & Control  | App Layer Protocol: Web (T1071.001) | c2_http_localhost.py          |

## 01 Reduced MFA coverage
| Order | Phase              | Technique (ATT&CK)             | Planned Script                  |
|-------|--------------------|--------------------------------|---------------------------------|
| 1     | Initial Access     | Valid Accounts (T1078)         | initial_access_valid_creds.py   |
| 2     | Execution          | Command Execution (T1059)      | exec_follow_on.py               |
| 3     | Persistence        | Scheduled Task/Job (T1053)     | persistence_temp_cron.py        |
| 4     | Command & Control  | App Layer Protocol: Web (T1071.001) | c2_http_localhost.py      |

## 02 Over-privileged user promotion
```mermaid
flowchart LR
    A[Privilege Escalation\nT1548\npriv_escal_group_change_sim.py] --> B[Discovery\nT1069\ndiscovery_sudoers_scan.py]
    B --> C[Lateral Movement\nT1021.004\nssh_attempt_reserved.py]
```

![Navigator preview](navigator/previews/02_over_privileged_user_promotion.svg)

| Order | Phase                 | Technique (ATT&CK)                     | Planned Script                    |
|-------|-----------------------|----------------------------------------|-----------------------------------|
| 1     | Privilege Escalation  | Abuse Elevation Control (T1548)        | priv_escal_group_change_sim.py    |
| 2     | Discovery             | Permission Groups Discovery (T1069)    | discovery_sudoers_scan.py         |
| 3     | Lateral Movement      | Remote Services: SSH (T1021.004)       | ssh_attempt_reserved.py           |

## 03 Email security relaxation
```mermaid
flowchart LR
    A[Initial Access\nT1566\nmacro_like_temp_exec.py] --> B[Execution\nT1059\nmacro_like_temp_exec.py]
    B --> C[Collection\nT1119\ncollection_dummy_archive.py]
    C --> D[Exfiltration\nT1041\nexfil_localhost_log.py]
```

![Navigator preview](navigator/previews/03_email_security_relaxation.svg)

| Order | Phase              | Technique (ATT&CK)                     | Planned Script                   |
|-------|--------------------|----------------------------------------|----------------------------------|
| 1     | Initial Access     | Phishing (T1566)                       | macro_like_temp_exec.py          |
| 2     | Execution          | Command Execution (T1059)              | macro_like_temp_exec.py          |
| 3     | Collection         | Automated Collection (T1119)           | collection_dummy_archive.py      |
| 4     | Exfiltration       | Exfiltration Over C2 Channel (T1041)   | exfil_localhost_log.py           |

## 04 Execution policy weakening
```mermaid
flowchart LR
    A[Execution\nT1059\nexec_policy_toggle_sim.py] --> B[Persistence\nT1053\npersistence_temp_autorun.py]
    B --> C[Defense Evasion\nT1562.001\nexec_policy_toggle_sim.py]
```

![Navigator preview](navigator/previews/04_execution_policy_weakening.svg)

| Order | Phase              | Technique (ATT&CK)                    | Planned Script                    |
|-------|--------------------|---------------------------------------|-----------------------------------|
| 1     | Execution          | Command Execution (T1059)             | exec_policy_toggle_sim.py         |
| 2     | Persistence        | Scheduled Task/Job (T1053)            | persistence_temp_autorun.py       |
| 3     | Defense Evasion    | Impair Defenses (T1562.001)           | exec_policy_toggle_sim.py         |

## 05 Endpoint protection exclusions
```mermaid
flowchart LR
    A[Defense Evasion\nT1562.001\nedr_exclusion_tempfile.py] --> B[Execution\nT1059\nexec_unsigned_analog.py]
    B --> C[Collection\nT1119\ncollection_dummy_archive.py]
```

![Navigator preview](navigator/previews/05_endpoint_protection_exclusions.svg)

| Order | Phase              | Technique (ATT&CK)                    | Planned Script                    |
|-------|--------------------|---------------------------------------|-----------------------------------|
| 1     | Defense Evasion    | Impair Defenses (T1562.001)           | edr_exclusion_tempfile.py         |
| 2     | Execution          | Command Execution (T1059)             | exec_unsigned_analog.py           |
| 3     | Collection         | Automated Collection (T1119)          | collection_dummy_archive.py       |

## 06 Password policy relaxation
```mermaid
flowchart LR
    A[Initial Access\nT1110\nspray_sim_logonly.py] --> B[Credential Access\nT1552\npasswd_read_log.py]
    B --> C[Defense Evasion\nT1562\nloglevel_toggle.py]
```

![Navigator preview](navigator/previews/06_password_policy_relaxation.svg)

| Order | Phase              | Technique (ATT&CK)                    | Planned Script                    |
|-------|--------------------|---------------------------------------|-----------------------------------|
| 1     | Initial Access     | Brute Force / Spraying (T1110)        | spray_sim_logonly.py              |
| 2     | Credential Access  | Unsecured Credentials (T1552)         | passwd_read_log.py                |
| 3     | Defense Evasion    | Impair Defenses (T1562)               | loglevel_toggle.py                |

## 07 VPN trust expansion
```mermaid
flowchart LR
    A[Initial Access\nT1133\nvpn_policy_change_log.py] --> B[Discovery\nT1018\nnet_scan_reserved.py]
    B --> C[Lateral Movement\nT1021.004\nssh_attempt_reserved.py]
    C --> D[C2\nT1071.001\nc2_http_localhost.py]
```

![Navigator preview](navigator/previews/07_vpn_trust_expansion.svg)

| Order | Phase              | Technique (ATT&CK)                      | Planned Script                    |
|-------|--------------------|-----------------------------------------|-----------------------------------|
| 1     | Initial Access     | External Remote Services (T1133)        | vpn_policy_change_log.py          |
| 2     | Discovery          | Remote System Discovery (T1018)         | net_scan_reserved.py              |
| 3     | Lateral Movement   | Remote Services: SSH (T1021.004)        | ssh_attempt_reserved.py           |
| 4     | Command & Control  | App Layer Protocol: Web (T1071.001)     | c2_http_localhost.py              |

## 08 Firewall temporary allow / IDS bypass
```mermaid
flowchart LR
    A[Defense Evasion\nT1562.004\nfw_rule_toggle_log.py] --> B[Lateral Movement\nT1021\ntcp_connect_attempt.py]
    B --> C[C2\nT1071.001\nc2_http_localhost.py]
```

![Navigator preview](navigator/previews/08_firewall_allow_ids_bypass.svg)

| Order | Phase              | Technique (ATT&CK)                       | Planned Script                    |
|-------|--------------------|------------------------------------------|-----------------------------------|
| 1     | Defense Evasion    | Modify Firewall (T1562.004)              | fw_rule_toggle_log.py             |
| 2     | Lateral Movement   | Remote Services (T1021)                  | tcp_connect_attempt.py            |
| 3     | Command & Control  | App Layer Protocol: Web (T1071.001)      | c2_http_localhost.py              |

## 09 Backup & recovery suppression
```mermaid
flowchart LR
    A[Impact\nT1490\nbackup_disable_log.py] --> B[Discovery\nT1083\ncollection_dummy_archive.py]
    B --> C[Exfiltration\nT1041\nexfil_localhost_log.py]
```

![Navigator preview](navigator/previews/09_backup_recovery_suppression.svg)

| Order | Phase              | Technique (ATT&CK)                     | Planned Script                    |
|-------|--------------------|----------------------------------------|-----------------------------------|
| 1     | Impact             | Inhibit System Recovery (T1490)        | backup_disable_log.py             |
| 2     | Discovery          | File and Directory Discovery (T1083)   | collection_dummy_archive.py       |
| 3     | Exfiltration       | Exfiltration Over C2 Channel (T1041)   | exfil_localhost_log.py            |

## 10 Service account credential exposure
```mermaid
flowchart LR
    A[Credential Access\nT1552\nsecret_file_scan.py] --> B[Persistence\nT1136.001\ntoken_store_temp.py]
    B --> C[Execution\nT1059\ntoken_use_log.py]
```

![Navigator preview](navigator/previews/10_service_account_credential_exposure.svg)

| Order | Phase              | Technique (ATT&CK)                    | Planned Script                    |
|-------|--------------------|---------------------------------------|-----------------------------------|
| 1     | Credential Access  | Unsecured Credentials (T1552)         | secret_file_scan.py               |
| 2     | Persistence        | Token Persistence                     | token_store_temp.py               |
| 3     | Execution          | Command Execution (T1059)             | token_use_log.py                  |

## 11 Logging/alert suppression
```mermaid
flowchart LR
    A[Defense Evasion\nT1562\nloglevel_toggle.py] --> B[Execution\nT1059\nexec_marker.py]
    B --> C[Impact\nT1499 analog\nalert_suppression_marker.py]
```

![Navigator preview](navigator/previews/11_logging_alert_suppression.svg)

| Order | Phase              | Technique (ATT&CK)                         | Planned Script                    |
|-------|--------------------|--------------------------------------------|-----------------------------------|
| 1     | Defense Evasion    | Impair Defenses (T1562)                    | loglevel_toggle.py                |
| 2     | Execution          | Command Execution (T1059)                  | exec_marker.py                    |
| 3     | Impact             | Alert Suppression / Impact Analog          | alert_suppression_marker.py       |

## 12 Change control bypass
```mermaid
flowchart LR
    A[Defense Evasion\nT1562\nchange_without_ticket.py] --> B[Execution\nT1059\nconfig_touch_tmp.py]
    B --> C[Impact\nT1499 analog\nimpact_marker.py]
```

![Navigator preview](navigator/previews/12_change_control_bypass.svg)

| Order | Phase              | Technique (ATT&CK)                         | Planned Script                    |
|-------|--------------------|--------------------------------------------|-----------------------------------|
| 1     | Defense Evasion    | Impair Defenses (T1562)                    | change_without_ticket.py          |
| 2     | Execution          | Command Execution (T1059)                  | config_touch_tmp.py               |
| 3     | Impact             | Service Disruption Analog                  | impact_marker.py                  |
