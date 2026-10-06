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

Các bước hypotheses, freeze, đánh giá và bảng so sánh tiếp tục theo kế hoạch sau khi tập học có bằng chứng thật. Không chạy eval sớm. REPORT hiện là bản nháp, chưa phải báo cáo hoàn thành.
