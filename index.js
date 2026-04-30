require('dotenv').config();
const JobSpider = require('./src/spider/JobSpider');
const JobFilter = require('./src/filter/JobFilter');
const ToolExtractor = require('./src/extractor/ToolExtractor');
const PositionRecommender = require('./src/recommender/PositionRecommender');
const fs = require('fs');
const path = require('path');

class SectorAISkill {
  constructor(options = {}) {
    this.outputDir = options.outputDir || process.env.OUTPUT_DIR || 'output';
    this.companyScale = options.companyScale || '中型';
    this.headless = options.headless !== false;
    this.verbose = options.verbose || false;
    
    this.ensureOutputDir();
  }

  ensureOutputDir() {
    if (!fs.existsSync(this.outputDir)) {
      fs.mkdirSync(this.outputDir, { recursive: true });
    }
  }

  async run(keywords, options = {}) {
    console.log('🚀 启动 SectorAISkill - AI岗位工具配置分析系统');
    console.log(`📊 公司规模: ${this.companyScale}`);
    console.log(`🔍 搜索关键词: ${keywords.join(', ')}`);
    console.log('');

    const results = [];

    for (const keyword of keywords) {
      console.log(`\n${'='.repeat(60)}`);
      console.log(`🎯 正在分析: ${keyword}`);
      console.log(`${'='.repeat(60)}`);

      try {
        const result = await this.analyzeKeyword(keyword, options);
        results.push(result);
      } catch (error) {
        console.error(`❌ 分析 "${keyword}" 时出错:`, error.message);
      }
    }

    this.printSummary(results);
    return results;
  }

  async analyzeKeyword(keyword, options = {}) {
    const startTime = Date.now();
    
    // 1. 爬取岗位
    const spiderOptions = {
      headless: this.headless,
      maxPages: options.maxPages || parseInt(process.env.SPIDER_PAGE_COUNT || 2),
      city: options.city || ''
    };

    const spider = new JobSpider(spiderOptions);
    const rawJobs = await spider.crawl(keyword, spiderOptions);
    
    if (rawJobs.length === 0) {
      console.log(`⚠️ 未找到 "${keyword}" 相关岗位`);
      return { keyword, jobs: [], toolStats: {}, recommendations: {} };
    }

    // 2. 智能筛选岗位
    const filter = new JobFilter({
      minPositiveCount: 1,
      minJdLength: 50
    });
    
    const filterResult = filter.filter(rawJobs, { verbose: this.verbose });
    const validJobs = filterResult.valid;

    if (validJobs.length === 0) {
      console.log(`⚠️ 筛选后无有效岗位，请调整关键词或筛选条件`);
      return { keyword, jobs: [], toolStats: {}, recommendations: {} };
    }

    // 3. 提取AI工具
    const extractor = new ToolExtractor();
    const toolStats = extractor.extractFromJobs(validJobs);

    if (Object.keys(toolStats).length === 0) {
      console.log(`⚠️ 未提取到AI工具信息`);
      return { keyword, jobs: validJobs, toolStats: {}, recommendations: {} };
    }

    // 4. 生成推荐
    const recommender = new PositionRecommender();
    const recommendations = recommender.generateRecommendations(toolStats, {
      companyScale: this.companyScale
    });

    // 5. 导出报告
    const reportPath = await recommender.exportRecommendations(recommendations, keyword);

    // 6. 保存原始数据
    await this.saveRawData(keyword, validJobs, toolStats, recommendations);

    const duration = ((Date.now() - startTime) / 1000).toFixed(1);
    
    console.log(`\n✅ "${keyword}" 分析完成！`);
    console.log(`   耗时: ${duration}秒`);
    console.log(`   有效岗位: ${validJobs.length} 个`);
    console.log(`   AI工具: ${Object.keys(toolStats).length} 种`);
    console.log(`   报告: ${reportPath}`);

    return {
      keyword,
      jobs: validJobs,
      toolStats,
      recommendations,
      reportPath,
      duration
    };
  }

  async saveRawData(keyword, jobs, toolStats, recommendations) {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const safeKeyword = keyword.replace(/[^a-zA-Z0-9\u4e00-\u9fa5]/g, '_');
    
    const data = {
      keyword,
      timestamp,
      companyScale: this.companyScale,
      summary: {
        totalJobs: jobs.length,
        totalTools: Object.keys(toolStats).length,
        positionDistribution: this.getPositionDistribution(jobs)
      },
      jobs: jobs.map(job => ({
        title: job.title,
        company: job.company,
        salary: job.salary,
        location: job.location,
        experience: job.experience,
        education: job.education,
        positionLevel: job.positionLevel,
        relevanceScore: job.relevanceScore,
        matchedKeywords: job.matchedKeywords,
        extractedTools: job.extractedTools || [],
        tags: job.tags,
        url: job.url
      })),
      toolStats,
      recommendations: this.simplifyRecommendations(recommendations)
    };

    const fileName = `${this.outputDir}/${safeKeyword}_raw_data_${timestamp}.json`;
    fs.writeFileSync(fileName, JSON.stringify(data, null, 2), 'utf8');
  }

  getPositionDistribution(jobs) {
    const distribution = {};
    jobs.forEach(job => {
      const level = job.positionLevel || '未知';
      distribution[level] = (distribution[level] || 0) + 1;
    });
    return distribution;
  }

  simplifyRecommendations(recommendations) {
    const simplified = {};
    
    Object.entries(recommendations).forEach(([level, data]) => {
      simplified[level] = {
        level: data.level,
        companyScale: data.companyScale,
        budgetLevel: data.budgetLevel,
        skillLevel: data.skillLevel,
        essentialTools: data.essentialTools.map(t => ({
          tool: t.tool,
          frequency: t.frequency,
          category: t.category,
          monthlyCost: t.monthlyCost
        })),
        recommendedTools: data.recommendedTools.map(t => ({
          tool: t.tool,
          frequency: t.frequency,
          category: t.category,
          monthlyCost: t.monthlyCost
        })),
        costEstimate: data.costEstimate
      };
    });
    
    return simplified;
  }

  printSummary(results) {
    console.log(`\n${'='.repeat(60)}`);
    console.log('📊 分析完成汇总');
    console.log(`${'='.repeat(60)}`);

    results.forEach(result => {
      console.log(`\n🎯 ${result.keyword}`);
      console.log(`   岗位: ${result.jobs?.length || 0} 个`);
      console.log(`   工具: ${Object.keys(result.toolStats || {}).length} 种`);
      console.log(`   报告: ${result.reportPath || '未生成'}`);
      
      if (result.recommendations) {
        Object.entries(result.recommendations).forEach(([level, data]) => {
          console.log(`   ${level}: 必备${data.essentialTools.length} | 推荐${data.recommendedTools.length} | 可选${data.optionalTools.length}`);
        });
      }
    });

    console.log(`\n🎉 所有任务已完成！`);
    console.log(`📁 报告保存在: ${path.resolve(this.outputDir)}`);
  }
}

// CLI入口
async function main() {
  const args = process.argv.slice(2);
  
  // 解析参数
  const options = {
    keywords: [],
    companyScale: '中型',
    headless: false,
    maxPages: 2,
    verbose: false
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    
    switch (arg) {
      case '--keywords':
      case '-k':
        options.keywords = args[++i].split(',').map(k => k.trim());
        break;
      case '--scale':
      case '-s':
        options.companyScale = args[++i];
        break;
      case '--headless':
        options.headless = true;
        break;
      case '--pages':
      case '-p':
        options.maxPages = parseInt(args[++i]);
        break;
      case '--verbose':
      case '-v':
        options.verbose = true;
        break;
      case '--help':
      case '-h':
        printHelp();
        return;
      default:
        if (!arg.startsWith('-')) {
          options.keywords.push(arg);
        }
    }
  }

  // 如果没有指定关键词，使用环境变量或默认值
  if (options.keywords.length === 0) {
    const envKeywords = process.env.SPIDER_KEYWORDS;
    if (envKeywords) {
      options.keywords = envKeywords.split(',').map(k => k.trim());
    } else {
      options.keywords = ['AI设计总监'];
    }
  }

  const app = new SectorAISkill({
    companyScale: options.companyScale,
    headless: options.headless,
    verbose: options.verbose
  });

  await app.run(options.keywords, {
    maxPages: options.maxPages
  });
}

function printHelp() {
  console.log(`
SectorAISkill - AI岗位工具配置分析系统

用法: node index.js [选项] [关键词...]

选项:
  -k, --keywords <关键词>    搜索关键词，多个用逗号分隔 (默认: AI设计总监)
  -s, --scale <规模>         公司规模: 小型|中型|大型 (默认: 中型)
  -p, --pages <页数>         爬取页数 (默认: 2)
  --headless                 无头模式运行（不显示浏览器）
  -v, --verbose              显示详细日志
  -h, --help                 显示帮助

示例:
  node index.js AI设计总监
  node index.js -k "AI设计总监,AI视觉设计师" -s 中型 -p 3
  node index.js --headless -k AI设计师 -s 小型
`);
}

if (require.main === module) {
  main().catch(err => {
    console.error('❌ 系统执行失败:', err);
    process.exit(1);
  });
}

module.exports = SectorAISkill;
