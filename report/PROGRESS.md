# Tiến độ Lab 20

Ngày thực hiện: 06/10/2026. Nhánh: `feature/day20-self-evolving-agents`.

| Bước | Trạng thái | Bằng chứng |
|---|---|---|
| 0. Môi trường | Xong | Docker Python 3.12.15, Deep Agents 0.7.21, Git 2.47.3; tour và API smoke gpt-6-luna/temperature=0. |
| 1. Agent/subagents | Xong | 9/9 test gốc; explorer và reviewer; không kế thừa biến khóa trong shell. |
| 2. Runner | Xong | 6/6 test gốc; sandbox tạm, đo token/trace/hash, chuẩn hóa bản sao Python sang LF. |
| 3. Tập học | Xong | Baseline/subagents cùng 7/10, 5/8, 6/9; taxonomy 9 lỗi nhóm E. |
| 4. Curator và dev | Xong | 2/2 test gốc; 3 skill tự sinh, không sửa tay/không rerun; dev 10/10, 6/8, 9/9, cả ba đọc skill. |
| 5. Hypotheses/freeze | Xong | hypotheses `4c9cb63`, freeze `fc1f6dd`; Git verifier OK trước eval (0 run vì chưa chạy skills-auto chính thức). |
| 6. Đánh giá | Xong | 18 run/trace chính thức; verifier kiểm tra 6 skill runs: OK. Eval mean baseline/subagents 0,597306; skills-auto 0,788215. |
| 8. Mở rộng 6e | Xong | Đủ 18 run/trace bổ sung; thống kê 27 eval, kiểm tra riêng 6 skill runs bổ sung OK; 29/29 tests. Xem REPEATS_6E.md. |
| 7. Báo cáo và kiểm tra | Xong | Báo cáo đủ 10 mục; 29/29 tests cuối; bảng khớp compare; 53 hash tệp bảo toàn, skill và H1–H3 không đổi; quét secret OK. |

## Bảo toàn và môi trường

- `.env` người dùng đã điền; API hoạt động. Không có khóa trong tệp dự định commit (đối chiếu literal cục bộ, chỉ báo trạng thái).
- Toàn bộ 29 test gốc đạt trước freeze: `offline-prefreeze.xml`. Review độc lập bốn module không có finding cần sửa.
- SHA của tests/tasks/scripts/module provided và tài liệu đề không đổi. Thay đổi source chỉ ở TODO/import; constants, helper, chữ ký/docstring và CLI giữ nguyên.
- Lượt code-learn đầu 6/10 có false failure `tests_not_modified` do CRLF Windows, giữ tại `results/archive/baseline-pre-lf/code-learn`. Reproducer no-op chứng minh; runner chuẩn hóa bản sao Python trước agent; code-learn hợp lệ chạy lại, data/log giữ nguyên.
- Docker Git ban đầu báo README trong skills khác tag chỉ do CRLF; cấu hình repo `core.autocrlf=true` đồng bộ Windows/Linux làm verifier OK. Không sửa byte của skill hoặc di chuyển tag.
- Hash skill đo trên Linux: `648e0f3ab02acb02cb940dc4a0d83d07210b0bafb71f7f9a67780867a614fa86`.
- Raw trace có whitespace từ output công cụ; giữ nguyên bằng chứng. Kiểm tra whitespace của mã nguồn, skill và tài liệu riêng.
- Commit/tag đã tạo đúng quy trình; trạng thái gửi kho ở READINESS.md, chưa nộp LMS.

## Bàn giao

Phần bắt buộc hoàn thành cục bộ. Tổng 40 lượt tác vụ, 1.955.772 token đo; curator một lần chưa ghi token. Đã hoàn tất 6e thêm 18 lượt và 826.907 token theo yêu cầu bổ sung; mean eval ba vòng baseline/subagents 0,597306, skills-auto 0,812907. Đối chiếu chi tiết rubric ở `READINESS.md`; kết quả phân tích ở `REPORT.md`, hướng dẫn tái lập ở `RUN_COMMANDS.md`. Bản nộp đã đẩy lên GitHub main kèm tag freeze và đối chiếu remote, chưa nộp LMS. Không cần người dùng thao tác thêm để kiểm tra bài đã lưu; muốn chạy mới cần Docker và .env, để nộp bài, dùng liên kết kho main trên GitHub.

Phần 6e được chuẩn bị bổ sung lên main, giữ nguyên tag freeze và tệp tổng quan cá nhân không được push.
