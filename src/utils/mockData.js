const mockJobs = [
  {
    title: 'AI设计总监',
    company: '北京创意广告有限公司',
    salary: '30-50K',
    location: '北京',
    experience: '5-10年',
    education: '本科',
    tags: ['AI设计', '团队管理', 'Midjourney', 'Stable Diffusion'],
    url: 'https://www.zhipin.com/job_detail/123.html',
    detail: '岗位职责：1. 负责公司AI设计团队的整体管理和战略规划；2. 带领团队完成各类AI设计项目，包括品牌视觉、营销物料等；3. 深入研究AI设计工具，如Midjourney、Stable Diffusion、Figma AI等，提升团队工作效率；4. 制定AI设计流程和标准，确保交付质量。任职要求：1. 本科及以上学历，设计相关专业；2. 5年以上设计管理经验，有广告公司经验优先；3. 熟练使用Midjourney、Stable Diffusion、DALL·E等AI绘图工具；4. 熟悉Figma、PS等传统设计工具；5. 具备团队管理能力和项目协调能力。',
    companySize: '50-150人',
    companyType: '民营',
    welfare: ['五险一金', '年终奖', '带薪年假']
  },
  {
    title: 'AI视觉设计师',
    company: '上海数字营销公司',
    salary: '18-30K',
    location: '上海',
    experience: '3-5年',
    education: '本科',
    tags: ['AI绘图', '品牌设计', 'Runway', 'Pika'],
    url: 'https://www.zhipin.com/job_detail/456.html',
    detail: '岗位职责：1. 使用AI工具进行视觉设计创作；2. 参与品牌视觉系统设计；3. 配合团队完成各类设计项目。任职要求：1. 熟练使用Midjourney、Stable Diffusion进行AI绘图；2. 掌握Runway、Pika等视频AI工具；3. 具备良好的审美能力和创意思维；4. 有广告设计经验优先。',
    companySize: '150-500人',
    companyType: '民营',
    welfare: ['五险一金', '团建活动']
  },
  {
    title: 'AI设计专员',
    company: '广州广告集团',
    salary: '12-20K',
    location: '广州',
    experience: '1-3年',
    education: '大专',
    tags: ['Canva', 'AI辅助设计', '剪映AI'],
    url: 'https://www.zhipin.com/job_detail/789.html',
    detail: '岗位职责：1. 使用AI工具协助完成日常设计工作；2. 负责基础视觉物料制作；3. 配合团队完成项目交付。任职要求：1. 熟练使用Canva、Figma等设计工具；2. 了解AI绘图工具的基本使用；3. 具备良好的沟通能力和团队协作精神。',
    companySize: '500-1000人',
    companyType: '民营',
    welfare: ['五险一金', '餐补']
  },
  {
    title: 'AI视频设计师',
    company: '深圳新媒体公司',
    salary: '20-35K',
    location: '深圳',
    experience: '3-5年',
    education: '本科',
    tags: ['视频AI', 'Runway', 'Sora', 'HeyGen'],
    url: 'https://www.zhipin.com/job_detail/101.html',
    detail: '岗位职责：1. 使用AI视频工具进行视频创作；2. 参与短视频、广告片的制作；3. 研究最新AI视频技术，提升创作效率。任职要求：1. 熟练使用Runway、Pika、Sora等视频AI工具；2. 熟悉HeyGen数字人技术；3. 有视频制作经验优先；4. 具备良好的审美和创意能力。',
    companySize: '100-200人',
    companyType: '民营',
    welfare: ['五险一金', '年终奖']
  },
  {
    title: 'AI创意总监',
    company: '杭州品牌策划公司',
    salary: '35-60K',
    location: '杭州',
    experience: '8-10年',
    education: '本科',
    tags: ['AI策略', 'Midjourney', 'Nano Banana', 'Lovart'],
    url: 'https://www.zhipin.com/job_detail/202.html',
    detail: '岗位职责：1. 负责公司AI创意策略的制定；2. 带领团队完成AI驱动的创意项目；3. 深入研究AI工具在创意领域的应用。任职要求：1. 8年以上广告创意经验；2. 精通Midjourney高级技巧；3. 熟悉Nano Banana、Lovart等AI协作工具；4. 具备出色的创意能力和团队管理能力。',
    companySize: '200-500人',
    companyType: '民营',
    welfare: ['五险一金', '股票期权']
  },
  {
    title: 'AI插画师',
    company: '成都动漫设计公司',
    salary: '15-25K',
    location: '成都',
    experience: '2-4年',
    education: '本科',
    tags: ['AI插画', 'Stable Diffusion', 'Firefly'],
    url: 'https://www.zhipin.com/job_detail/303.html',
    detail: '岗位职责：1. 使用AI工具进行插画创作；2. 参与游戏、动画项目的美术设计；3. 不断提升AI绘画技巧。任职要求：1. 熟练使用Stable Diffusion、Firefly等AI绘画工具；2. 具备扎实的绘画基础；3. 了解游戏或动画行业优先。',
    companySize: '50-100人',
    companyType: '民营',
    welfare: ['五险一金', '弹性工作']
  }
];

module.exports = {
  mockJobs,
  getMockJobs: () => mockJobs,
  getJobsByKeyword: (keyword) => {
    const lowerKeyword = keyword.toLowerCase();
    return mockJobs.filter(job => 
      job.title.toLowerCase().includes(lowerKeyword) ||
      job.tags.some(tag => tag.toLowerCase().includes(lowerKeyword))
    );
  }
};