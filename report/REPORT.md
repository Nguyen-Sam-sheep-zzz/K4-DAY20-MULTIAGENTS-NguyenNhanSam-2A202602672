# Báo cáo Lab 20: Self-evolving Agentic

## 1. Thông tin và cấu hình

| Họ tên | Mã sinh viên | Đóng góp |
|---|---|---|
| NguyenNhanSam | 2A202602672 | Thực hiện cá nhân với hỗ trợ Codex: harness, thí nghiệm, kiểm chứng và báo cáo; người dùng cấu hình .env. |

Mô hình thực tế **gpt-6-luna**, temperature **0.0**, recursion_limit **60**, cùng cấu hình cho cả ba điều kiện. API smoke qua `make_model()` trả OK, 16 token. Docker Linux trên Windows: Python 3.12.15, Deep Agents 0.7.21, LangChain 1.4.3, langchain-core 1.6.6, langchain-openai 1.6.7, pytest 9.1.1 và Git 2.47.3. Phiên bản/cấu hình không chứa secret ở [environment.json](environment.json), [requirements-resolved.txt](requirements-resolved.txt), [api-smoke.json](api-smoke.json).

Đã chạy **22 lượt tác vụ**: 18 chính thức, 3 dev trước freeze, 1 code-learn lưu trữ do CRLF; cộng 1 lần curator và API smoke. Tổng token đo cho tác vụ **1.128.865**, trong đó chính thức 932.473, dev 151.624, lượt CRLF 44.768. Smoke thêm 16 token; **không có số token curator** vì CLI provided không ghi usage. Không coi tổng này là tổng chi phí tiền. Không thực hiện 18 lượt lặp tùy chọn.

Nhánh `feature/day20-self-evolving-agents`; hypotheses commit `4c9cb639906b0303c4fab523a9fdc4b5ee4d5d2d`; tag **freeze** tại commit riêng `fc1f6dd0ea21b585654ce281d334ee1c2cc03f86`, thời gian `2026-10-06T12:19:58+07:00`. Mọi eval bắt đầu sau commit/tag; skill nguyên bản không sửa, tag không di chuyển. [freeze-provenance.json](freeze-provenance.json) ghi sự cố Git CRLF và cách xử lý bằng cấu hình, không đổi byte skill. Bản nộp đã được đẩy lên GitHub `main` kèm tag `freeze` và đối chiếu remote; chi tiết ở READINESS.md và publication.json. Chưa nộp LMS.

## 2. Giả thuyết đăng ký trước freeze

Ba dòng sau giữ nguyên nội dung trong hypotheses commit; kết quả kiểm định được ghi riêng ở mục 8.

- H1 (subagents so với baseline): Trên eval, mức tăng điểm trung bình không quá 0,10 (10 điểm phần trăm), nhưng token trung bình ít nhất 1,5 lần baseline. Trên learn, hai điều kiện đều đạt 18/18 check kỹ thuật và 0/9 quy ước, trong khi subagents tốn 2,13 lần token; thêm đồng đội không tự cung cấp quy ước còn thiếu. Hướng dẫn [02_subagents](../guides/pseudocode/02_subagents.md) giải thích ngữ cảnh tách biệt và overhead giao việc; đây là căn cứ định tính từ tài liệu môn học.
- H2 (skills-auto so với baseline): Trên eval, skills-auto tăng điểm trung bình ít nhất 0,15 so với baseline nhờ chuyển các quy ước dùng chung đã học; dự đoán đây là điều kiện có điểm cao nhất, nhưng không đạt tất cả check quy ước mới. Dev learn đạt 18/18 check kỹ thuật và 7/9 quy ước; skill dữ liệu bỏ sót header và chưa làm rõ filename. [SkillsBench README](https://github.com/benchflow-ai/skillsbench) mô tả việc đo hiệu quả skill và hành vi dùng skill, không bảo đảm skill nào cũng hữu ích; [05_skill_quality](../guides/pseudocode/05_skill_quality.md) phân biệt chọn đọc và làm theo.
- H3 (tác vụ học so với tác vụ đánh giá): Gọi G_learn = mean(skills-auto learn) - mean(baseline learn), G_eval tương tự trên eval. Dự đoán G_learn > G_eval vì curator chỉ có phản hồi learn và quy ước mới có thể không nằm trong skill. Dev đang cho G_learn = 0,252778, nhưng sẽ dùng lượt learn chính thức sau freeze để kiểm định; đối chiếu dev/chính thức của cùng hash để đo nhiễu. [04_curator](../guides/pseudocode/04_curator.md) cảnh báo tổng quát hóa/quá khớp; không dùng nội dung hay kết quả eval khi viết dự đoán này.

## 3. Làm quen Deep Agents (Phần 0.3)

Đã chạy `scripts/tour.py` bằng mô hình giả, không gọi API; đầu ra nguyên bản ở `report/deepagents-tour.txt`.

1. Công cụ thực tế được cung cấp: `ls`, `read_file`, `write_file`, `edit_file`, `delete`, `glob`, `grep`, `execute`, `task`. Công cụ `execute` chạy lệnh shell; `task` giao việc cho subagent.
2. Subagent `general-purpose` dùng để nghiên cứu, tìm tệp/nội dung và thực hiện công việc nhiều bước; có cùng các công cụ với tác tử chính. Mỗi lần gọi mặc định là phiên không lưu trạng thái: chỉ nhận prompt được giao và trả một báo cáo cuối, không tự thấy toàn bộ hội thoại của tác tử chính.
3. System prompt mặc định trong tour là chuỗi rỗng `''`. Trích từ mô tả `task`: "Each invocation is stateless by default: the agent sees only the prompt you give it and returns a single final report." Trích từ mô tả `execute`: "Quote paths containing spaces (e.g. cd \"/path/with spaces\")." Khi dựng agent của lab, `BASE_PROMPT` vẫn được giữ nguyên và bổ sung quy ước đường dẫn tương đối dùng chung cho file tool và shell.


## 4. Baseline và phân loại lỗi

Baseline learn: **7/10, 5/8, 6/9**, mean **0,663889**; **18/18** check kỹ thuật đạt, **0/9** quy ước đạt. Baseline eval: **7/11, 5/9, 6/10**, mean **0,597306**; **18/18** kỹ thuật và **0/12** quy ước. Bảng lỗi chỉ sử dụng phản hồi learn:

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

Cả chín lỗi thuộc **E: vi phạm quy ước tổ chức** chưa được mô tả trong đề visible. Nguyên nhân chung là thiếu tri thức quy ước Acme; skill có thể lưu phản hồi này. 18/18 check kỹ thuật đạt là bằng chứng phủ định cho việc gán các check thất bại sang A–D, trong phạm vi bộ chấm; không chứng minh mọi bước tác tử đều tối ưu. Không có bằng chứng check thất bại thuộc F/G trong ba lượt hợp lệ. Bảng đầy đủ và nguồn ở [learning-error-taxonomy.md](learning-error-taxonomy.md).

Lượt code-learn đầu **6/10** có false failure `tests_not_modified`: checkout Windows là CRLF, còn hash checker là Git LF. Tác tử không sửa test; đã tái hiện bằng tác tử no-op. Runner chuẩn hóa **bản sao .py trong sandbox trước khi agent chạy** sang LF; không sửa repo, dữ liệu hay skill. Chạy lại riêng code-learn thành 7/10 và giữ nguyên lượt đầu tại `results/archive/baseline-pre-lf/code-learn`; data/log không có .py nên không cần retry. Không đưa lỗi hạ tầng này vào taxonomy hay nguồn curator; cùng quy trình chuẩn hóa dùng cho tất cả điều kiện.

## 5. Subagents: thiết kế và hành vi thực tế

Thiết kế hai custom roles: **explorer** đọc README/docstring/dữ liệu để tìm yêu cầu, edge case và caller; **reviewer** kiểm tra kết quả bằng tệp/test thật sau thực hiện. Description nêu lúc cần gọi và yêu cầu gửi đầy đủ quy tắc/đường dẫn. Mục tiêu là main agent thực hiện, hai vai trò đọc/kiểm tra; quyền không sửa tệp chỉ được mô tả bằng prompt. Built-in `general-purpose` vẫn có mặt.

| Tác vụ | Số lần giao việc | Vai trò được gọi | Token |
|---|---:|---|---:|
| code-learn | 2 | general-purpose, reviewer | 105.480 |
| data-learn | 1 | explorer | 45.399 |
| logs-learn | 2 | explorer, reviewer | 58.338 |
| code-eval | 1 | explorer | 76.600 |
| data-eval | 2 | explorer, general-purpose | 89.696 |
| logs-eval | 1 | explorer | 27.521 |

Giao việc thật có **9 lần** trên 6 bài. Learn bằng baseline về điểm nhưng token tăng **2,13 lần**, giây/lượt tăng **2,30 lần**; eval cũng bằng baseline và token tăng **1.90 lần**. Tất cả check kỹ thuật đạt, tất cả check quy ước trượt. Trong bộ việc này, đồng đội không cung cấp được các quy ước chưa xuất hiện trong ngữ cảnh.

Bằng chứng nguyên lời giao việc ở [subagent-all-evidence.json](subagent-all-evidence.json) và trace tương ứng:

- Data-learn chỉ giao “Inspect workspace README/data ... report required values” mà không liệt kê năm khóa output hay khoảng UTC cụ thể. Main phải giữ các yêu cầu đó; không suy luận thiếu ngữ cảnh này đã làm sai kỹ thuật vì điểm kỹ thuật vẫn đạt.
- Data-eval có hai lượt tính/kiểm tra, lượt sau bổ sung quy tắc giữ first event, chuẩn hóa category, missing sentinel và tháng UTC; token 89.696 so với baseline 21.489, nhưng vẫn 5/9.
- Logs-learn giao reviewer “preserving source order” dù quy ước ẩn cần sort service/time. Đây là suy đoán khi chưa có phản hồi, không phải reviewer biết quy tắc ẩn rồi cố ý bỏ qua.
- Code-eval giao explorer “You may implement changes”, trái ý định chỉ đọc. Báo cáo subagent nói đã sửa billing/schedule/timeutil và chạy 3 visible tests; bên trong subagent không nằm trong trace chính nên không thể xác minh từng thao tác nội bộ. Hành vi này cho thấy giới hạn role bằng prompt chưa bảo đảm được main/delegation tuân thủ. Giữ thiết kế và kết quả nguyên trạng trong thí nghiệm, không đổi sau khi thấy eval.

## 6. Skill tự sinh và chất lượng

Curator chạy thật **một lần** bằng `python -m lab.curator`, nguồn ba baseline learn hợp lệ. Hàm lọc role=learn và bỏ run.error, đưa failed name/detail cùng cuối trace ~6.000 ký tự, gọi model một lần, parse/validate trước khi ghi. **Không sửa tay, không xóa skill, không rerun curator.** [curator-provenance.json](curator-provenance.json) ghi SHA các nguồn và skill. Ba skill đều qua `validate_skill`, không chứa eval markers.

| Skill | Tổng quát hóa | Đúng/sai và giới hạn | Độ dài/description, việc đọc |
|---|---|---|---|
| typed-regression-maintenance | Sửa nhiều bug với annotation, regression và changelog; không chứa package/hàm/đáp án riêng. | Khớp ba quy ước learn; thiếu quy tắc mới bump version nên code-eval trượt rule_version_bump. | 12 dòng, body 8; description “typed package” hơi hẹp, nhưng cả code learn/eval đều đọc 1 skill và áp dụng đủ ba quy ước đã học. |
| normalized-tabular-output | Dedup, UTC, cents và meta cho tabular output. | Thiếu header clean.csv chính xác, filename chưa làm rõ basename; region North/South/East/West đặc thù learn và không khớp miền category của eval. Đây là giới hạn tổng quát hóa. | 17 dòng, body 13; description rộng. Dev đọc 1 skill, đạt 1/3 quy ước; learn chính thức đọc 1, đạt 2/3; data-eval đọc 2 skill nhưng 0/4 quy ước. |
| structured-log-triage | Normalize service, sort, repeat counts, UTC và schema của báo cáo log. | Khớp learn; giữ chỉ ERROR/CRITICAL quá hẹp cho eval có ERROR/SEVERE/FATAL. Agent eval dùng mức severity theo README nên vẫn đạt kỹ thuật; thiếu source_line nên quy ước mới trượt. | 15 dòng, body 11; description rõ xử lý log. Logs-learn đọc 1; logs-eval đọc cả 3 skill, trong đó 2 không cần cho việc này. Cả hai đạt ba quy ước đã học. |

Dev trước freeze: **10/10, 6/8, 9/9**, mean **0,916667**, kỹ thuật **18/18**, quy ước **7/9**. Lưu tại `results/skills-auto-dev`; không nhập vào bảng chính thức. Hash Linux cho dev và cả sáu run sau freeze giống nhau: `648e0f3ab02acb02cb940dc4a0d83d07210b0bafb71f7f9a67780867a614fa86`. Các dòng quy ước/tên file output là phản hồi Acme được phép giữ; chúng không phải đáp án tính toán.

## 7. Kết quả chính thức

Bảng sau được sinh nguyên bản bằng `python -m lab.compare`, lưu ở [table.md](table.md):

| Task | baseline | subagents | skills-auto |
|---|---|---|---|
| code-learn | 7/10 | 7/10 | 10/10 |
| data-learn | 5/8 | 5/8 | 7/8 |
| logs-learn | 6/9 | 6/9 | 9/9 |
| code-eval | 7/11 | 7/11 | 10/11 |
| data-eval | 5/9 | 5/9 | 5/9 |
| logs-eval | 6/10 | 6/10 | 9/10 |
| **Mean score - learning tasks** | 0.66 | 0.66 | 0.96 |
| **Mean score - evaluation tasks** | 0.60 | 0.60 | 0.79 |
| **Mean tokens per run** | 33,369 | 67,172 | 54,870 |
| **Runs that read a skill** | 0/6 | 0/6 | 6/6 |

Breakdown từ script provided, lưu ở [check_breakdown.txt](check_breakdown.txt):

```text
condition     role    technical  house rules  mean tokens  read a skill
baseline      eval     18/18         0/12          34,025      0/3
baseline      learn    18/18         0/9           32,714      0/3
subagents     eval     18/18         0/12          64,605      0/3
subagents     learn    18/18         0/9           69,739      0/3
skills-auto   eval     18/18         6/12          43,363      3/3
skills-auto   learn    18/18         8/9           66,376      3/3
```

Đủ **18 run.json + 18 trace.md** chính thức. Không run nào có `error` hoặc `skills_modified=true`. Verifier báo **checked 6 runs of skill conditions: OK**, lưu ở [freeze-verification.txt](freeze-verification.txt). Điểm trung bình là mean của tỷ lệ passed/total **từng tác vụ**, không lấy tổng check làm mẫu số chung. Bảng compare làm tròn điểm 2 chữ số và lấy phần nguyên mean tokens; [final-metrics.json](final-metrics.json) giữ giá trị đầy đủ.

## 8. Phân tích

### 8.1. Điểm và kiểm định giả thuyết

Subagents không tăng điểm learn hoặc eval. Skills-auto tăng learn **29.44 điểm phần trăm**, từ 66,39% lên 95,83%; tăng eval **19.09 điểm phần trăm**, từ 59,73% lên 78,82%. Chuyển kinh nghiệm rõ ở code (7/11→10/11) và log (6/10→9/10), nhưng data-eval giữ 5/9. Lợi ích trên learn lớn hơn eval **10.35 điểm phần trăm**, phù hợp chuyển giao chưa đầy đủ; chưa đủ bằng chứng kết luận quá khớp thống kê.

- **H1 được số liệu một lượt hỗ trợ:** gain eval=0,00≤0,10 và token ratio=1.8988≥1,5.
- **H2 được số liệu một lượt hỗ trợ:** gain eval=0.190909≥0,15; skills-auto điểm cao nhất và không đạt mọi quy ước mới.
- **H3 được số liệu một lượt hỗ trợ:** G_learn=0.294444>G_eval=0.190909. Đây là kiểm định trên mẫu nhỏ, không phải xác nhận phổ quát.

### 8.2. Kỹ thuật, quy ước đã học và quy ước mới

Mỗi điều kiện đạt **18/18 kỹ thuật trên learn và 18/18 trên eval**. Skill cải thiện quy ước: learn **0/9→8/9**, eval **0/12→6/12**. Sáu check eval đạt thêm đều là quy ước dùng chung: ba code và ba log. Ba quy ước mới (`rule_version_bump`, `rule_sorted_keys_format`, `rule_source_line`) đều trượt ở cả ba điều kiện, nên **0/3** quy ước mới. Không có quy tắc tương ứng trong skill và không có phản hồi eval để học thêm sau freeze.

### 8.3. Đọc skill và làm theo: bằng chứng cơ chế

Code-eval đọc `skills/typed-regression-maintenance/SKILL.md`, ghi `workspace/tests/test_regressions.py` với ba test, ghi `CHANGELOG.md` có `## Unreleased` và ba `- fix(...)`; cuối cùng chạy `PYTHONPATH=workspace python -m pytest -q` đạt 6 tests sau khi sửa lỗi import do thư mục chạy. Ba rule đã học đạt; `__version__` vẫn 1.4.2, rule_version_bump trượt. Trace [code-eval](../results/skills-auto/code-eval/trace.md) là bằng chứng cụ thể về chuyển quy trình, không chỉ dựa vào skills_read.

Data-eval đọc skill tabular **và** log (`skills_read=2`) nhưng trong lệnh execute vẫn ghi `march_revenue_utc: rev/100`, `meta.source: 'workspace/orders.json'` và `json.dump(..., indent=2)`. Lệnh chỉ tạo answer.json, không ghi clean.csv; thiếu sort_keys/newline đúng chuẩn. Do đó bốn rule trượt dù kỹ thuật đạt. Đây là trường hợp **đọc nhưng không làm theo đầy đủ**, cùng với skill thiếu header và quy tắc format mới; không thể quy toàn bộ thất bại cho description. Trace [data-eval](../results/skills-auto/data-eval/trace.md) chứa các đoạn này.

Data-learn dev ghi header `order_id,date,region,amount` và source `workspace/sales.csv`: hai rule trượt. Lượt chính thức sửa source thành `sales.csv`, meta đạt, nhưng vẫn trượt clean_csv. Header đúng đã có trong feedback learn nhưng bị curator bỏ sót trong skill. Logs-eval đọc 3 skill; lệnh execute dùng `{'ERROR','SEVERE','FATAL'}` theo đặc tả mới, normalize service, sort và thêm schema header, đạt 9/10. Skill không nói source_line nên trường mới vẫn thiếu. Không khẳng định việc đọc thêm skill không liên quan gây ra lỗi data; chưa có thí nghiệm cô lập nhân quả.

### 8.4. Token, thời gian và hiệu quả

| Điều kiện | Token/lượt learn | Token/lượt eval | Token/lượt (6 bài) | Giây/lượt (6 bài) | Điểm/triệu token (6 bài) | Điểm/triệu token eval |
|---|---:|---:|---:|---:|---:|---:|
| baseline | 32,714.33 | 34,025.33 | 33,369.83 | 45.98 | 18.90 | 17.55 |
| subagents | 69,739.00 | 64,605.67 | 67,172.33 | 97.85 | 9.39 | 9.25 |
| skills-auto | 66,376.67 | 43,363.33 | 54,870.00 | 54.37 | 15.92 | 18.18 |


Chỉ số “điểm/triệu token” = mean_score / mean_tokens × 1.000.000, dùng tỷ lệ điểm 0–1. Đây là tỷ số mô tả, không phải số tác vụ thành công hay chi phí tiền; token cached/input/output có giá khác nhau.

Trên toàn bộ sáu bài, baseline hiệu quả token cao nhất (**18,90**), skills-auto **15,92**, subagents **9,39**. Riêng eval, skills-auto **18,18** so với baseline **17,55**, một chênh lệch nhỏ; token tăng **1.27 lần** nhưng điểm tăng 19,09 điểm phần trăm. Curator/dev có chi phí khởi tạo chưa được khấu hao vào tỷ số eval; không tuyên bố tiết kiệm tiền. Với các tác vụ nhỏ này, subagents chưa đáng chi phí theo điểm đo được; không suy rộng cho nhiệm vụ lớn hơn hoặc có thể song song.

### 8.5. Quá khớp và rò rỉ

Nguồn curator chỉ là baseline learn hợp lệ; không mở đặc tả/checker riêng hoặc xem kết quả eval để thiết kế skill trước freeze. H1–H3 và skill được Git lưu trước eval. Validation chặn eval markers; nội dung skill không có ID/đáp án/con số kết quả eval. Bằng chứng provenance/hashes/tag hỗ trợ quy trình này, nhưng regex không chứng minh mọi dạng rò rỉ ngữ nghĩa đều không thể xảy ra.

Skill còn lệ thuộc region và severity của learn; data-eval thất bại dù đọc, trong khi code/log chuyển được quy ước dùng chung. Kết quả cho thấy **tổng quát hóa có chọn lọc** và lợi ích learn cao hơn eval, không chứng minh mô hình đã học mọi quy ước mới. Không sửa skill hay chạy lại curator để cải thiện điểm eval.

### 8.6. Nhiễu với cùng bộ skill

| Tác vụ học | Dev trước freeze | Chính thức sau freeze | Chênh điểm | Token dev → chính thức |
|---|---:|---:|---:|---:|
| code-learn | 10/10 | 10/10 | 0,000 | 70.681 → 61.316 |
| data-learn | 6/8 | 7/8 | +0,125 | 42.990 → 33.126 |
| logs-learn | 9/9 | 9/9 | 0,000 | 37.953 → 104.688 |
| Mean score | 0,916667 | 0,958333 | **+0,041667** | mean 50.541,33 → 66.376,67 |

Cùng hash, model và temperature=0 vẫn có lệch **4,17 điểm phần trăm** mean learn; riêng data lệch 12,5 điểm phần trăm. Token log tăng **2,76 lần** dù điểm không đổi: trace chính thức ghi counts_by_service ban đầu sai, tự kiểm chứng phát hiện 11 thay vì 13, sửa rồi gặp assertion dự đoán 24 thay vì 25 records, cuối cùng xác nhận đúng 25. Các bước phục hồi/tái kiểm tra làm tăng số call và lịch sử ngữ cảnh; không phải lỗi cuối cùng của harness. Hai lượt chỉ minh họa biến thiên, không phải khoảng tin cậy hay ước lượng nhiễu eval. Các chênh lệch nhỏ về hiệu quả token chưa đáng để khẳng định vượt trội ổn định.

## 9. Hạn chế và tính hợp lệ

1. **Mẫu nhỏ, một lượt chính thức mỗi cấu hình/tác vụ:** ba eval không đại diện miền công việc rộng, không kiểm định được ý nghĩa thống kê. Dev chỉ lặp learn; chưa đo noise eval.
2. **Một mô hình/cổng API:** gpt-6-luna ở temperature=0 vẫn biến thiên; kết luận phụ thuộc provider, công cụ và phiên bản thư viện. Không so mô hình khác.
3. **Quy ước do giảng viên thiết kế:** feedback learn nêu rõ rule, nên tăng điểm chủ yếu là truyền tri thức; không đồng nghĩa tăng năng lực suy luận trên dữ liệu thực ngoài lab.
4. **Quan sát chưa đầy đủ:** render_trace provided chỉ giữ luồng chính và cắt 1.500 ký tự/message; API trả content dạng list với encrypted reasoning làm phần text có thể bị cắt. Token có cộng subagent, tool/skill counts không bao gồm nội bộ subagent. Chỉ diễn giải những thao tác nhìn thấy được.
5. **Giới hạn chuyển giao/role:** skill tabular bỏ header, skill log có severity hẹp; prompt vai trò không cưỡng chế quyền không sửa. Tách chất lượng skill khỏi việc model đọc/làm theo, và không chỉnh chúng theo eval.
6. **Đo chi phí và môi trường:** curator usage không được ghi; token không quy ra tiền. Chuẩn hóa CRLF ở sandbox đã được áp dụng nhất quán và kiểm chứng, nhưng hash/path phụ thuộc nền tảng, cần chạy verifier trên Linux và giữ LF cho SKILL.md.

## 10. Kết luận

Skills-auto tăng điểm mean eval từ 59,73% lên 78,82%, chủ yếu nhờ chuyển ba quy ước code và ba quy ước log đã học.
Subagents không tăng điểm trong sáu tác vụ, dù token tăng khoảng gấp đôi baseline.
Đọc skill không đảm bảo làm theo: data-eval vẫn 5/9, và cả ba quy ước mới đều trượt.
Cùng bộ skill cho mean learn lệch 4,17 điểm phần trăm giữa hai lượt, nên chưa khẳng định cải thiện ổn định ngoài thí nghiệm nhỏ này.
Bước tiếp theo là lặp eval với budget riêng, giữ freeze, và ở một thí nghiệm mới cải thiện khả năng trích đủ convention và kiểm tra thực thi checklist.

## Phụ lục: tái lập và nguồn

- [RUN_COMMANDS.md](RUN_COMMANDS.md): lệnh PowerShell/Docker, thứ tự thực hiện, cách đọc kết quả không gọi API và cách tránh ghi đè.
- [final-metrics.json](final-metrics.json): số liệu đầy đủ và budget 22 lượt; [PROGRESS.md](PROGRESS.md): checkpoint.
- [offline-final.xml](offline-final.xml): 29/29 test gốc đạt; test provided dùng model giả, không đưa vào budget tác vụ thật. [source-integrity.json](source-integrity.json) và SHA manifest đối chiếu phạm vi được sửa.
- Chỉ có một retry code-learn do CRLF; giữ lượt đầu. Không retry eval, không sửa/xóa skill, không rerun curator. Không thực hiện phần 6e tùy chọn do đã hoàn thành phần bắt buộc; không tự mở rộng thêm 18 lượt API.
- Raw trace giữ nguyên cả whitespace và các lệnh lỗi đã phục hồi; không biên tập để làm đẹp bằng chứng. Code/skill/docs không có whitespace lỗi; kiểm tra khóa bằng đối chiếu literal .env cục bộ, không in giá trị.

Tài liệu tham khảo:

1. [SkillsBench official README](https://github.com/benchflow-ai/skillsbench), bản đọc ngày 06/10/2026 lưu ở [skillsbench-source.md](skillsbench-source.md): benchmark hiệu quả và hành vi sử dụng skill theo các workflow/skill-composition tasks. README đọc được không có kết quả bài báo để kiểm chứng các con số nghiên cứu.
2. Hướng dẫn môn học [02_subagents](../guides/pseudocode/02_subagents.md), [04_curator](../guides/pseudocode/04_curator.md), [05_skill_quality](../guides/pseudocode/05_skill_quality.md): context tách biệt, overhead, generalization/overfitting, description và đọc/làm theo. Hướng dẫn có dẫn SkillsBench/SkillEvolBench/Anthropic; các thống kê được dẫn ở đây **không coi là kết quả tự kiểm chứng**.
3. Các truy cập bài gốc khác gặp HTTP 403/429; không trích số liệu định lượng chưa xác minh. Giả thuyết dựa vào dữ liệu learn của lab và căn cứ định tính có nguồn; các kết luận định lượng chỉ dùng run.json của thí nghiệm này.
