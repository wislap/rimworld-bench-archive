# RimWorld机制核对：撤回上一轮未经充分校准的总分

2026-09-23，依据RimWorld Wiki、本机1.6.4871 rev600程序集/Defs/简体中文翻译，以及四份已有存档数据重新核对。没有重新调用模型，也没有在本轮运行救援动作模拟。

## 必须纠正的审查依据

1. **“医疗床”术语误判。** 本机中文明确 HospitalBed.label=医疗床，普通Bed.label=单人床，Medical开关=医疗专用。已保存的localization.json直接记录翻译。故“没有医疗床，仅有两张单人床”，如果是在列建筑类型，就是正确事实；不得强制解读成不存在任何Medical=true的普通床。baseline/05-combined原先唯一主要fail依据不足，撤销该依据。“若需医疗床加成则没有”也有事实根据：HospitalBed的MedicalTendQualityOffset为0.10，普通床没有该加成。只有明确否定普通床的医疗指定状态、或说普通床不能治疗，才是另一条可核实的错误。
2. **没有床或药不等于无法急救。** Wiki Drafting/Doctoring与本机FloatMenuOptionProvider_DraftedTend共同确认征召后可原地无药包扎。代码检查Doctor工作类型禁用、操作能力、目标与可达性等，但没有最低医疗等级门槛，也不要求床或现成药物。因此“医疗3可以先止血”有机制基础，不能仅以没有读取专门资格工具判错。没有床主要限制普通Rescue送床流程，不排除原地处理或手动搬到指定位置。
3. **普通床医疗用途与治疗质量不是一回事。** 普通床设Medical用于安排病人/去除所有者等；不是HospitalBed的0.10质量加成。床不是失血后恢复意识的必要条件；止住出血后血液可自然恢复。
4. **Slowpoke只直接改移动，有依据。** 本机SpeedOffset度数-1/1/2分别对应MoveSpeed偏移-0.2/+0.2/+0.4，未直接修改治疗质量。仅说“慢性子影响赶路，不直接降低治疗质量”正确。degree=2不是实际+2格/秒；但孤立“+2”也可能只是档位简记，不应自动判成有单位的错误。
5. **高医疗技能作为主治推荐依据合理。** Wiki和本机Stats_Pawns_WorkMedical.xml显示医疗技能、操作、视觉影响治疗速度/质量。Near的医疗3、视觉0.5、操作0.96与Doctor的医疗16、视觉/操作1.0相比，推荐Doctor负责治疗有充分机制基础。实际一次治疗仍有随机、药效/上限等因素，不能由此保证每次结果或整段任务必定最快。
6. **出血率不是无时间语义。** 本机HealthUtility.TicksUntilDeathDueToBloodLoss使用 (1-BloodLoss.Severity)/BleedRateTotal*60000。0.36相当于当前每游戏日36个百分点的失血；不是每秒0.36。当前失血0.65，按速率恒定估算约58333 ticks=23.33游戏小时。此为游戏公式的当前状态估计，不是对未来伤口变化、治疗、火灾等的模拟保证。原工具仅保留raw并不意味着客观机制不可求。

## 仍有客观依据的错误

- 将0.36写成0.36/s，和真实时间尺度不符。
- 将整体健康汇总0.92写成血量92%，与血液损失严重度0.65混淆。
- 将Touch路径终点(141,123)当患者真实位置(140,124)。
- 将两堆药的32步、6步合并称均6步；将(118,135)到(140,124)直线距离写13.6（应约24.60）。
- 将实际倒地的患者包括在“四人均未倒地”内。
- 火源场景中没有发现实际火源；但若答案诚实说安全未知，这属于未完成，不自动等同错误安全结论。距离短可作为有条件启发式，不能自动当实际路线更安全的证明。

## 对先前分数的处理

撤回“7通过/4受限/13失败”和“完整救援4/4失败”作为已确认结论。原始24题运行、136次请求、用量、工具错误轨迹仍有效，原始回答保留。原审查混入中文术语误解、过度要求每条常识来自tool、以及没有先按游戏机制校准建议合理性的问题。不能只机械减掉一个错误判定就发布新的准确率；本次给出的是已核实的逐项机制更正，不冒称完成了新的24题综合评分。

今后分别评价：游戏事实是否错误；建议是否符合机制/属于合理策略；当前工具能否验证该实例的动作；测试回执是否缺失。一般游戏常识可来自Wiki/本机定义，不以“tool没返回”自动判事实错误。

## 来源

- [Drafting](https://rimworldwiki.com/wiki/Draft)：原地有药/无药包扎、手动搬运。
- [Doctoring](https://rimworldwiki.com/wiki/Surgery)：治疗与包扎机制。
- [Rescue](https://rimworldwiki.com/wiki/Rescue)：普通送床与手动搬运区别。
- [Medical Tend Speed](https://rimworldwiki.com/wiki/Medical_Tend_Speed)：医疗、操作、视觉与全局工作速度。
- [Medical Tend Quality](https://rimworldwiki.com/wiki/Medical_Tend_Quality)：人物治疗质量及其他因素，普通床与HospitalBed区别。
- [Traits](https://rimworldwiki.com/wiki/Traits)：Jogger/Fast walker/Slowpoke效果。
- [Blood loss](https://rimworldwiki.com/wiki/Blood_loss)：失血阶段、意识上限与自然恢复。
- [Hospital bed](https://rimworldwiki.com/wiki/Hospital_bed)：专用建筑与治疗加成。

部分Wiki正文直连返回403，检索工具返回了可读索引正文；存在未验证标记的公式优先以本机程序集核对。本目录source/为本机反编译的核对材料，不是新游戏实测或正式产品源码变更。source/Verse.HealthUtility.cs:552–560为死亡时间公式；RimWorld.FloatMenuOptionProvider_DraftedTend.cs为本机原地包扎入口；Verse.Hediff_Injury.cs中已包扎伤口BleedRate返回0。
