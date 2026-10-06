# Báo cáo Lab: Self evolving Agentic

> Sao chép tệp này thành `report/REPORT.md` (đã làm ở Phần 0) và điền dần qua các Phần của lab. Xóa các dòng hướng dẫn dạng trích dẫn (bắt đầu bằng `>`). Văn phong kỹ thuật, ngắn gọn, mọi nhận định đi kèm số liệu hoặc bằng chứng. Trong buổi học: điền mục 1 đến 7 (bản nháp). Sau buổi học: hoàn thiện mục 8 đến 10.

## 1. Thông tin nhóm và cấu hình

| Họ tên | Mã sinh viên | Phần đóng góp |
|---|---|---|
| NguyenNhanSam | 2A202602672 | Thực hiện cá nhân: harness, thí nghiệm và báo cáo với hỗ trợ của Codex; tiến độ và bằng chứng được lưu trong report/PROGRESS.md. |

- Mô hình thực tế: `gpt-6-luna`, API smoke trả `OK` (16 token, lưu tại `report/api-smoke.json`). `LAB_TEMPERATURE=0`, đã kiểm tra giá trị thực tế `0.0`; `recursion_limit=60`.
- Môi trường đã kiểm tra: Docker Linux trên Windows, Python `3.12.15`, Deep Agents `0.7.21`, LangChain `1.4.3`, langchain-core `1.6.6`, langchain-openai `1.6.7`, pytest `9.1.1`. Phiên bản thực tế được lưu trong `report/environment.json`.
- Kế hoạch bắt buộc: 21 lượt tác vụ và gọi curator; có thêm một lượt code-learn phải chạy lại vì CRLF của Windows. Số lượt/token thực dùng được chốt ở báo cáo cuối.
- Tag `freeze`: chưa tạo; chưa chạy tác vụ đánh giá.

## 2. Giả thuyết (commit TRƯỚC tag `freeze`, Phần 4.0)

> Dự đoán điều kiện nào đạt điểm cao nhất trên **tác vụ đánh giá** và vì sao. Nêu căn cứ từ phân loại lỗi (mục 4) và từ tài liệu tham khảo. Điền cả ba dòng; `verify_freeze.py` kiểm tra điều này.

- H1 (subagents so với baseline): Trên eval, mức tăng điểm trung bình không quá 0,10 (10 điểm phần trăm), nhưng token trung bình ít nhất 1,5 lần baseline. Trên learn, hai điều kiện đều đạt 18/18 check kỹ thuật và 0/9 quy ước, trong khi subagents tốn 2,13 lần token; thêm đồng đội không tự cung cấp quy ước còn thiếu. Hướng dẫn [02_subagents](../guides/pseudocode/02_subagents.md) giải thích ngữ cảnh tách biệt và overhead giao việc; đây là căn cứ định tính từ tài liệu môn học.
- H2 (skills-auto so với baseline): Trên eval, skills-auto tăng điểm trung bình ít nhất 0,15 so với baseline nhờ chuyển các quy ước dùng chung đã học; dự đoán đây là điều kiện có điểm cao nhất, nhưng không đạt tất cả check quy ước mới. Dev learn đạt 18/18 check kỹ thuật và 7/9 quy ước; skill dữ liệu bỏ sót header và chưa làm rõ filename. [SkillsBench README](https://github.com/benchflow-ai/skillsbench) mô tả việc đo hiệu quả skill và hành vi dùng skill, không bảo đảm skill nào cũng hữu ích; [05_skill_quality](../guides/pseudocode/05_skill_quality.md) phân biệt chọn đọc và làm theo.
- H3 (tác vụ học so với tác vụ đánh giá): Gọi G_learn = mean(skills-auto learn) - mean(baseline learn), G_eval tương tự trên eval. Dự đoán G_learn > G_eval vì curator chỉ có phản hồi learn và quy ước mới có thể không nằm trong skill. Dev đang cho G_learn = 0,252778, nhưng sẽ dùng lượt learn chính thức sau freeze để kiểm định; đối chiếu dev/chính thức của cùng hash để đo nhiễu. [04_curator](../guides/pseudocode/04_curator.md) cảnh báo tổng quát hóa/quá khớp; không dùng nội dung hay kết quả eval khi viết dự đoán này.

## 3. Làm quen Deep Agents (Phần 0.3)

Đã chạy `scripts/tour.py` bằng mô hình giả, không gọi API; đầu ra nguyên bản ở `report/deepagents-tour.txt`.

1. Công cụ thực tế được cung cấp: `ls`, `read_file`, `write_file`, `edit_file`, `delete`, `glob`, `grep`, `execute`, `task`. Công cụ `execute` chạy lệnh shell; `task` giao việc cho subagent.
2. Subagent `general-purpose` dùng để nghiên cứu, tìm tệp/nội dung và thực hiện công việc nhiều bước; có cùng các công cụ với tác tử chính. Mỗi lần gọi mặc định là phiên không lưu trạng thái: chỉ nhận prompt được giao và trả một báo cáo cuối, không tự thấy toàn bộ hội thoại của tác tử chính.
3. System prompt mặc định trong tour là chuỗi rỗng `''`. Trích từ mô tả `task`: "Each invocation is stateless by default: the agent sees only the prompt you give it and returns a single final report." Trích từ mô tả `execute`: "Quote paths containing spaces (e.g. cd \"/path/with spaces\")." Khi dựng agent của lab, `BASE_PROMPT` vẫn được giữ nguyên và bổ sung quy ước đường dẫn tương đối dùng chung cho file tool và shell.

## 4. Đường cơ sở và phân loại lỗi (Phần 2.2)

Baseline tập học: code-learn **7/10**, data-learn **5/8**, logs-learn **6/9**; trung bình **0,663889**. Toàn bộ **18/18 check kỹ thuật đạt**, **0/9 check quy ước đạt**. Bảng từng check và trích `detail` được lưu tại `report/learning-error-taxonomy.md`.

Cả chín lỗi đều thuộc nhóm E: quy ước tổ chức không được nêu đầy đủ trong đề. Các lỗi gồm type hints/test hồi quy/changelog; đơn vị tiền/metadata/bảng dữ liệu sạch; chuẩn hóa tên service/sắp xếp/header schema. Skill có thể lưu lại các quy ước được phản hồi này. Tỷ lệ kỹ thuật 18/18 là bằng chứng phủ định cho nhóm A–D trong phạm vi check; không khẳng định mọi quy trình của tác tử đều tối ưu.

Lưu ý môi trường: lượt code-learn đầu đạt 6/10 nhưng check `tests_not_modified` trượt chỉ vì CRLF trong checkout Windows. SHA bản Git LF đúng hash mà checker yêu cầu; tác tử không sửa test trong trace. Đã tái hiện bằng tác tử giả không thay đổi tệp, rồi chuẩn hóa CRLF→LF chỉ trên bản sao `.py` trong sandbox và chạy lại riêng code-learn. Lượt đầu giữ nguyên tại `results/archive/baseline-pre-lf/code-learn`, không dùng lỗi này trong taxonomy. Nguồn, dữ liệu và skill trong repo không bị sửa; cùng chuẩn hóa được áp dụng cho mọi điều kiện.

## 5. Điều kiện `subagents` (Phần 2.3)

- Các subagent đã định nghĩa: `explorer` đọc đặc tả, docstring và định dạng dữ liệu để tìm yêu cầu/trường hợp biên; `reviewer` kiểm tra độc lập đầu ra và các tuyên bố hoàn thành bằng tệp/test thật. Tác tử chính thực hiện thay đổi. Hai vai trò được giới hạn không sửa tệp bằng prompt, không phải cơ chế phân quyền cưỡng chế.
- Lý do thiết kế: bổ sung đọc đặc tả và kiểm chứng mà không tạo thêm một tầng implementer cho tác vụ nhỏ. Description chỉ rõ khi gọi; lời giao việc phải có đầy đủ quy tắc và đường dẫn.
- Tập học có giao việc thật: code-learn gọi hai lần (`general-purpose`, `reviewer`); data-learn gọi một lần (`explorer`); logs-learn gọi hai lần (`explorer`, `reviewer`). Trích nguyên lời giao việc ở `report/subagent-learning-evidence.json` và trace tương ứng.
- Điểm bằng baseline trên cả ba tác vụ. Token trung bình tăng từ 32.714,33 lên 69.739,00 (2,13 lần); thời gian trung bình từ 47,43 lên 109,23 giây (2,30 lần). Giao việc hỗ trợ hoàn thành yêu cầu kỹ thuật nhưng không cung cấp các quy ước Acme còn thiếu.
- Ngữ cảnh có thiếu: lời giao data cho explorer không liệt kê năm khóa đầu ra hoặc khoảng thời gian UTC; tác tử chính phải giữ/kiểm tra những yêu cầu đó. Lời giao log cho reviewer liệt kê hầu hết quy tắc kỹ thuật nhưng gợi ý “preserving source order” trong khi phản hồi Acme yêu cầu sắp xếp theo service/thời gian. Đây là ví dụ suy đoán quy ước khi chưa có phản hồi, không phải bằng chứng reviewer đã thấy quy tắc ẩn.

## 6. Self-evolving: skill do curator sinh (Phần 3)

- Curator chạy một lần thật bằng `python -m lab.curator`; không chạy lại, không xóa hoặc sửa tay skill. Nguồn là ba baseline learn, không gồm lượt lỗi CRLF đã lưu trữ. Provenance và SHA từng tệp ở `report/curator-provenance.json`.

| Skill | Tổng quát hay riêng cho tác vụ học? | Đúng hay sai (nêu chỗ sai nếu có) | Độ dài, `description` và `skills_read` ở Phần 3.4 |
|---|---|---|---|
| `typed-regression-maintenance` | Quy trình sửa nhiều lỗi: annotation, test hồi quy và changelog; không chứa tên package/hàm/đáp án riêng. | Khớp ba quy ước code trong phản hồi. `tests/test_regressions.py` và `CHANGELOG.md` là tên theo quy ước được phép giữ. | 12 dòng, body 8 dòng. Description nói “typed package”, có thể hẹp hơn một package chưa typed; Dev đọc 1 skill tương ứng và đạt cả ba check quy ước. |
| `normalized-tabular-output` | Khái quát cho báo cáo đơn hàng trong quy ước đã học; vẫn giới hạn vào region North/South/East/West. | Giữ cents, UTC và meta; chưa ghi rõ header bốn cột của clean.csv nên có nguy cơ áp dụng thiếu. Dev đạt money_in_cents nhưng trượt meta_block (source chứa workspace/ thay vì filename) và clean_csv (header dùng date/amount). | 17 dòng, body 13 dòng; description rộng về chuẩn hóa/deduplicate tabular data; dev skills_read=1, làm theo một phần. |
| `structured-log-triage` | Quy trình parsing log, normalize service, sort và schema; không chứa tên tệp log nguồn hay đáp án. | Khớp phản hồi schema_version=2/generated_by=log-triage, normalize và sắp xếp. Các hằng này là quy ước, không phải kết quả tính toán. | 15 dòng, body 11 dòng; description rõ tình huống chuyển log thành báo cáo lỗi; dev skills_read=1, đạt ba check quy ước. |

## 7. Kết quả so sánh (Phần 4.3, 4.4)

> Dán nội dung `report/table.md` và kết quả `python scripts/check_breakdown.py`. Nêu các lần chạy có `error` hoặc `skills_modified = true` (nếu có) và cách xử lý.

```text
(dán bảng ở đây)
```

## 8. Phân tích

> Trả lời từng câu bằng số liệu từ mục 7 và bằng chứng từ vết. Kết quả âm hoặc không có khác biệt vẫn hợp lệ nếu được phân tích tốt.

1. So với `baseline`, điều kiện nào cải thiện điểm tác vụ **học**? Điều kiện nào cải thiện điểm tác vụ **đánh giá**? Có điều kiện nào cải thiện tác vụ học nhưng không cải thiện tác vụ đánh giá? Nếu có, đó là dấu hiệu gì?
2. Tách điểm thành check kỹ thuật và check quy ước (`rule_`). Skill do curator sinh giúp nhóm check nào? Check quy ước **mới** của tác vụ đánh giá có được skill giúp không, và vì sao?
3. Dựa vào vết và `skills_read`, giải thích một check mà skill giúp đạt và một check mà skill không giúp (skill chưa được đọc, đọc nhưng không làm theo, skill thiếu hoặc sai).
4. Chi phí: so sánh số token trung bình giữa các điều kiện. Điều kiện nào có hiệu quả tốt nhất theo điểm trên mỗi token? Đa tác tử có đáng chi phí trong thí nghiệm này không?
5. Có dấu hiệu rò rỉ dữ liệu hoặc quá khớp nào trong skill sinh ra không? Nhóm đã phòng tránh như thế nào?
6. Nhiễu: so sánh điểm tác vụ học của cùng bộ skill ở Phần 3.4 (đã sao lưu) và sau đóng băng. Chênh lệch bao nhiêu? Nó cho biết điều gì về độ tin cậy của các chênh lệch trong bảng ở mục 7?

## 9. Hạn chế và tính hợp lệ

> Nêu ít nhất 3 hạn chế và ảnh hưởng của từng hạn chế đến kết luận (ví dụ: chỉ 3 tác vụ mỗi vai trò, mỗi cấu hình chạy một lần, nhiễu của mô hình, tác vụ do giảng viên thiết kế sẵn quy ước, chỉ một mô hình).

1.
2.
3.

## 10. Kết luận

> Tối đa 5 câu. Chỉ khẳng định điều số liệu hỗ trợ. Nêu một đề xuất cải tiến tiếp theo.

## Phụ lục

- Lệnh đã chạy (theo thứ tự):
- Thử thách mở rộng (nếu có): hướng chọn, kết quả, nhận xét.
- Ghi chú khác:

### Checkpoint trước freeze

Đã thử đúng bộ skill cuối trên ba learn: 10/10, 6/8, 9/9; mean=0,916667, technical=18/18, quy ước=7/9. Kết quả bảo toàn trong results/skills-auto-dev; hash Linux 648e0f3ab02acb02cb940dc4a0d83d07210b0bafb71f7f9a67780867a614fa86. Chưa chạy hoặc phân tích eval. Ba giả thuyết ở mục 2 được đăng ký trước; sẽ giữ nguyên sau khi có kết quả.
