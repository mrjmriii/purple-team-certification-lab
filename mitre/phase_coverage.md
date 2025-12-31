# Phase Coverage (Posture-Linked)

This table maps social-engineering postures to MITRE phases, techniques, and planned scripts.
Status is planning-focused; scripts and rules are not yet implemented.

| Posture ID | Name                                | Phases (examples)                                   | Techniques (examples)                                  | Planned Scripts (examples)                                        |
|------------|-------------------------------------|-----------------------------------------------------|--------------------------------------------------------|--------------------------------------------------------------------|
| 01         | Reduced MFA coverage                | Initial Access → Execution → Persistence → C2       | T1078, T1059, T1053, T1071.001                         | initial_access_valid_creds.py, exec_follow_on.py, persistence_temp_cron.py, c2_http_localhost.py |
| 02         | Over-privileged user promotion      | Priv Esc → Discovery → Lateral Movement             | T1548, T1069, T1021.004                                | priv_escal_group_change_sim.py, discovery_sudoers_scan.py, ssh_attempt_reserved.py               |
| 03         | Email security relaxation           | Initial Access → Execution → Collection → Exfil     | T1566, T1059, T1119, T1041                             | macro_like_temp_exec.py, collection_dummy_archive.py, exfil_localhost_log.py                    |
| 04         | Execution policy weakening          | Execution → Persistence → Defense Evasion           | T1059, T1053, T1562.001                                | exec_policy_toggle_sim.py, persistence_temp_autorun.py                                             |
| 05         | Endpoint protection exclusions      | Defense Evasion → Execution → Collection            | T1562.001, T1059, T1119                                | edr_exclusion_tempfile.py, exec_unsigned_analog.py, collection_dummy_archive.py                 |
| 06         | Password policy relaxation          | Initial Access → Credential Access → Defense Evasion| T1110, T1552, T1562                                    | spray_sim_logonly.py, passwd_read_log.py, loglevel_toggle.py                                      |
| 07         | VPN trust expansion                 | Initial Access → Discovery → Lateral Movement → C2  | T1133, T1018, T1021.004, T1071.001                     | vpn_policy_change_log.py, net_scan_reserved.py, ssh_attempt_reserved.py, c2_http_localhost.py    |
| 08         | Firewall allow / IDS bypass         | Defense Evasion → Lateral Movement → C2             | T1562.004, T1021, T1071.001                            | fw_rule_toggle_log.py, tcp_connect_attempt.py, c2_http_localhost.py                              |
| 09         | Backup & recovery suppression       | Impact → Discovery → Exfiltration                   | T1490, T1083, T1041                                    | backup_disable_log.py, collection_dummy_archive.py, exfil_localhost_log.py                       |
| 10         | Service account credential exposure | Credential Access → Persistence → Execution         | T1552, Token Persistence, T1059                        | secret_file_scan.py, token_store_temp.py, token_use_log.py                                        |
| 11         | Logging/alert suppression           | Defense Evasion → Execution → Impact                | T1562, T1059, Alert Suppression Analog                 | loglevel_toggle.py, exec_marker.py, alert_suppression_marker.py                                   |
| 12         | Change control bypass               | Defense Evasion → Execution → Impact                | T1562, T1059, Service Disruption Analog                | change_without_ticket.py, config_touch_tmp.py, impact_marker.py                                   |

## Notes
- Scripts are not implemented; names and `_SIM` log markers are reserved for planned safe simulations.
- Wazuh rule IDs are placeholders (TODO-*) and will be added once decoders/rules are authored.
- Runner and scoring integration will consume the posture manifests in `labs/postures/`.
