# SectorAISkill - AI岗位工具配置分析系统

**项目正在建设中……**

基于招聘网站数据，智能分析岗位所需AI工具，并按公司规模和岗位层级生成差异化推荐报告。

## 功能特点

- **智能爬虫**: 自动爬取Boss直聘、智联招聘等平台岗位信息
- **岗位筛选**: 智能过滤"标题党"岗位，确保数据质量
- **AI工具提取**: 从岗位JD中识别50+种AI工具，自动分类统计
- **分级推荐**: 按岗位层级（总监/主管/专员）生成差异化工具推荐
- **成本估算**: 自动计算工具采购成本，支持多规模企业
- **实施计划**: 生成8周分阶段落地计划
- **数据持久化**: 支持JSON/CSV/Excel多种格式导出
- **API接口**: 提供程序化调用接口，支持批量分析

## 技术栈

- Node.js 16+
- Puppeteer (浏览器自动化)
- Cheerio (HTML解析)
- xlsx (Excel导出)
- Jest (测试框架)

## 安装

```bash
npm install
```

## 配置

编辑 `.env` 文件：

```env
# 爬虫配置
SPIDER_KEYWORDS=AI设计总监,AI视觉设计师
SPIDER_PAGE_COUNT=3
SPIDER_TIMEOUT=30000

# 公司规模: 小型 | 中型 | 大型
COMPANY_SCALE=中型

# 输出配置
OUTPUT_DIR=output
OUTPUT_FORMAT=excel

# 浏览器配置
HEADLESS=false
```

## 使用方式

### 1. 演示模式（无需登录）

```bash
npm run demo
```

### 2. 命令行模式

```bash
# 基础用法
node index.js AI设计总监

# 指定公司规模
node index.js --keywords "AI设计总监" --scale 中型

# 多关键词分析
node index.js -k "AI设计总监,AI视觉设计师,AI创意总监" -s 中型 -p 3

# 无头模式（不显示浏览器）
node index.js --headless -k AI设计师 -s 小型

# 显示详细日志
node index.js --verbose -k AI设计总监
```

### 3. API调用

```javascript
const SkillAPI = require('./src/api/SkillAPI');

const api = new SkillAPI({ companyScale: '中型' });

// 获取推荐
const result = await api.getRecommendations('AI设计总监');

// 批量分析
const batch = await api.batchAnalyze(['AI设计总监', 'AI视觉设计师']);

// 对比关键词
const comparison = await api.compareKeywords(['AI设计总监', 'AI创意总监']);
```

## 项目结构

```
SectorAISkill/
├── index.js                 # 主入口（完整爬虫模式）
├── src/
│   ├── cli.js              # 演示模式入口
│   ├── spider/
│   │   └── JobSpider.js    # 招聘网站爬虫
│   ├── filter/
│   │   └── JobFilter.js    # 岗位智能筛选
│   ├── extractor/
│   │   └── ToolExtractor.js # AI工具提取器
│   ├── recommender/
│   │   └── PositionRecommender.js # 岗位推荐器
│   ├── storage/
│   │   └── DataStorage.js  # 数据持久化
│   ├── api/
│   │   └── SkillAPI.js     # API接口
│   └── utils/
│       └── mockData.js     # 演示数据
├── tests/                   # 测试用例
├── examples/                # 使用示例
├── .env                     # 环境配置
└── output/                  # 输出目录
```

## 工作流程

1. **爬取岗位**: 自动访问招聘网站，抓取目标岗位JD
2. **智能筛选**: 过滤"标题党"岗位，保留真实AI相关职位
3. **提取工具**: 从JD中识别AI工具关键词，统计频次
4. **生成推荐**: 按岗位层级和公司规模生成差异化推荐
5. **导出报告**: 输出Excel报告（含概览/岗位详情/工具汇总/成本分析/实施计划）

## 报告内容

生成的Excel报告包含5个Sheet：

- **概览**: 岗位对比、成本概览
- **设计总监**: 战略级工具推荐
- **设计主管**: 战术级工具推荐  
- **设计专员**: 执行级工具推荐
- **工具汇总**: 全量工具分析
- **成本分析**: 详细费用明细
- **实施计划**: 8周分阶段落地指南

## 测试

```bash
npm test
```

## 注意事项

- 使用爬虫功能需要个人求职者账号（非企业账号）
- 建议合理控制爬取频率，避免触发反爬机制
- 演示模式使用模拟数据，无需登录即可体验

## 许可证

MIT
