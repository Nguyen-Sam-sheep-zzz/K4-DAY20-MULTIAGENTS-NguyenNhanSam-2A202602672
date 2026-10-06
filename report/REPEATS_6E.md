# Phụ lục 6e: lặp eval để đo nhiễu

## Thiết kế

Thực hiện ngày 06/10/2026 sau khi phần bắt buộc đã hoàn thành và người dùng yêu cầu mở rộng. Mỗi điều kiện baseline/subagents/skills-auto chạy lại ba bài code-eval/data-eval/logs-eval **hai lần**, bổ sung **18 lượt tác vụ**. Kết hợp với 9 lượt eval chính thức đã có, mỗi cặp điều kiện–tác vụ có **3 lượt**; tổng dữ liệu phân tích là **27 eval run/trace pairs**.

Giữ nguyên gpt-6-luna, temperature=0.0, recursion_limit=60, source/prompt/backend/checker và skill/tag freeze. Đã kiểm tra lại make_model chỉ bằng construction, không thêm inference smoke. Không chạy curator lại, không sửa skill, không đổi giả thuyết H1–H3. Thứ tự tuần tự vòng 2 rồi vòng 3, mỗi vòng baseline → subagents → skills-auto, mỗi nhóm code → data → logs; thời điểm/provider vì thế là yếu tố chưa được ngẫu nhiên hóa.

Vòng 1 lấy từ results/<condition>/<task>/, vòng 2/3 ở results/repeat-2 và results/repeat-3. Không ghi đè bằng chứng chính thức hoặc trộn repeat vào report/table.md. Không có error/skills_modified, không retry hay chọn bỏ lượt điểm thấp. [repeat-design.json](repeat-design.json) lưu thiết kế/hash trước khi tổng hợp; ngày, timestamp và raw trace nằm trong từng run.

## Kết quả tái lập từ run.json

| Điều kiện | Tác vụ | Điểm lượt 1 / 2 / 3 | Mean score | Min–max score | Mean token | Min–max token |
|---|---|---|---:|---:|---:|---:|
| baseline | code-eval | 7/11 / 7/11 / 7/11 | 0.636364 | 0.636364–0.636364 | 58,016.33 | 52,504–61,619 |
| baseline | data-eval | 5/9 / 5/9 / 5/9 | 0.555556 | 0.555556–0.555556 | 18,519.00 | 16,296–21,489 |
| baseline | logs-eval | 6/10 / 6/10 / 6/10 | 0.600000 | 0.600000–0.600000 | 20,497.00 | 13,742–27,088 |
| subagents | code-eval | 7/11 / 7/11 / 7/11 | 0.636364 | 0.636364–0.636364 | 84,909.33 | 73,943–104,185 |
| subagents | data-eval | 5/9 / 5/9 / 5/9 | 0.555556 | 0.555556–0.555556 | 60,565.33 | 33,156–89,696 |
| subagents | logs-eval | 6/10 / 6/10 / 6/10 | 0.600000 | 0.600000–0.600000 | 31,895.00 | 27,521–36,423 |
| skills-auto | code-eval | 10/11 / 10/11 / 10/11 | 0.909091 | 0.909091–0.909091 | 83,533.00 | 71,363–98,266 |
| skills-auto | data-eval | 5/9 / 6/9 / 6/9 | 0.629630 | 0.555556–0.666667 | 39,022.00 | 31,167–48,070 |
| skills-auto | logs-eval | 9/10 / 9/10 / 9/10 | 0.900000 | 0.900000–0.900000 | 20,673.00 | 19,767–21,354 |

| Điều kiện | Mean score 9 run | Mean theo vòng 1 / 2 / 3 | Min–max mean theo vòng | Mean token/run | Mean giây/run | Điểm/triệu token | Kỹ thuật | Quy ước |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| baseline | 0.597306 | 0.597306 / 0.597306 / 0.597306 | 0.597306–0.597306 | 32,344.11 | 42.48 | 18.47 | 54/54 | 0/36 |
| subagents | 0.597306 | 0.597306 / 0.597306 / 0.597306 | 0.597306–0.597306 | 59,123.22 | 93.33 | 10.10 | 54/54 | 0/36 |
| skills-auto | 0.812907 | 0.788215 / 0.825253 / 0.825253 | 0.788215–0.825253 | 47,742.67 | 45.69 | 17.03 | 54/54 | 20/36 |

18 lượt thêm dùng 826,907 token đo. Tổng 40 lượt tác vụ dùng 1,955,772 token; smoke 16 token, curator không ghi token.

Score là tỷ lệ 0–1; mean theo tác vụ/vòng có cùng trọng số cho ba họ. Min–max là dao động quan sát, không phải khoảng tin cậy. Token có cộng subagent; trace chỉ có luồng chính.


Mean score 9 run cũng là mean của ba mean theo vòng vì mỗi vòng có đúng ba tác vụ. Mean theo tác vụ dùng tỷ lệ passed/total để ba họ có trọng số bằng nhau; điểm không được tính bằng cộng tất cả check rồi chia chung. Điểm/triệu token = mean_score / mean_tokens × 1.000.000; không khấu hao chi phí curator/dev và không đổi token ra tiền.

## So với lượt chính thức

Baseline và subagents giữ mean eval **59,7306%** ở cả ba vòng. Skills-auto từ **78,8215%** lượt chính thức lên **82,5253%** ở mỗi vòng 2/3; mean ba vòng **81,2907%**, khoảng mean theo vòng **78,8215%–82,5253%** (độ rộng **3,7037 điểm phần trăm**).

Gain skills-auto so baseline theo vòng là **19,0909 / 22,7946 / 22,7946 điểm phần trăm**; gain trung bình **21,5600 điểm phần trăm**. Code giữ **10/11** và log giữ **9/10** cả ba lần; data thay đổi **5/9→6/9→6/9**, mean **0,629630**, min–max **0,555556–0,666667**. Lợi ích code/log được lặp lại trên chính các bài này, nhưng ba mẫu không chứng minh độ ổn định trên nhiệm vụ mới ngoài bộ eval.

Tổng check qua 9 run/condition: tất cả đạt **54/54 kỹ thuật**. Baseline/subagents đạt **0/36 quy ước**, skills-auto **20/36**; trong đó code 9/12, data 2/12, log 9/12. Hai check thêm so với lặp kết quả vòng 1 là rule_meta_block ở data vòng 2/3. Ba quy ước mới rule_version_bump/rule_sorted_keys_format/rule_source_line đều trượt cả ba lượt mỗi điều kiện: skills-auto **0/9** new-rule checks. Không có thay đổi skill dựa trên kết quả này.

## Chi phí và dao động

Mean token eval qua 9 run: baseline **32.344,11**, subagents **59.123,22** (**1,8279 lần** baseline), skills-auto **47.742,67** (**1,4761 lần** baseline). Mean giây/run lần lượt **42,48 / 93,33 / 45,69**; các tỷ lệ là quan sát, không phải bảo đảm độ trễ.

Điểm/triệu token qua ba vòng: baseline **18,47**, subagents **10,10**, skills-auto **17,03**. Lượt chính thức riêng từng cho skills-auto 18,18 so baseline 17,55; sau thêm hai vòng, baseline đứng đầu tỷ số này. Vì vậy không giữ nhận định skill tiết kiệm token chỉ dựa vào một lượt; skill đạt điểm cao hơn nhưng cũng tiêu thụ thêm token trên tập nhỏ này. Chi phí khởi tạo skill chưa tính vào tỷ số và curator usage không được ghi.

Dao động token theo task đáng kể dù điểm không đổi: baseline logs **13.742–27.088** (1,97 lần), subagents data **33.156–89.696** (2,71 lần), skills-auto code **71.363–98.266** (1,38 lần). Lượt code subagents vòng 3 kéo dài **265,8 giây**, so với **122,7/99,3 giây** ở vòng 1/2, nhưng vẫn 7/11.

## Cơ chế quan sát từ trace

1. **Meta đúng/sai làm điểm data biến thiên.** [Skills-auto data vòng 1](../results/skills-auto/data-eval/trace.md) đọc hai skill nhưng ghi meta.source='workspace/orders.json'; rule_meta_block trượt. [Vòng 2](../results/repeat-2/skills-auto/data-eval/trace.md) và [vòng 3](../results/repeat-3/skills-auto/data-eval/trace.md) chỉ đọc skill tabular, ghi meta.source='orders.json' và rows_in/rows_used đúng; check đạt. Cả hai vẫn ghi rev/100 thay vì cents, header clean theo id/placed_at/category/total_cents và không sort keys đúng chuẩn, nên ba quy ước còn lại trượt. Đây là đọc/làm theo một phần; không kết luận việc đọc thêm skill ở vòng 1 trực tiếp gây lỗi, vì chưa cô lập biến.
2. **Số lần giao việc và lượng ngữ cảnh thay đổi.** Subagents code có số task calls **1/1/2**; [vòng 3](../results/repeat-3/subagents/code-eval/trace.md) gọi explorer rồi reviewer, token 104.185 so 76.600/73.943. Data có **2/1/1** task calls: vòng 1 explorer + general-purpose tốn 89.696, vòng 2 general-purpose 58.844, vòng 3 explorer 33.156. Trace chỉ có lời giao/báo cáo cuối, không có nội bộ subagent; số call phù hợp overhead quan sát nhưng chưa chứng minh là nguyên nhân duy nhất.
3. **Công cụ có lỗi phục hồi, tăng chi phí dù điểm cuối không đổi.** [Skills-auto data vòng 3](../results/repeat-3/skills-auto/data-eval/trace.md) hai lần gửi timeout=120000s, tool trả 'exceeds maximum allowed (3600s)', rồi sửa tham số và chạy được; token 48.070 so vòng 2 31.167. [Skills-auto code vòng 3](../results/repeat-3/skills-auto/code-eval/trace.md) test regression phát hiện parse_duration('45m') sai, agent sửa và chạy lại, kết thúc 10/11; token 98.266. Đây là lỗi công cụ/triển khai bên trong đã phục hồi, không phải run.error hay lỗi harness cuối.
4. **Đọc không đồng nghĩa hiệu quả, số đọc cũng biến thiên.** Code skills_read **1/1/1**, data **2/1/1**, log **3/1/1**; cả 9 lượt skills-auto đọc skill. Log đạt 9/10 cả ba lần dù số skill đọc khác nhau. Subagents logs task calls **1/0/1** nhưng đều 6/10; cấu hình có subagent không bảo đảm agent sẽ gọi.

Bằng chứng tool calls được trích nguyên văn tại [repeat-behavior-evidence.json](repeat-behavior-evidence.json); không dùng hoặc suy diễn encrypted reasoning. Raw trace giữ nguyên và bị giới hạn 1.500 ký tự/message của helper provided; chỉ khẳng định phần thấy được.

## Kiểm chứng, hạn chế và bước tiếp theo

- Công cụ [analyze_repeats.py](../docs/runtime/analyze_repeats.py) dùng stdlib, không API, đọc dữ liệu rồi tái sinh repeat-table/metrics/audit/behavior-evidence. Kiểm tra đủ 27 record/trace, 18 record bổ sung, role/condition/score/token consistency; 6 skill runs bổ sung có cùng hash, timestamp sau freeze, không error/skills_modified. Manifest Windows được xử lý separator và cho phép riêng khác biệt xuống dòng LF/CRLF khi đối chiếu clone Linux; skill/run nguồn vẫn đối chiếu byte chính xác. Không sửa manifest hay tệp provided.
- Hash skill/Linux giữ **648e0f3ab02acb02cb940dc4a0d83d07210b0bafb71f7f9a67780867a614fa86**, tag **fc1f6dd**, byte nguồn chính thức và tệp cấm sửa không đổi. Verifier gốc vẫn báo 6 lượt chính thức OK; [repeat-audit.json](repeat-audit.json) kiểm tra riêng 6 lượt skill bổ sung.
- Toàn bộ test gốc sau 6e: **29/29**, JUnit [offline-after-repeats.xml](offline-after-repeats.xml). Bảng chính thức và hypotheses giữ nguyên, source không chỉnh theo eval; bản tổng quan cá nhân tiếp tục không được push.
- Chỉ ba lượt mỗi cặp trên **ba bài eval cố định**, một mô hình và thứ tự không ngẫu nhiên: chưa có kiểm định thống kê hoặc khoảng tin cậy. Min–max chỉ là dao động quan sát và không chứng minh variance=0 khi ba điểm giống nhau. Lặp cùng dữ liệu không tăng số loại nhiệm vụ; không đồng nhất 27 run với 27 tác vụ độc lập khác nhau.
- Bước tiếp theo: lặp thêm với budget được duyệt và thứ tự cấu hình ngẫu nhiên/cân bằng; thử bộ nhiệm vụ mới hoặc mô hình khác ở một thí nghiệm đăng ký trước. Muốn sửa skill thì tạo thí nghiệm mới, không di chuyển tag freeze này.

**Ngân sách:** phần 6e thêm **826.907 token** cho 18 lượt; toàn bộ lab **40 lượt tác vụ**, **1.955.772 token tác vụ đo được**, cộng smoke 16 token; curator một lần chưa ghi token. Budget giai đoạn bắt buộc 22 lượt ở final-metrics.json vẫn giữ làm lịch sử; số cộng dồn mới nằm trong repeat-metrics.json. Điểm thưởng cuối do giảng viên chấm, không tự khẳng định +5.
