const puppeteer = require('puppeteer');
const cheerio = require('cheerio');

class JobSpider {
  constructor(options = {}) {
    this.browser = null;
    this.page = null;
    this.platform = options.platform || 'boss';
    this.headless = options.headless !== false;
    this.timeout = options.timeout || 30000;
    this.userDataDir = options.userDataDir || './user_data';
    
    this.platforms = {
      boss: {
        name: 'Boss直聘',
        baseUrl: 'https://www.zhipin.com',
        searchPath: '/web/geek/job',
        listSelector: '.job-list-box .job-card-wrapper',
        titleSelector: '.job-name',
        companySelector: '.company-name',
        salarySelector: '.salary',
        locationSelector: '.job-area',
        experienceSelector: '.tag-list li:nth-child(1)',
        educationSelector: '.tag-list li:nth-child(2)',
        tagSelector: '.job-card-footer li',
        detailSelector: '.job-sec-text',
        companySizeSelector: '.company-info .company-tag-list li:nth-child(1)',
        companyTypeSelector: '.company-info .company-tag-list li:nth-child(2)',
        loginCheckSelector: '.btn-login',
        nextPageSelector: '.options-pages a:nth-last-child(2)',
        detailUrlAttr: 'href',
        detailUrlPrefix: ''
      },
      zhaopin: {
        name: '智联招聘',
        baseUrl: 'https://sou.zhaopin.com',
        searchPath: '/',
        listSelector: '.joblist-box__item',
        titleSelector: '.jobinfo__name',
        companySelector: '.companyinfo__name',
        salarySelector: '.jobinfo__salary',
        locationSelector: '.jobinfo__place',
        experienceSelector: '.jobinfo__exp',
        educationSelector: '.jobinfo__edu',
        tagSelector: '.joblist-box__item-tag',
        detailSelector: '.describtion__detail-content',
        companySizeSelector: '.companyinfo__tag li:nth-child(1)',
        companyTypeSelector: '.companyinfo__tag li:nth-child(2)',
        loginCheckSelector: '.login-btn',
        nextPageSelector: '.pagination__next',
        detailUrlAttr: 'data-url',
        detailUrlPrefix: ''
      }
    };
  }

  async init() {
    if (!this.browser) {
      const launchOptions = {
        headless: this.headless,
        args: [
          '--disable-blink-features=AutomationControlled',
          '--disable-dev-shm-usage',
          '--disable-gpu',
          '--no-sandbox',
          '--disable-setuid-sandbox',
          '--disable-infobars',
          '--window-size=1920,1080',
          '--start-maximized',
          `--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36`
        ],
        defaultViewport: null
      };

      if (this.userDataDir) {
        launchOptions.userDataDir = this.userDataDir;
      }

      this.browser = await puppeteer.launch(launchOptions);
    }

    this.page = await this.browser.newPage();
    
    await this.page.setExtraHTTPHeaders({
      'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      'Accept-Encoding': 'gzip, deflate, br',
      'Connection': 'keep-alive',
      'Upgrade-Insecure-Requests': '1'
    });

    await this.page.setViewport({ width: 1920, height: 1080 });

    await this.page.evaluateOnNewDocument(() => {
      Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
      Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
      window.chrome = { runtime: {} };
    });
  }

  async close() {
    if (this.browser) {
      await this.browser.close();
      this.browser = null;
      this.page = null;
    }
  }

  async crawl(keyword, options = {}) {
    await this.init();
    const jobs = [];
    const platform = this.platforms[this.platform];
    const maxPages = options.maxPages || parseInt(process.env.SPIDER_PAGE_COUNT || 2);
    const city = options.city || '';
    
    try {
      console.log(`🔍 开始爬取 ${platform.name} - 关键词: "${keyword}"`);
      
      const isLoggedIn = await this.checkLogin();
      if (!isLoggedIn) {
        console.log('⚠️ 未检测到登录状态，请先登录...');
        await this.performLogin();
      }

      const searchUrl = this.buildSearchUrl(keyword, city);
      console.log(`🌐 访问搜索页面: ${searchUrl}`);
      
      await this.page.goto(searchUrl, { 
        waitUntil: 'networkidle2', 
        timeout: this.timeout 
      });

      await this.randomDelay(2000, 4000);

      for (let pageIndex = 1; pageIndex <= maxPages; pageIndex++) {
        console.log(`📄 正在处理第 ${pageIndex}/${maxPages} 页...`);
        
        try {
          await this.page.waitForSelector(platform.listSelector, { 
            timeout: 15000,
            visible: true 
          });
        } catch (e) {
          console.log('⚠️ 未找到岗位列表，可能已到达末页或触发反爬');
          break;
        }

        await this.randomDelay(1000, 3000);

        const content = await this.page.content();
        const pageJobs = this.parseJobList(content);
        
        if (pageJobs.length === 0) {
          console.log('⚠️ 本页未解析到岗位，停止爬取');
          break;
        }

        console.log(`✅ 第 ${pageIndex} 页解析到 ${pageJobs.length} 个岗位`);
        jobs.push(...pageJobs);

        if (pageIndex < maxPages) {
          const hasNext = await this.goToNextPage();
          if (!hasNext) {
            console.log('📄 已到达最后一页');
            break;
          }
        }
      }

      console.log(`🔍 开始获取 ${jobs.length} 个岗位的详细描述...`);
      for (let i = 0; i < jobs.length; i++) {
        const job = jobs[i];
        try {
          await this.scrapeJobDetail(job);
          if ((i + 1) % 5 === 0) {
            console.log(`  进度: ${i + 1}/${jobs.length}`);
          }
          await this.randomDelay(1500, 3500);
        } catch (error) {
          console.warn(`⚠️ 获取岗位详情失败 [${i + 1}/${jobs.length}]: ${job.title}`);
        }
      }

    } catch (error) {
      console.error('❌ 爬虫执行出错:', error.message);
    }
    
    await this.close();
    console.log(`🎉 爬取完成！共获取 ${jobs.length} 个岗位`);
    return jobs;
  }

  buildSearchUrl(keyword, city) {
    const platform = this.platforms[this.platform];
    const encodedKeyword = encodeURIComponent(keyword);
    
    if (this.platform === 'boss') {
      let url = `${platform.baseUrl}${platform.searchPath}?query=${encodedKeyword}`;
      if (city) url += `&city=${encodeURIComponent(city)}`;
      return url;
    } else if (this.platform === 'zhaopin') {
      let url = `${platform.baseUrl}${platform.searchPath}?kw=${encodedKeyword}`;
      if (city) url += `&jl=${encodeURIComponent(city)}`;
      return url;
    }
    
    return `${platform.baseUrl}${platform.searchPath}?query=${encodedKeyword}`;
  }

  async checkLogin() {
    try {
      await this.page.goto(this.platforms[this.platform].baseUrl, { 
        waitUntil: 'networkidle2', 
        timeout: 15000 
      });
      
      const loginBtn = await this.page.$(this.platforms[this.platform].loginCheckSelector);
      return !loginBtn;
    } catch (error) {
      return false;
    }
  }

  async performLogin() {
    console.log('🔐 请在浏览器中完成登录...');
    console.log('   登录完成后，程序将自动继续');
    
    try {
      await this.page.waitForNavigation({ 
        waitUntil: 'networkidle2', 
        timeout: 120000 
      });
      console.log('✅ 检测到登录成功');
    } catch (error) {
      console.log('⚠️ 登录等待超时，将继续执行...');
    }
  }

  parseJobList(html) {
    const $ = cheerio.load(html);
    const jobs = [];
    const platform = this.platforms[this.platform];
    
    $(platform.listSelector).each((index, element) => {
      const $el = $(element);
      
      try {
        const job = {
          title: this.extractText($el, platform.titleSelector),
          company: this.extractText($el, platform.companySelector),
          salary: this.extractText($el, platform.salarySelector),
          location: this.extractText($el, platform.locationSelector),
          experience: this.extractText($el, platform.experienceSelector),
          education: this.extractText($el, platform.educationSelector),
          tags: this.extractTags($el, platform.tagSelector),
          url: this.extractUrl($el, platform),
          detail: '',
          platform: this.platform,
          crawlTime: new Date().toISOString()
        };
        
        if (job.title && job.company) {
          jobs.push(job);
        }
      } catch (error) {
        console.warn('⚠️ 解析单个岗位时出错:', error.message);
      }
    });
    
    return jobs;
  }

  extractText($el, selector) {
    const text = $el.find(selector).first().text().trim();
    return text || '';
  }

  extractTags($el, selector) {
    const tags = [];
    $el.find(selector).each((i, el) => {
      const tag = $(el).text().trim();
      if (tag && tag.length < 20) {
        tags.push(tag);
      }
    });
    return tags;
  }

  extractUrl($el, platform) {
    const urlAttr = platform.detailUrlAttr;
    let url = $el.find('a').first().attr(urlAttr) || 
              $el.find('a').first().attr('href') || '';
    
    if (url && !url.startsWith('http')) {
      url = platform.baseUrl + (platform.detailUrlPrefix || '') + url;
    }
    
    return url;
  }

  async goToNextPage() {
    try {
      const platform = this.platforms[this.platform];
      const nextBtn = await this.page.$(platform.nextPageSelector);
      
      if (nextBtn) {
        const isDisabled = await this.page.evaluate(
          (selector) => {
            const btn = document.querySelector(selector);
            return btn ? btn.classList.contains('disabled') || btn.disabled : true;
          }, 
          platform.nextPageSelector
        );
        
        if (!isDisabled) {
          await nextBtn.click();
          await this.page.waitForNavigation({ 
            waitUntil: 'networkidle2', 
            timeout: this.timeout 
          });
          await this.randomDelay(2000, 4000);
          return true;
        }
      }
      return false;
    } catch (error) {
      return false;
    }
  }

  async scrapeJobDetail(job) {
    if (!job.url) return;
    
    try {
      await this.page.goto(job.url, { 
        waitUntil: 'networkidle2', 
        timeout: this.timeout 
      });
      
      const platform = this.platforms[this.platform];
      
      try {
        await this.page.waitForSelector(platform.detailSelector, { 
          timeout: 10000 
        });
      } catch (e) {
        console.warn(`⚠️ 等待详情超时: ${job.title}`);
      }

      const content = await this.page.content();
      const $ = cheerio.load(content);
      
      job.detail = $(platform.detailSelector).text().trim() || 
                   $('.job-sec-text').text().trim() ||
                   $('.job-description').text().trim() ||
                   '';
      
      job.companySize = $(platform.companySizeSelector).text().trim() || '';
      job.companyType = $(platform.companyTypeSelector).text().trim() || '';
      job.welfare = $('.job-tags span, .welfare-list li').map((i, el) => $(el).text().trim()).get() || [];
      
      if (!job.detail) {
        job.detail = $('.job-detail-section, .position-desc, .detail-content').text().trim() || '';
      }
      
    } catch (error) {
      console.warn(`⚠️ 获取详情失败: ${job.url}`, error.message);
    }
  }

  async randomDelay(min, max) {
    const delay = Math.floor(Math.random() * (max - min + 1)) + min;
    await new Promise(resolve => setTimeout(resolve, delay));
  }

  async crawlMultiplePlatforms(keyword, platforms = ['boss'], options = {}) {
    const allJobs = [];
    
    for (const platform of platforms) {
      this.platform = platform;
      try {
        const jobs = await this.crawl(keyword, options);
        allJobs.push(...jobs);
      } catch (error) {
        console.error(`❌ ${platform} 平台爬取失败:`, error.message);
      }
    }
    
    return this.deduplicateJobs(allJobs);
  }

  deduplicateJobs(jobs) {
    const seen = new Set();
    return jobs.filter(job => {
      const key = `${job.title}-${job.company}-${job.location}`;
      if (seen.has(key)) {
        return false;
      }
      seen.add(key);
      return true;
    });
  }
}

module.exports = JobSpider;

// 命令行入口
if (require.main === module) {
  const spider = new JobSpider();
  
  // 获取命令行参数
  const args = process.argv.slice(2);
  const keyword = args[0] || 'AI 产品经理';
  const city = args[1] || '北京';
  const maxPages = parseInt(args[2]) || 2;
  
  console.log(`🕷️ 开始爬取：${keyword} (${city})`);
  console.log(`📄 最多爬取 ${maxPages} 页\n`);
  
  spider.crawl(keyword, { city, maxPages })
    .then(jobs => {
      console.log(`✅ 爬取完成！共获取 ${jobs.length} 个岗位\n`);
      console.log('--- 数据开始 ---');
      console.log(JSON.stringify(jobs, null, 2));
      console.log('--- 数据结束 ---');
    })
    .catch(error => {
      console.error('❌ 爬取失败:', error.message);
      process.exit(1);
    });
}
