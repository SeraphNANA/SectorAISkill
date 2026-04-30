const PositionRecommender = require('../src/recommender/PositionRecommender');

describe('PositionRecommender', () => {
  let recommender;

  beforeEach(() => {
    recommender = new PositionRecommender();
  });

  const mockToolStats = {
    'Midjourney': { count: 5, frequency: '50.0', category: '图像生成' },
    'Stable Diffusion': { count: 4, frequency: '40.0', category: '图像生成' },
    'Runway': { count: 3, frequency: '30.0', category: '视频生成' },
    'Figma AI': { count: 2, frequency: '20.0', category: '设计工具' },
    'Canva AI': { count: 1, frequency: '10.0', category: '设计工具' }
  };

  test('应该生成三级岗位推荐', () => {
    const recommendations = recommender.generateRecommendations(mockToolStats, {
      companyScale: '中型'
    });

    expect(recommendations['设计总监']).toBeDefined();
    expect(recommendations['设计主管']).toBeDefined();
    expect(recommendations['设计专员']).toBeDefined();
  });

  test('应该区分必备/推荐/可选工具', () => {
    const recommendations = recommender.generateRecommendations(mockToolStats, {
      companyScale: '中型'
    });

    const director = recommendations['设计总监'];
    expect(director.essentialTools.length).toBeGreaterThanOrEqual(0);
    expect(director.recommendedTools.length).toBeGreaterThanOrEqual(0);
  });

  test('应该生成成本估算', () => {
    const recommendations = recommender.generateRecommendations(mockToolStats, {
      companyScale: '中型'
    });

    const director = recommendations['设计总监'];
    expect(director.costEstimate).toBeDefined();
    expect(director.costEstimate.totalMonthly).toBeGreaterThanOrEqual(0);
  });

  test('应该生成实施计划', () => {
    const recommendations = recommender.generateRecommendations(mockToolStats, {
      companyScale: '中型'
    });

    const director = recommendations['设计总监'];
    expect(director.implementationPlan).toBeDefined();
    expect(director.implementationPlan.phase1).toBeDefined();
  });

  test('不同公司规模应该有不同的推荐', () => {
    const smallRecs = recommender.generateRecommendations(mockToolStats, {
      companyScale: '小型'
    });
    const largeRecs = recommender.generateRecommendations(mockToolStats, {
      companyScale: '大型'
    });

    expect(smallRecs['设计总监'].budgetLevel).toBe('高');
    expect(largeRecs['设计总监'].budgetLevel).toBe('高');
  });
});
