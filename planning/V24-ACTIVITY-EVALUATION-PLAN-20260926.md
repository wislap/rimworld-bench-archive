# N.E.K.O RimWorld v2.4：通用活动求值层

状态：设计与实施计划，未开始编码。

本文为下一个小版本的工程计划。它不是一次新的模型实验，也不是救援专用方案。目标是把 Agent 目前反复手工完成的机械调查，收进一个可复用的深模块，同时保留 Agent 对目标、取舍和策略的控制。

## 1. 为什么需要这一版

当前三个仓库已经具备较完整的原生观察能力：

- Mod 能按 `actor`、`user`、`start`、`to` 读取路线、环境和对象状态；
- `look` 能读取人物状态、技能、装备、工作和指定 Stat；
- `inspect_state`/`look` 能用上下文检查床位、门、预约等原生谓词；
- 插件已经有对象解析、批量读取、分页、范围和完整性语义；
- `spatial_ranking.py` 已经能对同一执行者的已观测路径做有界排序。

但是这些能力仍以观察工具为中心。Agent 必须自己完成以下机械编排：

1. 把用户问题拆成活动阶段；
2. 展开执行者、对象和目的地的组合；
3. 为每个阶段绑定正确的 actor、user、origin 和 destination；
4. 为同一候选反复发出路线、状态和 Stat 查询；
5. 把每个结果放回正确的候选和阶段；
6. 选择同单位、同范围的指标进行比较；
7. 区分未计算、部分覆盖、当前可达和实际动作资格；
8. 再把这些结果重新组织成答案。

救援只是这个问题最明显的例子。物资运输、人员转移、取药、巡逻、设备操作和工作分工也会复用同一组关系。问题不是缺少一个 `rescue` 工具，而是缺少一个通用的活动关系执行层。

## 2. 版本目标

v2.4 交付一个插件内的 `evaluate_activity` 私有模块和一个 Agent 可见入口。它接收一个受限、可校验的活动描述，执行通用活动阶段，返回按候选和阶段组织的证据结果。

首版只实现两个活动原语：

- `move`：一个 actor 从自身当前位置或显式起点到目标；
- `transfer`：一个 actor 将一个 subject 从 subject 位置转移到候选目的地，自动展开接近段和转移段。

`transfer` 不是救援特化。它适用于伤员、俘虏、物资、药品和其他可被转移的对象。床位、门、药品和工作台仍由现有对象状态 Adapter 处理。

首版不执行游戏动作，不预测 Job 成功，不计算万能安全分数，不选择唯一最佳方案。它输出可比较的候选、条件、未知和原生读数，由 Agent 负责策略取舍。

## 3. 核心职责划分

### Agent 负责

- 识别用户想完成的活动；
- 选择活动原语和候选对象；
- 选择要比较的指标和偏好，例如速度、暴露、能力或目的地条件；
- 决定是否继续调查某个未决条件；
- 根据求值结果提出条件式方案、改变策略并向用户解释。

### 活动求值层负责

- 校验活动描述；
- 一次解析并绑定所有实体身份；
- 展开有界候选组合；
- 根据活动原语生成阶段关系；
- 将阶段关系编译成现有观察操作；
- 合并同一评价所需的重复读取；
- 保留每个结果的 actor、subject、origin、destination、stage 和 observation；
- 只在同单位、同范围、同状态下排序；
- 传播 `partial`、`not_computed`、`unknown`、歧义和世界变化；
- 返回确定性覆盖报告，不把“求值完成”说成“行动成功”。

### Mod 负责

v2.4 不增加新的 C# wire operation。活动层只调用现有的：

- `look` / `count`；
- `survey_space`；
- `inspect_route`；
- `inspect_state`；
- 现有的原生 Stat 和对象上下文检查。

这样可以避免同时修改协议、游戏 DLL 和 Agent 入口。需要的新语义应先在插件的活动契约中组合已有原生语义；只有发现现有 Mod 无法表达真实关系时，才单独提出后续 Mod 版本。

## 4. Agent 入口的最小接口

入口名称：`evaluate_activity`。

它不是通用 GraphQL，也不是让模型编写 Python。参数是一个受限的活动描述：

```json
{
  "kind": "transfer",
  "actor": {
    "candidates": [
      {"kind": "pawn", "name": "Rescue_Near"},
      {"kind": "pawn", "name": "Rescue_Doctor"},
      {"kind": "pawn", "name": "Rescue_Middle"}
    ]
  },
  "subject": {"kind": "pawn", "name": "Rescue_Patient"},
  "destination": {
    "candidates": {"kind": "things", "capabilities": ["sleeping_place"]}
  },
  "inspect": [
    "actor_state",
    "approach_route",
    "transfer_route",
    "destination_state"
  ],
  "compare": ["steps", "native_cost", "path_hazards"],
  "detail": "summary"
}
```

这个例子只说明语义，不是最终 wire schema。首版 schema 必须限制：

- `kind` 只允许 `move` 或 `transfer`；
- 每类活动有明确的必填角色；
- 候选数量有上限；
- 不接受任意字段路径、任意表达式、任意 Python、任意排序函数；
- `inspect` 和 `compare` 只接受注册过的活动能力和指标；
- 候选只能使用现有 ObjectRef、capability 或明确 ID/名称；
- 歧义返回候选，不静默选择；
- 没有目的地、无法解析 subject 或跨地图时直接返回结构化错误。

入口返回的顶层结构：

```json
{
  "status": "ok|partial|invalid|world_changed",
  "activity": {"kind": "transfer", "evaluation_id": "..."},
  "sample": {
    "load_epoch": "...",
    "snapshot_sequence": 12,
    "started_tick": 4,
    "finished_tick": 4,
    "atomic": false
  },
  "candidates": [],
  "comparison": {},
  "coverage": {},
  "unknowns": [],
  "limitations": []
}
```

## 5. 活动关系模型

活动不是答案模板，而是一个有类型的关系图。每个阶段都必须明确：

```text
stage.id
stage.kind
actor
subject
origin
destination
metric scope
observation ids
coverage
```

### `move`

```text
actor = selected actor
subject = none
origin = explicit start OR actor.current_position
destination = selected target
```

### `transfer`

对每个 actor × destination 组合生成两个阶段：

```text
approach:
  actor      = actor
  subject    = subject
  origin     = actor.current_position
  destination= subject.current_position

transfer:
  actor      = actor
  subject    = subject
  origin     = subject.current_position
  destination= destination.current_position
  hypothetical_start = true
```

第二段始终保留同一个 actor，并明确说明起点只是求值假设；它不表示 actor 已经拿起 subject，也不模拟携带后的速度、重量、预约或 Job 状态变化。

### 上下文检查

`destination_state` 可以对每个 actor × destination 绑定：

```text
user  = subject when the destination is used by the subject
actor = selected actor when the native predicate accepts an actor
```

返回必须保留原生谓词的真实范围。例如当前床位的 `IsValidBedFor` 从 actor 的当前位置检查，它不能被呈现成“搬到该床以后一定有效”。活动结果需要带 `meaning` 和 `not_evaluated`，而不是合并成 `can_use=true`。

## 6. 内部模块与接口

插件新增以下内部模块，外部只暴露一个活动入口：

### `agent/activity_contracts.py`

定义不可变的 `ActivitySpec`、`ActorSet`、`SubjectRef`、`DestinationSet`、`StageSpec`、`MetricSpec`、`ObservationBinding` 和 `Coverage`。

要求：

- 解析后所有引用使用稳定 ID；
- 名称解析结果必须保留候选列表和解析状态；
- `stage` 不允许缺 origin/destination；
- 指标携带单位、方向、可排序条件和未知策略；
- 活动对象不可在执行中被悄悄替换。

### `agent/activity_compiler.py`

把 `ActivitySpec` 编译成有界的 `EvaluationPlan`：

- 解析候选；
- 展开组合并计算上限；
- 生成活动阶段；
- 生成每个阶段需要的 `look`、`inspect_route`、`inspect_state` 请求；
- 去除完全相同的请求，但不合并不同 actor、不同 origin 或不同 sample；
- 在计划中记录每个请求对应的阶段和候选。

编译器不读取游戏、不判断推荐，不产生自由文本。

### `agent/activity_executor.py`

执行 `EvaluationPlan`：

- 复用现有 `ToolHandler` 和 `Observation`；
- 共享当前 run 的时间、读取和输出预算；
- 保持请求顺序，避免当前游戏线程并发；
- 遇到一次 world change 使整个评价标记失效，不把旧阶段拼到新世界；
- 保留原始 observation id 和请求参数；
- 将失败限定到对应候选/阶段，除非失败影响所有候选；
- 不执行任何游戏写操作。

### `agent/activity_compare.py`

只做可证明的比较：

- 同一阶段、同一目的地、同一 metric；
- 单位相同；
- coverage 足够；
- status 为可比较状态；
- 同值共享 rank；
- partial、unknown、not_computed 不进入正常排序；
- 比较结果表明“按该指标的观测值排序”，不写“最快”“最安全”或“最优 Job”。

### `agent/activity_presenter.py`

输出紧凑但关系完整的结果：

- 每个 candidate 一行；
- 每个 stage 使用独立的 `origin`、`destination`、`metric` 和 `scope`；
- 路线环境只在对应 stage 下出现；
- `hazard_cells=0` 只表示该阶段已覆盖路径未观察到该因素；
- 对象状态和路线状态分开；
- 不把程序计算字段伪装成 RimWorld 原生字段；
- 结果大时按 candidate/page 分页，而不是截断字段。

### `agent/activity_tools.py`

把 evaluator 注册成一个 Agent tool。它必须从 Mod 目录和插件自身的能力表生成 schema，不在 `prompt.py` 里维护第二份参数表。

## 7. 现有接口如何适配

活动层使用 Adapter，而不直接依赖各个底层实现：

```text
ActivityDataSource
  resolve(ref)
  read_object(ref, aspects, context)
  read_route(actor, origin, destination, detail)
  read_space(region, selection)
```

生产 Adapter 调用现有 semantic tools 和 world tools；bench Adapter 使用冻结世界和封存回执；测试 Adapter 使用最小 JSON fixture。

这样可以在没有游戏的环境中验证关系绑定、组合展开、单位比较和覆盖传播，不需要伪造模型质量结果。

需要明确三个 Adapter 的能力边界：

- **Fixture Adapter**：只验证编译、绑定、去重、排序和错误传播，不声称能够重算游戏路径。
- **Replay Adapter**：从 `base-A/base-B` 等封存请求与回执重建已发生的观察，验证历史路线的 actor/start/to/stage 绑定；它不重新运行模型，也不把回执变成新的游戏事实。
- **Native Adapter**：复用现有 `NativeWorld`/`WorldReadHost` 和生产 semantic interaction，执行真实只读请求。它只在实际连接广告 `world_observation.v2.2` 和 `spatial_query.v1` 时启用相关阶段；冻结 `FrozenWorld` 默认没有空间能力，不能假装支持 `inspect_route`。

这三个 Adapter 的输出都必须标记 `source_kind` 和能力集合。活动结果不能因为三个 Adapter 的 JSON 形状相同，就声称它们具有相同的游戏真实性。

## 8. 指标与比较的严格边界

“同单位”不是跨所有候选的充分条件。每个指标需要声明自己的比较域：

```text
metric_scope = (activity_kind, stage_kind, actor_identity_policy,
                subject_identity_policy, origin_policy, destination_policy,
                native_metric, unit)
```

例如：

- `transfer.approach.native_cost` 可以比较同一 subject、同一目的地、不同 actor 的返回值，但必须说明这是每个 actor 的当前位置到 subject 的路径；
- `transfer.transfer.native_cost` 可以比较同一 subject、同一目的地、不同 actor 的假设起点路径，但结果仍然是按不同 Pawn 的路径策略求出的值；
- `native_cost` 不能和 `steps` 混排，也不能自动变成“最快”；
- `path_hazards` 必须绑定具体 stage 和路径覆盖，不能把接近、搬送、取药的结果合并成一个“路线安全”值；
- `look` 的床位谓词和 `inspect_route` 的路径结果不属于同一 metric，不能合成一个布尔 `can_rescue`。

比较器只返回“按某一观测指标的排序”，不返回“最佳执行者”“最快到达”或“最安全方案”。所有跨指标取舍仍由 Agent 负责。

## 9. 不采用多个子 Agent 作为机械层

v2.4 不创建“每个候选一个子 Agent”或“路线子 Agent/床位子 Agent”。这会把当前问题复制成多个自然语言报告，随后还需要主 Agent 合并；它们可能采用不同 scope、sample 和未知口径。

如果未来需要多个 Agent，它们只适合策略层：例如产生不同的活动偏好或备选方案。所有策略 Agent 必须读取同一个 `EvaluationResult`，不能各自重新调查游戏。该方向不属于 v2.4。

## 10. 失败与未知语义

活动求值必须区分：

| 状态 | 含义 |
|---|---|
| `invalid` | 活动描述本身无法编译；没有发出游戏读取 |
| `ambiguous` | 引用有多个候选；要求 Agent 选择或缩小范围 |
| `not_computed` | 该阶段不适用于对象或缺少上下文 |
| `partial` | 读取有明确缺失或超出预算；其他结果仍可用 |
| `world_changed` | 评价期间世界/加载 epoch 变化；整份结果不可用于合并决策 |
| `complete` | 所声明阶段和指标都得到可比较的读数；仍不表示行动成功 |

任何 `unknown` 都必须带原因和所属阶段。缺失路径环境不能被呈现为空路径；缺少床位 actor/user 不能被呈现为床位不可用或可用。

## 11. 实施顺序

### M1：契约和离线执行器（插件）

- 新增 contracts/compiler/compare/presenter；
- 使用最小 fixture 覆盖 `move` 和 `transfer`；
- 先不注册 Agent tool；
- 验证所有绑定关系、组合上限、单位和未知传播。

### M2：生产 Adapter 与工具入口

- 将现有 `look`、`inspect_route`、`inspect_state` 接入 `ActivityDataSource`；
- 注册 `evaluate_activity`；
- 通过能力目录动态生成 schema；
- 增加功能开关，默认保留现有工具和旧路径。

### M3：原生 smoke 和回放

- 用 `base-A/base-B` 封存路线回放验证三人 × 床位的阶段关系；回放只重建历史观察，不重新计算缺失路径；
- 必须证明 Middle 搬送阶段的毒气值保留为 2，不能被取药或接近阶段覆盖；
- 运行现有 v23 native probe 风格的真实游戏只读检查；
- 不调用模型、不改存档、不替换生产 DLL。

### M4：接入 Agent 的受限默认体验

- 仅在 Mod 宣布 `world_observation.v2.2` 且插件开关启用时展示；
- Agent 可以继续使用 `look/count/inspect_route` 诊断或处理活动层明确不支持的请求；
- `evaluate_activity` 失败时返回结构化原因，不自动把原始长 JSON 倾倒回模型；
- 旧接口完全保留，便于回滚。

## 12. 仓库改动与验收顺序

### Plugin 仓库

新增：

- `agent/activity_contracts.py`；
- `agent/activity_compiler.py`；
- `agent/activity_executor.py`；
- `agent/activity_compare.py`；
- `agent/activity_presenter.py`；
- `agent/activity_tools.py`；
- 对应 fixture、replay 和 contract tests。

修改：

- `agent/semantic_tools.py`：提供 `ActivityDataSource` Adapter，而不是把 evaluator 逻辑塞入 `look`；
- `query_tools.py` 或工具装配路径：仅在能力广告和 feature flag 同时满足时注册 `evaluate_activity`；
- `README.md`：记录活动契约和不保证的行动语义；
- `config.example.toml`：增加显式 opt-in 开关，默认关闭。

不修改：

- `agent/loop.py` 的总生命周期和提交契约；
- 180-token handoff；
- 默认审查；
- 旧 `look/count/inspect_route` 的语义。

### Mod 仓库

v2.4 目标是零 C# wire 变更。只做必要的目录/能力广告修订和 BridgeSmoke 回归；如果发现活动所需的原生事实不存在，另立 Mod 版本，不在本版本偷偷添加一条救援判断。

### Bench 仓库

新增离线验证：

- `tests/test_activity_contracts.py`：最小 fixture；
- `tests/test_activity_replay.py`：历史回执绑定；
- `tests/test_activity_native_adapter.py`：原生只读 smoke 的契约验证；
- `programmatic/activity_replay.py`：只读重建与 provenance 报告；
- `planning/evidence/activity-evaluation-v24/`：只保存契约、回放和 native smoke 摘要。

不新增付费模型 runner，不修改历史评分，不生成新的“救援准确率”。

验收顺序固定为：

1. fixture contract tests；
2. replay binding tests；
3. plugin full regression；
4. Mod BridgeSmoke/build；
5. native read-only smoke；
6. tool registration and opt-in integration。

任何一层失败都停止，不进入下一层；没有“模型跑起来再看”的补偿路径。

## 13. 验收标准

这些是确定性工程验收，不是模型准确率承诺：

1. **绑定验收**：三 actor × 三 destination 的所有阶段都能追溯到正确 actor、subject、origin、destination。
2. **反例验收**：固定回放中，Middle 的三条 transfer 路线均保留 `ToxGas=2`；任何接近或取药路线不能覆盖它。
3. **组合验收**：同一 activity spec 在 JSON、冻结世界和最小 fixture Adapter 上得到相同的候选/阶段结构。
4. **比较验收**：不同单位、partial、unknown、不同 actor 或不同阶段不能进入同一排序；相同值有稳定并列 rank。
5. **失败验收**：歧义、world_changed、过大结果、过期 cursor、目标消失均有结构化错误，并且不产生伪成功。
6. **预算验收**：组合上限、单请求上限、总读取预算和输出预算都在编译阶段可见；不能执行后才静默截断。
7. **交付验收**：结果包含原始 observation IDs、scope、sample 和 limitations；不把 `complete` 命名为 action success。
8. **兼容验收**：旧 Mod、旧工具和旧报告路径行为不变；功能开关关闭时零行为变化。

## 14. 明确不做的事情

- 不新增 `rescue`、`find_bed_for_patient`、`best_doctor` 等场景专用工具；
- 不新增“安全分数”“最佳执行者”“最短成功 Job”等黑箱派生结论；
- 不让 Agent 编写 Python 或任意查询程序来使用活动层；
- 不使用多个子 Agent 分摊机械读取；
- 不把活动求值当作行动执行或行动成功预测；
- 不修改 180-token handoff、不启用默认审查、不做新的模型矩阵；
- 不在本版本中删除 `look/count/inspect_route`；
- 不以软件测试通过宣称复杂救援能力已达标。

## 15. 完成定义

v2.4 完成的含义是：活动描述可以被确定性地编译和执行，结果能保持跨阶段关系、范围、单位、覆盖和未知，并在冻结回放及原生只读 smoke 中通过。

它不等于：Agent 已经能稳定选择所有活动、能生成正确的救援建议、能预测 Job 成功，或已经具备自主游玩能力。

如果这条深模块在完成后仍不能减少 Agent 的机械查询负担，或者 Agent 仍必须重新理解原始路线 JSON 才能使用结果，那么 v2.4 设计没有达到目标，应停止扩展而不是继续加指标。

## 16. 并行验证的三个接口变体

为了避免再次进行不可归因的模型矩阵，v2.4 可以并行实现三个**同一内核、不同 Agent 表面**的变体。三者共享 `ActivitySpec`、`EvaluationPlan`、`ActivityDataSource`、执行预算和结果绑定；只改变 Agent 能表达什么以及结果如何呈现。

### A：保守契约版（推荐基线）

Agent 只能提交显式对象引用和有限阶段：

```text
kind: move | transfer
actors: explicit ids/names
subject: one explicit ref
destinations: explicit refs or one registered capability selector
metrics: registered metrics only
```

特点：

- 不支持任意自然语言目标、任意字段路径和任意排序；
- 不自动选择指标；
- 不输出跨指标总分；
- 每个候选返回完整的 stage matrix、coverage、unknowns 和原生限制；
- 比较器只做单指标、同范围、同阶段排序；
- 结果中不出现“最佳”“最快”“安全”等结论词。

它最适合验证核心是否真的保持关系和范围。代价是 Agent 需要表达更多结构，不能作为最终用户体验。

### B：Agent 简化版

Agent 只看到一个较小的 `evaluate_activity` 工具：

```text
activity kind
actor candidates
subject
destination candidates
preferences
```

`approach_route`、`transfer_route`、`destination_state` 等阶段由编译器按活动原语固定展开，不由 Agent 逐项指定。`preferences` 只能引用已注册的比较维度，例如 `shorter_route`、`lower_observed_hazard`、`higher_observed_stat`，不能传入公式。

特点：

- Agent 不再写机械调查计划；
- 能够直接验证“较小接口是否足以承载高层意图”；
- 隐含策略较多，若默认展开不适合某个任务，可能产生不必要读取；
- 不能把固定展开称为通用规划器，活动原语仍有明确边界。

这是最接近产品目标的 Agent 表面，但应建立在 A 的契约和回放全部通过之后。

### C：兼容混合版

Agent 同时看到：

- `evaluate_activity`，用于通用活动比较；
- 现有 `look/count/inspect_route`，用于活动层明确不支持的局部事实或后续追问；
- `submit_response`。

特点：

- 活动求值承担主机械路径；
- 原始工具保留诊断和补充事实能力；
- 活动层失败时不会把整份原始 JSON 自动倾倒给模型；
- Agent 可以在活动结果指出 `unknown` 后自行做一个窄范围补读。

它是最安全的迁移方案，但 Agent 仍可能绕过活动层重新手工编排。因此它适合验证兼容性和渐进迁移，不适合单独证明机械负担已经消失。

### 并行验证顺序

三种变体不能各自拥有一套 evaluator。实施顺序应是：

1. 先让 A、B、C 生成完全相同的 `EvaluationPlan` 和底层读取请求；
2. 用同一组 fixture 检查三者的 actor/subject/origin/destination/stage 绑定一致；
3. 用历史 `base-A/base-B` 回放检查三者都保留 Middle 搬送阶段的 `ToxGas=2`；
4. 用同一真实 native smoke 检查三者只读请求、覆盖和错误语义一致；
5. 比较 schema 大小、结果结构、未知传播和回滚行为；
6. 只有 A/B/C 的确定性结果一致后，才考虑极小的模型接线 smoke；该 smoke 不产生质量率，不决定生产晋升。

不做三组新的 agent 质量实验，不做三种 prompt 变体，不做三组子 Agent。若 A 与 B 在确定性结果上不一致，先修接口或放弃其中一个，不用模型结果掩盖契约差异。
