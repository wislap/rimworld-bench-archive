# v1.10：在当前共同基线上复测四项候选

2026-09-19。**阶段：准备与离线预演；尚未授权正式API运行。** 不恢复已停止的旧实验，不部署、不改变生产默认，不把mock结果当模型质量。

## 用户确认

- 先准备并离线预演。
- 模型：`glm-5.3-flash`，提供商OpenAI Chat Completions入口 `https://open.bigmodel.cn/api/coding/paas/v4`。使用现有客户端；不切Anthropic或Responses协议。尚未请求/验证该服务是否支持当前stream/tool/usage设置。
- 12题，每格一次。四项各自与独立当前基线配对，每项24咨询，合计计划96；不是共享12次基线反复当成四项配对。
- 新身份/持有者世界为主，历史回归单列。密钥不写入任何源码、计划或工件；正式运行再提供私有配置，本阶段不读取密钥。

## 基线

插件`9181d5d`，Mod`b5a02ab`，准备前bench`28dbace`。实际运行以封存源文件和DLL hash为准，bench准备实现可能包含未提交修改。宿主只读，不改；生产插件与Mod源码不改。候选D仅在实验副本改C#并单独编译。

所有臂固定：原始问题、世界、当前生产research/completion policy、claims当前行为、工具提交schema、文本answer+detail、模型设置、90秒运行/15秒收尾、180模型文字/200总运输上限。`NEKO_PUBLIC_REFERENCES=0`显式固定。不得把claims拒绝数当作模型能力改善，不新增gate或把历史TASK_POLICY偷偷引入生产基线。

基线每次从原始用户问题自主取证，不能预注入参考查询/期望值/菜单/正确答案。参考资料只在scorer与离线表达力探针使用。

## 四个比较

| 顺序 | 候选 | 唯一干预/归因边界 |
|---|---|---|
| 第一梯队A | working_data | 完成的读批次转换为证据数据消息；保留请求、结果、错误、partial、公开assistant文本；审计原轨迹不变。工具和生产prompt不改。 |
| 第一梯队B | answer_task（P） | 仅替换system submission段；原文来自task-depth PLAIN_SUBMISSION，非v1.6 task_goal；工具描述/schema、停止规则不变。finalization使用同样替换。 |
| 第二梯队C | semantic | 当前修正后的look/count及其结果投影；共享当前生产prompt主体、提交器和截止，只用TOOL_GUIDE替代query目录。是整个接口包比较，不声称只测工具名或token。 |
| 第二梯队D | aggregate_default | 复制当前C#：无group/select/显式limit/offset/order/on/上层projection的aggregate默认limit0且不编译默认实例字段；对应目录说明同步。不是删除已读结果行，也不是伪造过滤。 |

A/B不组合；B不叠T/B；C不加新的语义规则或偷偷补缺失能力；D不改模型查询参数。修C的表达力缺陷需要明确另记候选revision、重新离线预演再封存。

### C候选修订1（离线发现后、正式调用前，用户已确认）

首版和第二版prepare均在`steel-detail`发现`hit_points/max_hit_points`缺失，其他11题有限表达探针通过。用户选择“补齐通用明细后重验”。因此仅给bench的`LISTING_FIELDS['things']`增加这两个原生字段，不增工具、不修改生产插件或Mod、不改题目。准确值/null/未采集三种路径都走真实冻结查询回归，聚合与明细数量保持不变。此前失败工件保留，修订后用新目录封存；C不再冒称与ABC历史适配器逐字相同。

## 12题固定内容

8题来自 `.bench-data/identity-heldby-20260918/snapshot.json`：

1. 白银简单总量/实例数，明确只要简答。
2. 钢铁完整总量 + **只展示一行ID/数量/当前最大耐久**；区分列表与总量完整性。
3. 含持有/迷雾的塑钢，禁止把持有当所有权。
4. 已生成自由殖民者完整名单及真实身份/派系。
5. 医疗候选比较与依据/限制。
6. 烹饪候选、禁用与健康条件比较。
7. 一个实际非玩家人类Pawn的身份和装备/穿戴/库存/搬运清单，区分持有与可交易。
8. 可见spawned Building实例总数及完整定义分布，不推建造来源。

4题取既有世界（源路径和hash封存）：黄金含持有74/3；白银800/2与零部件42/6；Campos缺pain派生快照；整图8192扫描限制+独立完整零部件量。历史附件未注入，本轮黄金是当前状态范围回归，不冒称历史报告机制测试。

三层分别报告：`current_identity`8题、`historical_regression`3题、`historical_missing_fields`1题。每层内部仍非独立世界随机抽样。名单/具体名字来自游戏事实，不包含参考答案提示。

独立参考以捕获native graph/index读取资源、人物身份/技能/健康字段，另以当前基线C#执行显式参考查询交叉核对。字段缺失不得填0。所有cases有manual contract，自动评分应是manual_review_required，不再出现case_contract_missing；不假装regex能裁决自由推理。

## 离线必须验证

1. 生产默认与adapter baseline在research/finalization的prompt、工具schema完全等价（排除每轮时间数字）；P只改submission段；A只改读取消息投影。
2. 封存当前插件、当前Mod源码/fixture、两份新编译DLL、执行器全部递归依赖、每份快照；核验哈希，不借用旧DLL。
3. D实际触发：同一个未指定select/limit的完整聚合，基线有非空rows，候选无rows/page，聚合/范围/扫描完整性不变；显式参考查询两DLL完全一致。
4. C每题程序化表达探针，检查原题所需字段/人口/范围可得到。**缺耐久等字段则记离线block，不能删题或改要求通过。**有限探针成功也不证明通用表达力；失败阻止此候选live准入。
5. 全部96槽位mock预演仅查地图后提交，覆盖进程/封存/真实工具/提交/记录路径；它不回答题目，不评分为质量pass，不覆盖表达力block。
6. 复用已有versions调度，AB/BA按题交错；每slot新进程、env隔离、日志发送前/后fsync，started无receipt不自动重发，输入变化不能resume。
7. 模型原始输入不带参考答案、case contract或semantic探针结果；密钥不入档。mock通过httpx.MockTransport，外部模型请求0。

## 正式运行前另行确认

正式调度尚未开放在v110入口；四份计划带`offline_only:true`，通用versions入口在读取配置/启动worker前也拒绝这些计划的live执行。需先解决离线block、人工审阅参考与判据、确认端点协议/模型限制和有限额度。预期192–约500次模型请求只是粗量级，不是费用承诺；GLM新端点不能沿用旧DeepSeek费用估计。max_output32768也必须在正式协议检查时确认支持，不暗中降参。

正式矩阵顺序：先A24、B24并复核；随后C24、D24，C未过表达力门则明确标24槽位未启动。失败不自动补跑；未知费用请求不重发；任何代码变动须新档案。单个题失败不作为删除该题的理由。

## 判断标准（开发筛选，不是上线证明）

同一题配对报告原始结果：

- 正文与短交接分别：必需事实/清单覆盖、数值/主体/单位、范围/完整性/未知、推测依据、过度/欠执行；major/minor/review区分。
- 允许基于证据的推断；不能因为不是逐字复制而判错。额外正确细节与严重幻觉分开。
- gate拒绝/提交成功/数字出现/非空回答不等于质量通过；保留原始首次提交和所有修复。
- 比较模型往返、取齐后查询、重复读、查询构造与提交失败（按唯一事件计数）、使用的候选机制、token已知/未知、模型等待与进程准备时间。
- 只在两臂均满足任务时谈正确答案成本；不以漏答/少说/超时省token作为收益。
- 候选出现明确导致的重大退步或表达力缺失，暂停晋升并定位；效果不清晰归为待确认，而非为了通过放宽标准。
- D另报实际省略暴露、同批补回、随后查回。未形成信息差异时，不将总分不变解释成“减少明细无效”。
- 每格一次、12题不能证明统计等效/稳定总体错误率；第一梯队通过后也不自动合并或部署。

## 入口

`python bench.py experiment retest prepare --out NEW_DIR`

`python bench.py experiment retest check --out DIR`

`python bench.py experiment retest mock --out DIR`

输出包括四份versions plan、带contract的cases、scorer-only references、semantic-capability、aggregate-default-probe、公开model-profile（无key）、源码与DLL、manifest、mock回执。`check`只校验哈希和报告block，不把软件通过冒称质量通过。

## 离线实现审计与修正轮（正式运行之后）

用户质疑“是否存在 bug 或意外设计缺陷”后，主代理用**正式运行封存的源码、DLL 与原快照**做离线黑盒复现（零模型调用），确认多个确定缺陷并完成修正。证据：

- 缺陷报告：`.codex/experiments/rimworld-v110-deepseek-full-20260919/implementation-audit/FINDINGS.md`
- 修正记录（含前后哈希）：`.codex/experiments/rimworld-v110-correction-20260919-170512/correction-record.json`
- 原始红测试脚本与输出：`.../rimworld-v110-deepseek-full-20260919/implementation-audit/v110-*-audit.py` 与 `*-red.txt`

### 实际命中本轮数据的缺陷

| 缺陷 | 命中 | 修正 |
|---|---:|---|
| 完整聚合被当成部分列举的全称断言 | 5 次 | 聚合叙述与明细列举分账；同一总体的聚合完整性跨结果节点按 `from/args/where/规模` 关联 |
| `include_held=未包含持有物` 被读成“包含” | 1 次 | 动词级否定（未/不/没/无 + 可选 包含/包/含） |
| `count(detail=0)` 实际读并返回默认 20 行 | 16 次/7 场 | 未分组 count 只在 `detail>0` 时取明细 |
| 原生 scope 说明经两次投影被丢弃 | 30 次/12 场 | `_scope` 同时认打包后的 `notes` 与旧键 |
| 分组计数自加实例 `id`，自造 21 条 partial | 1 场 | 分组读取不再选入主语字段 |
| 单对象 `map` 重名时擅自取第一个 | 未命中（反例） | 歧义的单对象 kind 交回候选；pawn/thing 逐个列出是有意保留 |
| `pawns` 按 `map` 分组抛 `KeyError` | 未命中（反例） | 补齐 `GROUP_PATHS['pawns']` |
| 非零 offset 末页被当成完整列举 | 未命中（反例） | 完整列举要求 `offset==0` |
| 紧贴中文的数字未被量词提取 | 潜在漏放 | 边界改为 ASCII 标识符字符 |
| 父持有者只有不透明 `ref` | 命中（误推诱因） | 明细改为 `spawned` + `parent_holder.runtime_type`，并内联语义 |
| 耐久字段可发现性 | 命中 2 次无效尝试 | `count` 说明列出明细行内容；新增耐久 null 语义 |

### 准入门禁的缺口

旧 `semantic-capability` 门只查“调用没抛错 + 少数数字相等 + 耐久键存在 + 缺失/下界标记出现”，上述契约缺陷全部漏门。现在新增 `semantic_contract_findings()`，对每条探针的**模型可见结果**检查：detail 语义、分组完整性、原生 scope/参数说明是否到达、歧义是否只回一个对象。门禁自身有红能力测试。

### 修正后的验证

- 插件 Python：254 通过（含新 `tests/test_claims_contract.py` 56 项）
- bench Python：458 通过（含新 `tests/test_v110_contract_repairs.py` 10 项）
- 四组原始缺陷探针在修正后实现上全部转绿（`POSTFIX FAILURES: []`）
- 强化门禁下重跑完整离线准备：12 题契约全通过，`reference_errors=[]`

### 解释边界

- 旧 96 份回执**原样保留**，描述的是修正前的实现，不能当作修正后候选的成绩。
- 不能用“删掉几次误拒”推算新成绩：模型的后续轨迹会随错误反馈改变。
- 新配对必须使用**新封存的基线**，旧基线分数不可复用。
- 本轮未晋升任何候选为生产默认，未改 Mod，未部署。

## 15. 修正后首次配对的再审计（第二轮）

在 `correction2` 封存下完成首次重新配对（96/96、274 请求、无失败流）后，对**本轮实际回执**做同类审计，又确认两类问题并修复：

### 15.1 聚合叙述豁免过窄（误拒 2 次）

数字型量词的豁免原本要求子句里出现聚合名词，于是“基于全部 20 个匹配项计算”、“总量是全部 20 个匹配的完整聚合”仍被拒。已改为：数字分支靠**逐行列举措辞**反向排除，不再强制聚合名词；标签分支（“唯一/只有”）仍保守。

同时校正了“非零 offset 末页”与“紧贴中文的数字未被提取”两处（后者靠 `\w` 边界错误，导致 `所有20实例都已逐项检查` 根本没进入检查）。

### 15.2 证据绑定用的是整篇而不是子句（保留缺陷）

`check_claims` 把**整篇文本**交给 `_evidence_present`，再用其中的“被提及主体”决定授权。后果双向：

- **漏放**：“Alice 的身份已读取。Bob 是殖民者。”——“Bob”没有派系证据，却因同篇提到 Alice 而被放行（实测三例）；
- **误拒**：建筑题明细里满是 `Thing_*` 行 id，而“按阵营筛选属于玩家阵营的实例为 0”的子句里并无对象名，证据（已执行的 `where.faction.is_player`）因此不被承认。

已改为**按命中断言所在子句**绑定证据，并补四例红测试（三例串证 + 一例反向误报）。这把该缺陷从“已知未修”变成“已修且有回归”。

### 15.3 修正后应保留的真错

重新配对中仍被拒的两例是**真错**，不是误拒：模型声称“64 个部位全部读取（has_more=false）”“全部为满血”，而该轮 `body_parts` 只返回 20/64（另一例 10/64）。门禁保留这类拒绝是设计意图。

### 15.4 账本与取代关系

首轮重新配对（`rimworld-v110-deepseek-repair-20260919`，276 请求）的回执在旧门禁下产生，已被后一轮取代；其消耗**不重置**，由 `--carry-budget` 显式编入同一授权账本（1000 请求／2000 万 token）。被取代的回执与账本原样保留。


## 16. 冻结后的最终轮（gate3 / repair2）

门禁在用户决定下**冻结**，不再打补丁；`rimworld-v110-deepseek-repair2-20260919` 是最终有效轮次。

- 96/96 交付，**0 degraded**（修复前 1 degraded）；287 请求、5 356 360 tokens；无 HTTP 错误。
- 独立核验：48 配对、287 个成功流全部从解析前记录重建一致。
- 逐例复核 96/96：`review-recovery/quality-aggregate-final.json`（`complete=true`、`errors=[]`）。

分层结果（每臂 12）：

| variant | 基线 pass/fail/review | 候选 pass/fail/review | major 基线→候选 |
|---|---|---|---|
| working_data | 10/2/0 | 10/1/1 | 2→1 |
| P 任务表达 | 9/3/0 | 11/1/0 | 2→0 |
| semantic | 12/0/0 | 12/0/0 | 0→0 |
| aggregate_default | 11/1/0 | 9/3/0 | 0→0 |

Tier 1（working_data + answer_task）：基线 19/5（4 major）→ 候选 21/2（1 major）。
Tier 2（semantic + aggregate_default）：基线 23/1 → 候选 21/3。

效率：语义候选在**请求数相同（各 37 次、尝试数也同为 37）**且质量同为 12/12 的情况下，tokens 由 736 475 降至 250 887（−66%），来源是 `detail=0` 不再回传实例明细。P 候选 35→31 请求、763 902→608 675 tokens 且质量 9/3→11/1。

### 16.1 门禁审计更正（重要）

§15 之后新增的 `gate-audit.json` 曾断言“5 条非长度拒绝全部成立”，**该结论已作废**：它只验证了拒绝能在冻结门禁下复现，未判断拒绝是否正确。更正见 `gate-audit-corrected.json`。

本轮 22 次提交拒绝 = 16 次 `handoff_over_budget`（长度上限，设计如此）+ 6 次语义拒绝。其中 **4 次为误拒**，且**全部偏宽松**（挡住了正确句子）：

- `answer_task--21-baseline` ×2：`body_parts` 后一轮已 `matched=64, returned=64, has_more=False`，断言为真，校验命中了上一轮的陈旧部分读取（§15.3 当时判为“真错”，实为误拒，此处更正）；
- `semantic--05-baseline`：`identity_claim`（“0 个属于玩家阵营的玻璃钢堆”，观测已含 `is_player=false`）与 `ownership_claim`（原句是免责句“……因此不对『殖民地自有玻璃钢数量』下结论”）；
- `semantic--14-candidate`：`ownership_claim`（原句“这些只是『她持有』的事实，不构成我方财产或可交易物资，不能直接说成我们的或可出售”）。

`health_completeness_claim`（`working_data--10-candidate`，“没有伤员”而 conditions/body_parts 从未读全）判为**可辩**，不算误拒。

**误拒的下游后果**：`answer_task--21-baseline` 的正确断言被拒后，模型重交时把 `answer` 换成占位句“无需重复的要点已并入上段。”，`handoff` 即该句（11 tokens），宿主只收到空壳——**本轮唯一一次交付失败源自门禁误拒加模型重试行为**，不是已修复的交付层。

### 16.2 聚合默认仍无支持证据

候选臂 24 包中**未出现任何 matched>0 的裸聚合**，新默认从未被真正触发，故本轮既不能支持也不能否定该假设，只能说暴露为 0；且该臂质量 11/1→9/3 略差。

### 16.3 复核自查

辅助复核为证据绑定的 AI 复核（hash 绑定 + 逐字引文回查），非独立人工盲评。已发现并登记两处代理瑕疵：`semantic--12-baseline-cook` 引用的 `spawned_count` 报错在包内不存在（真实为 `requests/0/select/3/status`，且仅 1 次）；`semantic--14` 的失败次数被夸大约 5 倍（实测 `semantic_request_invalid` 5 次、`ownership_claim` 1 次）。两者都不改变任何 pass/fail 判定。
