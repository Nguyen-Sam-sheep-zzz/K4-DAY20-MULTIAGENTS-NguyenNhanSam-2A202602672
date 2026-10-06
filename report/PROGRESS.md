# Tiến độ Lab 20

Ngày bắt đầu: 06/10/2026. Nhánh: `feature/day20-self-evolving-agents`.

| Bước | Trạng thái | Bằng chứng / việc còn lại |
|---|---|---|
| 0. Môi trường | Đã xong | Docker Python 3.12.15, Deep Agents 0.7.21, Git 2.47.3; 12/12 test phần có sẵn đạt; tour/phiên bản đã lưu; API gpt-6-luna trả OK. |
| 1. Subagents và agent | Mã nguồn đã xong | 9/9 test gốc đạt; explorer/reviewer có vai trò rõ ràng; backend không kế thừa biến khóa. |
| 2. Runner | Đã xong | 6/6 test gốc đạt; baseline data-learn thật đạt 5/8, token và trace hợp lệ. |
| 3. Tập học | Đang làm | Baseline đủ ba learn: 7/10, 5/8, 6/9; technical 18/18, quy ước 0/9. Đang chạy subagents learn. |
| 4. Curator | Mã nguồn đã xong; chưa sinh skill thật | 2/2 test gốc đạt. Lọc role=learn, bỏ lượt error, giới hạn/kiểm tra skill trước khi ghi. |
| 5. Hypotheses và freeze | Chưa bắt đầu | Chỉ thực hiện sau tập học và thử skill. |
| 6. Đánh giá | Chưa bắt đầu | Chỉ thực hiện sau freeze. |
| 7. Báo cáo cuối | Chưa bắt đầu | Đã tạo report/REPORT.md từ mẫu, chưa có số liệu thực nghiệm. |

## Cấu hình API đã được xử lý

Cổng API từ biến môi trường ban đầu trả HTTP 401 khi đọc danh sách mô hình. Người dùng đã điền `.env` cục bộ; API smoke qua `make_model` thực tế trả OK với `gpt-6-luna` và 16 token. Nhiệt độ 0.0. Không còn cần thao tác của người dùng ở bước này.

Trong lúc chờ, tiếp tục hoàn thiện mã nguồn và test ngoại tuyến. Không gọi bài đánh giá, tạo skill giả hoặc ghi số liệu thí nghiệm thay cho dữ liệu thật.

Git bỏ qua `.env` đúng yêu cầu. Không đưa giá trị khóa vào báo cáo hoặc chat. Các tác vụ học đang được chạy tuần tự.

## Kiểm tra mã nguồn

- Toàn bộ test gốc: **29 passed**, không có failure/error; bằng chứng JUnit ở `report/offline-all.xml`.
- Các test trước cài đặt agent/runner/curator còn lỗi đúng tại NotImplementedError; lưu ở `report/offline-before-implementation.xml`. `get_subagents` đã có kiểm tra hợp đồng đỏ/xanh trước đó, rồi được kiểm tra tích hợp bằng test gốc.
- So sánh AST với HEAD: constants, hàm có sẵn, chữ ký và docstring giữ nguyên; thay đổi mã chỉ nằm trong phần TODO/import cho phép.
- Đối chiếu SHA-256: tệp đề, tests/tasks/scripts và module có sẵn không đổi.
- Review độc lập theo `superpowers:requesting-code-review`: không phát hiện lỗi cần sửa trong bốn module; sẵn sàng chạy tập học sau khi API smoke đạt. Chưa xác nhận khả năng gọi tool và token metadata của nhà cung cấp thật.
- Test dùng mô hình giả và thư mục tạm; `results/` chính thức vẫn chưa có dữ liệu. Chưa tạo tag freeze, commit hoặc push.

## Bổ sung tương thích Windows

Đã chứng minh `tests_not_modified` của lượt code-learn đầu trượt do CRLF, không phải tác tử sửa test. Runner chuẩn hóa bản sao Python sang LF trước khi tác tử chạy; không sửa nguồn/dữ liệu/skill. Reproducer no-op chuyển từ trượt sang đạt; toàn bộ 29 test vẫn đạt sau sửa. Review độc lập không phát hiện vấn đề vật chất với thay đổi này.

Lượt cũ được giữ ở `results/archive/baseline-pre-lf/code-learn`; chỉ bài code được chạy lại, vì data/logs không có `.py` trong workspace. Không dùng lỗi CRLF làm dữ liệu lỗi tác tử. Thêm một lượt vào ngân sách thực dùng.

## Phạm vi bảo toàn

Đã lưu SHA-256 của tệp đề và các tệp cấm sửa vào `source-document-hashes.txt` và `protected-file-hashes.txt`. Danh sách hash chỉ dùng đối chiếu nội dung, không chứa dữ liệu hoặc đáp án của tác vụ.

Thêm `.dockerignore` để lần build sau không gửi `.env`, Git và kết quả vào build context. Không sửa Dockerfile hoặc pyproject.toml.
