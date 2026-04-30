class JobFilter {
  constructor(options = {}) {
    this.positiveKeywords = options.positiveKeywords || [
      'AI设计', '人工智能', 'AIGC', '生成式AI', 'AI绘图',
      'Midjourney', 'Stable Diffusion', 'DALL·E', 'Firefly',
      'Runway', 'Pika', 'Sora', 'HeyGen', '可灵',
      'Figma AI', 'Canva AI', 'Nano Banana', 'Lovart',
      'AI视觉', '智能设计', 'AI创意', 'AI生成',
      'prompt', '提示词', '文生图', '图生图',
      'AI视频', '数字人', 'AI动画', 'AI插画',
      'ComfyUI', 'LoRA', 'ControlNet', 'SDXL'
    ];

    this.negativeKeywords = options.negativeKeywords || [
      '电商美工', '淘宝详情页', '修图打杂', '纯平面',
      '印刷排版', '影楼修图', '美工助理', '抠图',
      '仅PS', '仅AI软件', '传统设计', '不涉及AI',
      '不接受AI', '禁止AI', '纯手绘', '纯手工'
    ];

    this.positionKeywords = {
      '设计总监': ['总监', '负责人', ' head', 'leader', '管理', '团队'],
      '设计主管': ['主管', '经理', '组长', 'leader', '督导'],
      '设计专员': ['专员', '助理', '初级', '实习', '执行']
    };

    this.minPositiveCount = options.minPositiveCount || 1;
    this.minJdLength = options.minJdLength || 50;
  }

  filter(jobs, options = {}) {
    const filtered = [];
    const rejected = [];
    
    console.log(`🔍 开始筛选 ${jobs.length} 个岗位...`);

    for (const job of jobs) {
      const result = this.evaluateJob(job);
      
      if (result.isValid) {
        job.relevanceScore = result.score;
        job.matchedKeywords = result.matchedKeywords;
        job.positionLevel = this.detectPositionLevel(job);
        filtered.push(job);
      } else {
        job.rejectReason = result.reason;
        rejected.push(job);
      }
    }

    console.log(`✅ 有效岗位: ${filtered.length} 个`);
    console.log(`❌ 过滤岗位: ${rejected.length} 个`);
    
    if (rejected.length > 0 && options.verbose) {
      console.log('\n📋 过滤原因统计:');
      const reasonCount = {};
      rejected.forEach(job => {
        const reason = job.rejectReason || '未知';
        reasonCount[reason] = (reasonCount[reason] || 0) + 1;
      });
      Object.entries(reasonCount).forEach(([reason, count]) => {
        console.log(`  - ${reason}: ${count} 个`);
      });
    }

    return {
      valid: filtered.sort((a, b) => b.relevanceScore - a.relevanceScore),
      rejected: rejected,
      stats: {
        total: jobs.length,
        valid: filtered.length,
        rejected: rejected.length,
        validityRate: jobs.length > 0 ? (filtered.length / jobs.length * 100).toFixed(1) : 0
      }
    };
  }

  evaluateJob(job) {
    const text = this.getJobText(job).toLowerCase();
    
    if (!text || text.length < this.minJdLength) {
      return {
        isValid: false,
        score: 0,
        matchedKeywords: [],
        reason: '岗位描述过短或为空'
      };
    }

    const positiveMatches = this.countMatches(text, this.positiveKeywords);
    const negativeMatches = this.countMatches(text, this.negativeKeywords);

    if (negativeMatches.count > 0) {
      return {
        isValid: false,
        score: 0,
        matchedKeywords: positiveMatches.matched,
        reason: `包含负向关键词: ${negativeMatches.matched.join(', ')}`
      };
    }

    if (positiveMatches.count < this.minPositiveCount) {
      return {
        isValid: false,
        score: 0,
        matchedKeywords: positiveMatches.matched,
        reason: '未匹配到AI相关关键词'
      };
    }

    const score = this.calculateScore(job, positiveMatches, negativeMatches);

    return {
      isValid: true,
      score,
      matchedKeywords: positiveMatches.matched,
      reason: null
    };
  }

  countMatches(text, keywords) {
    let count = 0;
    const matched = [];

    for (const keyword of keywords) {
      const keywordLower = keyword.toLowerCase();
      if (text.includes(keywordLower)) {
        count++;
        matched.push(keyword);
      }
    }

    return { count, matched };
  }

  calculateScore(job, positiveMatches, negativeMatches) {
    let score = 0;

    score += positiveMatches.count * 10;
    score -= negativeMatches.count * 20;

    const text = this.getJobText(job);
    if (text.length > 500) score += 5;
    if (text.length > 1000) score += 5;

    const title = (job.title || '').toLowerCase();
    if (title.includes('ai') || title.includes('人工智能') || title.includes('AIGC')) {
      score += 15;
    }

    const tags = (job.tags || []).join(' ').toLowerCase();
    if (tags.includes('ai') || tags.includes('人工智能')) {
      score += 10;
    }

    if (job.detail && job.detail.includes('岗位职责') && job.detail.includes('任职要求')) {
      score += 5;
    }

    return Math.max(0, score);
  }

  detectPositionLevel(job) {
    const title = (job.title || '').toLowerCase();
    
    for (const [level, keywords] of Object.entries(this.positionKeywords)) {
      for (const keyword of keywords) {
        if (title.includes(keyword.toLowerCase())) {
          return level;
        }
      }
    }

    if (title.includes('总监') || title.includes('负责人')) return '设计总监';
    if (title.includes('主管') || title.includes('经理')) return '设计主管';
    if (title.includes('专员') || title.includes('助理') || title.includes('初级')) return '设计专员';

    const detail = (job.detail || '').toLowerCase();
    if (detail.includes('团队管理') || detail.includes('战略规划')) return '设计总监';
    if (detail.includes('流程管控') || detail.includes('质量把控')) return '设计主管';
    if (detail.includes('执行') || detail.includes('协助')) return '设计专员';

    return '设计专员';
  }

  getJobText(job) {
    return [
      job.title || '',
      job.detail || '',
      (job.tags || []).join(' '),
      job.company || ''
    ].join(' ');
  }

  addPositiveKeywords(keywords) {
    this.positiveKeywords.push(...keywords);
  }

  addNegativeKeywords(keywords) {
    this.negativeKeywords.push(...keywords);
  }

  getFilterReport(filterResult) {
    const { stats, valid, rejected } = filterResult;
    
    return {
      summary: {
        totalJobs: stats.total,
        validJobs: stats.valid,
        rejectedJobs: stats.rejected,
        validityRate: `${stats.validityRate}%`
      },
      validJobs: valid.map(job => ({
        title: job.title,
        company: job.company,
        relevanceScore: job.relevanceScore,
        positionLevel: job.positionLevel,
        matchedKeywords: job.matchedKeywords
      })),
      rejectedJobs: rejected.map(job => ({
        title: job.title,
        company: job.company,
        rejectReason: job.rejectReason
      })),
      keywordStats: this.getKeywordStats(valid)
    };
  }

  getKeywordStats(jobs) {
    const keywordCount = {};
    
    jobs.forEach(job => {
      (job.matchedKeywords || []).forEach(keyword => {
        keywordCount[keyword] = (keywordCount[keyword] || 0) + 1;
      });
    });

    return Object.entries(keywordCount)
      .sort((a, b) => b[1] - a[1])
      .map(([keyword, count]) => ({ keyword, count }));
  }
}

module.exports = JobFilter;
