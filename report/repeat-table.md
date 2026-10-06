# Phần 6e: bảng thống kê ba lượt eval

Lượt 1 là kết quả chính thức; lượt 2/3 từ results/repeat-2 và repeat-3. Không trộn vào table.md.

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
