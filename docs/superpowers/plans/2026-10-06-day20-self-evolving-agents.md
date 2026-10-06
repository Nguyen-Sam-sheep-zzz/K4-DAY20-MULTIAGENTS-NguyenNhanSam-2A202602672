# Kế hoạch hoàn thiện Day 20: Self-evolving Agentic

> **For agentic workers:** Thực hiện từng nhiệm vụ theo `superpowers:executing-plans`, có checkpoint sau mỗi phần. Các bước dùng checkbox để theo dõi. Đây là kế hoạch được yêu cầu, chưa phải lệnh bắt đầu triển khai hay chạy thí nghiệm.

**Goal:** Hoàn thiện harness Deep Agents đúng phạm vi, thực hiện thí nghiệm ba điều kiện có bằng chứng thật, và nộp đủ mã nguồn, skill tự sinh, kết quả, báo cáo theo rubric.

**Architecture:** Dùng harness và bộ chấm có sẵn. Mỗi lượt chạy sao chép workspace vào thư mục tạm, chạy một cấu hình tác tử, đo chi phí và chấm trên bản sao. Curator chỉ học từ phản hồi và trace của tập học; chốt giả thuyết và skill trước khi đo tập đánh giá.

**Tech Stack:** Python >=3.11; `deepagents==0.7.21`; LangChain; pytest; Git; Linux qua WSL2 hoặc Docker; mô hình hỗ trợ tool calling được cấu hình bằng `lab.model.make_model()`.

**Spec:** `README.md`, `GUIDE.md`, `RUBRIC.md`, `REPORT_TEMPLATE.md`, các tài liệu trong `guides/pseudocode/`, và thiết kế đề xuất ở phần B của tài liệu này.

## Global Constraints

- Chỉ cài đặt các phần TODO và import cần thiết trong bốn tệp `agent.py`, `subagents.py`, `runner.py`, `curator.py`.
- Không sửa `tests/`, `tasks/`, `scripts/`, `model.py`, `tasks.py`, `grading.py`, `testing.py`, `compare.py`.
- Giữ nguyên `PATHS_NOTE`, `BASE_PROMPT`, `SKILLS_NOTE`, `SUBAGENTS_NOTE`, `CONDITIONS`, `render_trace`, CLI `main`, `validate_skill`, `parse_skill_blocks`.
- Không sửa tay nội dung `skills/auto/`; chỉ được xóa skill kém chất lượng hoặc chạy lại curator tối đa hai lần, có ghi lý do.
- Không chạy hoặc phân tích kết quả tác vụ đánh giá trước khi chốt giả thuyết và freeze. Không dùng đặc tả riêng, dữ liệu hay checker của tập đánh giá để thiết kế skill.
- Không đưa khóa API vào shell của tác tử, Git, trace hay báo cáo. `.env` được giữ cục bộ.
- Chạy thí nghiệm tuần tự; cùng mô hình, nhiệt độ và recursion limit giữa ba điều kiện.
- Kết quả âm hoặc không cải thiện vẫn hợp lệ. Không sửa số liệu hoặc tối ưu theo đáp án để tạo kết quả đẹp.
- Commit và tag là bước thật, không thể thay bằng ghi chú trong báo cáo. Kế hoạch này không tự thực hiện commit/push.

## A. Bài lab làm gì và trạng thái hiện tại

### A1. Ý nghĩa dễ hiểu

Bài lab đặt câu hỏi: AI làm việc tốt hơn nhờ có đồng đội, hay nhờ rút kinh nghiệm từ lỗi của chính mình?

So sánh ba cấu hình:

| Cấu hình | Cách hoạt động | Điều cần kiểm chứng |
|---|---|---|
| `baseline` | Deep Agents mặc định, không thêm skill | Mốc chất lượng và chi phí |
| `subagents` | Thêm tác tử chuyên đọc đặc tả và kiểm tra kết quả | Giao việc có giúp và có đáng token không? |
| `skills-auto` | Đọc skill do curator tự sinh từ lỗi tập học | Kinh nghiệm cũ có giúp tác vụ mới không? |

Mỗi cấu hình xử lý sáu tác vụ, thuộc ba họ: sửa code Python; làm sạch và phân tích dữ liệu; phân tích log. Mỗi họ có một tác vụ học và một tác vụ đánh giá.

Điểm tác vụ là số check đạt chia tổng check; đạt toàn bộ mới gọi là thành công hoàn toàn. Agent còn phải học quy ước tổ chức Acme từ phản hồi tập học. Một số quy ước mới ở tập đánh giá kiểm tra khả năng tổng quát hóa.

"Tự tiến hóa" ở đây là bổ sung tri thức dưới dạng `SKILL.md`, không huấn luyện lại trọng số mô hình.

### A2. Kiểm tra ngày 06/10/2026

- Năm hàm chưa cài đặt: `get_subagents`, `make_backend`, `build_agent`, `run_task`, `curate_skills`.
- `results/` chỉ có `.gitkeep`; `skills/auto/` chỉ có README; chưa có thư mục `report/`.
- Chưa có `.env`, `.venv`, tag `freeze` trong checkout. Chưa kiểm tra thông tin API trong biến môi trường.
- Git working tree sạch trước khi thêm kế hoạch này. Đọc Git trong sandbox phải dùng `git -c safe.directory=<đường-dẫn-repo> ...`; chưa sửa cấu hình Git toàn cục.
- Có lệnh Docker và WSL trên PATH. `docker info` chưa kết nối được daemon và báo không đọc được cấu hình người dùng; WSL báo `E_ACCESSDENIED` trong phiên sandbox. Chưa thể kết luận WSL chưa cài distro hoặc Docker không hoạt động ở phiên người dùng.
- Chưa chạy pytest hay gọi mô hình. Con số 29 test bên dưới là mục tiêu theo bộ test, không phải kết quả đã đạt.
- Đã đọc đề, rubric, mẫu báo cáo, pseudo-code, module harness và test triển khai. Chưa mở nội dung riêng của `tasks/*-eval/` để thiết kế phương án.

## B. Phương án đề xuất

### B1. So sánh cách làm

1. **Khuyến nghị: bám harness gốc, hai subagent rõ vai trò, curator ngắn gọn, dữ liệu đo đầy đủ.** Phù hợp rubric, dễ giải thích và giảm thay đổi ngoài phạm vi.
2. Ba subagent `explorer`/`implementer`/`reviewer`: phân công rõ hơn nhưng tăng lượt giao việc và token; tác vụ nhỏ có thể không hưởng lợi.
3. Làm thêm UI hoặc thay kiến trúc bằng một framework mới: không phục vụ tiêu chí bắt buộc, làm chậm phần chạy và báo cáo; không chọn cho đợt hoàn thiện này.

### B2. Vai trò subagent

- `explorer`: dùng khi cần đọc README, docstring, cấu trúc dữ liệu/log và xác định trường hợp biên. Trả về yêu cầu, bằng chứng tệp và vị trí liên quan; không sửa workspace.
- `reviewer`: dùng sau khi có thay đổi hoặc đầu ra để kiểm tra độc lập theo đặc tả và test. Trả về kết quả thực tế, phần chưa kiểm chứng và vấn đề còn lại; không sửa workspace.
- Tác tử chính thực hiện thay đổi và quyết định kết thúc. Mỗi lời giao việc phải chứa đủ đề bài, quy tắc và đường dẫn; subagent không tự có toàn bộ ngữ cảnh.
- Vai trò chỉ đọc được diễn đạt trong prompt; không tuyên bố đây là cơ chế phân quyền cưỡng chế của hệ điều hành.
- Không thêm skill vào custom subagent trong thí nghiệm chính để giữ ba điều kiện đúng đề.
- `single` vẫn có `general-purpose` mặc định của Deep Agents. Vì vậy gọi baseline là "không thêm subagent chuyên biệt", không khẳng định baseline không bao giờ giao việc.

### B3. Phạm vi đầu ra

| Đường dẫn | Trách nhiệm |
|---|---|
| `src/lab/subagents.py` | Hai định nghĩa subagent, trả về danh sách dict |
| `src/lab/agent.py` | Backend có shell và dựng graph theo cấu hình |
| `src/lab/runner.py` | Sandbox, chạy, đo, chấm, lưu record/trace, dọn thư mục tạm |
| `src/lab/curator.py` | Lọc phản hồi tập học, gọi mô hình, ghi skill hợp lệ |
| `skills/auto/<name>/SKILL.md` | Đầu ra nguyên bản của curator, đóng băng trước đánh giá |
| `results/<condition>/<task>/` | 18 cặp `run.json` và `trace.md` chính thức |
| `results/skills-auto-dev/` | Ba lượt thử skill trước freeze, giữ để đo nhiễu |
| `report/REPORT.md` | Đủ 10 mục và phụ lục theo mẫu |
| `report/table.md` | Bảng tạo từ `lab.compare`, không nhập số liệu bằng tay |
| `report/check_breakdown.txt` | Thống kê từ script gốc, hỗ trợ phân tích |

## C. Các nhiệm vụ và checkpoint

### Nhiệm vụ 0: Môi trường chạy và hồ sơ thí nghiệm

**Tệp:** tạo `.env` cục bộ, `.venv/` nếu dùng WSL, và `report/REPORT.md` từ mẫu. Không thay `model.py` hay thư viện được pin.

- [ ] Xác nhận môi trường Linux có Python >=3.11, Git, `/bin/sh` và thư mục repo đọc/ghi được.
- [ ] Ưu tiên WSL2 nếu distro của người dùng dùng được. Tạo venv trong Linux; không dùng lại một venv Windows.
- [ ] Nếu dùng Docker, dùng Dockerfile có sẵn. Kiểm tra thêm Git trong container: image `python:3.12-slim` không đảm bảo có Git, trong khi script freeze cần Git. Bổ sung Git vào môi trường chạy nếu thiếu; không sửa script kiểm tra để né yêu cầu này.
- [ ] Giữ cùng nền tảng cho các lượt chạy và việc băm skill; không trộn kết quả Linux với Windows vì cách biểu diễn đường dẫn có thể làm hash khác.
- [ ] Cấu hình mô hình theo `.env.example`; kiểm tra từng biến chỉ in `set`/`missing`, không in giá trị.
- [ ] Ghi mô hình, temperature=0, recursion_limit=60, phiên bản thư viện, nền tảng, ngân sách vào mục 1 báo cáo. Nếu cần đổi giới hạn, ghi lý do và áp dụng nhất quán trước thí nghiệm chính.
- [ ] Kiểm tra kết nối bằng một câu ngắn. Ghi rõ đây là API smoke, không coi là lượt giải tác vụ.
- [ ] Chạy bộ test phần có sẵn và `scripts/tour.py`; điền ba câu hỏi mục 3 báo cáo từ đầu ra thực tế.

Lệnh trong shell Linux, ở thư mục gốc repo:

```bash
python3 --version
git --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
mkdir -p report
cp REPORT_TEMPLATE.md report/REPORT.md
# Chỉ tạo .env từ mẫu nếu chưa có; điền cấu hình ở máy người dùng.
test -f .env || cp .env.example .env
python -m pytest tests/test_01_provided.py
python scripts/tour.py
python -c "from lab.model import make_model; print(make_model().invoke('Reply with OK').content)"
```

**Checkpoint 0:** có môi trường Linux và Git hoạt động; test phần có sẵn đạt 12 test; API smoke có phản hồi; mục 1 và 3 được điền. Nếu sandbox vẫn không truy cập WSL/Docker, xử lý quyền truy cập hoặc chạy từ phiên người dùng; không kết luận code thất bại do lỗi môi trường.

### Nhiệm vụ 1: Định nghĩa subagent và dựng agent

**Modify:** chỉ TODO/import trong `src/lab/subagents.py`, `src/lab/agent.py`.

**Interfaces:**

```python
get_subagents() -> list[dict]
make_backend(sandbox: Path)
build_agent(sandbox: Path, mode: str = "single", use_skills: bool = False, model=None)
```

- [ ] Cài `get_subagents()` theo B2; mỗi dict có tên duy nhất, description nêu tình huống gọi và system_prompt xác định phạm vi.
- [ ] Chạy test subagent.
- [ ] Cài `make_backend`: root=sandbox, virtual_mode=True, timeout=120, inherit_env=False; PATH chứa thư mục Python hiện tại và các thư mục lệnh Linux; HOME trỏ sandbox; không kế thừa khóa API.
- [ ] Cài `build_agent`: kiểm tra mode, giữ prompt gốc, nối PATHS_NOTE vào từng custom subagent, chỉ nạp `/skills/` khi use_skills=True, hỗ trợ model giả truyền vào test.
- [ ] Không dùng `permissions=` vì backend shell của phiên bản này không hỗ trợ tổ hợp đó.
- [ ] Chạy toàn bộ `test_02` để xác nhận đường dẫn file tool và shell thống nhất.

```bash
python -m pytest tests/test_02_agent.py -k subagents
python -m pytest tests/test_02_agent.py
```

**Checkpoint 1:** chín test agent đạt; backend tìm thấy Python và không lộ biến khóa; skill chỉ nạp đúng điều kiện. Chưa tính token từ test ngoại tuyến.

### Nhiệm vụ 2: Runner có đo lường đúng

**Modify:** TODO/import của `src/lab/runner.py`.

**Interface:** giữ `run_task(task_id: str, condition: str, results_dir="results", model=None, recursion_limit: int = 60) -> dict`.

- [ ] Dùng `get_task`, `prepare_sandbox` và `grade` có sẵn. Tạo thư mục tạm ngoài repo, không sửa workspace gốc.
- [ ] Ghi timestamp UTC khi bắt đầu và hash skill trước chạy.
- [ ] Dùng `UsageMetadataCallbackHandler` cộng token của mọi lần gọi mô hình, gồm cả subagent.
- [ ] Chạy graph với model truyền vào hoặc make_model, recursion_limit từ tham số.
- [ ] Bắt lỗi chạy agent, ghi loại lỗi/thông báo vào `error`; vẫn chấm workspace hiện có và ghi record.
- [ ] Đếm tool call ở luồng chính; `subagent_calls` là số lần gọi `task`; `skills_read` là số thư mục skill khác nhau qua `read_file`, không đếm số lần đọc lặp.
- [ ] So hash trước/sau để ghi `skills_modified`; lấy final_message từ kết quả thật.
- [ ] Ghi UTF-8 `run.json` và trace bằng `render_trace` gốc; xóa sandbox trong finally.
- [ ] Kiểm tra record có toàn bộ trường trong docstring, kể cả các nhánh lỗi được kiểm tra.
- [ ] Chạy bộ test runner, rồi một smoke thật `baseline/data-learn`. Lượt này được dùng lại trong tập học, không chạy lần nữa chỉ để smoke.

```bash
python -m pytest tests/test_03_runner.py
python -m lab.runner --condition baseline --tasks data-learn
```

**Checkpoint 2:** sáu test runner đạt; có run.json/trace.md thật cho data-learn; token >0; không có lỗi hạ tầng chưa giải quyết; workspace nguồn không thay đổi.

**Giới hạn phải ghi đúng:** trace, tool_calls, subagent_calls và skills_read chỉ phản ánh luồng chính. Token có tính subagent. Nếu invoke ném lỗi và không trả message, trace có thể rỗng theo cách cài đặt tối thiểu; không diễn giải số đếm bằng 0 thành "agent không làm gì".

### Nhiệm vụ 3: Tập học và phân loại lỗi

**Create:** sáu cặp kết quả baseline/subagents trên learn; điền mục 4–5 báo cáo.

- [ ] Chạy hai baseline learn còn lại và ba subagents learn, tuần tự.
- [ ] Lưu nguyên lần chạy đầu; nếu phải retry vì API lỗi, chuyển bản lỗi sang thư mục lưu trữ riêng trước khi chạy lại.
- [ ] Phân loại ít nhất bốn check thất bại thực tế nếu có đủ: tên task, tên check, nhóm A–G, trích detail/trace và giải thích.
- [ ] Nếu lỗi chủ yếu là E (`rule_`), dùng tỷ lệ check kỹ thuật đạt/tổng để hỗ trợ nhận xét về các nhóm A–D. Không bịa thêm lỗi cho đủ số dòng.
- [ ] Không dùng API timeout, 401, 429 hoặc lỗi môi trường làm bằng chứng về lỗi suy luận của tác tử.
- [ ] Ghi tên subagent thực sự được gọi, nội dung giao việc, thông tin đủ/thiếu, token và thời gian. Nếu không được gọi, ghi trung thực và phân tích.

```bash
python -m lab.runner --condition baseline --tasks code-learn logs-learn
python -m lab.runner --condition subagents --tasks learn
python scripts/check_breakdown.py
```

**Checkpoint 3:** đủ sáu lượt learn baseline/subagents; phân loại lỗi có trích dẫn; biết vấn đề nào curator có thể học. Chưa chạy tập eval.

### Nhiệm vụ 4: Curator và thử skill trên tập học

**Modify:** TODO/import trong `src/lab/curator.py`. **Create:** skill nguyên bản do mô hình sinh và ba lượt skills-auto learn.

**Interface:** giữ `curate_skills(results_dir="results", source_condition="baseline", out_dir=None, model=None, max_skills: int = 3) -> list[Path]`.

- [ ] Đọc run.json của source_condition; chỉ dùng role=learn và trace tương ứng. Không dùng lượt lỗi hạ tầng làm nguồn học; hoàn tất retry hợp lệ trước khi curate.
- [ ] Lấy tên/detail của check thất bại và khoảng 6.000 ký tự cuối trace. Không có check thất bại thì cảnh báo và trả [] mà không gọi model.
- [ ] Prompt yêu cầu tối đa ba skill tổng quát, description nêu khi dùng, checklist ngắn khoảng 40 dòng, không ghi đáp án hay tên dữ liệu riêng của task.
- [ ] Cho phép những tên tệp/khóa là quy ước tổ chức mà phản hồi tập học yêu cầu, đúng hướng dẫn chất lượng skill; không cấm máy móc mọi tên tệp.
- [ ] Gọi model một lần; dùng parse_skill_blocks và validate_skill gốc; kiểm tra tên trước khi tạo đường dẫn, bỏ skill invalid và giữ tối đa max_skills skill hợp lệ.
- [ ] Chạy test curator, rồi chạy curator thật từ baseline learn.
- [ ] Đánh giá từng skill theo ba câu hỏi mục 6: tổng quát, đúng, độ dài/description. Giữ nguyên nội dung; nếu xóa hoặc chạy lại, ghi lý do, không vượt hai lần chạy lại.
- [ ] Chạy skills-auto trên learn; đối chiếu skills_read và trace với từng quy tắc, không chỉ nhìn tổng điểm.
- [ ] Với bộ skill cuối cùng định freeze, giữ đủ ba lượt learn thử. Nếu skill thay đổi sau thử nghiệm, phải đo lại bộ cuối và tính thêm ngân sách.
- [ ] Đổi tên kết quả thử thành `results/skills-auto-dev` trước khi chạy chính thức. Lưu hash của bộ skill để bảo đảm so sánh nhiễu đúng cùng bộ skill.

```bash
python -m pytest tests/test_04_curator.py
python -m lab.curator
python -m lab.runner --condition skills-auto --tasks learn
```

Di chuyển kết quả trong Linux, chỉ khi thư mục đích chưa có:

```bash
test ! -e results/skills-auto-dev && mv results/skills-auto results/skills-auto-dev
```

Nếu đã có backup, dùng tên khác và ghi tên vào báo cáo; không ghi đè backup trước đó.

**Checkpoint 4:** hai test curator đạt; ít nhất một skill hợp lệ do curator sinh; ba kết quả dev của bộ skill cuối được bảo toàn; toàn bộ bộ test dự kiến đạt 29 test. Chưa thấy điểm eval.

### Nhiệm vụ 5: Giả thuyết và freeze đúng thứ tự

**Modify:** mục 2 của `report/REPORT.md`. **Git:** hai commit riêng và tag freeze, khi bước thực thi này được tiến hành.

- [ ] Viết H1–H3 thành dự đoán có thể kiểm chứng, dựa trên lỗi learn thật và nguồn tham khảo.
- [ ] H1: so subagents với baseline về điểm eval và chi phí token; nêu lý do dựa trên loại lỗi đã thấy.
- [ ] H2: so skills-auto với baseline, phân biệt quy ước đã học với quy ước mới; không dự đoán chắc chắn đạt tuyệt đối.
- [ ] H3: dự đoán chênh lệch learn/eval và nguy cơ overfitting, kèm cách kiểm chứng.
- [ ] Tra cứu đúng bài và đường dẫn gốc trước khi trích nguồn. Các hướng dẫn lab nhắc SkillsBench, SkillEvolBench và tài liệu multi-agent của Anthropic; chưa coi các số liệu nghiên cứu trong hướng dẫn là kết quả thí nghiệm của mình.
- [ ] Kiểm tra diff không chạm tệp cấm hoặc chứa secret; stage đường dẫn cụ thể.
- [ ] Tạo commit có thông điệp bắt đầu `hypotheses`, chứa REPORT với đủ ba dòng H1–H3 có nội dung sau dấu hai chấm.
- [ ] Tạo commit freeze riêng, gắn tag freeze, giữ nguyên skills/ kể từ đó. Không tạo lại hoặc di chuyển tag sau khi thấy kết quả eval.
- [ ] Lưu commit ID của freeze và cấu hình vào báo cáo; không sửa skill để đáp ứng lỗi mới trên eval.

Ví dụ lệnh, sau khi xác nhận không có tag freeze cũ và diff đúng phạm vi:

```bash
git status --short
git diff --check
git add src/lab/agent.py src/lab/subagents.py src/lab/runner.py src/lab/curator.py skills/auto report/REPORT.md results/baseline results/subagents results/skills-auto-dev
git commit -m "hypotheses"
git commit --allow-empty -m "freeze skills"
git tag freeze
git rev-parse freeze
```

**Checkpoint 5:** REPORT trong hypotheses commit có đủ H1–H3; commit đó đứng trước commit của freeze; bộ skill cuối đã được Git lưu. Chỉ sau checkpoint này mới đánh giá eval.

### Nhiệm vụ 6: Thí nghiệm chính thức và bảng so sánh

**Create:** thêm 12 cặp kết quả, hoàn thành 18 cặp chính thức; table.md và breakdown.

- [ ] Chạy baseline và subagents trên ba eval, rồi skills-auto trên cả sáu task. Dùng cùng cấu hình đã ghi.
- [ ] Không sửa skill dựa trên kết quả mới. Lỗi hạ tầng được retry có lưu bản cũ và ghi nhận; không chỉ chọn lần có điểm cao nhất.
- [ ] Đảm bảo đủ chính xác 6 task x 3 condition trong kết quả chính thức. Kiểm tra error, schema, trace, timestamp và hash; không chỉ kiểm tra thư mục tồn tại.
- [ ] Chạy verify_freeze, xác nhận kiểm tra đủ sáu run skills-auto và OK. Script có thể trả OK khi không có run, vì vậy phải kiểm tra số lượng riêng.
- [ ] Sinh bảng bằng công cụ gốc, lưu breakdown và đối chiếu bảng với run.json.

```bash
python -m lab.runner --condition baseline --tasks eval
python -m lab.runner --condition subagents --tasks eval
python -m lab.runner --condition skills-auto --tasks all
python scripts/verify_freeze.py
python -m lab.compare > report/table.md
python scripts/check_breakdown.py > report/check_breakdown.txt
```

**Checkpoint 6:** 18 run.json và 18 trace.md chính thức; sáu skills-auto dùng bộ đã freeze, timestamp hợp lệ, skills_modified=false; bảng đủ ba điều kiện/sáu tác vụ/các hàng tổng hợp. Không cam kết cả 18 lượt đạt điểm tối đa.

### Nhiệm vụ 7: Báo cáo và kiểm tra nộp

**Modify:** `report/REPORT.md`; giữ `report/table.md` từ chương trình.

- [ ] Hoàn thiện tất cả 10 mục của mẫu, xóa hướng dẫn và ô trống; kết luận tối đa năm câu.
- [ ] Phân tích riêng điểm learn/eval và check kỹ thuật/quy ước; dùng breakdown thay vì chỉ báo tổng điểm.
- [ ] Trích ít nhất một trường hợp skill giúp và một trường hợp không giúp nếu dữ liệu có, kèm skill, check và đoạn trace. Nếu không có cải thiện, nói rõ và dùng bằng chứng tương ứng.
- [ ] So token, thời gian, giao việc, skill được đọc; chỉ dùng số liệu đo. Có thể chuẩn hóa hiệu quả thành điểm trung bình trên một triệu token để dễ so sánh; ghi công thức và không tính với token=0.
- [ ] So ba điểm skills-auto-dev và ba điểm learn sau freeze của đúng cùng hash skill để ước lượng nhiễu.
- [ ] Nêu ít nhất ba hạn chế cùng tác động: mẫu nhỏ, ít lượt lặp, một mô hình, quy ước thiết kế sẵn, trace không có nội bộ subagent.
- [ ] Ghi nguồn tham khảo, lệnh theo thời gian, lượt retry/xóa skill, ngân sách thực dùng, commit freeze và cách tái lập.
- [ ] Chạy lại toàn bộ pytest và verify_freeze; kiểm tra bảng không sai lệch với dữ liệu, Git diff không sửa tệp cấm, và không có secret trong tệp dự định nộp.
- [ ] Báo rõ trạng thái local, commit/tag, push và nộp LMS riêng biệt. Không coi local hoàn thiện là đã nộp.

```bash
python -m pytest
python scripts/verify_freeze.py
git diff --check
git status --short
```

**Checkpoint 7:** đối chiếu từng dòng rubric, chỉ ra đã đạt/thiếu/chưa xác minh. Chỉ đánh giá sẵn sàng nộp khi dữ liệu thực và Git đáp ứng điều kiện.

## D. Ngân sách và mở rộng

### D1. Khối lượng tối thiểu theo quy trình đề

| Giai đoạn | Lượt chạy tác vụ |
|---|---:|
| Baseline learn, gồm smoke data-learn | 3 |
| Subagents learn | 3 |
| Skills-auto learn thử trước freeze | 3 |
| Baseline eval | 3 |
| Subagents eval | 3 |
| Skills-auto chính thức, all | 6 |
| **Tổng** | **21** |

Trong đó 18 lượt dùng trong bảng chính thức và ba lượt dev để so nhiễu. Curator thêm một lần gọi mô hình ban đầu, tối đa hai lần chạy lại. API smoke, retry do hạ tầng và thử lại bộ skill mới được tính riêng.

Một lượt chạy tác vụ có nhiều lượt gọi LLM; 21 lượt tác vụ không đồng nghĩa 21 request API. Chưa thể ước lượng tiền khi chưa có mô hình, giá và token smoke thật. Không có mức ngân sách cứng được nêu trong những tệp đề đã đọc; cần ghi ngân sách người dùng/giảng viên cấp trước khi chạy.

### D2. Mở rộng khuyến nghị: 6e, đo nhiễu

Chỉ làm sau khi phần bắt buộc hoàn thành và còn ngân sách. Chạy thêm hai lượt cho mỗi cấu hình trên ba eval: 18 lượt bổ sung, tổng tối thiểu 39 lượt tác vụ nếu làm cả phần này. Giữ nguyên skill, mô hình, prompt và tham số.

```bash
python -m lab.runner --condition baseline --tasks eval --results results/repeat-2
python -m lab.runner --condition subagents --tasks eval --results results/repeat-2
python -m lab.runner --condition skills-auto --tasks eval --results results/repeat-2
python -m lab.runner --condition baseline --tasks eval --results results/repeat-3
python -m lab.runner --condition subagents --tasks eval --results results/repeat-3
python -m lab.runner --condition skills-auto --tasks eval --results results/repeat-3
```

Báo cáo trung bình, min–max điểm và token qua ba lượt, giải thích cơ chế bằng trace, nêu hạn chế; không suy rộng thành kết luận thống kê chắc chắn từ ba mẫu. Script verify_freeze gốc chỉ kiểm tra cây kết quả chính, nên phải đối chiếu hash/timestamp/skills_modified của các lượt mở rộng riêng. Không trộn kết quả mở rộng vào bảng chính thức.

## E. Đối chiếu rubric và kế hoạch ưu tiên

| Hạng mục | Điểm | Nhiệm vụ và bằng chứng |
|---|---:|---|
| Harness | 30 | 1, 2, 4; test_02/03/04 đạt, đúng tệp và phần cho sửa |
| Baseline, phân loại lỗi | 14 | 3, 6; đủ sáu baseline, taxonomy có detail/trace thật |
| Subagents | 10 | 1, 3, 6; >=2 vai trò, đủ sáu lượt, phân tích giao việc/token |
| Skill tự sinh | 16 | 4, 6; skill nguyên bản hợp lệ, review nội dung, skills_read và freeze |
| So sánh và freeze | 10 | 5, 6; hypotheses trước freeze, sáu lượt skill được xác minh, table từ compare |
| Báo cáo | 20 | 0, 3–7; đủ mục, giả thuyết, phân tích, nhiễu, hạn chế, tái lập |
| Thưởng | +5, tổng không quá 100 | D2; thí nghiệm riêng và có số liệu |

Thứ tự ưu tiên: môi trường → harness → tập học → curator và thử skill → hypotheses/freeze → đánh giá → báo cáo → mở rộng. Sau mỗi checkpoint, báo tệp thay đổi, kiểm tra đạt/chưa đạt, dữ liệu đã có, ngân sách đã dùng và việc kế tiếp. Không bắt đầu triển khai trong bước đọc và lập kế hoạch này.
