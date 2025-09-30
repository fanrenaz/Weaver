#### **Phase 2.2: 学术实验平台搭建 (Building the Research Platform)**

*目标：创建可复现的、可量化的实验任务和评估指标，为撰写论文的“Experiments”章节收集决定性的数据。*

**TODO LIST:**

- [ ] **1. 设计并实现“实验运行器 (Experiment Runner)”**
    - [ ] 创建一个新的目录，例如 `experiments/`。
    - [ ] 在 `experiments/runner.py` 中，编写一个主脚本。它的功能是：
        1.  加载一个“实验配置”文件（可以是YAML或JSON）。
        2.  根据配置，循环运行多次模拟（e.g., 100次）。
        3.  在每次模拟结束后，收集结果和评估指标。
        4.  将所有运行的结果汇总，并保存到一个结构化的文件中（如`results.json`或`results.csv`）。

- [ ] **2. 实现第一个实验任务：“商业谈判 (Business Negotiation)”**
    - [ ] 在 `experiments/tasks/negotiation.py` 中，定义这个任务的环境。
    - [ ] 创建两个**“模拟用户Agent (Simulated User Agents)”**：一个扮演“买家”，一个扮演“卖家”。
    - [ ] 每个模拟用户都有自己的私密信息（如：买家的最高预算、卖家的最低心理价位）。
    - [ ] 他们的对话将通过我们的`WeaverRuntime`进行。Weaver扮演“商业调解员”的角色。
    - [ ] **关键**: 定义一个`is_successful()`的判断逻辑：当双方在对话中达成一个价格，且该价格在各自的心理价位范围内时，则谈判成功。

- [ ] **3. 实现用于对比的“基线模型 (Baselines)”**
    - [ ] 在 `experiments/baselines.py` 中，实现我们在论文规划中讨论过的几个对照组。
    - [ ] **`ZeroShotBaseline`**: 创建一个非常简单的、不使用Weaver框架的函数。它只是将所有对话历史拼接起来，加上一个简单的Prompt，然后直接调用LLM。
    - [ ] **`BroadcastBaseline`**: 创建一个模拟“信息广播站”的Agent，它会将所有私密信息都公开。
    - *这两个基线是证明Weaver价值的关键。*

- [ ] **4. 定义并实现核心评估指标 (Metrics)**
    - [ ] 在 `experiments/metrics.py` 中，编写计算指标的函数。
    - [ ] **`task_success_rate`**: 计算在N次运行中，谈判成功的比例。
    - [ ] **`information_leakage_rate`**: 设计一个简单的、基于关键词的检测方法。例如，如果在公开对话中出现了买家的“最高预算”这个数字，就记为一次信息泄露。
    - [ ] **`negotiation_efficiency`**: 计算达成协议所用的对话轮次。

- [ ] **5. 整合并进行第一次“试运行”**
    - [ ] 修改`experiments/runner.py`，使其能够选择运行`WeaverAgent`, `ZeroShotBaseline`, `BroadcastBaseline`中的任意一个。
    - [ ] 以一个较小的运行次数（如10次）进行一次完整的试运行。
    - [ ] **验收标准**:
        - [ ] 脚本能顺利跑完，并生成一个包含所有模型运行结果的`results.json`文件。
        - [ ] 初步结果符合直觉：Weaver的成功率应该显著高于基线，而信息泄露率应该显著低于`BroadcastBaseline`。