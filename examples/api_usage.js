const SkillAPI = require('../src/api/SkillAPI');

async function example() {
  const api = new SkillAPI({
    companyScale: '中型',
    headless: true
  });

  console.log('🚀 SectorAISkill API 使用示例');
  console.log('');

  // 示例1: 分析单个关键词
  console.log('=== 示例1: 分析单个关键词 ===');
  const result1 = await api.getRecommendations('AI设计总监', {
    companyScale: '中型'
  });
  
  if (result1.success) {
    console.log('✅ 分析成功');
    console.log(`关键词: ${result1.keyword}`);
    console.log(`公司规模: ${result1.companyScale}`);
    
    Object.entries(result1.recommendations).forEach(([level, data]) => {
      console.log(`\n【${level}】`);
      console.log(`  必备工具: ${data.essentialTools.map(t => t.name).join(', ')}`);
      console.log(`  推荐工具: ${data.recommendedTools.map(t => t.name).join(', ')}`);
      console.log(`  预估月费: $${data.costEstimate.totalMonthly}`);
    });
  }

  // 示例2: 对比多个关键词
  console.log('\n=== 示例2: 对比多个关键词 ===');
  const comparison = await api.compareKeywords(
    ['AI设计总监', 'AI视觉设计师'],
    { companyScale: '中型' }
  );
  
  if (comparison.success) {
    console.log('✅ 对比完成');
    console.log('工具差异:');
    Object.entries(comparison.comparison.tools).forEach(([tool, data]) => {
      console.log(`  ${tool}:`);
      Object.entries(data).forEach(([keyword, stats]) => {
        if (stats) {
          console.log(`    ${keyword}: ${stats.frequency}%`);
        }
      });
    });
  }

  // 示例3: 批量分析
  console.log('\n=== 示例3: 批量分析 ===');
  const batchResult = await api.batchAnalyze([
    'AI设计总监',
    'AI视觉设计师', 
    'AI创意总监'
  ], {
    companyScale: '中型',
    maxPages: 1
  });
  
  console.log(`批次ID: ${batchResult.batchId}`);
  console.log(`成功: ${batchResult.success}/${batchResult.total}`);

  // 示例4: 查看历史记录
  console.log('\n=== 示例4: 查看历史记录 ===');
  const history = api.getHistory();
  console.log(`共有 ${history.length} 条历史记录`);
  history.slice(0, 3).forEach(record => {
    console.log(`  - ${record.keyword} (${record.timestamp})`);
  });

  // 示例5: 导出数据
  console.log('\n=== 示例5: 导出数据 ===');
  if (history.length > 0) {
    const latest = history[0];
    const exportResult = await api.exportData(latest.keyword, 'csv');
    
    if (exportResult.success) {
      console.log('✅ 导出成功');
      exportResult.exports.forEach(exp => {
        console.log(`  文件: ${exp.fileName}`);
      });
    }
  }

  // 示例6: 查看统计
  console.log('\n=== 示例6: 查看统计 ===');
  const stats = api.getStats();
  console.log('存储统计:');
  Object.entries(stats).forEach(([key, count]) => {
    console.log(`  ${key}: ${count}`);
  });
}

// 运行示例
example().catch(err => {
  console.error('❌ 示例运行失败:', err);
});
