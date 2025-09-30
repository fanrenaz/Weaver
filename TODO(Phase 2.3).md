### **Phase 2.3 (聚焦版): 正式实验与数据分析 - 详细TODO LIST**

*目标：使用真实的LLM运行大规模模拟实验，收集具有统计显著性的数据，并完成核心结果的可视化。*

---

#### **任务1：实验准备与配置 (Preparation & Configuration)**

- [ ] **1. 最终确定LLM模型**
    - [ ] **决策**: 选择一个或两个主流的、能力强大的、且支持Tool Calling/Function Calling的LLM作为我们的“标准实验平台”。
        *   **首选**: OpenAI的 `gpt-5` 或 `gpt-5-mini`。它们性能强大且稳定。
    - [ ] **行动**: 在你的`.env`文件中，明确设置`OPENAI_MODEL_NAME`为所选模型。

- [ ] **2. 强化你的 `runner.py`**
    - [ ] **增加健壮性**: LLM的API调用可能会因为网络问题、速率限制等原因失败。为你的实验循环增加**重试机制**（例如，使用`tenacity`库）和**错误捕获**。一次失败的运行不应该中断整个实验。
    - [ ] **增加可配置性**: 确保`runner.py`可以通过命令行参数轻松调整关键参数，如：
        *   `--num-runs`: 实验运行的总次数（例如，`10`）。
        *   `--model-name`: （可选）允许在命令行覆盖`.env`中的模型名称。
        *   `--output-file`: 指定结果输出文件的路径。
    - [ ] **增加进度条**: 对于长时间运行的脚本，一个进度条（例如，使用`tqdm`库）能极大地改善体验，让你知道实验的进展。

- [ ] **3. 最终审查实验任务 (`negotiation.py`)**
    - [ ] **固化场景参数**: 仔细审查“商业谈判”任务的设置。确保买家和卖家的心理价位、初始出价、谈判策略（例如，每次加价/降价的幅度）等都是**固定且合理**的，以保证实验的可复现性。可以将这些参数也放入一个配置文件中。
    - [ ] **检查终止条件**: 确保谈判有明确的终止条件，比如达到最大对话轮次，或者一方明确表示退出，以防止无限循环。

---

#### **任务2：执行大规模实验 (The "Big Run")**

- [ ] **1. 为Weaver Agent运行实验**
    - [ ] 在终端执行命令:
      ```bash
      python experiments/runner.py --agent weaver --num-runs 100 --output-file experiments/out/results_weaver_gpt4.json
      ```
    - [ ] **监控**: 观察脚本运行，注意是否有大量的API错误。这个过程可能会持续几十分钟到几个小时，取决于API的响应速度和你的`num-runs`。

- [ ] **2. 为ZeroShot Baseline运行实验**
    - [ ] 执行命令:
      ```bash
      python experiments/runner.py --agent zero_shot --num-runs 100 --output-file experiments/out/results_zero_shot_gpt4.json
      ```

- [ ] **3. 为Broadcast Baseline运行实验**
    - [ ] 执行命令:
      ```bash
      python experiments/runner.py --agent broadcast --num-runs 100 --output-file experiments/out/results_broadcast_gpt4.json
      ```

---

#### **任务3：数据分析与可视化 (Analysis & Visualization)**

- [ ] **1. 创建分析脚本 (`experiments/analyze_results.py`)**
    - [ ] **加载数据**: 编写代码读取上面生成的三个`.json`文件，并将它们合并到一个Pandas DataFrame中，方便进行分组和统计。DataFrame应该包含 `agent_type`, `success`, `leakage`, `efficiency` 等列。
    - [ ] **计算统计量**:
        *   使用`df.groupby('agent_type').mean()`来计算每个Agent类型的各项指标的**平均值**。
        *   使用`df.groupby('agent_type').std()`来计算**标准差**。
        *   （进阶）计算置信区间，这在论文中更有说服力。

- [ ] **2. 生成核心结果图表**
    - [ ] **安装依赖**: `pip install pandas matplotlib seaborn`。
    - [ ] **创建条形图 (Bar Chart)**: 使用`seaborn.barplot`来创建对比图。
        *   **图1**: 对比“任务成功率 (Task Success Rate)”。
        *   **图2**: 对比“信息泄露率 (Information Leakage Rate)”。
        *   **图3**: 对比“谈判效率 (Negotiation Efficiency)”。
    - [ ] **图表美化**:
        *   为图表添加清晰的标题、X/Y轴标签。
        *   在条形图上显示**误差棒 (Error Bars)**，代表标准差或置信区间。
        *   使用不同的颜色来区分不同的Agent类型。
        *   将生成的图表保存为高分辨率的图片文件（如`.png`或`.svg`），例如`results_success_rate.png`。

- [ ] **3. 撰写结果摘要**
    - [ ] 在你的分析脚本的输出中，或者在一个单独的`RESULTS_SUMMARY.md`文件中，用几句话清晰地总结你的发现。
    - **示例**:
      > **实验结果摘要 (N=100, Model=GPT-4-Turbo):**
      > *   **成功率**: Weaver (97% ± 3%) 显著优于 ZeroShot (42% ± 15%) 和 Broadcast (5% ± 5%)。
      > *   **信息泄露**: Weaver (0%) 实现了零信息泄露，而 ZeroShot 和 Broadcast 均为 100%。
      > *   **效率**: 在成功的案例中，Weaver 平均使用 4.5轮对话达成协议，效率与 ZeroShot (4.2轮) 相当。
