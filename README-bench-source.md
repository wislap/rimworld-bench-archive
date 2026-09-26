# RimWorld Bench

离线 Def 快照验收：[合成 fixture 与零模型请求说明](cases/defs/README.md)。与历史 live 实验分开；不代表模型质量或真实游戏定义。

最新：[简化接口配对实验结果](planning/SURFACE-PAIR-RESULTS.md)。64份真实咨询及复核（DeepSeek48、Sol16；80个预定槽位未启动）。DeepSeek全文明确通过旧/新均10/24，模型请求101→205、查询构造失败11→114；未证明能力提升，未晋升生产。服务阻断、预检准入纠正、完整分母与证据见报告。统一现状入口为[CURRENT-STATE](planning/CURRENT-STATE.md)。

以下为历史检查点：[v1.7完整架构验证状态](planning/VERSION-1.7-STATUS.md)。充值后已完成160个原开发槽位及7个单列环境故障补充，正在双评分和全体主代理裁决；确认尚未启动。272项软件测试及40个真实宿主的零API双轮接线场景通过，不代表架构有效。执行依据见[固定计划](planning/VERSION-1.7.md)及[宿主验收细化](planning/VERSION-1.7-HOST-VALIDATION.md)。

当前入口：[基线、归档与测试勘误](planning/CURRENT-STATE.md)；最新[同证据跨模型结果](planning/CROSS-MODEL-RESULTS.md)：Kimi/DeepSeek84次完成并复核，Terra服务阻断、42次主样本未启动。软件验证使用 `uv run python bench.py diagnose software`，先重建冻结引擎，避免旧DLL测试假绿。

独立开发评测项目，不是 N.E.K.O 插件的运行依赖。使用 Inspect AI 管理样本、重复试验、评分和日志；直接调用工作区里的生产 AgentRuntime / OpenAICompatibleModelClient，以及 Mod 的原始 C# GameQueryEngine。

## 从这里选择实验入口

最新：[接口语义一致性完整记录](planning/SEMANTIC-CONSISTENCY.md)：对象/位置/持有/未知说明从原注册表统一，96次原始用户问题完整内部Agent对照完成；确认全文通过16/24→18/24但读取35→38，尚无稳定总体收益。

此前：[H6扫描诊断落地与验证](planning/H6-SCAN-DIAGNOSTICS.md)：查询层按真实扫描范围说明补救限制，32次生产引擎对照分两版保留；受限查询少了无效重试，可恢复Item/Pawn保护都完成，额外解释错误仍未解决。

此前：[v1.6.1完整结果](planning/VERSION-1.6.1-RESULTS.md)。32次真实对照，查询恢复改善、请求87→58；严格复核未改善，错误扩写和正确停止仍未解决。

此前后续：[原生枚举值域完整结果](planning/VALUE-DOMAINS-RESULTS.md)。24次真实对照，品质值域核对改善；全文复核9/12→10/12，尸体题仍有错误解释。保留全部10域的通用校验，未增加Agent游戏工具。

此前从[v1.6完整结果](planning/VERSION-1.6-RESULTS.md)开始：140个真实会话已完成。模型输入候选减少约20%请求，但两批正常预算确认未证明正确率改善，已撤回默认；查询语义、截止控制和采集修复保留。原始结果、评分修订、候选源码与边界均记录。

此前[阶段成果与交接](planning/RESEARCH-CHECKPOINT.md)及[自主查询对照](planning/AUTONOMOUS-EVIDENCE-RESULTS.md)保留各自历史条件，不能与本轮直接混成一个准确率。

此前[交互架构实验结果](planning/INTERACTION-RESULTS.md)：两轮60个会话、130次模型请求已完成；分阶段、自然结束和上下文查询的正反证据均保留，不与后续不同条件的结果直接合并评分。

[v1.5 原计划](planning/VERSION-1.5.md)的自然结束主线已降为待验证假设。该阶段执行的[交互架构对照](planning/INTERACTION-STUDY.md)，比较同时/分阶段输出、自然结束和上下文查询；实验不改变生产默认，也不宣称已完成宿主交付。

历史结果见 [v1.4.2 集成与对照](planning/VERSION-1.4.2-INTEGRATION.md)：选择编译器、文本提交反馈与评测记录已改进；18 次完整任务中非法查询 10→1、模型调用 31→20，但固定观察成文质量没有改善，仍未发布稳定版。26 个样本及 59 次模型响应全部保留，成功交付与语义质量分开报告。

历史 v1.3 结论见 [v1.3开发实验](planning/VERSION-1.3-RESULTS.md)：通用查询与答复片段候选已实现，但完整Agent出现覆盖和取证效率回退，E2按计划提前停止，未发布1.3。原始实验与已尝试样本均保留；没有把软件测试或局部渲染通过当作质量改善。

[v1.3完整改进方案](planning/VERSION-1.3.md) 已整理：按公开schema完整覆盖的统一筛选与事实呈现、Mod资源读模型、开放Agent分析、统一提交/草稿协议、兼容及完整实验矩阵。禁止主题专用focus或药品参数旁路；旧专用参数列入迁移清理。方案已实施并经历否定性实验；当前候选未达到晋升要求。

历史 v1.2 结果见 [v1.2第二批实验](planning/VERSION-1.2-ITERATION-2.md)：完成数量表达消融与受控参数恢复，共24次实验。数量删减未显示稳定内容收益，已撤回；保留参数定位、发现引导及“未知精确总量/已知下界”的评分修复。恢复轮数未改善，不以较短提交宣称整体提速。

此前的 [v1.2第一批](planning/VERSION-1.2-ITERATION-1.md) 实现资源v2结构和原生药品筛选，尚未发布1.2。

现有26轮已完成[统一离线质量复核](planning/VERSION-1.1-QUALITY-REVIEW.md)：参考由世界图独立生成，正文/摘要按同一五维规则处理，自动结果与实现者辅助复核分开保留，新增真实API调用为0。Inspect和显式配对入口现已共用合同评分；复用旧配对结果可用`--score-existing`。

本项目用于迭代 **RimWorld Agent tools**：固定数据，比较工具方案与 Agent 行为。当前统一入口和输入输出说明见 [ENTRYPOINTS.md](ENTRYPOINTS.md)。

此前开发结果见 [1.1第一轮实现与真实API实验](planning/VERSION-1.1-ITERATION-1.md)：三组26次咨询，分别比较契约、交付要求及错误反馈；保留改善与退化结果，不把交付率当回答正确率。显式tools配对可用 `experiment versions --plan` 指定两组源码、查询DLL和自然问题。

```sh
uv run python bench.py --help
uv run python bench.py experiment resources --mode mock --repeats 1
uv run python bench.py experiment resources --help
```

入口按 `experiment`（运行实验）、`prepare`（准备固定方案）、`data`（采集与案例）、`analyze`（分析结果）、`diagnose`（机制探针）分组。原脚本仍可直接调用；总入口不修改实验逻辑或自动运行付费实验。全文自然语言自动评分不是启动工具迭代的前提。

下文保留历次实现、实验和数据边界说明；其中 G0–G2 的准入状态属于对应历史研究计划，不作为所有 tools 实验的统一门槛。当前资源 1.0 及宿主探针结果另见 [资源工具升级实验](planning/RESOURCE-UPGRADE-1.0.md)和[宿主实验记录](planning/RUNTIME-PROBE-20260910.md)。

## 历史 G0–G2 研究状态

新运行会同时记录旧的数字标签诊断与 `quality_contract_score`。后者区分 `pass / fail / unscorable / invalid`，核对完整答案、handoff 与实际观察；有 `unscorable` 或 `invalid` 时，不得把显示的比例解释成完整语义准确率。当前自动批准的文字仍限受控数字短句；证据适配已覆盖可见地面、资源栏缓存、储存组 HeldThings、殖民者穿着/库存和穿着与地面并集。各范围含义不互换，未知表述或无法确定身份/覆盖的观察仍待复核。

35 个软件校准例通过；协议 canary 已完成 12 次、3,872 token；58 条不同历史查询回放一致。更大候选对比尚未就绪，详见 [G0–G2 实施记录](planning/G0-G2-IMPLEMENTATION.md)。这些结果不是新候选效果提升，也没有迁入生产策略。

证据适配后续结果见 [G0 证据适配记录](planning/G0-EVIDENCE-ADAPTERS.md)。它把“参考数量是否有充分观察支持”和“整篇自然回答是否正确”分开报告，不把证据覆盖率当成答案准确率。

自然回答检查现增加受限的堆数/明细算式核验、原文位置与复核输入哈希。[复核规则 v1](planning/NATURAL-REVIEW-RUBRIC.md)明确数值匹配不能批准整段解释；[后续实施结果](planning/G0-PROSE-CALIBRATION.md)保留新发现和未解决项。

剩余15份现已完成[实现者辅助开发复核](planning/G0-DEVELOPMENT-REVIEW.md)：9份有依据、1份过程描述矛盾、5份具体规则/语义证据不足；未覆盖自动分数，也不冒称独立盲评。用户取消聚合预算后，[三轮固定观察实验](planning/FINALIZATION-LIVE-RESULTS.md)已执行24次真实请求、146331 token：24次正常响应、21次首次提交通过，未晋升任何生产提示。

随后完成[初始/当前版本的自然提问Agent闭环对照](planning/VERSION-AGENT-E2E-RESULTS.md)：12轮、54次模型请求。初始默认0/4交付，输出参数统一后的初始版2/4，当前3/4；但当前两次资源概况均困在岩块分页、主要物资未查全，不能把交付率当整体质量提升。最近评测阶段的生产源码与首份基准一致，未声称已部署新策略。

```sh
# 零模型调用的软件校准；输出路径须为新文件
uv run python calibrate_quality.py --out ../.bench-results/my-calibration.json
```

对已有冻结日志生成审计和元数据盲化的本地复核包（零模型请求；须给新输出目录）：

```sh
uv run python audit_readiness.py --snapshot /绝对路径/snapshot.json --log /绝对路径/run.eval --review-packets --out ../.bench-results/my-review
```

只向复核者提供输出中的 `review-packets/` 和复核规则；`private-review-index.json` 保留分组映射，不交给盲评者。导出包不会自动改分、上传资料或启动评审模型。包里的完整观察可用于追查，不只是摘要；原文位置按 Unicode 字符索引而非 UTF-8 字节。

## 全自动入口

不需要点游戏菜单或手动切 DLL。以下命令会构建采集器，创建独立 quicktest 实例，等开局过渡结束后自动暂停、导出、退出，验证快照并建立参考案例，再进行原版/候选各三次的交错对比：

```sh
uv run python workflow.py --out ../.bench-results/my-run --read-neko-config
```

只采集与验证、不调用模型：加 `--capture-only`。后续优化应复用同一快照：加 `--snapshot /绝对路径/resources-....json`，避免拿不同开局的成绩直接比较。`--out` 必须为新目录，历史结果不覆盖；默认整个配对评测合计 200 万 token 调度预算。

自动实例使用独立保存目录和唯一采集 Mod ID，不加载网络桥接 Mod，不改已有游戏的加载配置/DLL链接。任务结束会移除自己创建的临时 Mod 链接，保留快照、构建记录与日志；超时或取消只清理自己启动的子进程。模型密钥不会传入采集游戏进程。没有明确自动采集参数时，普通游戏不会触发自动采集。

当前采集器按原生对象身份去重，避免地图持有容器被数万物体路径重复展开；保留 100,000 节点限制。游戏字段原本会抛出的错误以错误形式冻结并回放，不伪装成空数据。两次真实 quicktest 导出及回放检查已成功；并不意味着所有更大地图/Mod 组合都已通过。

```text
N.E.K.O_rimworld/
├── N.E.K.O/plugin/plugins/neko_rimworld/  产品，不放评测数据或 Inspect 依赖
├── RimWorldMod/NekoRimWorld/             产品 Mod，与插件一起迭代
├── rimworld-bench/                      独立 Git 仓库、Python 环境与开发导出器
├── .bench-data/                         真实存档、冻结数据、旧实验归档（不在三个仓库内）
└── .bench-results/                      Inspect 日志、结果和临时打包产物
```

旧插件 `evaluations/` 已原样移至 `../.bench-data/legacy/neko-rimworld-evaluations-20260908/`。其中脚本可能修改在线配置、重载插件；仅作为历史归档，不属于新运行入口。插件的 `[tool.neko.build].exclude_dirs` 提供打包防漏，不能只依赖 `.gitignore`。

## 快速使用

在此目录运行（需要 uv、.NET 8 SDK）：

本工作区的 K 盘为 `noexec` 挂载，因此 `.venv` 指向用户缓存目录 `/home/yun_wan/.cache/rimworld-bench-runtime`，未改磁盘挂载选项；旧环境保留在 `.bench-data/runtime-archive/`。在其他 `noexec` 工作区可用 `UV_PROJECT_ENVIRONMENT=/可执行目录/venv uv sync --locked` 安装环境。全自动入口由 Python 驱动，查询和测试通过 `dotnet` 加载 DLL，不要求在工作区执行原生 apphost。

```sh
uv sync --locked
dotnet build frozen-world/FrozenWorld.csproj
uv run pytest -q
uv run python run.py --mode mock --repeats 1
```

`mock` 只测试“生产 SSE 解析 → Agent → 实际查询引擎 → 提交 → Inspect”是否通畅；模型是脚本替身，事实分数为零是预期，不能当能力结果。

真实模型基线：

```sh
uv run python run.py --mode live --read-neko-config --repeats 3 --log-dir ../.bench-results/baseline
```

此选项只读取 `127.0.0.1:48916` 上插件**现有模型服务地址、模型名和密钥**。不保存密钥，不修改在线配置，不调用在线 Agent，也不重载 N.E.K.O 或连接游戏。模型的其它设置采用产品默认值，包含 max_output_tokens=32768，实际参数会记入日志。也可自行设置 `RIMWORLD_BENCH_BASE_URL`、`RIMWORLD_BENCH_MODEL`、`RIMWORLD_BENCH_API_KEY` 环境变量，不使用 `--read-neko-config`。

查看及汇总：

```sh
uv run inspect view --log-dir ../.bench-results
uv run python summarize.py /绝对路径/运行.eval --out ../.bench-results/summary-unique.json
```

不要把真实密钥作为命令行参数或写进案例文件。`.eval` 包含问题、模型公开回答、调用参数和游戏观察，真实存档日志应按私人数据处理，不自动上传。隐藏推理文本不记录，只有产品本来提供的推理 token/长度等元数据；日志不是模型完整思维过程。

## 这版实际测什么

第一批是**合成资源场景**，不是用户当前存档：65 个无关石块、分堆钢铁、地面/库存药品、迷雾物资，以及“资源缓存为零但实际有库存”的反例。

| 用例 | 能捕捉的问题 |
| --- | --- |
| visible-ground | 精确按物品定义查询、可见范围、正确汇总 |
| medicine-held | 地面与随身库存的范围区分、容器漏读 |
| cached-vs-observed | 缓存≠实际总量、储存物与地图物重复计数 |

三个问题 × 三次重复；每次独立 Agent 状态和查询子进程。没有预录 query→response 表：改变字段、过滤器或分页后，原 C# 引擎重新执行查询。工具、schema、系统 prompt 来自产品文件，没有另写一套 Agent。初始导出 profile 未捕获的字段/带参数 getter 会返回 `snapshot_field_not_captured`，不伪装为零、空列表或成功 null。

旧 `resource_facts` 评分只核对答案末尾约定标签的事实数字，另外记录交付与成本。它仅作诊断，**不证明解释文字正确或所有结论都有证据**。新的合同评分在其支持范围内检查两种答案表面与证据，其余明确待复核；不能将这些待复核样本偷偷作零分或删掉。

记录 snapshot/cases 的 SHA256、源仓库 commit/dirty 状态与实际源码哈希、编译 DLL、bench 文件、模型参数和 schema_id。汇总按比较指纹分组，禁止把不同模型/数据/源码悄悄合成一个平均分。A/B 还要确认 sample_keys 相同；本批是开发集，没有独立 holdout，不报告“泛化提升”。

后续运行还会在 `../.bench-results/inputs/` 本地归档选中的源码、快照与案例，元数据记录压缩包校验值；不会打包在线配置或密钥。首轮 `baseline-v1` 在此归档功能加入前完成，只有源码/数据哈希及完整请求轨迹，不宣称包含可还原的全套源码包。

## 预算与重试

- 串行执行；Inspect 外层重试为 0，生产客户端原有安全重试仍保留并逐次计费/记录。
- 产品默认 90 秒运行预算；每样本最多 12 次模型尝试，全套最多 108 次。超过基准限制是 `benchmark_budget`，不是上游 API 故障。
- 默认全套调度 token 预算 2,000,000；发请求前按输入估算 + 最大输出预留，有返回用量时结算；未知用量不释放预留。
- 这是防止无界请求的**调度护栏**，不是账单硬上限：不同供应商 tokenizer、计费和失败计费方式可能不同。请同时设置供应商账户限额。
- 原 httpx 模型客户端不经过 Inspect 内置模型接口，所以 Inspect 原生 model usage 显示 0 不等于免费。看每样本 scorer metadata / evidence.requests 的真实用量与 missing_usage。
- Inspect 页头的 `mockllm/model` 是自定义 solver 的占位模型；实际是否联网以 `mode` 为准，真实服务模型在 `model_settings` 与每次请求 response 中记录。
- 冻结查询采用 5000ms 读预算用于语义测试；不能据此声称解决了真实 Verse 12ms 读预算、游戏卡顿、桥接或 Hosted UI 并发问题。

## 采集真实存档（下一道验收门）

提供独立、可选的开发 Mod，仅增加 `RimWorld Bench → Export paused resources snapshot` 调试动作，无启动任务或网络端口。它链接产品读取代码，不修改生产 Mod，不会自动安装。

```sh
uv run python stage_capture.py --out ../.bench-results/capture-dev-unique
```

已安装并启用采集 Mod 后，使用专用入口确保加载的 DLL 与当前构建一致。可以选择 quicktest 新局，不要求手工准备存档：

```sh
uv run python launch_capture.py --staged ../.bench-results/capture-dev-v3 --quicktest
```

它拒绝在游戏运行时切换 DLL，核对产物/源码哈希与 Mod 启用状态后，更新独立采集 Mod 的链接。`--quicktest` 自动创建测试局；不带该选项则启动到菜单，供指定存档采集。不会杀游戏进程或覆盖旧 DLL。`--check` 只核验并准备链接，不启动游戏。quicktest 的新游戏状态同样可冻结；后续对比使用导出的同一份快照，不在每次模型评测时重新开局。

采集步骤：

1. 先自行保存游戏。将产物作为单独开发 Mod 安装/启用，重启游戏并载入希望测试的存档。日常游戏无需保留启用。
2. 从开发者调试动作菜单执行 `Export paused resources snapshot`。采集器会显式暂停游戏，确认暂停成功后再同步采样，结束后保持暂停，并弹窗显示成功路径或失败原因。无需依赖调试菜单自身的临时暂停。采样可能短暂冻结 UI；它是离线采集，不是生产实时路径。
3. 只在采样前后同一个游戏/地图集/tick、仍然暂停，且现场/冻结查询比对通过时，发布完整 `.json`。失败不会发布有效数据集。
4. 导出位置是**当前游戏用户数据目录**的 `RimWorldBench/`，日志会给完整路径。将 JSON、对应 `.rws`、`capture-build.json` 一起保存到 `../.bench-data/<场景>/`；存档不会自动复制，防止误拿另一份保存。
5. 导出包括所有已加载地图的 spawned Thing 索引、定义、资源/仓储/殖民者装备及库存关联。任意 Mod 子容器的全图 thing(id) 查找、健康/心情/按参数统计等不承诺覆盖；未捕获必须报错。不是“整个 RimWorld 完整模拟器”。
6. 内置同 tick parity 检查是有限资源查询集，不是全 schema 等价证明。将本轮 Agent 的实际查询加入回归 corpus 后，才扩大覆盖。首轮真实游戏导出尚需实际运行验收，编译成功不等于游戏内成功。

离线复核导出时保留的现场查询，然后为该快照建立独立案例（结构参考 `cases/resources-cases.json`），再运行：

```sh
uv run python verify_snapshot.py ../.bench-data/场景/snapshot.json
uv run python run.py --mode live --read-neko-config --snapshot ../.bench-data/场景/snapshot.json --cases ../.bench-data/场景/cases.json --repeats 3
```

自定义快照必须同时指定对应案例，入口拒绝把合成参考答案套到真实存档上。参考数字需通过人工核验的查询/游戏 UI 确定一次，不能采用被测 Agent 自己的回答作为标准答案；之后重复试验与比较是自动化的。

## 如何推进优化，而不扩大产品复杂度

先保留基线，再实验 `--variant resource-focus`：只在现有工具目录 context 后追加一段资源调查策略，不改模型工具集合，也不写入生产 prompt。

```sh
uv run python run.py --mode live --read-neko-config --variant resource-focus --repeats 3 --log-dir ../.bench-results/candidate
```

先比较同样本事实正确率、交付率与失败类型，再比较请求数、token 与耗时。不要用“更便宜但漏物资”的候选替换产品。这个开发集稳定后，增加真实冻结场景与独立 holdout，再决定是否把验证有效的 prompt 或 query 设计修改迁回产品；不预先建设通用平台、数据库或额外 Agent 服务。

基础设施参考：[Inspect 自定义 solver](https://inspect.aisi.org.uk/solvers.html)、[scoring](https://inspect.aisi.org.uk/scoring.html)、[日志查看](https://inspect.aisi.org.uk/log-viewer.html)。依赖锁定在 `uv.lock`，C# 在两个 `packages.lock.json`。

### Reasoning effort diagnostic

`reasoning_study.py` seals eight existing public evidence contexts and compares
one-shot `deepseek-flash` low/high/max decisions with identical inputs and
independent per-slot budgets. It performs no new game reads or production edits.
`reasoning_grade_packets.py` creates arm-hidden review packets;
`reasoning_integrity.py` checks actual wire differences and usage after completion.
See [the results](planning/REASONING-EFFORT-RESULTS-20260925.md) for limitations,
protocol/content separation and the preserved failures. This is not an
end-to-end rescue acceptance benchmark.
