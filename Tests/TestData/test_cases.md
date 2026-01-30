# Test Cases

| ID | Scenario | Steps | Expected Result |
| --- | --- | --- | --- |
| TC-001 | Simple box | Export with `simple_box.json` | Watertight shell mesh |
| TC-002 | Shell only | Export with `shell_only.json` | Exterior only, no MEP |
| TC-003 | Structure | Export with `shell_with_structure.json` | Columns/beams included |
| TC-004 | Full exterior | Export with `full_exterior.json` | Exterior + site context |
