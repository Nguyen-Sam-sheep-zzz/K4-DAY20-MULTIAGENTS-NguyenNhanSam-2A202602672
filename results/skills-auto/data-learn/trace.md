### Human
Analyse the sales data in `workspace/sales.csv` (see `workspace/README.md` for the column descriptions).

Write a file `workspace/answer.json` with exactly these keys, plus whatever the Acme reporting conventions require:

- `north_q1_revenue` (number): sum of `amount` of the orders in region North placed in the first quarter of 2024, that is from 2024-01-01 00:00 UTC up to and including 2024-03-31 23:59:59 UTC.
- `north_q1_orders` (integer): number of distinct orders counted in `north_q1_revenue`.
- `top_region` (string): the region (North, South, East or West) with the highest total `amount` over the whole file.
- `missing_amount_orders` (integer): number of distinct orders whose amount is missing.
- `duplicate_rows_removed` (integer): number of duplicate rows you removed.

Orders with a missing amount must not be added to any revenue.
Your output files are also checked by Acme's review bot against the Acme reporting conventions.
When you are done, reply with a short summary of how you cleaned the data.


### Assistant
[{'id': 'rs_06540952ce1ad06d016ac48787b5788191ace8029bf0f7a851', 'summary': [], 'type': 'reasoning', 'content': [], 'encrypted_content': 'gAAAAABqxIeHOPSqPI0OAm9UgL8IOUyifRCJ9C7FGYKsiz0RLsQxQHvoQHSkOkLJzNzD3_M5oEdmqLGIsPcgpWR-cWHkTr2aweeJ3rIg8DfgdiqC25-5MV0HCM-jPJSkRycS9X2qY33s4cw7mHDSMnYXPNvXgN1DgpQjR9WbYcfkPLCinIF2qqTgWNn3TORxyuLGETuGpEfV4SuigHKjNlz9sMhYMCP9BqZg8QEH3cvFiy4SvUbLUYxfhwAXOKrYc_pewkX58iIpi7c5WYxHoLf7cFbexJHPlZ5rbh1ZkK7YG6zVh94YWDKqjTB4_eABzB1hXs2k0O7oZ2GVoqrWig6tcF5HVBdC4Ept-8RQe61gIRKgoudoPIrUiLrG8Vls8iIlQypG0XfPOKgA4T0jaMCpCQyJ9BUAKy1ejFJpc1TEm3L4jljMMGUinjQkjhLEVscsXbG8U859d4LnH-4F3mllgmIWdd3k43Lus8wuVFgJdK5Uk7GH0qeoeZayTnNy_SDfC1woTsw6DaT0VdOnZ0RJwmqVskAdOo3jUxE1lgY6FF64YmXXscxHC4RzFyGmK9h0ZywcWFwCwHQ5eCkvtK8btSworJc9TOvsOKm0oaDQendv9ZQohvjI5kFqHSmqnCX7Q4FOWrweRjhd3-lKkrBBxYuWO9jEzJMgWlQqlwbmltnHq-ghI9JCT9TZfizsyOox8eoHA1cebrAoBgy1dMI6ZJuTn7zia9t9AKKW2hoZdePA5AyFpVnt26nYJ6lX-kRuIBEzD4FdLfGb0YzQYLmjLyf469UGzuuDQ_S_cMhindz0eM3o8dp7qWenGJHfPuMTXh7KSIReEU96bGcxY_7oCT3kM_ol9LwwChw8MayaTf5OrP6H4pZOtp0M6MS1UNNUe84zikOM3Em2Q95xGS9Tk7xnpGKlj3wIg7u9yU5FWy3zFO6U8RbNVN6ZI1BHocmfa8BGJK0AZ630xMG6cF-vs5nTwrNHXC_dbOnR2ofekWlFW1ghdG6TqEbO1OMQjr5Gwn11XRwHjrneJiBTiqGaDXq3xVYLyVWZCFh7mvRA0ZOGmywtphTgRip0-w4Ysp4idEQyyHX_UYuckxnCr4ojIyogr677kj0hrAtdNi0kBeHjX0J2j32h8LS9V-1troHc_rAIEOxe_Rttf0YPXFrnaEXumxQ8_aEayhY6kUyOZHSzk14DSM-b_Q7WbIBBracRsjBLVCXkJtkd-phSjhEmA3Vfor6TcSkyceUFmYki9Z3L0XCkFaU1mdnTCJDUwVKN84ZdA4Y7qKF2oJg_1ls_B7RYbhFNcv_yRc4k7O8GezsJ8UJNgI2OS0Z8nQM9iwL-UgNg4eXSLz-Y2i

### Tool call: read_file
{"file_path": "/skills/normalized-tabular-output/SKILL.md", "offset": 0, "limit": 1000}

### Tool result
@@ lines 1-17 of 17 @@
---
name: normalized-tabular-output
description: Use when transforming tabular records into deduplicated, normalized analytical outputs.
---
- Count input rows before deduplication, including duplicate records.
- Deduplicate by the record's order identifier before computing distinct-record metrics.
- Exclude records whose amount is unknown from amount-based metrics and cleaned output.
- Represent monetary values as integer cents rather than floating-point currency values.
- Parse dates consistently and emit UTC timestamps in `YYYY-MM-DDTHH:MM:SSZ` form.
- Normalize region labels to the canonical spellings North, South, East, and West.
- Write the cleaned records to `workspace/clean.csv`.
- Write analytical results to `workspace/answer.json`.
- Include a top-level `meta` object in `answer.json`.
- Set `meta.source` to the input filename.
- Set `meta.rows_in` to the original data-row count, including duplicates.
- Set `meta.rows_used` to the distinct-record count with known amounts.
- Verify deduplication, unknown-amount exclusion, cent encoding, region spelling, UTC formatting, and the required output files.

### Assistant
[{'id': 'rs_06540952ce1ad06d016ac48789de7081918270bb37d8ca646d', 'summary': [], 'type': 'reasoning', 'content': [], 'encrypted_content': 'gAAAAABqxIeJ7L6LMRoDvPT4hO0Uv1GBZtFVk3UGkVKni8yFxaYzUMB8bVQSJQA3XoXAd0rNwa8j720vsbvQ0N-1zFrQCllLo9RRKEXBNr3CtMx4_hfpCS-I6NWRMLiX1x2VgNiR-JRTiTFIx0hUkmbvM9NSAdreLx_A8PgC-TjVRNe0StgG0ap3vUI0JQQu3aYJEc6Jof04Nq8EBhM4yUKeKXBtcS4VcbOH4JX2w6a61rbY7PO4_DxoMQDRlq-yT1MVde9zptrNwGIA4MT4jFfp7G9vnFrvOai-WovpdUOtWQZiBxGaYpnpG0UY0C1gJ2OCzJ-81xFzZ94VOcC2eqypL4ZFmy3QsiX3CBdKPgISXrewSPUh2YXeO0VsW1WqQaBsAZ6T9H464MRLwbZY4cgIRq4yLUwyvf7oh9g-AQ2l7d_K4HX9vndeRf6J1ys4rX7NKxFmbf3MR-ZOELkxnEHer9qVyzU7pEoAIyJnG8_JBBaCoN4swxJHZXpqPbKDmgkJL7El3qC69I1AYcl64zfVm5-hS7Xxo6O842aZjVKjKrepxcurWdAZb1D9FSm-_uHAsevsApFUaW0z0zI-iMqESTlJSJUPZAUTsI9AEOwcEL7bAjAYmHMVKH5MKvsn-B2EzLni7fA2quCF-qwKQBWiejUONKewxYUcA2U4uKgXYRA1LYI8roy0brz0DbXoYvgLkqdX2qI3FBXpFRp-fNipzVstVj9q4BD-aOLb6KaBi3MRAIW_xbOvUJyvZfQql4diPc6GbHp_INJ0EfUQ2qCes5Wf-fz6bP46CAJVB9Xvltiigkzg9jvj2ZGlxfBeAMoGQwUysMFzkgY542kYjbswLLU-nYlfGdZ8E0Gs6rObqEGvj-57EZIl_rY689fqzlnase2_pSG88w-HoKuGRACeWyv0t0vsd5ylLR0v-Z4BpERp8D_hZpAr8BhsSUwbmQl6UuQekBtkwzwLWxrq0sG1dACOGXGxjCoUZ3vs_WgrCxsY4cLKUO3BsMddcupGpEUi27Qf7C0nDk-Hq121Q-nN1XwtKHLwZohnM6N1-aiSLe5KHFrlkn_VcrPb6Bui7Wxyo9ndAIVFSfJLHfJOFV1_60uPeSyyMV87qvnEfqUs0ssADlx_biP5BKRjsP9tKAjZFRYA8-Xo2M3Rdx12sG612m8w27LWZAst_-WLFCxJ5jJTIvEhuCvzVwnrppep40VBVRRRjox8StdMNtnIHBL5idQ_M5oVYYdSusliFvbtU20-dMZF_tusV7WGq7-sBRF9liAsLkLUp-hvTTxCSEVKnzvrQexxQe0Z9P9SAZTuCqAVJzf9GpU='}, {'arguments': '{"path"

### Tool call: ls
{"path": "workspace"}

### Tool result
['/workspace/README.md', '/workspace/sales.csv']

### Assistant
[{'arguments': '{"file_path":"/workspace/README.md","offset":0,"limit":1000}', 'call_id': 'call_dIBtSDu8T8R23PeKfa0MIurk', 'name': 'read_file', 'type': 'function_call', 'id': 'fc_06540952ce1ad06d016ac4878cea848191add254f03171df07', 'status': 'completed'}, {'arguments': '{"file_path":"/workspace/sales.csv","offset":0,"limit":1000}', 'call_id': 'call_Hoc4IfRs9cXqwYVvMcmQh77C', 'name': 'read_file', 'type': 'function_call', 'id': 'fc_06540952ce1ad06d016ac4878cea9c8191a83d003138b53f75', 'status': 'completed'}]

### Tool call: read_file
{"file_path": "/workspace/README.md", "offset": 0, "limit": 1000}

### Tool call: read_file
{"file_path": "/workspace/sales.csv", "offset": 0, "limit": 1000}

### Tool result
@@ lines 1-8 of 8 @@
# sales.csv - data dictionary

| column | description |
|---|---|
| order_id | order identifier. The same order may appear more than once because of re-exports; keep one row per order_id. |
| date | when the order was placed. Three formats occur: `YYYY-MM-DD` and `DD/MM/YYYY` (a date only, meaning 00:00 UTC of that day) and an ISO-8601 timestamp with a UTC offset such as `2024-02-03T21:30:00-05:00`. |
| region | sales region (North, South, East, West). Spelling and capitalisation are not consistent. |
| amount | order amount in USD. The value `-999` means the amount is unknown (missing). |

### Tool result
@@ lines 1-102 of 102 @@
order_id,date,region,amount
S-1090,2024-03-05T16:15:00+00:00,west,591.39
S-1022,09/02/2024,NORTH,379.22
S-1005,2024-05-26T12:30:00-05:00,West ,513.84
S-1020,2024-02-23, North,-999
S-1014,10/06/2024,west,335.88
S-1010,16/04/2024, East,145.97
S-1002,20/06/2024, South,-999
S-1076,2024-03-20, South,346.27
S-1032,2024-01-07T23:15:00-05:00,South,637.30
S-1053,09/02/2024,West,883.27
S-2002,2024-01-01T00:30:00+07:00,North,64.10
S-1088,08/01/2024,West ,209.51
S-1015,2024-03-01,NORTH,160.16
S-1071,2024-03-31,West,386.29
S-1025,2024-01-20T16:00:00-05:00,north,200.28
S-1048,2024-03-21, West,646.12
S-1023,01/05/2024,North ,205.13
S-1079,14/03/2024, South,384.80
S-1042,2024-02-27, West,577.22
S-1069,2024-06-11,North ,298.76
S-1057,20/01/2024,North ,579.47
S-1018,30/05/2024,south,545.00
S-1008,2024-05-08,North,560.80
S-1064,2024-03-18,WEST,152.57
S-1031,2024-01-31T18:15:00+00:00,East ,184.73
S-1041,07/06/2024, South,142.31
S-1011,2024-06-01,south,775.56
S-1054,2024-03-26T23:30:00-05:00,east,157.51
S-1030,10/04/2024,SOUTH,337.52
S-1081,2024-06-22,North,564.16
S-1003,08/02/2024, East,66.02
S-1016,10/04/2024,North ,114.29
S-1035,2024-01-22T05:15:00+07:00,West,237.99
S-1033,20/03/2024,North,-999
S-1073,2024-06-13T02:15:00Z,north,91.94
S-1066,12/06/2024,east,474.58
S-1063,2024-05-09, North,213.81
S-1026,2024-02-01T20:30:00-05:00,SOUTH,-999
S-2000,2024-03-31T22:30:00-05:00,North,120.50
S-1040,2024-01-02T08:15:00Z,SOUTH,65.02
S-1077,2024-06-24,WEST,726.47
S-1055,04/03/2024

### Assistant
[{'id': 'rs_06540952ce1ad06d016ac4878edd0081919bd2d552907c0b39', 'summary': [], 'type': 'reasoning', 'content': [], 'encrypted_content': 'gAAAAABqxIeVLAQy9Yf3_WvCLG0Dgak1Yaz4rJheVa5aC1G4ojyTElGZdsJTDRlP9ZBrj01zBFh4uGxjF_3bjhYWfBQLoQ8H5iIHuXTXshIyP2Ic548EUj00xcck--OkGizAekrZIZEbbNPGf_zxKxEooXY7KrmOCK2nmZNUJFMhv6Xzb2cauRBspp-iuISNnLhf765Jd4r5X-wDmWLmIfDLTEXI5YLAFPDWZmuUncM63wXCvnC_YOJ3HK4PBu2jut9rqHJr28NYYVeNpwLRSUHY4M7rRglkdCEP0znQqLDO7YLw4E8a5NgeiFmHcotyuqvq3maUMpHq6EJDPMpBXLmj6RumKhtlA7XdLndLoF9eBdHXjEfMHvKBo59BPr-P93R_29A0o9ezW0-y5OSspCsfqLLC_XJhS7yLbO4-unaLtfqHydBCZhD3K7L7xaDXNxQNki9Xn7F5OQF_LWpLLojFJIAFuGDE_mi1uUKtap6klstccWRO4mJCtOt4XKTI9qbHfATtEr9K-rRM3vzRD6reg-216ATlvOybj368nUyGnd0TG9wX6JE0zYXlxsz1-B4J__SZRbEIEWYM9MR-WTPEDSyyUjUrJU80UJB4AGYWC2_VGyubJoGAyLLgNicpDQVVxnpLraZLjOjs_1pB3sc9QZCtinVn5YNiDcVeE1nAONB9lyKNK91PIBAOjRJ0_dfxyRB4JHjKdA4m9Ot2beIpEbHV0zty0IQna88UUz_drC1rasqi-jDuLfZPN1E6gxQ5yYtM2ZcuuJSGTjXwaHNorRdyfRQRTvYrsRc5BmFks9SdzJ24FgTNuHpd3DFgLhDSsQN3G1nQH7WALAGKNg04uZP1Ft8c6tuRQ9ZMOlrm9lnuzzc6PNV2C2Sg1bddDHzpbM_fZrS7V_1k839byzQCzQ8HlyXaMKMsooNnlppZu3HLRokXghb30rhBPavr_u6c7Iz4TKbZ82SS4JGQalSC1t8ZPs0eapepD18WZFa597BPxNI13uwRiDVLafLqcR2Ru3adY2WGBlt2GZTHyerLaEo5u0IzP8GUJDpL6treYPN_05qzfNAF-eoH3KoqTF-_Qj63CZoGu9Ev112rZVHQiEeIRXnol2qfJj5rPSuPcGjEn4VTSkXTfeqXfhfnd-uwZirR-3zvdUEbfP6607W8vhZhoYgcSW8JcLL7uFCaE-zRTUU0whpGjRqIg2wx1ZKdbj0YsQFGHYf89Bbjvh0HUJrfzkaL51ze_b9LNzdAC-ZvTFclfKS2KIKJEn95YLCBjJh0wzG0zO8CZ0EhzwWAzucGsgavIV5smIwb_Ik0szWlbTlsrSlmcG77PpSSVezKUptmyesuqkZ0Dz

### Tool call: execute
{"command": "python - <<'PY'\nimport csv, json\nfrom datetime import datetime, timezone\nfrom decimal import Decimal, ROUND_HALF_UP\nfrom pathlib import Path\n\nsrc=Path('workspace/sales.csv')\nrows=list(csv.DictReader(src.open(newline='')))\nseen=set(); dedup=[]; dup=0\nfor r in rows:\n    oid=r['order_id']\n    if oid in seen:\n        dup += 1\n        continue\n    seen.add(oid); dedup.append(r)\n\nregion_map={x:x.title() for x in ['north','south','east','west']}\ndef parse_dt(s):\n    if '/' in s:\n        dt=datetime.strptime(s,'%d/%m/%Y').replace(tzinfo=timezone.utc)\n    elif 'T' not in s:\n        dt=datetime.strptime(s,'%Y-%m-%d').replace(tzinfo=timezone.utc)\n    else:\n        dt=datetime.fromisoformat(s.replace('Z','+00:00')).astimezone(timezone.utc)\n    return dt\n\ndef cents(s):\n    return int((Decimal(s)*100).quantize(Decimal('1'), rounding=ROUND_HALF_UP))\nknown=[]; missing=set(); totals={x:0 for x in ['North','South','East','West']}\nfor r in dedup:\n    reg=region_map[r['region'].strip().lower()]\n    dt=parse_dt(r['date'])\n    amt=None if r['amount'].strip() in ('-999','') else cents(r['amount'])\n    if amt is None:\n        missing.add(r['order_id'])\n        continue\n    known.append({'order_id':r['order_id'],'date':dt.strftime('%Y-%m-%dT%H:%M:%SZ'),'region':reg,'amount':amt})\n    totals[reg]+=amt\nstart=datetime(2024,1,1,tzinfo=timezone.utc); end=datetime(2024,3,31,23,59,59,tzinfo=timezone.utc)\nnq1=sum(x['amount'] for x in known if x['region']=='

### Tool result
{
  "north_q1_revenue": 313024,
  "north_q1_orders": 10,
  "top_region": "North",
  "missing_amount_orders": 8,
  "duplicate_rows_removed": 7,
  "meta": {
    "source": "sales.csv",
    "rows_in": 101,
    "rows_used": 86
  }
}
totals {'North': 950447, 'South': 913624, 'East': 879082, 'West': 847568} distinct 94 missing {'S-1068', 'S-1033', 'S-1020', 'S-1002', 'S-1026', 'S-1067', 'S-1082', 'S-1059'}
{
    "north_q1_revenue": 313024,
    "north_q1_orders": 10,
    "top_region": "North",
    "missing_amount_orders": 8,
    "duplicate_rows_removed": 7,
    "meta": {
        "source": "sales.csv",
        "rows_in": 101,
        "rows_used": 86
    }
}
clean rows 86

[Command succeeded with exit code 0]

### Assistant
[{'id': 'rs_06540952ce1ad06d016ac487a527e481919b04a8fcc2d0c0f1', 'summary': [], 'type': 'reasoning', 'content': [], 'encrypted_content': 'gAAAAABqxIeo2-TRjGM8kHkKjHpraWwboxTJ5j3RyZ6O41VdDEIvW4MQ-Qjg53xok_n-H0HFhLRR1cDGRldyEkM2wGFHTeLXSWw-mc8Inp2n3vAfAHJBxVnhQqraIXBo8TE4TAeIZMuFcmq79RAiw7_6WyMibuc9JtEQ99SLKifTJe7gSL-7Mz9TGSzSDQ-g01CYGYdyXVdElI4qpOYRQMR_ZN6U17bcj4e1o6zCe3CrqObQXiXuack3chC6-vXHmf5dRTuLehcB6zXV3TkVExWqDoG6mJdu3gzHZ_KFDWxLplIuEtf2cla-PxBiXoMKGGEhaBjfkUNOPTE5ShArSs7UNvA6yrRSf8LqOsYFO1Ag2CRW_44q7MUJ0Ra8AU6jQ3BOiKO0Hn3oliTPyPrlwKSSN7DWMOQ5sBS80CRTAkJUQ3kVGnr6l7Mcguu0e2AK8sA2JnoBMnGXCFhdbe9BO4-849oTstaQx8j5RKV2IjZk0cfWX0OVrg7I2fcEphZu-NQ2daYx2uMAk8jDhnuv0PjIIxRIyb3_Qiz0Y9Tgb2LOAXfmXlpfH5gavIgpivoY9FdRZWDGB-60h-rHILzC8i8bgUUHd6C0pz8HWcVJVq0WekKdbAVb5IuNT5Qe9-NinVdtpSWxzcOQ4Q-DPQ9N7JTQWYDl3ZXOurGu5er7wh09ZH6w_4BtxmHJLWW3kf0sQ9Nim-ZD0rSb3qQU-tGeDRPIXCIoDv7YEhgaZPwO4zxq19gIHNQ6aSlZulB1RmTPyEUICAsHEn-G0lkQVuYuQmMUQvzMidIGEIpkd0tHTJyCjv40TgUGBM-PSSxATZt7BbjJpFvt60VR-IBbSbUlF95-FyT6qgzUbsdtS7EpS3slo2nf0rRurTqs2os2_Dl5RIJ4Y1I30gf_Bcpy9FzsMbz-h30r6E_fkgXLXeLKO-fqIstprxvr-Hqow_UR6fZP0WtrKa75ArOkPbyVb_yU3DuDCn6e4H5RM5RNzTiwr11b8TmkZamqu6rZmcDgX4Ny-NxquiYn3BcCX3fhr2GQL1q1hOpralf7S8Bhq1SipwKO8u8727Sup_GjZZqH7sLiGrc_bqexQ0MBNBcRSME43r8srJTNZTCCULhDG9P7VGmWgqp6HaWbUsV9yqnnuhLfmvduf03-fi75vtV3tZg7nKAngmmgi8ovQpLDkv6aARwvT0QhCyDz1rLPEI6_bRAYwFLUE0xqKeb3FHjFywpb1PMZbNE6IJywQX-Qv81ITFDzSEc31-tRjgiDLLGhrxmqxH4XKaAbdkvfUF7gdn5Aqjs-Ng1ue9G4YNOUsimYKCCraFLr5mwM6kdArPdtxv_DaMgV3brBKpZsFeiWjX

### Tool call: execute
{"command": "python - <<'PY'\nimport csv\nfrom datetime import datetime,timezone\nwith open('workspace/clean.csv') as f:\n rows=list(csv.DictReader(f))\nfor r in rows:\n d=datetime.fromisoformat(r['date'].replace('Z','+00:00'))\n if r['region']=='North' and datetime(2024,1,1,tzinfo=timezone.utc)<=d<=datetime(2024,3,31,23,59,59,tzinfo=timezone.utc): print(r)\nPY", "timeout": 120}

### Tool result
{'order_id': 'S-1022', 'date': '2024-02-09T00:00:00Z', 'region': 'North', 'amount': '37922'}
{'order_id': 'S-1015', 'date': '2024-03-01T00:00:00Z', 'region': 'North', 'amount': '16016'}
{'order_id': 'S-1025', 'date': '2024-01-20T21:00:00Z', 'region': 'North', 'amount': '20028'}
{'order_id': 'S-1057', 'date': '2024-01-20T00:00:00Z', 'region': 'North', 'amount': '57947'}
{'order_id': 'S-1055', 'date': '2024-03-04T00:00:00Z', 'region': 'North', 'amount': '64128'}
{'order_id': 'S-1051', 'date': '2024-01-12T00:00:00Z', 'region': 'North', 'amount': '30086'}
{'order_id': 'S-1039', 'date': '2024-03-31T22:00:00Z', 'region': 'North', 'amount': '31772'}
{'order_id': 'S-2001', 'date': '2024-03-31T19:00:00Z', 'region': 'North', 'amount': '8025'}
{'order_id': 'S-1056', 'date': '2024-03-23T00:00:00Z', 'region': 'North', 'amount': '42600'}
{'order_id': 'S-2003', 'date': '2024-01-01T02:00:00Z', 'region': 'North', 'amount': '4500'}

[Command succeeded with exit code 0]

### Assistant
[{'id': 'rs_06540952ce1ad06d016ac487adac088191a5b58b9ecd859cd8', 'summary': [], 'type': 'reasoning', 'content': [], 'encrypted_content': 'gAAAAABqxIevvffiHg74K-C98Wz0tvFB50nuocA55XVzzKDKCtNtF1Gvd-aiDgpEhhJyl-C-zM-2oHxZtYlx8cqXwPKoyp4hD2RWvrAjT-3XVUQuPPPZzmFywuVITheecm3A0aUhFFRS7_Gc4BPfptOM8Vuzt3Ooh_GaBrPwq9cHByicZqu8WVqCNugxNwqbrNYERFrrxhNvzktpUfNQOiYbKB5G9kokIcO4N-r_y-hA5btYiP4anKbuOqrzUE-UVbP7QUuwxK27n2SYi68tXid0YCr3cv9bajDTBviJ2SE9DGsuS3VV9J11jOoSxNyJqfXP6nGIeO5LV1jDI4iTMTAmGeHFc_aCb_nYl_Ylh2tf_Ov4MroEwB0a1OKxce2Fk6FgHuSDqdfA2fH5tLb-KLspNDE4prp0WwffhtL0VgE-1eXn_4wyF9J7_tBIWU_YIGfEKJy8D_mzRBbHCD_hkx63gU_hKySOFn9CWuyu85OphJZUz4EbXpvWsrADIbW8Aq7bV8zaaPOR5TPaUqBTsOminPjuRkS6cNQnKMF08EL5wsZhiOhRWoZsaxldCvOC_jgRDjOzrIAsvRid1jez-BXcC12ZOEQZOHUlVTRdOVuQJmcDmPJzxEikpRHZH3IYjBlDqGc4ChBMZ_tlbGIQ7KnMiUbnS8ucBreIn_z2AyxyPHVzu7RsslzxzZ2KlMs6ZlEzZP9PxjaOXl3VM_elgTp7I5t1NsAcGWtjksWKIUAzkB3xjuX2vhllTBMaJzatdD6hcONh_uwgeKw_Q8u4Z6NOhfnTWeVgLOpjJWl5wN4qWiaEdEkvsuRjNB4kNG0U-wjNjq4Tk1AN6_3hV5hWnYJCNUqZsyELifUBdQer8JyDFRfa0Zvt7ujgFNASnCE8DQ1TB_zC0lzyejjlGD3h57rAQXdeoFpD7OfgpYwNiI-UXfjiaVPTAuloywxrBW-lgoJI603_o-S_adAp8ymvU2fOr8jmXsC8XMwoPD-WcJge5Sa4RE2rpnsP8RUkZbDHQJAVpkfYffwg8oozbnO_C4SnQChBoJkxTsES62sJLujrwm1VyngxSQzzmzqC7NApufJqdnBEBDAcQgC-CtPdOEX4TwP9T-ebE9CEYFQJSD0HuVovYyDDMVAba_cljepa_lhcL4OuyQeYXGq0vp3LrZH8C-PCD5fSVfCHRSN7nOwmDaeWNSazlPSvQcuY27Z4ZnhcHbbpLosgfkYV9kPYvWmaMOwjwSxDrMqVCoopIUiOnbJWEsPFd5Ew8SMst1hfNUTvrqJXY418E9HiUHsKTRGMQyVD6iWGMoj940R1CKu-UU6rNAB0VSY5typ4dMJG4QsNLBA9KxwwjMZSie