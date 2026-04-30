class ToolExtractor {
  constructor(options = {}) {
    this.toolKeywords = options.toolKeywords || [
      // 图像生成
      'Midjourney', 'Stable Diffusion', 'DALL·E', 'DALL-E', 'Dalle', 'Firefly',
      'Adobe Firefly', '文心一格', '通义万相', '可图', '即梦', 'Dreamina',
      'LiblibAI', '吐司', 'Civitai', 'Leonardo.ai', 'Playground',
      
      // 视频生成
      'Runway', 'Pika', 'Pika Labs', 'Sora', 'HeyGen', '可灵', 'Kling',
      '剪映AI', 'CapCut AI', '度加', '腾讯智影', '万兴喵影',
      'Stable Video', 'Gen-2', 'Luma Dream Machine', 'Vidu',
      
      // 设计工具
      'Figma AI', 'Figma', 'Canva AI', 'Canva', 'Nano Banana',
      'Lovart', 'MasterGo', '即时设计', 'Pixso', '墨刀',
      'Adobe Illustrator', 'Photoshop AI', 'PS AI', '创成式填充',
      
      // 3D/建模
      'Blender', 'Spline', 'Meshy', 'Tripo', 'Rodin', 'CSM',
      
      // 代码/开发
      'GitHub Copilot', 'Cursor', 'Bolt', 'V0', 'Replit',
      'Claude', 'ChatGPT', 'GPT-4', 'GPT-4o', 'Gemini',
      
      // 音频/音乐
      'Suno', 'Udio', 'Mureka', '天工音乐', 'ACE Studio',
      
      // 灵感/素材
      'Pinterest', 'Eagle', '零泉', 'Freepik', 'Unsplash',
      
      // 工作流/自动化
      'ComfyUI', 'Comfy UI', 'LoRA', 'ControlNet', 'IP-Adapter',
      'LangChain', 'AutoGPT', 'Dify', 'Coze', '扣子',
      
      // 通用AI
      '文心一言', '通义千问', 'Kimi', '智谱清言', '讯飞星火',
      '豆包', '元宝', '海螺AI', '百川智能'
    ];

    this.toolCategories = {
      '图像生成': ['Midjourney', 'Stable Diffusion', 'DALL·E', 'DALL-E', 'Dalle', 'Firefly', 'Adobe Firefly', '文心一格', '通义万相', '可图', '即梦', 'Dreamina', 'LiblibAI', '吐司', 'Civitai', 'Leonardo.ai', 'Playground'],
      '视频生成': ['Runway', 'Pika', 'Pika Labs', 'Sora', 'HeyGen', '可灵', 'Kling', '剪映AI', 'CapCut AI', '度加', '腾讯智影', '万兴喵影', 'Stable Video', 'Gen-2', 'Luma Dream Machine', 'Vidu'],
      '设计工具': ['Figma AI', 'Figma', 'Canva AI', 'Canva', 'Nano Banana', 'Lovart', 'MasterGo', '即时设计', 'Pixso', '墨刀', 'Adobe Illustrator', 'Photoshop AI', 'PS AI', '创成式填充'],
      '3D建模': ['Blender', 'Spline', 'Meshy', 'Tripo', 'Rodin', 'CSM'],
      '代码开发': ['GitHub Copilot', 'Cursor', 'Bolt', 'V0', 'Replit', 'Claude', 'ChatGPT', 'GPT-4', 'GPT-4o', 'Gemini'],
      '音频音乐': ['Suno', 'Udio', 'Mureka', '天工音乐', 'ACE Studio'],
      '灵感素材': ['Pinterest', 'Eagle', '零泉', 'Freepik', 'Unsplash'],
      '工作流': ['ComfyUI', 'Comfy UI', 'LoRA', 'ControlNet', 'IP-Adapter', 'LangChain', 'AutoGPT', 'Dify', 'Coze', '扣子'],
      '通用AI': ['文心一言', '通义千问', 'Kimi', '智谱清言', '讯飞星火', '豆包', '元宝', '海螺AI', '百川智能']
    };

    this.toolAliases = {
      'DALL-E': 'DALL·E',
      'Dalle': 'DALL·E',
      'Adobe Firefly': 'Firefly',
      'CapCut AI': '剪映AI',
      'Kling': '可灵',
      'Comfy UI': 'ComfyUI',
      'PS AI': 'Photoshop AI',
      'GPT-4': 'ChatGPT',
      'GPT-4o': 'ChatGPT'
    };

    this.companyScaleRules = {
      '大型': { budget: '高', teamSize: '50+', priority: ['企业版', '团队协作', 'API接入'] },
      '中型': { budget: '中', teamSize: '10-50', priority: ['性价比', '混合方案', '标准版'] },
      '小型': { budget: '低', teamSize: '10以下', priority: ['免费版', '基础功能', '易上手'] }
    };
  }

  extractFromJobs(jobs, options = {}) {
    const toolStats = {};
    
    this.toolKeywords.forEach(tool => {
      const normalizedTool = this.normalizeToolName(tool);
      if (!toolStats[normalizedTool]) {
        toolStats[normalizedTool] = {
          count: 0,
          jobs: [],
          category: this.getCategory(tool),
          frequency: 0,
          mentions: []
        };
      }
    });

    const validJobs = this.filterValidJobs(jobs);
    const totalJobs = validJobs.length;
    
    console.log(`🔍 从 ${totalJobs} 个有效岗位中提取AI工具...`);

    validJobs.forEach(job => {
      const text = this.getJobText(job).toLowerCase();
      const foundTools = new Set();
      
      this.toolKeywords.forEach(tool => {
        const normalizedTool = this.normalizeToolName(tool);
        const toolPattern = this.createToolPattern(tool);
        
        if (toolPattern.test(text)) {
          foundTools.add(normalizedTool);
          toolStats[normalizedTool].count++;
          
          if (!toolStats[normalizedTool].jobs.find(j => j.url === job.url)) {
            toolStats[normalizedTool].jobs.push({
              title: job.title,
              company: job.company,
              url: job.url,
              positionLevel: job.positionLevel || '未知'
            });
          }

          const mention = this.extractMentionContext(text, tool);
          if (mention) {
            toolStats[normalizedTool].mentions.push({
              job: job.title,
              context: mention
            });
          }
        }
      });

      job.extractedTools = Array.from(foundTools);
    });

    Object.keys(toolStats).forEach(tool => {
      toolStats[tool].frequency = totalJobs > 0 ? (toolStats[tool].count / totalJobs * 100).toFixed(1) : 0;
    });

    const result = this.sortByFrequency(toolStats);
    
    console.log(`✅ 提取到 ${Object.keys(result).length} 种AI工具`);
    
    return result;
  }

  createToolPattern(tool) {
    const escaped = tool.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const variations = [
      escaped,
      escaped.replace(/\s+/g, ''),
      escaped.replace(/\s+/g, '-'),
      escaped.replace(/\s+/g, '_')
    ];
    
    return new RegExp(`(${variations.join('|')})`, 'i');
  }

  extractMentionContext(text, tool) {
    const sentences = text.split(/[。！？.!?]/);
    const toolLower = tool.toLowerCase();
    
    for (const sentence of sentences) {
      if (sentence.toLowerCase().includes(toolLower)) {
        const clean = sentence.trim();
        if (clean.length > 10 && clean.length < 200) {
          return clean;
        }
      }
    }
    
    return null;
  }

  normalizeToolName(tool) {
    return this.toolAliases[tool] || tool;
  }

  getJobText(job) {
    return [
      job.title || '',
      job.detail || '',
      (job.tags || []).join(' '),
      (job.welfare || []).join(' ')
    ].join(' ');
  }

  filterValidJobs(jobs) {
    return jobs.filter(job => {
      const text = this.getJobText(job);
      return text.length > 30;
    });
  }

  getCategory(tool) {
    const normalized = this.normalizeToolName(tool);
    
    for (const [category, tools] of Object.entries(this.toolCategories)) {
      if (tools.includes(tool) || tools.includes(normalized)) {
        return category;
      }
    }
    
    return '其他';
  }

  sortByFrequency(toolStats) {
    return Object.entries(toolStats)
      .filter(([, stats]) => stats.count > 0)
      .sort((a, b) => b[1].count - a[1].count)
      .reduce((acc, [tool, stats]) => {
        acc[tool] = stats;
        return acc;
      }, {});
  }

  getTopTools(toolStats, limit = 15) {
    return Object.entries(toolStats)
      .slice(0, limit)
      .map(([tool, stats]) => ({
        tool,
        count: stats.count,
        frequency: stats.frequency,
        category: stats.category,
        mentions: stats.mentions || []
      }));
  }

  getToolsByCategory(toolStats) {
    const categorized = {};
    
    Object.entries(toolStats).forEach(([tool, stats]) => {
      const category = stats.category;
      if (!categorized[category]) {
        categorized[category] = [];
      }
      categorized[category].push({ tool, ...stats });
    });

    Object.keys(categorized).forEach(category => {
      categorized[category].sort((a, b) => b.count - a.count);
    });

    return categorized;
  }

  analyzeToolTrends(toolStats, jobs) {
    const trends = {
      highFrequency: [],
      mediumFrequency: [],
      lowFrequency: [],
      emerging: []
    };

    Object.entries(toolStats).forEach(([tool, stats]) => {
      const freq = parseFloat(stats.frequency);
      
      if (freq >= 30) {
        trends.highFrequency.push({ tool, frequency: freq, category: stats.category });
      } else if (freq >= 15) {
        trends.mediumFrequency.push({ tool, frequency: freq, category: stats.category });
      } else if (freq >= 5) {
        trends.lowFrequency.push({ tool, frequency: freq, category: stats.category });
      } else {
        trends.emerging.push({ tool, frequency: freq, category: stats.category });
      }
    });

    return trends;
  }

  getCompanyScaleRecommendations(toolStats, scale = '中型') {
    const rules = this.companyScaleRules[scale] || this.companyScaleRules['中型'];
    const recommendations = {
      essential: [],
      recommended: [],
      optional: []
    };

    Object.entries(toolStats).forEach(([tool, stats]) => {
      const freq = parseFloat(stats.frequency);
      const category = stats.category;
      
      if (freq >= 25) {
        recommendations.essential.push({ tool, frequency: freq, category });
      } else if (freq >= 10) {
        recommendations.recommended.push({ tool, frequency: freq, category });
      } else if (freq >= 5) {
        recommendations.optional.push({ tool, frequency: freq, category });
      }
    });

    return {
      scale,
      budget: rules.budget,
      priority: rules.priority,
      ...recommendations
    };
  }

  generateToolReport(toolStats, jobs) {
    const totalJobs = jobs.length;
    const totalTools = Object.keys(toolStats).length;
    const categorizedTools = this.getToolsByCategory(toolStats);
    const trends = this.analyzeToolTrends(toolStats, jobs);

    return {
      summary: {
        totalJobs,
        totalTools,
        avgToolsPerJob: totalJobs > 0 ? (Object.values(toolStats).reduce((sum, s) => sum + s.count, 0) / totalJobs).toFixed(1) : 0
      },
      topTools: this.getTopTools(toolStats, 20),
      byCategory: categorizedTools,
      trends,
      companyScaleAnalysis: {
        large: this.getCompanyScaleRecommendations(toolStats, '大型'),
        medium: this.getCompanyScaleRecommendations(toolStats, '中型'),
        small: this.getCompanyScaleRecommendations(toolStats, '小型')
      }
    };
  }
}

module.exports = ToolExtractor;
