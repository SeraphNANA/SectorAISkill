require('dotenv').config();
const ToolExtractor = require('./extractor/ToolExtractor');
const JobFilter = require('./filter/JobFilter');
const PositionRecommender = require('./recommender/PositionRecommender');
const { getMockJobs } = require('./utils/mockData');
const fs = require('fs');

async function runDemo() {
  console.log('🚀 启动 SectorAISkill - AI岗位工具配置分析系统（演示模式）');
  console.log('');

  const outputDir = process.env.OUTPUT_DIR || 'output';
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  // 1. 加载模拟数据
  const mockJobs = getMockJobs();
  console.log(`✅ 加载到 ${mockJobs.length} 个演示岗位数据`);
  console.log('');

  // 2. 智能筛选岗位
  console.log('🔍 执行岗位智能筛选...');
  const filter = new JobFilter();
  const filterResult = filter.filter(mockJobs, { verbose: true });
  const validJobs = filterResult.valid;

  console.log(`\n📊 筛选结果:`);
  console.log(`   原始岗位: ${filterResult.stats.total} 个`);
  console.log(`   有效岗位: ${filterResult.stats.valid} 个`);
  console.log(`   过滤岗位: ${filterResult.stats.rejected} 个`);
  console.log(`   有效率: ${filterResult.stats.validityRate}%`);

  // 3. 提取AI工具
  console.log(`\n🔍 从 ${validJobs.length} 个有效岗位中提取AI工具...`);
  const extractor = new ToolExtractor();
  const toolStats = extractor.extractFromJobs(validJobs);

  console.log(`\n📊 AI工具提取结果:`);
  Object.entries(toolStats).forEach(([tool, stats]) => {
    console.log(`   - ${tool}: 出现 ${stats.count} 次 (${stats.frequency}%) [${stats.category}]`);
  });

  // 4. 生成工具分析报告
  const toolReport = extractor.generateToolReport(toolStats, validJobs);
  
  console.log(`\n📈 工具趋势分析:`);
  console.log(`   高频工具 (≥30%): ${toolReport.trends.highFrequency.map(t => t.tool).join(', ') || '无'}`);
  console.log(`   中频工具 (15-30%): ${toolReport.trends.mediumFrequency.map(t => t.tool).join(', ') || '无'}`);
  console.log(`   低频工具 (5-15%): ${toolReport.trends.lowFrequency.map(t => t.tool).join(', ') || '无'}`);

  // 5. 生成岗位推荐
  console.log(`\n🎯 生成岗位AI工具推荐报告...`);
  const recommender = new PositionRecommender();
  const recommendations = recommender.generateRecommendations(toolStats, {
    companyScale: '中型'
  });

  // 6. 导出报告
  const reportPath = await recommender.exportRecommendations(recommendations, '演示数据');

  // 7. 打印详细推荐结果
  console.log(`\n${'='.repeat(60)}`);
  console.log('📋 推荐结果预览');
  console.log(`${'='.repeat(60)}`);

  Object.entries(recommendations).forEach(([level, data]) => {
    console.log(`\n【${level}】`);
    console.log(`  📍 职责: ${data.responsibilities.join('、')}`);
    console.log(`  💰 预算: ${data.budgetLevel} | 👥 团队: ${data.teamSize}`);
    console.log(`  📈 学习曲线: ${data.learningCurve} | 🎯 决策范围: ${data.decisionScope}`);
    
    console.log(`\n  🔴 必备工具 (${data.essentialTools.length}个):`);
    data.essentialTools.forEach(tool => {
      console.log(`     • ${tool.tool} (${tool.frequency}%) - ${tool.description}`);
    });

    console.log(`\n  🟡 推荐工具 (${data.recommendedTools.length}个):`);
    data.recommendedTools.forEach(tool => {
      console.log(`     • ${tool.tool} (${tool.frequency}%) - ${tool.description}`);
    });

    console.log(`\n  🟢 可选工具 (${data.optionalTools.length}个):`);
    data.optionalTools.slice(0, 3).forEach(tool => {
      console.log(`     • ${tool.tool} (${tool.frequency}%)`);
    });

    console.log(`\n  💡 核心技能:`);
    data.skills.forEach(skill => {
      console.log(`     • ${skill.name} (${skill.level}) - ${skill.duration}`);
    });

    console.log(`\n  💵 成本估算:`);
    console.log(`     • 月费: $${data.costEstimate.totalMonthly}`);
    console.log(`     • 年费: $${data.costEstimate.totalAnnual}`);

    console.log(`\n  📅 实施计划:`);
    Object.entries(data.implementationPlan).forEach(([phase, plan]) => {
      console.log(`     • ${plan.name}: ${plan.tools.join(', ')}`);
    });
  });

  console.log(`\n${'='.repeat(60)}`);
  console.log('🎉 演示完成！');
  console.log(`📁 报告已保存至: ${reportPath}`);
  console.log('');
  console.log('💡 提示: 使用真实数据运行请执行:');
  console.log('   node index.js --keywords "AI设计总监" --scale 中型');
}

runDemo().catch(err => {
  console.error('❌ 演示执行失败:', err);
  process.exit(1);
});
