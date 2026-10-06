# Phân loại lỗi baseline trên tập học

| Tác vụ | Check thất bại | Nhóm | Bằng chứng detail |
|---|---|---|---|
| code-learn | `rule_type_hints` | E | RULE: every public function (name not starting with '_') in the package has type annotations on all parameters and on the return value. |
| code-learn | `rule_regression_tests` | E | RULE: add tests/test_regressions.py with one test function per bug you fixed (at least 3); the file must pass. |
| code-learn | `rule_changelog` | E | RULE: record each fix in CHANGELOG.md under the heading '## Unreleased' as a bullet '- fix(<function name>): <short description>' (at least 3 bullets). |
| data-learn | `rule_money_in_cents` | E | RULE: money values in answer.json are integer cents (1606.67 USD is written 160667). |
| data-learn | `rule_meta_block` | E | RULE: answer.json has an object `meta` = {"source": <input file name>, "rows_in": <number of data rows in the input file, duplicates included>, "rows_used": <number of distinct orders with a known amount>}. |
| data-learn | `rule_clean_csv` | E | RULE: write workspace/clean.csv with the header order_id,timestamp_utc,region,amount_cents; one row per distinct order with a known amount; timestamp_utc as YYYY-MM-DDTHH:MM:SSZ (UTC); region in canonical spelling (North, South, East, West); amount in integer cents. |
| logs-learn | `rule_service_names` | E | RULE: service names in the output are lower-case with '-' replaced by '_' (payment-service -> payment_service). |
| logs-learn | `rule_sorted_errors` | E | RULE: `errors` is sorted by service, then by timestamp_utc, ascending. |
| logs-learn | `rule_schema_header` | E | RULE: the top-level object has "schema_version": 2 and "generated_by": "log-triage". |

Nguồn: `results/baseline/<task>/run.json`, trường `checks`. Sau khi sửa CRLF trong bản sao Python, 18/18 check kỹ thuật đạt và 0/9 check quy ước đạt. Lỗi tập trung nhóm E: thiếu quy ước tổ chức trong đặc tả visible; thêm đọc kỹ hay đồng đội không tự tạo được tri thức chưa có. Đây là bằng chứng phủ định trong phạm vi bộ check đối với A–D (đọc đặc tả, tìm caller, sửa lỗi, xử lý kỹ thuật), không chứng minh toàn bộ quy trình tác tử đều tối ưu; không có bằng chứng check thất bại thuộc F/G trong ba lượt hợp lệ.

Lượt code-learn trước sửa CRLF lưu tại `results/archive/baseline-pre-lf/code-learn`. Lỗi `tests_not_modified` của lượt này do checksum CRLF/LF, đã tái hiện bằng tác tử không sửa tệp; không đưa vào taxonomy lỗi tác tử.
