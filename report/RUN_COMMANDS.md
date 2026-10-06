# Cách chạy Lab 20 từ PowerShell

Chạy ở thư mục gốc repo. Docker Desktop phải hoạt động. Image có Git được mở rộng từ Dockerfile gốc, không thay đổi đề.

## 1. Dựng môi trường

```powershell
docker build -t lab-day20:local .
docker build -f docs/runtime/Dockerfile.git -t lab-day20:git .
$labRoot = (Get-Location).Path
```

Image cài thư viện editable ở `/lab/src`. Khi bind mount repo, container dùng mã nguồn hiện tại trong checkout; không phải bản TODO đã copy lúc build.

## 2. Kiểm tra ngoại tuyến

```powershell
docker run --rm --network none --mount "type=bind,source=$labRoot,target=/lab" lab-day20:git python -m pytest
docker run --rm --network none --mount "type=bind,source=$labRoot,target=/lab" lab-day20:git python scripts/tour.py
```

Các test dùng mô hình giả, không tính vào số lượt chạy thí nghiệm. Bằng chứng hiện tại: 29 test gốc đạt trên image Python 3.12, có JUnit tại `report/offline-all.xml`.

## 3. Cấu hình API

Điền `.env` cục bộ theo một trong hai nhóm biến của `.env.example`:

- Cổng tương thích OpenAI/Azure: `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_KEY`, `AZURE_OPENAI_DEPLOYMENT_MODEL`.
- DeepSeek: `LAB_MODEL=deepseek:deepseek-chat` và `DEEPSEEK_API_KEY`; để trống ba biến Azure.

Giữ `LAB_TEMPERATURE=0`. Không commit `.env`, không gửi khóa vào chat. `model.py` ưu tiên nhóm Azure khi đủ endpoint/key/deployment. Chỉ có `OPENAI_API_KEY` và `OPENAI_BASE_URL` không tự cấu hình nhánh Azure của module được cấp sẵn.

Sau khi điền, kiểm tra kết nối:

```powershell
docker run --rm --env-file .env --mount "type=bind,source=$labRoot,target=/lab" lab-day20:git python -c "from lab.model import make_model; print(make_model().invoke('Reply with OK').content)"
```

## 4. Chạy tập học

Chỉ thực hiện sau khi API smoke đạt. Chạy tuần tự; không chạy lại nếu đã có kết quả hợp lệ ở cùng đường dẫn. Khi cần retry, giữ bản cũ trong thư mục khác và ghi lý do.

```powershell
docker run --rm --env-file .env --mount "type=bind,source=$labRoot,target=/lab" lab-day20:git python -m lab.runner --condition baseline --tasks data-learn
docker run --rm --env-file .env --mount "type=bind,source=$labRoot,target=/lab" lab-day20:git python -m lab.runner --condition baseline --tasks code-learn logs-learn
docker run --rm --env-file .env --mount "type=bind,source=$labRoot,target=/lab" lab-day20:git python -m lab.runner --condition subagents --tasks learn
```

## 5. Sinh skill và thử trên tập học

```powershell
docker run --rm --env-file .env --mount "type=bind,source=$labRoot,target=/lab" lab-day20:git python -m lab.curator
docker run --rm --env-file .env --mount "type=bind,source=$labRoot,target=/lab" lab-day20:git python -m lab.runner --condition skills-auto --tasks learn
```

Đọc và đánh giá skill nguyên bản, không sửa nội dung bằng tay. Giữ kết quả thử của bộ skill cuối tại `results/skills-auto-dev` trước các lượt chính thức. Dùng PowerShell `Move-Item -LiteralPath` với đường dẫn đã xác nhận; không ghi đè backup.

## 6. Hypotheses và freeze

Thực hiện một lần sau khi viết H1–H3; không tạo lại tag sau eval. Repo này đã có commit `4c9cb63` và tag `freeze` ở `fc1f6dd`.

```powershell
# Checkout Windows dùng CRLF: đồng bộ Git Linux với cách Git Windows so sánh.
git config --local core.autocrlf true
git add src/lab/agent.py src/lab/subagents.py src/lab/runner.py src/lab/curator.py skills/auto report docs .dockerignore results/baseline results/subagents results/skills-auto-dev results/archive
git commit -m "hypotheses: preregister Day 20 comparison and learning evidence"
git commit --allow-empty -m "freeze skills"
git tag freeze
```

Trên clone Linux thuần dùng LF mặc định, không cần `core.autocrlf=true`. Chạy hash/verifier trên Linux: hash provided có đưa dạng đường dẫn vào digest. Các SKILL.md sinh ra và được Git lưu là LF; không chuyển chúng thành CRLF khi kiểm chứng kết quả cũ. Khi clone trên Windows, dùng `git -c core.autocrlf=false clone <URL> <thu-muc-moi>` để giữ LF; không dùng ZIP thay Git vì verifier cần lịch sử/tag.

## 7. Đánh giá chính thức

Đây là các lượt có chi phí API. Chỉ chạy trong một thí nghiệm mới hoặc dùng `--results results/new-experiment`; tránh ghi đè bằng chứng đang có. Giữ cùng model, temperature=0 và recursion-limit=60; không chạy song song.

```powershell
docker run --rm --env-file .env --mount "type=bind,source=$labRoot,target=/lab" lab-day20:git python -m lab.runner --condition baseline --tasks eval
docker run --rm --env-file .env --mount "type=bind,source=$labRoot,target=/lab" lab-day20:git python -m lab.runner --condition subagents --tasks eval
docker run --rm --env-file .env --mount "type=bind,source=$labRoot,target=/lab" lab-day20:git python -m lab.runner --condition skills-auto --tasks all
```

## 8. Kiểm chứng bài đã lưu, không gọi API

```powershell
docker run --rm --network none --mount "type=bind,source=$labRoot,target=/lab" lab-day20:git python -m pytest
docker run --rm --network none --mount "type=bind,source=$labRoot,target=/lab" lab-day20:git python scripts/verify_freeze.py
docker run --rm --network none --mount "type=bind,source=$labRoot,target=/lab" lab-day20:git python -m lab.compare
docker run --rm --network none --mount "type=bind,source=$labRoot,target=/lab" lab-day20:git python scripts/check_breakdown.py
```

Verifier phải kiểm tra **6** run và báo OK. Lưu bảng UTF-8 bằng redirect trong Linux (PowerShell cũ có thể ghi UTF-16):

```powershell
docker run --rm --network none --mount "type=bind,source=$labRoot,target=/lab" lab-day20:git sh -c "python -m lab.compare > report/table.md"
docker run --rm --network none --mount "type=bind,source=$labRoot,target=/lab" lab-day20:git sh -c "python scripts/check_breakdown.py > report/check_breakdown.txt"
```

## 9. Nhật ký thứ tự thực hiện

1. Build image → test/tour → API ban đầu 401 → người dùng điền .env → API smoke OK.
2. Baseline data-learn, code-learn, logs-learn; lưu code lỗi CRLF, sửa runner trên bản sao, test/review lại, chạy lại riêng code-learn.
3. Subagents learn (code, data, logs) → curator một lần → skills-auto learn dev (code, data, logs).
4. Bảo toàn dev → ghi H1–H3 → 29 tests → quét khóa → hypotheses commit → freeze commit/tag.
5. Verifier lần đầu báo README CRLF; đồng bộ cấu hình Git rồi OK; baseline eval → subagents eval → skills-auto all.
6. Bảng/breakdown → báo cáo → test/freeze/hash/secret audit cuối. Bước gửi kho ghi ở READINESS.md; chưa nộp LMS.
