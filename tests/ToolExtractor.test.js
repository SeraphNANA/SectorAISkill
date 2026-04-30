const ToolExtractor = require('../src/extractor/ToolExtractor');

describe('ToolExtractor', () => {
  let extractor;

  beforeEach(() => {
    extractor = new ToolExtractor();
  });

  const mockJobs = [
    {
      title: 'AI设计师',
      detail: '熟练使用Midjourney、Stable Diffusion进行AI绘图，了解Runway视频生成',
      tags: ['AI设计', 'Midjourney']
    },
    {
      title: 'AI视频设计师',
      detail: '精通Runway、Pika、Sora等视频AI工具，使用HeyGen制作数字人',
      tags: ['视频AI', 'Runway']
    }
  ];

  test('应该正确提取AI工具', () => {
    const stats = extractor.extractFromJobs(mockJobs);
    
    expect(Object.keys(stats).length).toBeGreaterThan(0);
    expect(stats['Midjourney']).toBeDefined();
    expect(stats['Runway']).toBeDefined();
  });

  test('应该正确计算工具频次', () => {
    const stats = extractor.extractFromJobs(mockJobs);
    
    expect(stats['Midjourney'].count).toBe(1);
    expect(stats['Runway'].count).toBe(2);
  });

  test('应该正确分类工具', () => {
    const stats = extractor.extractFromJobs(mockJobs);
    
    expect(stats['Midjourney'].category).toBe('图像生成');
    expect(stats['Runway'].category).toBe('视频生成');
  });

  test('应该生成工具趋势分析', () => {
    const stats = extractor.extractFromJobs(mockJobs);
    const trends = extractor.analyzeToolTrends(stats, mockJobs);
    
    expect(trends.highFrequency.length).toBeGreaterThanOrEqual(0);
    expect(trends.mediumFrequency.length).toBeGreaterThanOrEqual(0);
  });

  test('应该按公司规模生成推荐', () => {
    const stats = extractor.extractFromJobs(mockJobs);
    const recs = extractor.getCompanyScaleRecommendations(stats, '中型');
    
    expect(recs.scale).toBe('中型');
    expect(recs.budget).toBe('中');
  });
});
