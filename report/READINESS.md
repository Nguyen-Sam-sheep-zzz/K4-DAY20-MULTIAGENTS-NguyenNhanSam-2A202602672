# Đối chiếu bài nộp với rubric

Kiểm chứng cục bộ ngày 06/10/2026. “Đạt” dưới đây nói về bằng chứng đã có; điểm cuối do giảng viên chấm. Không đồng nhất phần trăm điểm agent với điểm môn học.

| Dòng rubric | Trạng thái | Bằng chứng |
|---|---|---|
| 1. Agent/backend (10đ) | Đạt | 9/9 test_02; shell không kế thừa biến API, path hợp đồng đúng. |
| 1. Runner (12đ) | Đạt | 6/6 test_03; đủ record, sandbox, usage, errors/hash/counts. |
| 1. Curator (8đ) | Đạt | 2/2 test_04; role learn/detail/validate; không gọi khi không failures. |
| Điều kiện provided | Đạt | 12/12 test_01; 29/29 toàn bộ tests cuối, offline-final.xml. |
| 2.1 Baseline đủ 6 bài (4đ) | Đạt | 6 run.json + 6 trace.md, không error. |
| 2.2 Taxonomy (10đ) | Đạt | REPORT mục 4, 9 check lỗi E có detail; 18/18 kỹ thuật là bằng chứng phủ định A–D. |
| 3.1 Thiết kế subagent (3đ) | Đạt | Explorer/reviewer, description/system_prompt rõ; báo cáo phân biệt thiết kế và hành vi lệch role. |
| 3.2 Kết quả subagents (3đ) | Đạt | 6 run.json + 6 trace.md. |
| 3.3 Phân tích giao việc (4đ) | Đạt | Mục 5, chín delegations thật, tên vai trò/ngữ cảnh thiếu/token. |
| 4.1 Skill do curator sinh (5đ) | Đạt | 3 SKILL.md hợp lệ, curator-provenance.json; một call, không sửa tay. |
| 4.2 Chất lượng skill (5đ) | Đạt | Mục 6: tổng quát/đúng-sai/độ dài-description cho từng skill; nêu header/region/severity bị thiếu hoặc hẹp. |
| 4.3 Kết quả skills-auto (3đ) | Đạt | 6 run/trace; freeze-verification.txt: checked 6 runs ... OK. |
| 4.4 Đọc/làm theo skill (3đ) | Đạt | Mục 6/8.3; code áp dụng rule, data đọc nhưng không làm đủ; skills_read khác nhau từng bài. |
| 5.1 Bảng so sánh (5đ) | Đạt | table.md từ lab.compare, audit tái sinh khớp; đủ 3 điều kiện/6 bài/hàng tổng hợp. |
| 5.2 Freeze (5đ) | Đạt | hypotheses 4c9cb63 trước freeze fc1f6dd; cùng hash, timestamp sau tag, skills_modified=false cả sáu lượt. |
| 6.1 Giả thuyết (4đ) | Đạt | H1–H3 cụ thể, căn cứ learn và tài liệu, giữ nguyên nội dung preregistered. |
| 6.2 Phân tích (8đ) | Đạt | Mục 8 đủ learn/eval, kỹ thuật/quy ước, trace, token, leakage, dev/frozen noise. |
| 6.3 Hạn chế (4đ) | Đạt | Mục 9 có sáu hạn chế và ảnh hưởng đến kết luận. |
| 6.4 Trình bày/tái lập (4đ) | Đạt | Đủ 10 mục, tour, model/tham số/phiên bản/commit; RUN_COMMANDS.md. |
| Phần thưởng mở rộng (+5) | Chưa làm, tùy chọn | Không có thêm 18 lượt 6e; không ghi nhận điểm thưởng. |
| Không sửa tệp cấm | Đạt | 53 đối chiếu SHA, AST bốn module; provided/tests/tasks/scripts và hằng/helper/chữ ký/docstring giữ nguyên. |
| Không lộ khóa | Đạt trong phạm vi scan | .env ignored/untracked, đối chiếu literal secret cục bộ; .dockerignore loại khỏi build context. |
| Số liệu khớp | Đạt | final-audit.json: 18 records/traces, table matching; final-metrics.json budget 22 lượt. |
| Push kho Git | Đã đẩy và đối chiếu remote | main và tag freeze có trên GitHub; đủ 18 cặp chính thức, báo cáo/table, không có tệp tổng quan trong cây hoặc lịch sử main. Xem publication.json. |
| Nộp LMS/đúng hạn | Chưa xác minh | Không thao tác LMS, chưa kiểm tra hạn nộp của lớp. |

## Tệp cần giao theo README

- Bốn module trong src/lab/.
- skills/auto/ nguyên bản.
- results/ đầy đủ chính thức và các lượt dev/archive dùng trong báo cáo.
- report/REPORT.md và report/table.md; giữ các bằng chứng phụ để kiểm chứng.
- Lịch sử Git có hypotheses commit và tag freeze. ZIP không đủ để chạy verifier.

## Kiểm chứng nhanh

Từ PowerShell, thực hiện các lệnh offline ở RUN_COMMANDS.md. Trên clone Windows mới, giữ LF khi clone theo RUN_COMMANDS.md và chạy hash/verifier trong Docker Linux. Không chạy lại curator hoặc ghi đè kết quả cũ.

Phần bắt buộc đã có trên **GitHub main cùng tag freeze**, đủ để nộp liên kết kho. Chưa nộp LMS hoặc xác minh hạn nộp của lớp.
