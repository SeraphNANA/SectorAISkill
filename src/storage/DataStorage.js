const fs = require('fs');
const path = require('path');

class DataStorage {
  constructor(options = {}) {
    this.baseDir = options.baseDir || './data';
    this.ensureDir(this.baseDir);
    
    this.subDirs = {
      jobs: path.join(this.baseDir, 'jobs'),
      reports: path.join(this.baseDir, 'reports'),
      exports: path.join(this.baseDir, 'exports'),
      cache: path.join(this.baseDir, 'cache')
    };
    
    Object.values(this.subDirs).forEach(dir => this.ensureDir(dir));
  }

  ensureDir(dir) {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
  }

  generateId() {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  saveJobs(keyword, jobs, options = {}) {
    const id = options.id || this.generateId();
    const timestamp = new Date().toISOString();
    const safeKeyword = this.sanitizeFilename(keyword);
    
    const data = {
      id,
      keyword,
      timestamp,
      total: jobs.length,
      jobs: jobs.map(job => ({
        title: job.title,
        company: job.company,
        salary: job.salary,
        location: job.location,
        experience: job.experience,
        education: job.education,
        tags: job.tags,
        detail: job.detail?.substring(0, 500),
        url: job.url,
        platform: job.platform,
        positionLevel: job.positionLevel,
        relevanceScore: job.relevanceScore,
        matchedKeywords: job.matchedKeywords,
        extractedTools: job.extractedTools
      }))
    };

    const filePath = path.join(this.subDirs.jobs, `${safeKeyword}_${id}.json`);
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
    
    return { id, filePath, count: jobs.length };
  }

  saveReport(keyword, reportData, options = {}) {
    const id = options.id || this.generateId();
    const timestamp = new Date().toISOString();
    const safeKeyword = this.sanitizeFilename(keyword);
    
    const data = {
      id,
      keyword,
      timestamp,
      companyScale: reportData.companyScale,
      summary: reportData.summary,
      recommendations: reportData.recommendations,
      toolStats: reportData.toolStats
    };

    const filePath = path.join(this.subDirs.reports, `${safeKeyword}_${id}.json`);
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
    
    return { id, filePath };
  }

  exportToCSV(keyword, data, options = {}) {
    const safeKeyword = this.sanitizeFilename(keyword);
    const timestamp = new Date().toISOString().split('T')[0];
    
    let csvContent = '';
    
    if (data.type === 'jobs') {
      csvContent = this.jobsToCSV(data.jobs);
    } else if (data.type === 'tools') {
      csvContent = this.toolsToCSV(data.toolStats);
    } else if (data.type === 'recommendations') {
      csvContent = this.recommendationsToCSV(data.recommendations);
    }

    const fileName = `${safeKeyword}_${data.type}_${timestamp}.csv`;
    const filePath = path.join(this.subDirs.exports, fileName);
    fs.writeFileSync(filePath, csvContent, 'utf8');
    
    return { filePath, fileName };
  }

  jobsToCSV(jobs) {
    const headers = [
      '岗位名称', '公司', '薪资', '地点', '经验要求', '学历',
      '岗位层级', '相关度评分', 'AI工具', '标签', 'URL'
    ];
    
    const rows = jobs.map(job => [
      this.escapeCSV(job.title),
      this.escapeCSV(job.company),
      this.escapeCSV(job.salary),
      this.escapeCSV(job.location),
      this.escapeCSV(job.experience),
      this.escapeCSV(job.education),
      this.escapeCSV(job.positionLevel),
      job.relevanceScore || 0,
      this.escapeCSV((job.extractedTools || []).join(';')),
      this.escapeCSV((job.tags || []).join(';')),
      this.escapeCSV(job.url)
    ]);

    return [headers.join(','), ...rows.map(row => row.join(','))].join('\n');
  }

  toolsToCSV(toolStats) {
    const headers = ['工具名称', '出现次数', '出现频率', '分类', '提及岗位数'];
    
    const rows = Object.entries(toolStats).map(([tool, stats]) => [
      this.escapeCSV(tool),
      stats.count,
      `${stats.frequency}%`,
      this.escapeCSV(stats.category),
      stats.jobs?.length || 0
    ]);

    return [headers.join(','), ...rows.map(row => row.join(','))].join('\n');
  }

  recommendationsToCSV(recommendations) {
    const headers = ['岗位层级', '工具名称', '推荐等级', '出现频率', '分类', '月费用', '难度', '学习周期'];
    const rows = [];

    Object.entries(recommendations).forEach(([level, data]) => {
      data.allTools.forEach(tool => {
        rows.push([
          this.escapeCSV(level),
          this.escapeCSV(tool.tool),
          this.escapeCSV(tool.recommendationLevel),
          `${tool.frequency}%`,
          this.escapeCSV(tool.category),
          tool.monthlyCost,
          this.escapeCSV(tool.difficulty),
          this.escapeCSV(tool.learningTime)
        ]);
      });
    });

    return [headers.join(','), ...rows.map(row => row.join(','))].join('\n');
  }

  escapeCSV(value) {
    if (value === null || value === undefined) return '';
    const str = String(value);
    if (str.includes(',') || str.includes('"') || str.includes('\n')) {
      return `"${str.replace(/"/g, '""')}"`;
    }
    return str;
  }

  sanitizeFilename(name) {
    return name.replace(/[^a-zA-Z0-9\u4e00-\u9fa5]/g, '_');
  }

  getHistory(options = {}) {
    const history = [];
    const files = fs.readdirSync(this.subDirs.reports);
    
    files.filter(f => f.endsWith('.json')).forEach(file => {
      try {
        const data = JSON.parse(fs.readFileSync(path.join(this.subDirs.reports, file), 'utf8'));
        history.push({
          id: data.id,
          keyword: data.keyword,
          timestamp: data.timestamp,
          companyScale: data.companyScale,
          file
        });
      } catch (e) {
        console.warn(`读取历史记录失败: ${file}`);
      }
    });

    return history.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
  }

  getReportById(id) {
    const files = fs.readdirSync(this.subDirs.reports);
    const file = files.find(f => f.includes(id));
    
    if (file) {
      const filePath = path.join(this.subDirs.reports, file);
      return JSON.parse(fs.readFileSync(filePath, 'utf8'));
    }
    
    return null;
  }

  clearCache() {
    const cacheFiles = fs.readdirSync(this.subDirs.cache);
    cacheFiles.forEach(file => {
      fs.unlinkSync(path.join(this.subDirs.cache, file));
    });
    console.log(`🗑️  已清理 ${cacheFiles.length} 个缓存文件`);
  }

  getStats() {
    const stats = {
      jobs: 0,
      reports: 0,
      exports: 0,
      cache: 0
    };

    Object.entries(this.subDirs).forEach(([key, dir]) => {
      if (fs.existsSync(dir)) {
        stats[key] = fs.readdirSync(dir).filter(f => !f.startsWith('.')).length;
      }
    });

    return stats;
  }
}

module.exports = DataStorage;
