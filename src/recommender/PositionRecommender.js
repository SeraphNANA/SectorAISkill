const xlsx = require('xlsx');
const fs = require('fs');

class PositionRecommender {
  constructor(options = {}) {
    this.positionLevels = options.positionLevels || ['设计总监', '设计主管', '设计专员'];
    
    this.positionRules = {
      '设计总监': {
        responsibilities: [
          'AI工具战略选型与规划',
          '团队AI能力建设与管理',
          '高阶AI工具深度应用',
          'AI设计流程标准化制定',
          '跨部门AI协作推进',
          'AI趋势研究与创新应用'
        ],
        toolPriority: [
          'Midjourney', 'Stable Diffusion', 'DALL·E', 'Firefly',
          'Runway', 'Sora', 'HeyGen',
          'Figma AI', 'Nano Banana', 'Lovart',
          'ComfyUI', 'ControlNet', 'LoRA'
        ],
        budgetLevel: '高',
        skillLevel: '高级',
        teamSize: '10人以上',
        decisionScope: '战略决策',
        learningCurve: '陡峭',
        costExpectation: '企业级付费',
        keyMetrics: ['创意质量', '团队效率', '工具ROI', '创新落地']
      },
      '设计主管': {
        responsibilities: [
          'AI设计流程管控与优化',
          '批量生产与质量把控',
          '中端AI工具熟练应用',
          '团队成员技能培训',
          '项目进度与资源协调',
          'AI产出合规性审核'
        ],
        toolPriority: [
          'Stable Diffusion', 'Figma AI', 'Runway', 'Pika',
          'Canva AI', '剪映AI', '可灵',
          'ComfyUI', 'Photoshop AI', 'MasterGo'
        ],
        budgetLevel: '中',
        skillLevel: '进阶',
        teamSize: '5-10人',
        decisionScope: '战术执行',
        learningCurve: '中等',
        costExpectation: '混合方案',
        keyMetrics: ['产出效率', '质量一致性', '成本控制', '团队技能覆盖']
      },
      '设计专员': {
        responsibilities: [
          'AI工具执行落地',
          '基础视觉物料制作',
          'AI辅助设计执行',
          '素材整理与优化',
          '配合团队完成项目交付',
          'AI工具基础操作'
        ],
        toolPriority: [
          'Canva AI', '剪映AI', '可灵', 'Figma',
          'ChatGPT', '文心一言', '通义万相',
          '即梦', '美图秀秀AI', '稿定设计'
        ],
        budgetLevel: '低',
        skillLevel: '入门',
        teamSize: '1-5人',
        decisionScope: '执行操作',
        learningCurve: '平缓',
        costExpectation: '免费/基础版',
        keyMetrics: ['执行速度', '基础质量', '学习进度', '工具熟练度']
      }
    };

    this.toolCostInfo = {
      // 图像生成
      'Midjourney': { 
        type: '付费', 
        monthlyCost: 60, 
        description: '视觉冲击力首选，艺术感天花板',
        difficulty: '中等',
        bestFor: '概念设计、品牌视觉、创意探索',
        learningTime: '2-4周'
      },
      'Stable Diffusion': { 
        type: '免费/付费', 
        monthlyCost: 0, 
        description: '开源灵活，可本地部署，生态丰富',
        difficulty: '较高',
        bestFor: '定制化生成、隐私敏感项目、批量生产',
        learningTime: '4-8周'
      },
      'DALL·E': { 
        type: '付费', 
        monthlyCost: 20, 
        description: 'OpenAI出品，易用性强，理解力好',
        difficulty: '低',
        bestFor: '快速原型、概念验证、简单生成',
        learningTime: '1-2周'
      },
      'Firefly': { 
        type: '免费/付费', 
        monthlyCost: 0, 
        description: 'Adobe生态，版权安全，商用友好',
        difficulty: '低',
        bestFor: '商业设计、Adobe工作流、版权敏感',
        learningTime: '1-2周'
      },
      
      // 视频生成
      'Runway': { 
        type: '付费', 
        monthlyCost: 35, 
        description: '视频AI全能工具，Gen-2效果出色',
        difficulty: '中等',
        bestFor: '视频生成、动画制作、特效处理',
        learningTime: '2-4周'
      },
      'Pika': { 
        type: '免费/付费', 
        monthlyCost: 0, 
        description: '视频生成新秀，操作简洁',
        difficulty: '低',
        bestFor: '短视频、社交媒体内容、快速生成',
        learningTime: '1-2周'
      },
      'Sora': { 
        type: '测试中', 
        monthlyCost: 0, 
        description: 'OpenAI视频模型，生成质量极高',
        difficulty: '未知',
        bestFor: '长视频、电影级生成（待开放）',
        learningTime: '待定'
      },
      'HeyGen': { 
        type: '付费', 
        monthlyCost: 50, 
        description: '数字人视频生成，多语言支持',
        difficulty: '低',
        bestFor: '口播视频、培训内容、多语言本地化',
        learningTime: '1周'
      },
      '可灵': { 
        type: '免费/付费', 
        monthlyCost: 0, 
        description: '国产AI视频工具，中文友好',
        difficulty: '低',
        bestFor: '国内项目、中文内容、快速上手',
        learningTime: '1-2周'
      },
      '剪映AI': { 
        type: '免费', 
        monthlyCost: 0, 
        description: '国内视频剪辑工具，AI功能丰富',
        difficulty: '低',
        bestFor: '短视频、抖音/小红书内容、快速剪辑',
        learningTime: '3-5天'
      },
      
      // 设计工具
      'Figma AI': { 
        type: '免费/付费', 
        monthlyCost: 0, 
        description: '设计协作平台，AI辅助设计',
        difficulty: '低',
        bestFor: 'UI/UX设计、团队协作、原型制作',
        learningTime: '1-2周'
      },
      'Canva AI': { 
        type: '免费/付费', 
        monthlyCost: 0, 
        description: '易用设计工具，AI功能丰富',
        difficulty: '极低',
        bestFor: '营销物料、社交媒体、快速设计',
        learningTime: '2-3天'
      },
      'Nano Banana': { 
        type: '付费', 
        monthlyCost: 40, 
        description: 'AI设计协作工具，团队管理',
        difficulty: '中等',
        bestFor: '团队协作、项目管理、设计系统',
        learningTime: '2-3周'
      },
      'Lovart': { 
        type: '付费', 
        monthlyCost: 35, 
        description: 'AI视频结构分析，创意辅助',
        difficulty: '中等',
        bestFor: '视频分析、创意研究、结构拆解',
        learningTime: '2-3周'
      },
      
      // 工作流
      'ComfyUI': { 
        type: '免费', 
        monthlyCost: 0, 
        description: '可视化AI工作流搭建',
        difficulty: '高',
        bestFor: '复杂工作流、自动化生产、高级定制',
        learningTime: '4-8周'
      },
      'ControlNet': { 
        type: '免费', 
        monthlyCost: 0, 
        description: '精确控制AI生成结果',
        difficulty: '高',
        bestFor: '精确控制、姿势/结构保持、专业产出',
        learningTime: '3-6周'
      },
      
      // 通用AI
      'ChatGPT': { 
        type: '免费/付费', 
        monthlyCost: 20, 
        description: '通用AI助手，文案/代码/分析',
        difficulty: '低',
        bestFor: '文案生成、代码辅助、数据分析',
        learningTime: '3-5天'
      },
      '文心一言': { 
        type: '免费/付费', 
        monthlyCost: 0, 
        description: '百度AI助手，中文优化',
        difficulty: '低',
        bestFor: '中文内容、国内项目、快速上手',
        learningTime: '2-3天'
      },
      'Kimi': { 
        type: '免费', 
        monthlyCost: 0, 
        description: '月之暗面AI，长文本处理强',
        difficulty: '低',
        bestFor: '长文档分析、内容总结、知识管理',
        learningTime: '1-2天'
      }
    };

    this.skillRequirements = {
      '设计总监': [
        { 
          name: 'AI战略与工具选型', 
          level: '专家', 
          duration: '持续学习', 
          description: '掌握各类AI工具优劣，制定团队工具栈',
          keyAbilities: ['工具评估', '成本分析', '团队适配', '趋势判断']
        },
        { 
          name: '高阶提示词工程', 
          level: '专家', 
          duration: '2-3个月', 
          description: '精通复杂提示词设计，实现精准控制',
          keyAbilities: ['复杂构图', '风格控制', '参数调优', '迭代优化']
        },
        { 
          name: 'AI工作流设计', 
          level: '高级', 
          duration: '1-2个月', 
          description: '设计高效AI辅助设计流程',
          keyAbilities: ['流程优化', '工具串联', '自动化', '质量控制']
        },
        { 
          name: '团队AI能力建设', 
          level: '高级', 
          duration: '持续', 
          description: '培养团队AI技能，建立知识体系',
          keyAbilities: ['培训设计', '知识管理', '技能评估', '激励机制']
        }
      ],
      '设计主管': [
        { 
          name: '中端AI工具应用', 
          level: '熟练', 
          duration: '1-2个月', 
          description: '熟练运用主流AI工具完成设计任务',
          keyAbilities: ['工具组合', '效率优化', '质量把控', '问题解决']
        },
        { 
          name: '批量生产管理', 
          level: '熟练', 
          duration: '2-4周', 
          description: '管理AI辅助的批量设计生产',
          keyAbilities: ['任务分配', '进度管理', '质量审核', '资源协调']
        },
        { 
          name: '提示词优化', 
          level: '进阶', 
          duration: '3-4周', 
          description: '编写高效提示词，提升产出质量',
          keyAbilities: ['关键词优化', '风格定义', '结果调优', '模板建立']
        },
        { 
          name: 'AI产出审核', 
          level: '熟练', 
          duration: '2-3周', 
          description: '审核AI生成内容的质量与合规性',
          keyAbilities: ['质量评估', '合规检查', '修改指导', '标准制定']
        }
      ],
      '设计专员': [
        { 
          name: '基础AI工具操作', 
          level: '入门', 
          duration: '1-2周', 
          description: '掌握基础AI设计工具的使用',
          keyAbilities: ['界面操作', '基础功能', '简单生成', '素材处理']
        },
        { 
          name: '简单提示词编写', 
          level: '入门', 
          duration: '1周', 
          description: '编写简单有效的AI提示词',
          keyAbilities: ['基础描述', '关键词使用', '结果调整', '模板应用']
        },
        { 
          name: 'AI辅助设计执行', 
          level: '入门', 
          duration: '2-3周', 
          description: '使用AI工具辅助完成设计任务',
          keyAbilities: ['素材生成', '初稿制作', '简单编辑', '格式转换']
        },
        { 
          name: '设计基础技能', 
          level: '基础', 
          duration: '持续', 
          description: '保持传统设计技能，结合AI工具',
          keyAbilities: ['设计基础', '软件操作', '审美能力', '沟通协作']
        }
      ]
    };
  }

  generateRecommendations(toolStats, options = {}) {
    const companyScale = options.companyScale || '中型';
    const recommendations = {};
    
    console.log(`🎯 生成岗位AI工具推荐（公司规模: ${companyScale}）...`);
    
    this.positionLevels.forEach(level => {
      const rules = this.positionRules[level];
      const matchedTools = this.matchToolsToPosition(toolStats, rules, companyScale);
      
      recommendations[level] = {
        level,
        companyScale,
        responsibilities: rules.responsibilities,
        budgetLevel: rules.budgetLevel,
        skillLevel: rules.skillLevel,
        teamSize: rules.teamSize,
        decisionScope: rules.decisionScope,
        learningCurve: rules.learningCurve,
        keyMetrics: rules.keyMetrics,
        
        essentialTools: matchedTools.filter(t => t.recommendationLevel === '必备'),
        recommendedTools: matchedTools.filter(t => t.recommendationLevel === '推荐'),
        optionalTools: matchedTools.filter(t => t.recommendationLevel === '可选'),
        
        allTools: matchedTools,
        skills: this.getRequiredSkills(level),
        
        implementationPlan: this.generateImplementationPlan(level, matchedTools),
        costEstimate: this.estimateCost(matchedTools, companyScale)
      };
    });
    
    return recommendations;
  }

  matchToolsToPosition(toolStats, rules, companyScale) {
    const matchedTools = [];
    
    Object.entries(toolStats).forEach(([tool, stats]) => {
      const priority = rules.toolPriority.includes(tool) ? 2 : 1;
      const costInfo = this.toolCostInfo[tool] || { 
        type: '未知', 
        monthlyCost: 0,
        difficulty: '未知',
        bestFor: '通用',
        learningTime: '未知'
      };
      
      const recommendationLevel = this.determineRecommendationLevel(
        tool, stats, rules, companyScale
      );
      
      matchedTools.push({
        tool,
        frequency: parseFloat(stats.frequency),
        count: stats.count,
        category: stats.category,
        priority,
        recommendationLevel,
        costType: costInfo.type,
        monthlyCost: costInfo.monthlyCost,
        description: costInfo.description,
        difficulty: costInfo.difficulty,
        bestFor: costInfo.bestFor,
        learningTime: costInfo.learningTime,
        suitable: this.isToolSuitable(tool, rules.budgetLevel),
        mentions: stats.mentions || []
      });
    });
    
    return matchedTools.sort((a, b) => {
      const levelOrder = { '必备': 3, '推荐': 2, '可选': 1 };
      if (levelOrder[b.recommendationLevel] !== levelOrder[a.recommendationLevel]) {
        return levelOrder[b.recommendationLevel] - levelOrder[a.recommendationLevel];
      }
      if (b.priority !== a.priority) return b.priority - a.priority;
      return b.frequency - a.frequency;
    });
  }

  determineRecommendationLevel(tool, stats, rules, companyScale) {
    const freq = parseFloat(stats.frequency);
    const isPriority = rules.toolPriority.includes(tool);
    const costInfo = this.toolCostInfo[tool] || { type: '未知', monthlyCost: 0 };
    
    if (isPriority && freq >= 15) return '必备';
    if (freq >= 25) return '必备';
    if (isPriority || freq >= 10) return '推荐';
    if (freq >= 5) return '可选';
    
    if (companyScale === '大型' && isPriority) return '推荐';
    if (companyScale === '小型' && costInfo.type === '免费') return '推荐';
    
    return '可选';
  }

  isToolSuitable(tool, budgetLevel) {
    const costInfo = this.toolCostInfo[tool];
    if (!costInfo) return true;
    
    if (budgetLevel === '高') return true;
    if (budgetLevel === '中' && (costInfo.type === '免费' || costInfo.type === '免费/付费')) return true;
    if (budgetLevel === '低' && costInfo.type === '免费') return true;
    
    return false;
  }

  getRequiredSkills(position) {
    return this.skillRequirements[position] || [];
  }

  generateImplementationPlan(level, tools) {
    const essential = tools.filter(t => t.recommendationLevel === '必备');
    const recommended = tools.filter(t => t.recommendationLevel === '推荐');
    
    return {
      phase1: {
        name: '基础搭建（第1-2周）',
        tasks: [
          '安装配置必备工具',
          '建立基础工作流',
          '团队基础培训'
        ],
        tools: essential.slice(0, 3).map(t => t.tool)
      },
      phase2: {
        name: '能力深化（第3-4周）',
        tasks: [
          '优化提示词模板',
          '建立质量标准',
          '扩展工具应用'
        ],
        tools: essential.map(t => t.tool)
      },
      phase3: {
        name: '全面应用（第5-8周）',
        tasks: [
          '整合推荐工具',
          '建立最佳实践',
          '持续优化迭代'
        ],
        tools: [...essential, ...recommended.slice(0, 3)].map(t => t.tool)
      }
    };
  }

  estimateCost(tools, companyScale) {
    const essential = tools.filter(t => t.recommendationLevel === '必备');
    const recommended = tools.filter(t => t.recommendationLevel === '推荐');
    
    const essentialCost = essential.reduce((sum, t) => sum + (t.monthlyCost || 0), 0);
    const recommendedCost = recommended.reduce((sum, t) => sum + (t.monthlyCost || 0), 0);
    
    const scaleMultiplier = {
      '大型': 1.5,
      '中型': 1.0,
      '小型': 0.6
    };
    
    const multiplier = scaleMultiplier[companyScale] || 1.0;
    
    return {
      essentialMonthly: Math.round(essentialCost * multiplier),
      recommendedMonthly: Math.round(recommendedCost * multiplier),
      totalMonthly: Math.round((essentialCost + recommendedCost) * multiplier),
      essentialAnnual: Math.round(essentialCost * multiplier * 12),
      totalAnnual: Math.round((essentialCost + recommendedCost) * multiplier * 12),
      costBreakdown: [
        ...essential.map(t => ({ tool: t.tool, cost: Math.round(t.monthlyCost * multiplier), level: '必备' })),
        ...recommended.map(t => ({ tool: t.tool, cost: Math.round(t.monthlyCost * multiplier), level: '推荐' }))
      ].filter(item => item.cost > 0)
    };
  }

  async exportRecommendations(recommendations, keyword, options = {}) {
    const outputDir = process.env.OUTPUT_DIR || 'output';
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }

    const fileName = `${outputDir}/${keyword}_AI工具推荐报告.xlsx`;
    const workbook = xlsx.utils.book_new();

    // 概览sheet
    const overviewData = this.generateOverviewSheet(recommendations);
    const overviewSheet = xlsx.utils.aoa_to_sheet(overviewData);
    xlsx.utils.book_append_sheet(workbook, overviewSheet, '概览');

    // 各岗位详细sheet
    Object.entries(recommendations).forEach(([level, data]) => {
      const sheetData = this.generatePositionSheet(data);
      const worksheet = xlsx.utils.aoa_to_sheet(sheetData);
      xlsx.utils.book_append_sheet(workbook, worksheet, level);
    });

    // 工具汇总sheet
    const toolsSheet = this.generateToolsSummarySheet(recommendations);
    const toolsWorksheet = xlsx.utils.aoa_to_sheet(toolsSheet);
    xlsx.utils.book_append_sheet(workbook, toolsWorksheet, '工具汇总');

    // 成本分析sheet
    const costSheet = this.generateCostSheet(recommendations);
    const costWorksheet = xlsx.utils.aoa_to_sheet(costSheet);
    xlsx.utils.book_append_sheet(workbook, costWorksheet, '成本分析');

    // 实施计划sheet
    const planSheet = this.generateImplementationSheet(recommendations);
    const planWorksheet = xlsx.utils.aoa_to_sheet(planSheet);
    xlsx.utils.book_append_sheet(workbook, planWorksheet, '实施计划');

    xlsx.writeFile(workbook, fileName);
    console.log(`📁 报告已导出: ${fileName}`);
    
    return fileName;
  }

  generateOverviewSheet(recommendations) {
    const data = [
      ['AI工具推荐报告 - 概览'],
      ['生成时间', new Date().toLocaleString('zh-CN')],
      [],
      ['岗位层级', '预算级别', '技能要求', '团队规模', '决策范围', '学习曲线', '关键指标']
    ];

    Object.entries(recommendations).forEach(([level, data_item]) => {
      data.push([
        level,
        data_item.budgetLevel,
        data_item.skillLevel,
        data_item.teamSize,
        data_item.decisionScope,
        data_item.learningCurve,
        data_item.keyMetrics.join('、')
      ]);
    });

    data.push([]);
    data.push(['岗位层级', '必备工具数', '推荐工具数', '可选工具数', '预估月成本(美元)']);
    
    Object.entries(recommendations).forEach(([level, data_item]) => {
      data.push([
        level,
        data_item.essentialTools.length,
        data_item.recommendedTools.length,
        data_item.optionalTools.length,
        data_item.costEstimate.totalMonthly
      ]);
    });

    return data;
  }

  generatePositionSheet(data) {
    const sheetData = [
      [`${data.level} - AI工具配置方案`],
      ['公司规模', data.companyScale],
      ['预算级别', data.budgetLevel],
      ['技能要求', data.skillLevel],
      ['团队规模', data.teamSize],
      ['决策范围', data.decisionScope],
      [],
      ['职责描述'],
      ...data.responsibilities.map(r => [r]),
      [],
      ['推荐AI工具', '推荐等级', '出现频率', '工具类型', '月费用(美元)', '难度', '学习周期', '最佳场景', '描述']
    ];

    data.allTools.forEach(tool => {
      sheetData.push([
        tool.tool,
        tool.recommendationLevel,
        `${tool.frequency}%`,
        tool.category,
        tool.monthlyCost,
        tool.difficulty,
        tool.learningTime,
        tool.bestFor,
        tool.description
      ]);
    });

    sheetData.push([]);
    sheetData.push(['技能要求', '级别', '学习周期', '描述', '关键能力']);
    
    data.skills.forEach(skill => {
      sheetData.push([
        skill.name,
        skill.level,
        skill.duration,
        skill.description,
        skill.keyAbilities.join('、')
      ]);
    });

    return sheetData;
  }

  generateToolsSummarySheet(recommendations) {
    const allTools = new Map();
    
    Object.values(recommendations).forEach(data => {
      data.allTools.forEach(tool => {
        if (!allTools.has(tool.tool)) {
          allTools.set(tool.tool, {
            ...tool,
            positions: []
          });
        }
        allTools.get(tool.tool).positions.push({
          position: data.level,
          level: tool.recommendationLevel
        });
      });
    });

    const data = [
      ['AI工具汇总分析'],
      ['工具名称', '出现频率', '分类', '成本类型', '月费用(美元)', '难度', '适用岗位', '推荐等级分布']
    ];

    Array.from(allTools.values())
      .sort((a, b) => b.frequency - a.frequency)
      .forEach(tool => {
        const positionSummary = tool.positions
          .map(p => `${p.position}(${p.level})`)
          .join('、');
        
        const levelCount = {};
        tool.positions.forEach(p => {
          levelCount[p.level] = (levelCount[p.level] || 0) + 1;
        });
        const levelDist = Object.entries(levelCount)
          .map(([level, count]) => `${level}:${count}`)
          .join('、');

        data.push([
          tool.tool,
          `${tool.frequency}%`,
          tool.category,
          tool.costType,
          tool.monthlyCost,
          tool.difficulty,
          positionSummary,
          levelDist
        ]);
      });

    return data;
  }

  generateCostSheet(recommendations) {
    const data = [
      ['成本分析'],
      ['岗位层级', '必备工具月费', '推荐工具月费', '总月费', '年费估算', '成本等级']
    ];

    Object.entries(recommendations).forEach(([level, data_item]) => {
      const cost = data_item.costEstimate;
      data.push([
        level,
        cost.essentialMonthly,
        cost.recommendedMonthly,
        cost.totalMonthly,
        cost.totalAnnual,
        data_item.budgetLevel
      ]);
    });

    data.push([]);
    data.push(['详细成本明细']);
    data.push(['岗位层级', '工具名称', '推荐等级', '月费用(美元)', '年费(美元)']);

    Object.entries(recommendations).forEach(([level, data_item]) => {
      data_item.costEstimate.costBreakdown.forEach(item => {
        data.push([
          level,
          item.tool,
          item.level,
          item.cost,
          item.cost * 12
        ]);
      });
    });

    return data;
  }

  generateImplementationSheet(recommendations) {
    const data = [
      ['实施计划'],
      ['岗位层级', '阶段', '时间周期', '主要任务', '涉及工具']
    ];

    Object.entries(recommendations).forEach(([level, data_item]) => {
      const plan = data_item.implementationPlan;
      
      Object.entries(plan).forEach(([phaseKey, phase]) => {
        data.push([
          level,
          phase.name,
          phaseKey === 'phase1' ? '第1-2周' : phaseKey === 'phase2' ? '第3-4周' : '第5-8周',
          phase.tasks.join('、'),
          phase.tools.join('、')
        ]);
      });
    });

    return data;
  }
}

module.exports = PositionRecommender;
