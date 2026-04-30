import streamlit as st
import pandas as pd
import json
from workflow_data import AI_WORKFLOWS, SKILL_MATRIX, PROMPT_TEMPLATES

st.set_page_config(
    page_title="AI岗位工具配置分析系统",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: bold;
        color: #1a1a2e;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        font-size: 1rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .step-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .result-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
    }
    .tool-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        text-align: center;
        border: 2px solid #e0e0e0;
    }
    .tool-card:hover {
        border-color: #667eea;
        transform: translateY(-2px);
        transition: all 0.3s;
    }
    .path-box {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .metric-box {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .recommend-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .level-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        color: white;
        margin: 2px;
    }
    .essential { background: #e74c3c; }
    .recommended { background: #f39c12; }
    .optional { background: #27ae60; }
</style>
""", unsafe_allow_html=True)

INDUSTRIES = [
    "互联网/IT", "电子商务", "游戏", "广告/公关/会展", 
    "媒体/出版", "教育/培训", "金融/投资", "房地产/建筑",
    "消费品/零售", "制造业", "物流/运输", "医疗/健康",
    "酒店/旅游", "能源/环保", "政府/非营利", "其他"
]

JOB_POSITIONS = [
    "创意总监", "设计总监", "视觉设计师", "UI设计师", "UX设计师",
    "产品经理", "运营经理", "市场经理", "品牌经理", "内容策划",
    "视频剪辑", "动画师", "插画师", "摄影师", "文案策划",
    "数据分析师", "用户研究员", "项目经理", "技术总监", "前端开发"
]

COMPANY_SCALES = ["小型（1-50人）", "中型（50-500人）", "大型（500人以上）"]

BUSINESS_SCOPES = [
    "品牌设计", "产品设计", "营销创意", "内容生产",
    "用户增长", "电商平台", "社交媒体", "视频制作",
    "游戏美术", "UI/UX设计", "全栈服务", "其他"
]

MOCK_JOBS = [
    {
        "title": "AI设计总监",
        "company": "创意广告公司",
        "salary": "30-50K",
        "location": "上海",
        "experience": "5-10年",
        "education": "本科",
        "detail": "负责AI设计团队管理，精通Midjourney、Stable Diffusion、DALL-E等AI绘图工具，具备团队管理能力",
        "tags": ["AI设计", "团队管理", "Midjourney"]
    },
    {
        "title": "AI视觉设计师",
        "company": "科技公司",
        "salary": "20-35K",
        "location": "北京",
        "experience": "3-5年",
        "education": "本科",
        "detail": "使用Runway、Pika、Sora进行视频创作，AIGC内容生产，熟悉Firefly、Photoshop AI",
        "tags": ["AI视频", "AIGC", "Runway"]
    },
    {
        "title": "AI创意设计师",
        "company": "互联网公司",
        "salary": "25-40K",
        "location": "深圳",
        "experience": "3-5年",
        "education": "本科",
        "detail": "精通Figma AI、Canva AI、Nano Banana等AI设计工具，具备创意策划能力",
        "tags": ["AI设计", "Figma", "Canva"]
    },
    {
        "title": "AI视频制作",
        "company": "传媒公司",
        "salary": "15-25K",
        "location": "杭州",
        "experience": "1-3年",
        "education": "大专",
        "detail": "使用剪映AI、可灵、HeyGen等工具进行视频制作和数字人创作",
        "tags": ["视频AI", "剪映", "数字人"]
    },
    {
        "title": "AI设计主管",
        "company": "电商平台",
        "salary": "25-35K",
        "location": "广州",
        "experience": "3-5年",
        "education": "本科",
        "detail": "管理AI设计团队，使用ComfyUI、ControlNet、LoRA等工具进行批量生产",
        "tags": ["AI管理", "ComfyUI", "批量生产"]
    },
    {
        "title": "AI设计师",
        "company": "设计公司",
        "salary": "12-20K",
        "location": "成都",
        "experience": "1-3年",
        "education": "本科",
        "detail": "使用ChatGPT、文心一言、Kimi等AI工具辅助设计工作",
        "tags": ["AI工具", "ChatGPT", "文心一言"]
    }
]

AI_TOOLS = {
    "图像生成": [
        {"name": "Midjourney", "frequency": 50, "cost": 60, "difficulty": "中等", "desc": "视觉冲击力首选，艺术感天花板"},
        {"name": "Stable Diffusion", "frequency": 40, "cost": 0, "difficulty": "较高", "desc": "开源灵活，可本地部署"},
        {"name": "DALL-E", "frequency": 30, "cost": 20, "difficulty": "低", "desc": "OpenAI出品，易用性强"},
        {"name": "Firefly", "frequency": 25, "cost": 0, "difficulty": "低", "desc": "Adobe生态，版权安全"}
    ],
    "视频生成": [
        {"name": "Runway", "frequency": 35, "cost": 35, "difficulty": "中等", "desc": "视频AI全能工具"},
        {"name": "Pika", "frequency": 20, "cost": 0, "difficulty": "低", "desc": "视频生成新秀"},
        {"name": "Sora", "frequency": 15, "cost": 0, "difficulty": "未知", "desc": "OpenAI视频模型"},
        {"name": "HeyGen", "frequency": 10, "cost": 50, "difficulty": "低", "desc": "数字人视频生成"},
        {"name": "可灵", "frequency": 10, "cost": 0, "difficulty": "低", "desc": "国产AI视频工具"},
        {"name": "剪映AI", "frequency": 8, "cost": 0, "difficulty": "低", "desc": "国内视频剪辑工具"}
    ],
    "设计工具": [
        {"name": "Figma AI", "frequency": 30, "cost": 0, "difficulty": "低", "desc": "设计协作平台"},
        {"name": "Canva AI", "frequency": 20, "cost": 0, "difficulty": "极低", "desc": "易用设计工具"},
        {"name": "Nano Banana", "frequency": 5, "cost": 40, "difficulty": "中等", "desc": "AI设计协作工具"},
        {"name": "Lovart", "frequency": 3, "cost": 35, "difficulty": "中等", "desc": "AI视频结构分析"}
    ],
    "工作流": [
        {"name": "ComfyUI", "frequency": 15, "cost": 0, "difficulty": "高", "desc": "可视化AI工作流"},
        {"name": "ControlNet", "frequency": 12, "cost": 0, "difficulty": "高", "desc": "精确控制AI生成"}
    ],
    "通用AI": [
        {"name": "ChatGPT", "frequency": 25, "cost": 20, "difficulty": "低", "desc": "通用AI助手"},
        {"name": "文心一言", "frequency": 15, "cost": 0, "difficulty": "低", "desc": "百度AI助手"},
        {"name": "Kimi", "frequency": 10, "cost": 0, "difficulty": "低", "desc": "长文本处理强"}
    ]
}

if 'step' not in st.session_state:
    st.session_state.step = 1
if 'search_results' not in st.session_state:
    st.session_state.search_results = None
if 'company_info' not in st.session_state:
    st.session_state.company_info = {}
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = None

def render_step1():
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.markdown("### 第一步：选择AI岗位")
    st.markdown("选择您的行业和目标AI岗位，系统将自动搜索相关招聘信息并分析所需AI工具")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏢 所属行业")
        industry = st.selectbox(
            "选择行业",
            options=INDUSTRIES,
            key="industry"
        )
        custom_industry = st.text_input("或自定义行业", placeholder="例如：广告/公关")
        final_industry = custom_industry if custom_industry else industry
    
    with col2:
        st.subheader("💼 AI岗位")
        position = st.selectbox(
            "选择岗位",
            options=JOB_POSITIONS,
            key="position"
        )
        custom_position = st.text_input("或自定义岗位", placeholder="例如：创意总监")
        final_position = custom_position if custom_position else position
    
    if final_industry and final_position:
        search_keyword = f"AI{final_position}"
        
        st.info(f"🔍 系统将搜索: **{search_keyword}** (行业: {final_industry})")
        
        if st.button("🚀 开始搜索分析", type="primary", use_container_width=True):
            with st.spinner("正在分析招聘数据..."):
                import time
                time.sleep(2)
                
                st.session_state.search_results = {
                    'keyword': search_keyword,
                    'industry': final_industry,
                    'position': final_position,
                    'jobs': MOCK_JOBS,
                    'tools': AI_TOOLS,
                    'stats': {
                        'total': len(MOCK_JOBS),
                        'valid': 5,
                        'tools_count': sum(len(tools) for tools in AI_TOOLS.values())
                    }
                }
                
                st.success("✅ 搜索完成！")
                st.rerun()

def render_step1_results():
    if not st.session_state.search_results:
        return
    
    results = st.session_state.search_results
    
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.markdown("### 第一步结果：AI工具汇总分析")
    st.markdown(f"基于 **{results['stats']['total']}** 个岗位分析，发现 **{results['stats']['tools_count']}** 种AI工具")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("分析岗位数", results['stats']['total'])
    with col2:
        st.metric("AI工具种类", results['stats']['tools_count'])
    with col3:
        st.metric("有效岗位", results['stats']['valid'])
    with col4:
        st.metric("搜索关键词", results['keyword'])
    
    st.markdown("---")
    st.markdown("### 🛠️ AI工具分类统计")
    
    for category, tools in results['tools'].items():
        with st.container():
            st.markdown(f"#### 📁 {category} ({len(tools)}个工具)")
            cols = st.columns(min(len(tools), 4))
            
            for idx, tool in enumerate(tools):
                with cols[idx % len(cols)]:
                    st.markdown(f"""
                    <div class="tool-card">
                        <h4 style="margin:0;color:#1a1a2e;">{tool['name']}</h4>
                        <p style="margin:0.5rem 0;font-size:0.9rem;color:#666;">{tool['desc']}</p>
                        <div style="display:flex;justify-content:space-between;font-size:0.8rem;color:#888;">
                            <span>📊 {tool['frequency']}%</span>
                            <span>💰 ${tool['cost']}</span>
                        </div>
                        <div style="margin-top:0.5rem;">
                            <span class="level-badge {'essential' if tool['frequency'] >= 30 else 'recommended' if tool['frequency'] >= 15 else 'optional'}">
                                {'必备' if tool['frequency'] >= 30 else '推荐' if tool['frequency'] >= 15 else '可选'}
                            </span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📊 岗位数据预览")
    
    job_data = []
    for job in results['jobs'][:5]:
        job_data.append({
            '岗位名称': job['title'],
            '公司': job['company'],
            '薪资': job['salary'],
            '地点': job['location'],
            '经验要求': job['experience'],
            '标签': ', '.join(job['tags'])
        })
    
    df = pd.DataFrame(job_data)
    st.dataframe(df, use_container_width=True)
    
    if st.button("➡️ 进入第二步：个性化推荐", type="primary", use_container_width=True):
        st.session_state.step = 2
        st.rerun()

def render_step2():
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.markdown("### 第二步：配置公司信息")
    st.markdown("告诉我们您的公司情况，为您生成个性化的AI工具配置方案")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🏢 所属行业")
        company_industry = st.selectbox(
            "公司所在行业",
            options=INDUSTRIES,
            index=INDUSTRIES.index(st.session_state.search_results['industry']) if st.session_state.search_results['industry'] in INDUSTRIES else 0,
            key="company_industry"
        )
    
    with col2:
        st.subheader("📊 企业规模")
        company_scale = st.selectbox(
            "选择企业规模",
            options=COMPANY_SCALES,
            key="company_scale"
        )
    
    with col3:
        st.subheader("🎯 业务范围")
        business_scope = st.multiselect(
            "选择业务范围（可多选）",
            options=BUSINESS_SCOPES,
            default=["品牌设计"],
            key="business_scope"
        )
    
    st.markdown("---")
    st.subheader("📋 岗位需求详情")
    
    col4, col5 = st.columns(2)
    with col4:
        team_size = st.number_input("团队人数", min_value=1, max_value=100, value=5)
        budget_level = st.select_slider(
            "预算水平",
            options=["低", "中", "高"],
            value="中"
        )
    
    with col5:
        priority = st.multiselect(
            "优先需求",
            options=["效率提升", "质量优化", "成本控制", "创新探索", "团队培训"],
            default=["效率提升"]
        )
        timeline = st.select_slider(
            "实施周期",
            options=["1个月内", "1-3个月", "3-6个月", "6个月以上"],
            value="1-3个月"
        )
    
    if st.button("🎯 生成个性化推荐方案", type="primary", use_container_width=True):
        with st.spinner("正在生成推荐方案..."):
            import time
            time.sleep(2)
            
            st.session_state.company_info = {
                'industry': company_industry,
                'scale': company_scale,
                'scope': business_scope,
                'teamSize': team_size,
                'budget': budget_level,
                'priority': priority,
                'timeline': timeline
            }
            
            st.session_state.recommendations = generate_recommendations(company_scale, budget_level)
            
            st.success("✅ 个性化推荐方案生成完成！")
            st.rerun()

def generate_recommendations(scale, budget):
    scale_factor = {"低": 0.5, "中": 1.0, "高": 1.5}[budget]
    
    recommendations = {
        "设计总监": {
            "essential": [
                {"name": "Midjourney", "cost": 60, "reason": "视觉创意核心工具", "path": "概念设计 → 视觉探索 → 方案输出"},
                {"name": "Stable Diffusion", "cost": 0, "reason": "本地部署，隐私安全", "path": "定制模型 → 批量生成 → 精细调整"},
                {"name": "Runway", "cost": 35, "reason": "视频生成全能", "path": "视频创意 → AI生成 → 后期优化"},
                {"name": "Figma AI", "cost": 0, "reason": "团队协作设计", "path": "原型设计 → AI辅助 → 团队评审"},
                {"name": "ChatGPT", "cost": 20, "reason": "文案与策略", "path": "需求分析 → 文案生成 → 策略优化"}
            ],
            "recommended": [
                {"name": "DALL-E", "cost": 20, "reason": "快速原型", "path": "快速出图 → 方案验证 → 迭代优化"},
                {"name": "Firefly", "cost": 0, "reason": "Adobe生态集成", "path": "设计制作 → AI增强 → 版权输出"},
                {"name": "Pika", "cost": 0, "reason": "短视频快速生成", "path": "脚本输入 → AI生成 → 快速发布"}
            ],
            "skills": [
                {"name": "AI战略与工具选型", "level": "专家", "time": "持续学习", "desc": "掌握各类AI工具优劣，制定团队工具栈"},
                {"name": "高阶提示词工程", "level": "专家", "time": "2-3个月", "desc": "精通复杂提示词设计，实现精准控制"},
                {"name": "AI工作流设计", "level": "高级", "time": "1-2个月", "desc": "设计高效AI辅助设计流程"},
                {"name": "团队AI能力建设", "level": "高级", "time": "持续", "desc": "培养团队AI技能，建立知识体系"}
            ],
            "cost": int(135 * scale_factor)
        },
        "设计主管": {
            "essential": [
                {"name": "Stable Diffusion", "cost": 0, "reason": "批量生产主力", "path": "模型配置 → 批量生成 → 质量把控"},
                {"name": "Figma AI", "cost": 0, "reason": "团队设计协作", "path": "设计规范 → 团队协作 → 版本管理"},
                {"name": "Runway", "cost": 35, "reason": "视频制作", "path": "素材准备 → AI生成 → 剪辑输出"},
                {"name": "剪映AI", "cost": 0, "reason": "国内视频工具", "path": "素材导入 → AI剪辑 → 快速输出"}
            ],
            "recommended": [
                {"name": "Midjourney", "cost": 60, "reason": "高质量概念图", "path": "创意输入 → AI生成 → 筛选优化"},
                {"name": "Canva AI", "cost": 0, "reason": "快速设计", "path": "模板选择 → AI调整 → 快速输出"},
                {"name": "Pika", "cost": 0, "reason": "短视频", "path": "内容输入 → AI生成 → 发布准备"},
                {"name": "ComfyUI", "cost": 0, "reason": "工作流自动化", "path": "工作流搭建 → 自动化运行 → 批量输出"}
            ],
            "skills": [
                {"name": "中端AI工具应用", "level": "熟练", "time": "1-2个月", "desc": "熟练运用主流AI工具完成设计任务"},
                {"name": "批量生产管理", "level": "熟练", "time": "2-4周", "desc": "管理AI辅助的批量设计生产"},
                {"name": "提示词优化", "level": "进阶", "time": "3-4周", "desc": "编写高效提示词，提升产出质量"},
                {"name": "AI产出审核", "level": "熟练", "time": "2-3周", "desc": "审核AI生成内容的质量与合规性"}
            ],
            "cost": int(95 * scale_factor)
        },
        "设计专员": {
            "essential": [
                {"name": "Canva AI", "cost": 0, "reason": "易上手设计工具", "path": "模板选择 → 内容替换 → 快速输出"},
                {"name": "剪映AI", "cost": 0, "reason": "视频剪辑", "path": "素材导入 → AI剪辑 → 效果调整"},
                {"name": "可灵", "cost": 0, "reason": "国产AI视频", "path": "文字描述 → AI生成 → 简单编辑"},
                {"name": "ChatGPT", "cost": 20, "reason": "文案辅助", "path": "需求输入 → 文案生成 → 修改使用"}
            ],
            "recommended": [
                {"name": "Figma", "cost": 0, "reason": "UI设计基础", "path": "界面设计 → 组件使用 → 原型输出"},
                {"name": "文心一言", "cost": 0, "reason": "中文AI助手", "path": "中文输入 → AI生成 → 内容调整"},
                {"name": "即梦", "cost": 0, "reason": "AI图像生成", "path": "文字描述 → AI绘图 → 简单后期"}
            ],
            "skills": [
                {"name": "基础AI工具操作", "level": "入门", "time": "1-2周", "desc": "掌握基础AI设计工具的使用"},
                {"name": "简单提示词编写", "level": "入门", "time": "1周", "desc": "编写简单有效的AI提示词"},
                {"name": "AI辅助设计执行", "level": "入门", "time": "2-3周", "desc": "使用AI工具辅助完成设计任务"},
                {"name": "设计基础技能", "level": "基础", "time": "持续", "desc": "保持传统设计技能，结合AI工具"}
            ],
            "cost": int(20 * scale_factor)
        }
    }
    
    return recommendations

def render_step2_results():
    if not st.session_state.recommendations:
        return
    
    company = st.session_state.company_info
    
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.markdown("### 第二步结果：个性化AI工具配置方案")
    st.markdown(f"**{company['industry']}** | **{company['scale']}** | 团队**{company['teamSize']}**人 | 预算**{company['budget']}** | 周期**{company['timeline']}**")
    st.markdown('</div>', unsafe_allow_html=True)
    
    tabs = st.tabs(["设计总监", "设计主管", "设计专员", "成本分析", "实施路径"])
    
    positions = ["设计总监", "设计主管", "设计专员"]
    
    for idx, (tab, position) in enumerate(zip(tabs[:3], positions)):
        with tab:
            if position in st.session_state.recommendations:
                data = st.session_state.recommendations[position]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("必备工具", len(data['essential']))
                with col2:
                    st.metric("推荐工具", len(data['recommended']))
                with col3:
                    st.metric("月费估算", f"${data['cost']}")
                
                st.markdown("---")
                
                if data['essential']:
                    st.markdown("#### 🔴 必备工具（核心配置）")
                    for tool in data['essential']:
                        render_tool_recommendation(tool, "essential")
                
                if data['recommended']:
                    st.markdown("#### 🟡 推荐工具（扩展配置）")
                    for tool in data['recommended']:
                        render_tool_recommendation(tool, "recommended")
                
                st.markdown("---")
                st.markdown("#### 📚 技能矩阵 - 为更好使用AI工具建议掌握的技能")
                
                # 使用新的技能矩阵数据
                if position in SKILL_MATRIX:
                    skill_data = SKILL_MATRIX[position]
                    
                    for category, skills in skill_data.items():
                        with st.expander(f"📖 {category}"):
                            # 创建技能矩阵表格
                            skill_df_data = []
                            for skill_name, skill_info in skills.items():
                                level_color = {
                                    "专家": "🔴", "高级": "🟠", "熟练": "🟡", 
                                    "进阶": "🟢", "入门": "🔵"
                                }.get(skill_info['level'], "⚪")
                                
                                priority_color = {
                                    "核心": "🔴", "重要": "🟠", "一般": "🟡"
                                }.get(skill_info['priority'], "⚪")
                                
                                skill_df_data.append({
                                    '技能名称': skill_name,
                                    '掌握程度': f"{level_color} {skill_info['level']}",
                                    '优先级': f"{priority_color} {skill_info['priority']}"
                                })
                            
                            if skill_df_data:
                                skill_df = pd.DataFrame(skill_df_data)
                                st.dataframe(skill_df, use_container_width=True, hide_index=True)
                
                # 传统技能展示作为补充
                st.markdown("---")
                st.markdown("**📖 详细技能说明**:")
                for skill in data['skills']:
                    with st.expander(f"{skill['name']} ({skill['level']})"):
                        st.write(f"**学习周期**: {skill['time']}")
                        st.write(f"**描述**: {skill['desc']}")
    
    with tabs[3]:
        st.markdown("#### 💰 成本分析对比")
        
        cost_data = []
        for pos in positions:
            if pos in st.session_state.recommendations:
                data = st.session_state.recommendations[pos]
                cost_data.append({
                    '岗位层级': pos,
                    '必备工具数': len(data['essential']),
                    '推荐工具数': len(data['recommended']),
                    '月费': data['cost'],
                    '年费': data['cost'] * 12
                })
        
        if cost_data:
            cost_df = pd.DataFrame(cost_data)
            st.dataframe(cost_df, use_container_width=True)
            
            st.bar_chart(cost_df.set_index('岗位层级')[['月费', '年费']])
            
            total_monthly = sum(item['cost'] for item in st.session_state.recommendations.values())
            st.info(f"**总月费预算**: ${total_monthly} | **总年费预算**: ${total_monthly * 12}")
    
    with tabs[4]:
        st.markdown("#### 🛤️ AI工具组合架构与最优路径")
        st.info("💡 这里展示的不是简单的工具使用步骤，而是基于当前AI技术发展的最优解——前后工具配合、调用关系、以及如何利用AI自动化减少人工操作")
        
        # 为每个关键工具展示AI组合架构
        key_tools = ["Midjourney", "Stable Diffusion", "Runway", "Figma AI", "Lovart/星流", "ChatGPT/Claude"]
        
        for tool_name in key_tools:
            if tool_name in AI_WORKFLOWS:
                workflow = AI_WORKFLOWS[tool_name]
                
                with st.expander(f"🎯 {tool_name} - {workflow['workflow_name']}"):
                    st.markdown(f"**{workflow['description']}**")
                    st.markdown(f"💡 **核心洞察**: {workflow['key_insight']}")
                    
                    st.markdown("---")
                    st.markdown("**🔄 最优工作流路径**:")
                    
                    for step in workflow['optimal_path']:
                        st.markdown(f"""
                        <div style="
                            background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
                            border-left: 4px solid #667eea;
                            border-radius: 8px;
                            padding: 1rem;
                            margin: 0.5rem 0;
                        ">
                            <div style="display:flex;justify-content:space-between;align-items:center;">
                                <h4 style="margin:0;color:#1a1a2e;">步骤 {step['step']}: {step['phase']}</h4>
                                <span style="background:#667eea;color:white;padding:2px 8px;border-radius:12px;font-size:0.8rem;">{step['tool']}</span>
                            </div>
                            <p style="margin:0.5rem 0;color:#666;"><strong>操作:</strong> {step['action']}</p>
                            <p style="margin:0;color:#888;font-size:0.9rem;"><strong>产出:</strong> {step['output']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Prompt模板展示
                    if 'prompt_template' in workflow:
                        st.markdown("---")
                        st.markdown("**📝 Prompt工程模板**:")
                        prompt_data = workflow['prompt_template']
                        st.markdown(f"**结构**: {prompt_data['structure']}")
                        
                        with st.expander("查看完整Prompt示例"):
                            st.code(prompt_data['example'], language='text')
        
        # Prompt模板库
        st.markdown("---")
        st.markdown("#### 📚 Prompt工程模板库")
        st.info("掌握这些Prompt结构，可以大幅提升AI工具的输出质量")
        
        for template_name, template_data in PROMPT_TEMPLATES.items():
            with st.expander(f"📝 {template_data['name']}"):
                st.markdown(f"**模板结构**: {template_data['template']}")
                st.markdown("**示例**:")
                st.code(template_data['example'], language='text')

def render_tool_recommendation(tool, level):
    colors = {"essential": "#e74c3c", "recommended": "#f39c12"}
    labels = {"essential": "必备", "recommended": "推荐"}
    
    st.markdown(f"""
    <div style="
        border-left: 5px solid {colors.get(level, '#ccc')};
        background: white;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    ">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">
            <h4 style="margin:0;color:#1a1a2e;">{tool['name']}</h4>
            <span style="
                background: {colors.get(level, '#ccc')};
                color: white;
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 0.8rem;
                font-weight: bold;
            ">{labels.get(level, '')}</span>
        </div>
        <p style="margin:0.5rem 0;color:#666;">{tool['reason']}</p>
        <div style="background:#f8f9fa;border-radius:8px;padding:0.8rem;margin-top:0.5rem;">
            <strong>🛤️ 使用路径:</strong> {tool['path']}
        </div>
        <div style="display:flex;gap:1rem;margin-top:0.5rem;font-size:0.9rem;color:#888;">
            <span>💰 月费: ${tool['cost']}</span>
            <span>📊 年费: ${tool['cost'] * 12}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def main():
    st.markdown('<div class="main-title">🎯 AI岗位工具配置分析系统</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">基于招聘大数据，为您的团队推荐最适合的AI工具配置方案</div>', unsafe_allow_html=True)
    
    st.sidebar.title("📋 使用导航")
    st.sidebar.markdown("""
    **使用流程**:
    1. 选择行业和AI岗位
    2. 查看AI工具汇总
    3. 配置公司信息
    4. 获取个性化推荐
    """)
    
    if st.sidebar.button("🔄 重新开始分析"):
        st.session_state.step = 1
        st.session_state.search_results = None
        st.session_state.recommendations = None
        st.session_state.company_info = {}
        st.rerun()
    
    if st.session_state.step == 1:
        render_step1()
        
        if st.session_state.search_results:
            render_step1_results()
    
    elif st.session_state.step == 2:
        if st.sidebar.button("⬅️ 返回第一步"):
            st.session_state.step = 1
            st.rerun()
        
        render_step2()
        
        if st.session_state.recommendations:
            render_step2_results()

if __name__ == "__main__":
    main()
