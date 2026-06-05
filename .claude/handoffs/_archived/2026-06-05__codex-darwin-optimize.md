# Handoff: codex-darwin-optimize

## 1. 意图与验收

问题：`zhang-xiaolong-skill` 已有强研究与产品决策模型，但 Darwin 基线评估指出显性检查点和失败分支不足，运行时遇到最新事实、平台特权、隐私/成瘾式增长时容易只靠隐含价值观处理。

完成 = `SKILL.md` 明确包含红灯检查点、失败分支和输出骨架；`scripts/quality_check.py` 能静态检查这些结构；独立 subagent 复评分数高于基线。

## 2. 范围

改了：

- `SKILL.md`：补 `🔴 CHECKPOINT：先停下的红灯` 和 `输出骨架`。
- `scripts/quality_check.py`：补红灯、失败分支、输出骨架检查。
- `test-prompts.json`：沉淀 Darwin 测试 prompt。
- `tests/`：归档旧 smoke 记录，新增本轮 Darwin 优化记录。

没改：

- 未修改六条研究线内容。
- 未联网补充 2026-06-05 后事实。
- 未重写心智模型、决策启发式、时间线和表达 DNA。
- 未处理另外两个旧 Skill；它们已在上层目录归档，后续由用户删除。

## 3. 改动

- `SKILL.md`：从隐含边界 → 明确 4 类红灯：事实、目标、平台特权、用户伤害；新增 9 条 `如果 X → Y` 分支。
- `SKILL.md`：从自由发挥式输出 → 固定落点：结论、用户任务、破坏点、替代做法、验证方式、失效条件。
- `scripts/quality_check.py`：从只检查章节/数量/来源 → 增加 Darwin 相关结构检查，防止后续删掉检查点。
- `tests/runs/2026-06-05__product-decision-smoke.md` → `tests/archive/2026-06-05__product-decision-smoke.md`：按测试归档规则移动旧产物。
- `tests/runs/2026-06-05__darwin-optimization.md`：记录基线分、复评分、横评结论、验证命令和未覆盖项。

## 4. 决策与假设

含糊点：是否做大规模重写。

选择：不重写，只做最小有效优化。

依据：基线 Skill 的研究、模型和启发式已经强；Darwin/subagent 指向的最低维度集中在检查点设计 2/10、失败模式编码 5/10。

何时重选：如果后续 full_test 发现输出模板化明显、角色味道被削弱，或普通增长/AI 问题被过度追问，再压缩输出骨架或改红灯触发条件。

## 5. 验证

命令：

```powershell
python scripts\quality_check.py
```

结果：PASS。新增检查项：红灯检查点 4 类、失败分支 9 条、输出骨架 6 步。

subagent 结果：

- 基线只读评估：78.8 / 100，最低维度为检查点设计 2/10。
- 优化版只读复评：83.2 / 100。
- 独立横评：推荐保留优化版，认为失败模式、检查点、输出稳定性、可执行性均优于基线。

环境前提：

- 维度 8 均为 dry-run，不是 full_test。
- 本地仓库基线已先推送到 GitHub：`https://github.com/Tongyawa/zhang-xiaolong-skill`。

未覆盖：

- 未做真实对话 full_test。
- 未联网校验最新微信/腾讯事实。
- 未请 Claude Code 做人工代码评审。

## 6. 风险与评审重点

重点查：

- `目标红灯` 是否仍会在普通增长/AI 问题中过度追问。
- `输出骨架` 是否让角色回答过于模板化。
- `用户伤害红灯` 的“不给实现细节”是否过硬，是否会阻断低打扰替代方案。

薄弱点：

- `SKILL.md` 的时间线和身份卡仍较长，可能稀释运行指令；本轮未处理。
- `quality_check.py` 是结构检查，不能替代真实对话质量验证。

未验证启发式：

- “普通产品取舍直接给结论”是否在多轮对话里稳定生效。
- “事实红灯”在可联网 runtime 里是否真的先查证。

## 7. 状态

分支/worktree：`codex-darwin-optimize` / `.claude/worktrees/codex-darwin-optimize`

base SHA：`9cc47e4`

提交：

- `9cc47e4 chore: establish zhang-xiaolong-skill baseline`
- `fc24bb6 fix: add Darwin checkpoints to zhang xiaolong skill`
- 本 handoff 提交为分支最后提交

已 rebase：否

已 push：否

## 8. 待办与移交

下一个 Agent：

- 集成时只把代码提交 `fc24bb6` 合入 `main`，不要把本 handoff 提交直接合进主线。
- 合并后运行 `python scripts\quality_check.py`。
- 将本 handoff 归档到 `main` 的 `.claude/handoffs/_archived/2026-06-05__codex-darwin-optimize.md`，单独提交。

阻塞：无。

待人决策：是否继续做第二轮优化，压缩时间线/身份材料并做 full_test。

---

## 评审

结论：有条件通过。

查了&命令：

- 独立 subagent 基线评估：78.8 / 100。
- 独立 subagent 优化版复评：83.2 / 100。
- 独立 subagent 横评：推荐保留优化版。
- `python scripts\quality_check.py`：PASS。

没查：

- 未做联网事实校验。
- 未做真实多轮对话 full_test。
- 未查 GitHub Actions；仓库无 CI。

问题：

- `SKILL.md:42` — 新增红灯会略增加模板感 — 建议后续 full_test 观察角色表达是否变硬。
- `SKILL.md:50` — 目标红灯可能误触发 — 已通过“已有具体产品、功能和指标则先给取舍”缓解，仍需实测。

最小修复：若误触发仍存在，只改 `目标红灯` 分支，不回滚整段 CHECKPOINT。
