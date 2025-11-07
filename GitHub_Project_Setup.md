# GitHub项目设置和维护计划

## 🎯 项目仓库信息

**仓库名称**: chi2026
**仓库地址**: https://github.com/wujiajunhahah/chi2026.git
**项目类型**: CHI2026 Poster投稿项目
**维护策略**: 版本控制 + 协作开发 + 进度追踪

---

## 📁 仓库结构规划

```
chi2026/
├── 📄 README.md                    # 项目总览和快速开始
├── 📄 CONTRIBUTING.md              # 贡献指南
├── 📄 LICENSE                      # 开源许可证
├── 📄 .gitignore                   # Git忽略文件
├── 📂 docs/                        # 项目文档
│   ├── 📄 CHI2026_Project_Management.md
│   ├── 📄 Conversation_Log.md
│   ├── 📄 Submission_Plan.md
│   ├── 📄 Experiment_Design_Protocol.md
│   ├── 📄 CHI2026_Paper_Structure_Optimized.md
│   └── 📄 GitHub_Project_Setup.md
├── 📂 paper/                       # 论文相关文件
│   ├── 📄 CHI2026_Poster_WuJiajun.tex
│   ├── 📄 CHI2026_Poster_WuJiajun.docx
│   ├── 📄 references.bib
│   ├── 📂 figures/
│   │   ├── 📄 system_architecture.pdf
│   │   ├── 📄 experimental_setup.jpg
│   │   ├── 📄 confusion_matrix.pdf
│   │   └── 📄 user_interface.png
│   └── 📂 supplemental/
│       ├── 📄 demo_video.mp4
│       └── 📄 data_dictionary.pdf
├── 📂 experiment/                  # 实验相关代码和数据
│   ├── 📂 protocols/
│   │   ├── 📄 consent_form.pdf
│   │   ├── 📄 questionnaires.pdf
│   │   └── 📄 experimental_procedure.md
│   ├── 📂 data_collection/
│   │   ├── 📄 data_logger.py
│   │   ├── 📄 sensor_interface.py
│   │   └── 📄 real_time_monitor.py
│   ├── 📂 analysis/
│   │   ├── 📄 feature_extraction.py
│   │   ├── 📄 classification_models.py
│   │   ├── 📄 statistical_analysis.py
│   │   └── 📄 visualization.py
│   └── 📂 dataset/
│       ├── 📄 README.md
│       ├── 📂 raw_data/           # 原始数据（私有）
│       ├── 📂 processed_data/      # 处理后数据
│       └── 📂 sample_data/         # 示例数据
├── 📂 system/                      # EmotionHand系统代码
│   ├── 📄 emotion_hand_core.py
│   ├── 📄 signal_processing.py
│   ├── 📄 real_time_inference.py
│   ├── 📄 unity_interface.py
│   └── 📄 calibration_module.py
├── 📂 unity/                       # Unity项目文件
│   ├── 📂 Assets/
│   │   ├── 📂 Scripts/
│   │   ├── 📂 Scenes/
│   │   └── 📂 Materials/
│   └── 📄 ProjectSettings/
└── 📂 .github/                     # GitHub配置文件
    ├── 📂 workflows/
    │   └── 📄 ci.yml               # 持续集成配置
    ├── 📄 ISSUE_TEMPLATE/           # Issue模板
    └── 📄 PULL_REQUEST_TEMPLATE.md  # PR模板
```

---

## 🔧 Git工作流程

### 分支策略
```
main                 # 主分支，包含稳定版本
├── develop         # 开发分支，集成最新功能
├── feature/paper   # 论文撰写分支
├── feature/experiment # 实验开发分支
├── feature/system  # 系统开发分支
└── hotfix/*        # 紧急修复分支
```

### 提交规范
**提交信息格式**: `type(scope): description`

**类型说明**:
- `feat`: 新功能
- `fix`: 错误修复
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建或工具链相关

**示例**:
```bash
feat(paper): add abstract and introduction sections
fix(experiment): resolve data synchronization issue
docs(readme): update installation instructions
```

### 版本标签
```
v0.1.0    # 项目初始化
v0.2.0    # 实验协议完成
v0.3.0    # 数据收集完成
v0.4.0    # 分析完成
v1.0.0    # 论文初稿完成
v1.1.0    # 论文修订完成
v2.0.0    # 投稿版本
```

---

## 📝 Issue和项目管理

### Issue模板
```markdown
## 任务描述
简要描述任务内容和目标

## 具体要求
- [ ] 要求1
- [ ] 要求2
- [ ] 要求3

## 预期结果
描述任务完成后的预期结果

## 相关文件
列出相关的文件和链接

## 时间节点
- 开始时间: YYYY-MM-DD
- 截止时间: YYYY-MM-DD
```

### Project看板
**列设置**:
- `Backlog`: 待办任务
- `In Progress`: 进行中
- `Review`: 待审核
- `Testing`: 测试中
- `Done`: 已完成

**标签系统**:
- `priority/high`: 高优先级
- `priority/medium`: 中等优先级
- `priority/low`: 低优先级
- `type/paper`: 论文相关
- `type/experiment`: 实验相关
- `type/code`: 代码开发
- `type/documentation`: 文档编写

---

## 🚀 自动化工作流

### CI/CD配置 (`.github/workflows/ci.yml`)
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run tests
      run: |
        python -m pytest tests/

  latex-build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Build LaTeX
      uses: xu-cheng/latex-action@v2
      with:
        root_file: paper/CHI2026_Poster_WuJiajun.tex
        args: -output-directory=build
```

### 自动化发布
- **论文版本**: 每次merge到main自动生成PDF
- **数据集更新**: 实验数据更新时自动处理
- **文档网站**: GitHub Pages自动部署文档

---

## 🔒 安全和隐私

### 数据保护
- **敏感数据**: 不提交原始实验数据到公开仓库
- **个人隐私**: 参与者信息完全匿名化
- **访问控制**: 私有仓库管理敏感数据

### 代码质量
- **代码审查**: 所有PR需要至少一人审查
- **测试覆盖**: 关键功能需要单元测试
- **文档维护**: 代码变更时同步更新文档

---

## 📊 进度追踪和报告

### 每周进度模板
```markdown
## Week XX Progress Report (YYYY-MM-DD)

### 本周完成
- [x] 任务1
- [x] 任务2
- [x] 任务3

### 下周计划
- [ ] 计划1
- [ ] 计划2
- [ ] 计划3

### 遇到的问题
- 问题1及解决方案
- 问题2及待解决

### 需要的支持
- 需要的协助或资源
```

### 里程碑跟踪
- **M1**: 项目初始化完成 ✅
- **M2**: 实验协议确定 ⏳
- **M3**: 数据收集完成 ⏳
- **M4**: 数据分析完成 ⏳
- **M5**: 论文初稿完成 ⏳
- **M6**: 投稿准备完成 ⏳

---

## 🤝 协作指南

### 贡献流程
1. **Fork仓库**: 创建个人副本
2. **创建分支**: `feature/your-feature-name`
3. **开发测试**: 完成功能并测试
4. **提交PR**: 创建Pull Request
5. **代码审查**: 维护者审核代码
6. **合并代码**: 合并到目标分支

### 代码规范
- **Python**: 遵循PEP 8规范
- **LaTeX**: 使用标准学术写作格式
- **注释**: 关键算法需要详细注释
- **文档**: 更新相关文档说明

### 沟通渠道
- **GitHub Issues**: 任务管理和问题报告
- **GitHub Discussions**: 讨论和想法交流
- **Pull Request**: 代码变更和审核
- **Releases**: 版本发布和变更记录

---

## 🛠️ 工具和资源

### 必需工具
- **Git**: 版本控制
- **GitHub Desktop**: 图形化Git工具（可选）
- **VS Code**: 代码编辑器
- **Overleaf**: LaTeX协作编辑
- **Python**: 数据分析和实验代码
- **Unity**: 3D可视化开发

### 推荐扩展
- **GitLens**: Git历史查看
- **Prettier**: 代码格式化
- **Markdown Preview**: Markdown预览
- **LaTeX Workshop**: LaTeX编辑支持

---

## 📋 维护清单

### 每日检查
- [ ] 提交当日工作进展
- [ ] 更新任务进度
- [ ] 检查Issues和PR状态

### 每周检查
- [ ] 生成进度报告
- [ ] 更新里程碑状态
- [ ] 整理和归档完成的工作
- [ ] 检查代码质量和测试覆盖率

### 每月检查
- [ ] 版本发布准备
- [ ] 文档完整性检查
- [ ] 依赖包更新
- [ ] 备份重要数据

---

**文档创建**: 2025-11-07
**最后更新**: 2025-11-07
**维护者**: 吴嘉俊 (Wu Jiajun)
**项目状态**: 初始化阶段，准备开始实验开发