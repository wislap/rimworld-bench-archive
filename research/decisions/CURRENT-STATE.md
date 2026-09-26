# 当前基线与下一项实验

更新：2026-09-18。此页是当前入口；旧版本报告保留原实验条件和原始结论。

**最新：[v1.9 阶段二结果](V19-STAGE2-RESULTS.md) —— 不晋升。** 18 对 × 2 臂、仅 deepseek、34/36 回执、34 份复核。新臂（`look`/`count`）vs 旧臂（原生 query）：**构造失败 5→14**、**提交失败 6→24**、请求 50→76、耗时 +78%；**token 972k→498k（−49%）**。质量：旧臂 **17/17 通过**，新臂 **14/17**（3 份 major）；配对 **3 对只有旧臂通过、0 对新臂通过**。三个失败里两个同因：`held:false` 被误用且把排除持有物的结果描述成“含被持有”——scope 标志极性不一致且 schema 未说明 `false` 含意。止损条件“质量下降”成立，故不晋升。

以上两行已过期，保留为历史：下一版设计记录见 [VERSION-1.9.md](VERSION-1.9.md)。

**下一版设计已登记：[v1.9 语义工具接口](VERSION-1.9.md)。** 依据是 46 场新接口咨询的实测失败分布（路径块 `read` 87.4% 失败，类型化 `observe`/`measure`/`discover` 4.5–11.8%）。设计提案，未实现、未跑模型；三份并行设计稿在 `.bench-results/v1.9-designs/`。实施前有 6 道离线门，任一不过不得进在线实验。

**待在有游戏的机器上执行：[身份字段重采快照](RECAPTURE-IDENTITY.md)。** Mod 侧已新增原生身份投影（`faction.is_player`、`is_free_colonist` 等），构建与测试通过；但冻结基准的 4 份快照采集于修改之前，本环境未装 RimWorld 无法重采，因此**实机验证仍缺**。校验脚本：`verify_identity_capture.py`（含拒绝旧采集的负向测试）。

**最新：[简化接口配对实验结果](SURFACE-PAIR-RESULTS.md)。** 计划144咨询，DeepSeek48/48、Sol16/48、Kimi0/48，共64份回执及64份复核；其余80份因服务/暂停规则未启动，所有模型请求已停止。DeepSeek旧→新：全文明确pass10/24→10/24、重大错误7→7、正常交付24→22、请求101→205、构造失败11→114。初始接口更短，但未证明回答质量改善，调用效率退步，未晋升生产。DeepSeek准入门槛有[公开纠正记录](SURFACE-PAIR-ENROLLMENT-CORRECTION.md)，原失败探针保留。工件：`/home/yun_wan/.codex/experiments/rimworld-surface-paired-20260917`。

**此前离线调查：[模型接口简化可行性](MODEL-INTERFACE-FEASIBILITY-RESULTS.md)。** 最终源码136/136历史有效调用等价（271子查询），相关31项测试通过，初始模型接口约14k→2k tokens；高级请求参数反而增加17.6%。仅证明工程可行性，新增在线模型调用为0，真实可靠性和Unity性能未验证，未晋升生产。

**此前在线实验完成：[v1.8机械负担诊断](VERSION-1.8-BURDEN-RESULTS.md)，96/96真实咨询、96份主复核。** 同菜单手工查询到可代执行组，请求97→72、含JSON的查询构造失败28→4，但全文明确pass仅11/24→14/24；收益主要来自Kimi，DeepSeek请求48→47、pass5/12→5/12。证据直给仍有5份实质错误，不能宣布幻觉解决或模型纯判断能力已测清。生产没有晋升。E额外展示colony_id的输入差异已披露；其历史题不能作等信息归因。原v1.7确认题在本轮已使用，未来不能再称首次未见确认。

v1.7已按用户要求停止，完整验证未完成，见[收尾记录](VERSION-1.7-CLOSEOUT.md)。v1.8是另立的有限诊断，没有覆盖或回填v1.7结果。以下“正在执行”等文字是9月15日历史检查点。

正在执行[v1.7五组架构完整验证](VERSION-1.7-STATUS.md)：原开发160槽位与7个环境故障补充已执行，双评分及全体主代理裁决进行中；确认和机制阶段尚未启动，未晋升任何候选。下文跨模型结果仍属于此前的固定证据研究。

## 当前保留的实现

- 插件：v1.6研究截止/收尾预留、流大小边界、请求审计；v1.6输入默认候选已撤回。
- Mod：public_query.v2、v1.6.1选择/条件兼容、十个原生枚举域、H6扫描诊断、对象/位置/持有/未知语义修正。
- 最新返回契约：aggregate且显式limit:0不返回rows/page；完整相同的嵌套聚合不再错误partial；include_unreal说明按实际后代遍历修正。
- 聚合默认省略明细、单字段答复、目录裁剪和其他提示组合没有成为生产默认。
- 包版本仍1.0.0；上述研究阶段名不等于发布版本。游戏安装DLL仍为9月9日部署版。

## 整理与归档

整理前可恢复快照：
`/home/yun_wan/.codex/experiments/rimworld-checkpoint-20260915-131038`

包含四仓Git bundle及验证记录，插件/Mod/bench的257份工作树文件，未提交和暂存差异；宿主为浅克隆，bundle只代表本地已有历史。未移动或覆盖历史实验目录。

已形成通过验证的本地提交：插件31b7ab3、Mod2d10e4f、bench基线db97300；clean-baseline/内有三仓新bundle与验证记录。未推送远端，未部署游戏DLL。当前软件检查为bench247、插件175、UI13项通过及BridgeSmoke通过；Mod构建零错误，保留既有nullable/GraphQL分析器警告。

历史研究索引为[EXPERIMENT-INDEX.json](EXPERIMENT-INDEX.json)，它不是所有研究的全集。正文阅读顺序：

1. [v1.6结果](VERSION-1.6-RESULTS.md)：默认候选撤回及运行机制保留。
2. [枚举](VALUE-DOMAINS-RESULTS.md)、[v1.6.1](VERSION-1.6.1-RESULTS.md)、[H6](H6-SCAN-DIAGNOSTICS.md)：局部查询改进。
3. [语义一致性](SEMANTIC-CONSISTENCY.md)、[语义清理/评分勘误](SEMANTIC-CLEANUP.md)。
4. [聚合默认候选撤回](AGGREGATE-DEFAULTS.md)、[任务深度](TASK-DEPTH-EXPERIMENTS.md)、[答案保真](ANSWER-FIDELITY-EXPERIMENTS.md)。
5. [返回契约修复](RETURN-CONTRACT-REPAIR.md)：确定性修复与尚未改善的全文质量。

## 重要测试勘误

9月15日调查发现：默认FrozenWorld DLL滞后源码，直接pytest的241通过不能证明新源码全绿。重建后240通过、1失败：test_semantic_contract.py仍要求limit:0聚合返回rows=[]。

现已同步该断言，仍保留精确2/0、null、未读取字段和真实协议检查。新增统一入口，先强制重建冻结引擎再测试：

```sh
uv run python bench.py diagnose software
```

原实验封存与报告正文未覆盖；本页记录勘误。该入口只编译和测试，不启动游戏、不调用模型。

## 跨模型对照

见[CROSS-MODEL.md](CROSS-MODEL.md)。比较gpt-5.6-terra、kimi-k2.7-code、deepseek-v4.1-flash的相同固定证据首次回答。查询选择、修复循环、宿主转述不在这一阶段的结论范围内。

[两组完成结果](CROSS-MODEL-RESULTS.md)：Kimi与DeepSeek各42次；全文明确通过28/42与21/42，明确不通过各9，歧义5与12。Terra服务阻断，尚未完成三模型目标；不将此表作为通用模型排名。

## 协作与判断原则

用户明确要求后续讨论保持独立批判性判断。用户提出的解释、模型偏好和设计不是证据；实施者此前的结论同样可以被新反证推翻。保留明确错误、歧义和无证据结论的区别；不得为迎合期望修改实验标准或选择性丢弃结果。
