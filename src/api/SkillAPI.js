const SectorAISkill = require('../../index');
const DataStorage = require('../storage/DataStorage');

class SkillAPI {
  constructor(options = {}) {
    this.storage = new DataStorage(options.storage);
    this.defaultOptions = {
      companyScale: '中型',
      headless: true,
      maxPages: 2,
      verbose: false,
      ...options
    };
  }

  async analyze(keyword, options = {}) {
    const opts = { ...this.defaultOptions, ...options };
    const app = new SectorAISkill(opts);
    
    try {
      const results = await app.run([keyword], opts);
      const result = results[0];
      
      if (result && result.jobs.length > 0) {
        // 保存到存储
        const jobSave = this.storage.saveJobs(keyword, result.jobs, { id: result.keyword });
        const reportSave = this.storage.saveReport(keyword, {
          companyScale: opts.companyScale,
          summary: {
            totalJobs: result.jobs.length,
            totalTools: Object.keys(result.toolStats).length
          },
          recommendations: result.recommendations,
          toolStats: result.toolStats
        });
        
        return {
          success: true,
          data: result,
          storage: {
            jobs: jobSave,
            report: reportSave
          }
        };
      }
      
      return {
        success: false,
        error: '未找到有效岗位数据',
        data: result
      };
    } catch (error) {
      return {
        success: false,
        error: error.message,
        stack: error.stack
      };
    }
  }

  async analyzeMultiple(keywords, options = {}) {
    const results = [];
    
    for (const keyword of keywords) {
      console.log(`\n🔄 分析进度: ${results.length + 1}/${keywords.length} - ${keyword}`);
      const result = await this.analyze(keyword, options);
      results.push({ keyword, ...result });
    }
    
    return {
      success: results.every(r => r.success),
      total: keywords.length,
      completed: results.filter(r => r.success).length,
      failed: results.filter(r => !r.success).length,
      results
    };
  }

  async getRecommendations(keyword, options = {}) {
    const result = await this.analyze(keyword, options);
    
    if (!result.success) {
      return result;
    }
    
    const recommendations = result.data.recommendations;
    const simplified = {};
    
    Object.entries(recommendations).forEach(([level, data]) => {
      simplified[level] = {
        level: data.level,
        budgetLevel: data.budgetLevel,
        skillLevel: data.skillLevel,
        teamSize: data.teamSize,
        essentialTools: data.essentialTools.map(t => ({
          name: t.tool,
          frequency: t.frequency,
          category: t.category,
          monthlyCost: t.monthlyCost,
          description: t.description,
          difficulty: t.difficulty,
          learningTime: t.learningTime
        })),
        recommendedTools: data.recommendedTools.map(t => ({
          name: t.tool,
          frequency: t.frequency,
          category: t.category,
          monthlyCost: t.monthlyCost,
          description: t.description
        })),
        skills: data.skills.map(s => ({
          name: s.name,
          level: s.level,
          duration: s.duration,
          description: s.description
        })),
        costEstimate: data.costEstimate,
        implementationPlan: data.implementationPlan
      };
    });
    
    return {
      success: true,
      keyword,
      companyScale: options.companyScale || this.defaultOptions.companyScale,
      recommendations: simplified
    };
  }

  async compareKeywords(keywords, options = {}) {
    if (keywords.length < 2) {
      return {
        success: false,
        error: '至少需要2个关键词进行对比'
      };
    }
    
    const analysisResults = await this.analyzeMultiple(keywords, options);
    
    if (!analysisResults.success) {
      return analysisResults;
    }
    
    const comparison = {
      keywords,
      tools: {},
      positions: {}
    };
    
    // 对比工具差异
    const allTools = new Set();
    analysisResults.results.forEach(result => {
      if (result.success && result.data.toolStats) {
        Object.keys(result.data.toolStats).forEach(tool => allTools.add(tool));
      }
    });
    
    allTools.forEach(tool => {
      comparison.tools[tool] = {};
      analysisResults.results.forEach(result => {
        if (result.success && result.data.toolStats) {
          const stats = result.data.toolStats[tool];
          comparison.tools[tool][result.keyword] = stats ? {
            frequency: stats.frequency,
            count: stats.count,
            category: stats.category
          } : null;
        }
      });
    });
    
    // 对比岗位层级差异
    const positionLevels = ['设计总监', '设计主管', '设计专员'];
    positionLevels.forEach(level => {
      comparison.positions[level] = {};
      analysisResults.results.forEach(result => {
        if (result.success && result.data.recommendations) {
          const rec = result.data.recommendations[level];
          comparison.positions[level][result.keyword] = rec ? {
            essentialCount: rec.essentialTools.length,
            recommendedCount: rec.recommendedTools.length,
            totalCost: rec.costEstimate.totalMonthly
          } : null;
        }
      });
    });
    
    return {
      success: true,
      comparison
    };
  }

  async exportData(keyword, format = 'csv', options = {}) {
    const reports = this.storage.getHistory();
    const report = reports.find(r => r.keyword === keyword);
    
    if (!report) {
      return {
        success: false,
        error: `未找到关键词 "${keyword}" 的历史数据`
      };
    }
    
    const data = this.storage.getReportById(report.id);
    
    if (!data) {
      return {
        success: false,
        error: '无法读取报告数据'
      };
    }
    
    const exports = [];
    
    if (format === 'csv' || format === 'all') {
      const toolExport = this.storage.exportToCSV(keyword, {
        type: 'tools',
        toolStats: data.toolStats
      });
      
      const recExport = this.storage.exportToCSV(keyword, {
        type: 'recommendations',
        recommendations: data.recommendations
      });
      
      exports.push(toolExport, recExport);
    }
    
    return {
      success: true,
      keyword,
      format,
      exports
    };
  }

  getHistory(options = {}) {
    return this.storage.getHistory(options);
  }

  getStats() {
    return this.storage.getStats();
  }

  clearCache() {
    this.storage.clearCache();
    return { success: true };
  }

  // 批量分析接口
  async batchAnalyze(keywords, options = {}) {
    const batchId = `batch-${Date.now()}`;
    const results = [];
    const errors = [];
    
    console.log(`🚀 启动批量分析 [${batchId}]`);
    console.log(`📊 共 ${keywords.length} 个关键词`);
    
    for (let i = 0; i < keywords.length; i++) {
      const keyword = keywords[i];
      console.log(`\n[${i + 1}/${keywords.length}] 分析: ${keyword}`);
      
      try {
        const result = await this.analyze(keyword, options);
        results.push({ keyword, ...result });
        
        // 间隔避免触发反爬
        if (i < keywords.length - 1) {
          await this.delay(5000);
        }
      } catch (error) {
        errors.push({ keyword, error: error.message });
      }
    }
    
    console.log(`\n✅ 批量分析完成 [${batchId}]`);
    console.log(`   成功: ${results.filter(r => r.success).length}`);
    console.log(`   失败: ${errors.length}`);
    
    return {
      batchId,
      total: keywords.length,
      success: results.filter(r => r.success).length,
      failed: errors.length,
      results,
      errors
    };
  }

  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

module.exports = SkillAPI;
