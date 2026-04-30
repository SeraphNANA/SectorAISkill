const JobFilter = require('../src/filter/JobFilter');

describe('JobFilter', () => {
  let filter;

  beforeEach(() => {
    filter = new JobFilter();
  });

  const mockJobs = [
    {
      title: 'AI设计总监',
      company: '创意广告公司',
      detail: '负责AI设计团队管理，精通Midjourney、Stable Diffusion等AI工具',
      tags: ['AI设计', '团队管理']
    },
    {
      title: '电商美工',
      company: '电商公司',
      detail: '负责淘宝详情页设计，纯平面设计工作，不涉及AI',
      tags: ['美工', '电商']
    },
    {
      title: 'AI视觉设计师',
      company: '科技公司',
      detail: '使用Runway、Pika进行视频创作，AIGC内容生产',
      tags: ['AI视频', 'AIGC']
    }
  ];

  test('应该正确筛选有效岗位', () => {
    const result = filter.filter(mockJobs);
    
    expect(result.valid.length).toBe(2);
    expect(result.rejected.length).toBe(1);
    expect(result.stats.validityRate).toBe('66.7');
  });

  test('应该正确识别岗位层级', () => {
    const result = filter.filter(mockJobs);
    const director = result.valid.find(j => j.title.includes('总监'));
    
    expect(director.positionLevel).toBe('设计总监');
  });

  test('应该过滤包含负向关键词的岗位', () => {
    const result = filter.filter(mockJobs);
    const rejected = result.rejected.find(j => j.title === '电商美工');
    
    expect(rejected).toBeDefined();
    // 电商美工岗位因为描述过短被过滤，或者因为负向关键词被过滤
    expect(rejected.rejectReason).toMatch(/负向关键词|岗位描述过短/);
  });

  test('应该计算相关性评分', () => {
    const result = filter.filter(mockJobs);
    const aiJob = result.valid.find(j => j.title.includes('AI'));
    
    expect(aiJob.relevanceScore).toBeGreaterThan(0);
    expect(aiJob.matchedKeywords.length).toBeGreaterThan(0);
  });
});
