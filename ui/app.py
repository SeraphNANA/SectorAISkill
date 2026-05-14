import streamlit as st
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src", "data", "job_categories_full.json")

# ============================
#  THEME CSS - 直接为每个主题写完整样式
# ============================

def get_theme_css():
    dark = {
        'bg': '#f8f7fc', 'bg_secondary': '#ffffff', 'card': '#ffffff',
        'border': '#e8e5f0', 'text_primary': '#1a1a2e', 'text_secondary': '#6b6680', 
        'text_muted': '#9b96b0', 'accent': '#7c3aed', 'accent_bg': 'rgba(124, 58, 237, 0.1)',
        'accent_border': 'rgba(124, 58, 237, 0.2)', 'blue': '#4f46e5', 'blue_bg': 'rgba(79, 70, 229, 0.1)',
        'purple': '#8b5cf6', 'shadow': '0 4px 12px rgba(124, 58, 237, 0.08)', 'shadow_hover': '0 6px 20px rgba(124, 58, 237, 0.12)',
        'input_bg': '#ffffff', 'footer': '#9b96b0',
    }
    
    light = {
        'bg': '#f8f7fc', 'bg_secondary': '#ffffff', 'card': '#ffffff',
        'border': '#e8e5f0', 'text_primary': '#1a1a2e', 'text_secondary': '#6b6680', 
        'text_muted': '#9b96b0', 'accent': '#7c3aed', 'accent_bg': 'rgba(124, 58, 237, 0.1)',
        'accent_border': 'rgba(124, 58, 237, 0.2)', 'blue': '#4f46e5', 'blue_bg': 'rgba(79, 70, 229, 0.1)',
        'purple': '#8b5cf6', 'shadow': '0 4px 12px rgba(124, 58, 237, 0.08)', 'shadow_hover': '0 6px 20px rgba(124, 58, 237, 0.12)',
        'input_bg': '#ffffff', 'footer': '#9b96b0',
    }
    
    def gen_theme(c, prefix=""):
        return f"""
        {prefix}html, {prefix}body, {prefix}.stApp, {prefix}#root, {prefix}section[data-testid="stAppViewContainer"] {{
            background: {c['bg']} !important;
            color: {c['text_secondary']} !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
        }}
        
        {prefix}.main .block-container {{
            background: {c['bg']} !important;
            padding: 24px 32px !important;
            max-width: 1400px !important;
        }}
        
        {prefix}.main {{
            background: {c['bg']} !important;
        }}
        
        {prefix}div[data-testid="stVerticalBlock"] > div {{
            background: transparent !important;
        }}
        
        {prefix}.stMarkdown, {prefix}.stText, {prefix}.stCode {{
            background: transparent !important;
        }}
        
        /* Sidebar */
        {prefix}[data-testid="stSidebar"] {{
            background: {c['bg_secondary']} !important;
            border-right: 1px solid {c['border']} !important;
        }}
        {prefix}[data-testid="stSidebar"] > div:first-child {{
            padding-top: 0 !important;
            background: {c['bg_secondary']} !important;
        }}
        {prefix}[data-testid="stSidebar"] .stMarkdown,
        {prefix}[data-testid="stSidebar"] label {{
            color: {c['text_secondary']} !important;
            font-size: 13px !important;
        }}
        {prefix}[data-testid="stSidebar"] h1, {prefix}[data-testid="stSidebar"] h2, {prefix}[data-testid="stSidebar"] h3 {{
            color: {c['text_primary']} !important;
        }}
        {prefix}[data-testid="stSidebar"] .stSelectbox > div > div {{
            background: {c['input_bg']} !important;
            border: 1px solid {c['accent']} !important;
            border-radius: 10px !important;
            color: {c['text_primary']} !important;
        }}
        
        /* Brand Header */
        {prefix}.brand-header {{
            display: flex; align-items: center; gap: 12px; padding: 20px 16px;
            border-bottom: 1px solid {c['border']}; margin-bottom: 24px;
        }}
        {prefix}.brand-header .logo-icon {{
            width: 40px; height: 40px;
            background: linear-gradient(135deg, {c['accent']}, {c['purple']});
            border-radius: 10px; display: flex; align-items: center; justify-content: center;
            font-size: 22px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            color: #ffffff !important;
        }}
        {prefix}.brand-header .brand-text {{
            font-size: 18px; font-weight: 700; color: {c['text_primary']}; letter-spacing: -0.3px;
        }}
        {prefix}.brand-header .brand-sub {{
            font-size: 11px; color: {c['text_secondary']}; letter-spacing: 1.5px;
            text-transform: uppercase; margin-top: 2px;
        }}
        
        /* Section Title */
        {prefix}.section-title {{
            font-size: 20px; font-weight: 700; color: {c['text_primary']};
            margin-bottom: 20px; display: flex; align-items: center; gap: 10px;
        }}
        {prefix}.section-title .badge-live {{
            background: {c['accent_bg']}; color: {c['accent']}; font-size: 11px;
            font-weight: 600; padding: 3px 10px; border-radius: 20px;
            border: 1px solid {c['accent_border']};
        }}
        
        /* Metric Cards */
        {prefix}.metric-card {{
            background: {c['card']}; border: 1px solid {c['border']}; border-radius: 12px;
            padding: 20px; transition: all 0.2s ease; box-shadow: {c['shadow']};
        }}
        {prefix}.metric-card:hover {{ border-color: {c['border']}; box-shadow: {c['shadow_hover']}; }}
        {prefix}.metric-card .metric-label {{ color: {c['text_secondary']}; font-size: 13px; font-weight: 500; margin-bottom: 8px; }}
        {prefix}.metric-card .metric-value {{ color: {c['text_primary']}; font-size: 28px; font-weight: 700; margin-bottom: 8px; }}
        {prefix}.metric-card .metric-change {{ font-size: 12px; font-weight: 600; display: flex; align-items: center; gap: 4px; }}
        {prefix}.metric-card .metric-change.up {{ color: {c['accent']}; }}
        
        /* Landing Hero */
        {prefix}.landing-hero {{
            text-align: center; padding: 80px 0 60px; background: {c['bg']} !important;
        }}
        {prefix}.landing-hero .hero-icon {{
            width: 80px; height: 80px;
            background: linear-gradient(135deg, {c['accent']}, {c['purple']});
            border-radius: 20px; display: inline-flex; align-items: center; justify-content: center;
            font-size: 40px; margin-bottom: 24px; color: #ffffff !important;
        }}
        {prefix}.landing-hero .hero-title {{
            font-size: 32px; font-weight: 800; color: {c['text_primary']};
            margin-bottom: 12px; letter-spacing: -0.5px;
        }}
        {prefix}.landing-hero .hero-subtitle {{
            font-size: 15px; color: {c['text_secondary']}; max-width: 480px; margin: 0 auto; line-height: 1.7;
        }}
        
        /* Step Guide */
        {prefix}.step-guide {{
            background: {c['card']}; border: 1px solid {c['border']}; border-radius: 16px;
            padding: 32px; box-shadow: {c['shadow']};
        }}
        {prefix}.step-item .step-circle {{
            width: 52px; height: 52px; background: {c['bg']}; border-radius: 50%;
            display: inline-flex; align-items: center; justify-content: center;
            font-size: 18px; font-weight: 700; color: {c['text_muted']};
            margin-bottom: 10px; border: 2px solid {c['border']};
        }}
        {prefix}.step-item .step-circle.active {{
            background: linear-gradient(135deg, {c['accent']}, {c['purple']});
            color: #ffffff; border-color: {c['accent']};
        }}
        {prefix}.step-item .step-label {{ font-size: 13px; color: {c['text_muted']}; font-weight: 500; }}
        {prefix}.step-item .step-label.active {{ color: {c['accent']}; font-weight: 700; }}
        
        /* Buttons */
        {prefix}.stButton > button {{
            background: linear-gradient(135deg, {c['accent']}, {c['purple']}) !important;
            color: #ffffff !important; border: none !important; border-radius: 10px !important;
            font-weight: 700 !important; font-size: 14px !important; padding: 12px 24px !important;
        }}
        
        /* Expander */
        {prefix}.streamlit-expanderHeader {{
            background: {c['card']} !important; border: 1px solid {c['border']} !important;
            border-radius: 10px !important; color: {c['text_primary']} !important;
        }}
        {prefix}.streamlit-expanderContent {{
            background: {c['bg']} !important; border: 1px solid {c['border']} !important;
            border-top: none !important;
        }}
        
        /* Footer */
        {prefix}.footer-text {{ text-align: center; color: {c['footer']}; font-size: 12px; padding: 16px 0; }}
        
        /* Analysis Summary */
        {prefix}.analysis-summary {{
            display: flex; gap: 24px; flex-wrap: wrap; padding: 16px 20px;
            background: {c['card']}; border: 1px solid {c['border']}; border-radius: 12px;
        }}
        {prefix}.analysis-item {{ display: flex; align-items: center; gap: 8px; }}
        {prefix}.analysis-label {{ font-size: 13px; color: {c['text_muted']}; }}
        {prefix}.analysis-value {{ font-size: 13px; color: {c['text_primary']}; font-weight: 600; }}
        
        /* Scrollbar */
        {prefix}::-webkit-scrollbar {{ width: 6px; }}
        {prefix}::-webkit-scrollbar-track {{ background: {c['bg']}; }}
        {prefix}::-webkit-scrollbar-thumb {{ background: {c['border']}; border-radius: 3px; }}
        """
    
    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* ===== Default Dark Theme ===== */
    html, body, .stApp, #root, section[data-testid="stAppViewContainer"] {{
        background: {dark['bg']} !important;
        color: {dark['text_secondary']} !important;
    }}
    .main .block-container, .main {{ background: {dark['bg']} !important; }}
    [data-testid="stSidebar"] {{ background: {dark['bg_secondary']} !important; }}
    .metric-card {{ background: {dark['card']} !important; }}
    .landing-hero {{ background: {dark['bg']} !important; }}
    .step-guide {{ background: {dark['card']} !important; }}
    
    /* ===== Light Theme (when Streamlit sets data-theme="light") ===== */
    .stApp[data-theme="light"],
    .stApp[data-theme="light"] html,
    .stApp[data-theme="light"] body,
    .stApp[data-theme="light"] #root,
    .stApp[data-theme="light"] section[data-testid="stAppViewContainer"] {{
        background: {light['bg']} !important;
        color: {light['text_secondary']} !important;
    }}
    .stApp[data-theme="light"] .main .block-container,
    .stApp[data-theme="light"] .main {{
        background: {light['bg']} !important;
    }}
    .stApp[data-theme="light"] [data-testid="stSidebar"] {{
        background: {light['bg_secondary']} !important;
    }}
    .stApp[data-theme="light"] .metric-card {{
        background: {light['card']} !important;
    }}
    .stApp[data-theme="light"] .landing-hero {{
        background: {light['bg']} !important;
    }}
    .stApp[data-theme="light"] .step-guide {{
        background: {light['card']} !important;
    }}
    
    /* ===== Common Styles ===== */
    .stApp {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif; }}
    
    /* Sidebar */
    [data-testid="stSidebar"] {{ border-right: 1px solid {dark['border']}; }}
    .stApp[data-theme="light"] [data-testid="stSidebar"] {{ border-right-color: {light['border']}; }}
    
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label {{ font-size: 13px; }}
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {{ color: {dark['text_primary']}; }}
    .stApp[data-theme="light"] [data-testid="stSidebar"] h1,
    .stApp[data-theme="light"] [data-testid="stSidebar"] h2,
    .stApp[data-theme="light"] [data-testid="stSidebar"] h3 {{ color: {light['text_primary']}; }}
    
    /* Brand Header */
    .brand-header {{ display: flex; align-items: center; gap: 12px; padding: 20px 16px; margin-bottom: 24px; }}
    .brand-header .logo-icon {{ width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 22px; }}
    .brand-header .brand-text {{ font-size: 18px; font-weight: 700; letter-spacing: -0.3px; }}
    .brand-header .brand-sub {{ font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; margin-top: 2px; }}
    
    .brand-header .logo-icon {{ background: linear-gradient(135deg, {dark['accent']}, {dark['purple']}); color: #ffffff !important; }}
    .brand-header .brand-text {{ color: {dark['text_primary']}; }}
    .brand-header .brand-sub {{ color: {dark['text_secondary']}; }}
    .brand-header {{ border-bottom: 1px solid {dark['border']}; }}
    
    .stApp[data-theme="light"] .brand-header .logo-icon {{ background: linear-gradient(135deg, {light['accent']}, {light['purple']}); color: #ffffff !important; }}
    
    /* Sidebar Selectboxes */
    [data-testid="stSidebar"] div[data-baseweb="select"] {{
        border: 1px solid {dark['accent']} !important;
        border-radius: 10px !important;
        background: #ffffff !important;
    }}
    .stApp[data-theme="light"] [data-testid="stSidebar"] div[data-baseweb="select"] {{
        border-color: {light['accent']} !important;
    }}
    .stApp[data-theme="light"] .brand-header .brand-text {{ color: {light['text_primary']}; }}
    .stApp[data-theme="light"] .brand-header .brand-sub {{ color: {light['text_secondary']}; }}
    .stApp[data-theme="light"] .brand-header {{ border-bottom-color: {light['border']}; }}
    
    /* Section Title */
    .section-title {{ font-size: 20px; font-weight: 700; margin-bottom: 20px; display: flex; align-items: center; gap: 10px; }}
    .section-title {{ color: {dark['text_primary']}; }}
    .stApp[data-theme="light"] .section-title {{ color: {light['text_primary']}; }}
    
    .section-title .badge-live {{ font-size: 11px; font-weight: 600; padding: 3px 10px; border-radius: 20px; }}
    .section-title .badge-live {{ background: {dark['accent_bg']}; color: {dark['accent']}; border: 1px solid {dark['accent_border']}; }}
    .stApp[data-theme="light"] .section-title .badge-live {{ background: {light['accent_bg']}; color: {light['accent']}; border-color: {light['accent_border']}; }}
    
    /* Metric Cards */
    .metric-card {{ border: 1px solid {dark['border']}; border-radius: 12px; padding: 20px; box-shadow: {dark['shadow']}; }}
    .metric-card .metric-label {{ color: {dark['text_secondary']}; font-size: 13px; font-weight: 500; margin-bottom: 8px; }}
    .metric-card .metric-value {{ color: {dark['text_primary']}; font-size: 28px; font-weight: 700; margin-bottom: 8px; }}
    .metric-card .metric-change {{ font-size: 12px; font-weight: 600; display: flex; align-items: center; gap: 4px; }}
    .metric-card .metric-change.up {{ color: {dark['accent']}; }}
    
    .stApp[data-theme="light"] .metric-card {{ border-color: {light['border']}; box-shadow: {light['shadow']}; }}
    .stApp[data-theme="light"] .metric-card .metric-label {{ color: {light['text_secondary']}; }}
    .stApp[data-theme="light"] .metric-card .metric-value {{ color: {light['text_primary']}; }}
    .stApp[data-theme="light"] .metric-card .metric-change.up {{ color: {light['accent']}; }}
    
    /* Landing Hero */
    .landing-hero {{ text-align: center; padding: 80px 0 60px; }}
    .landing-hero .hero-icon {{ width: 80px; height: 80px; border-radius: 20px; display: inline-flex; align-items: center; justify-content: center; font-size: 40px; margin-bottom: 24px; color: #ffffff !important; }}
    .landing-hero .hero-title {{ font-size: 32px; font-weight: 800; margin-bottom: 12px; letter-spacing: -0.5px; }}
    .landing-hero .hero-subtitle {{ font-size: 15px; max-width: 480px; margin: 0 auto; line-height: 1.7; }}
    
    .landing-hero .hero-icon {{ background: linear-gradient(135deg, {dark['accent']}, {dark['purple']}); }}
    .landing-hero .hero-title {{ color: {dark['text_primary']}; }}
    .landing-hero .hero-subtitle {{ color: {dark['text_secondary']}; }}
    
    .stApp[data-theme="light"] .landing-hero .hero-icon {{ background: linear-gradient(135deg, {light['accent']}, {light['purple']}); }}
    .stApp[data-theme="light"] .landing-hero .hero-title {{ color: {light['text_primary']}; }}
    .stApp[data-theme="light"] .landing-hero .hero-subtitle {{ color: {light['text_secondary']}; }}
    
    /* Step Guide */
    .step-guide {{ border: 1px solid {dark['border']}; border-radius: 16px; padding: 32px; box-shadow: {dark['shadow']}; }}
    .stApp[data-theme="light"] .step-guide {{ border-color: {light['border']}; box-shadow: {light['shadow']}; }}
    
    .step-item .step-circle {{ width: 52px; height: 52px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 18px; font-weight: 700; margin-bottom: 10px; }}
    .step-item .step-circle {{ background: {dark['bg']}; color: {dark['text_muted']}; border: 2px solid {dark['border']}; }}
    .step-item .step-circle.active {{ background: linear-gradient(135deg, {dark['accent']}, {dark['purple']}); color: #ffffff; border-color: {dark['accent']}; }}
    .step-item .step-label {{ font-size: 13px; font-weight: 500; }}
    .step-item .step-label {{ color: {dark['text_muted']}; }}
    .step-item .step-label.active {{ color: {dark['accent']}; font-weight: 700; }}
    
    .stApp[data-theme="light"] .step-item .step-circle {{ background: {light['bg']}; color: {light['text_muted']}; border-color: {light['border']}; }}
    .stApp[data-theme="light"] .step-item .step-circle.active {{ background: linear-gradient(135deg, {light['accent']}, {light['purple']}); border-color: {light['accent']}; }}
    .stApp[data-theme="light"] .step-item .step-label {{ color: {light['text_muted']}; }}
    .stApp[data-theme="light"] .step-item .step-label.active {{ color: {light['accent']}; }}
    
    /* Buttons */
    .stButton > button {{ border: none !important; border-radius: 10px !important; font-weight: 700 !important; font-size: 14px !important; padding: 12px 24px !important; }}
    .stButton > button {{ background: linear-gradient(135deg, {dark['accent']}, {dark['purple']}) !important; color: #ffffff !important; }}
    .stApp[data-theme="light"] .stButton > button {{ background: linear-gradient(135deg, {light['accent']}, {light['purple']}) !important; }}
    
    /* Footer */
    .footer-text {{ text-align: center; font-size: 12px; padding: 16px 0; }}
    .footer-text {{ color: {dark['footer']}; }}
    .stApp[data-theme="light"] .footer-text {{ color: {light['footer']}; }}
    </style>
    """

# ============================
#  PAGE CONFIG
# ============================
st.set_page_config(
    page_title="SectorAI - AI岗位工具配置",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(get_theme_css(), unsafe_allow_html=True)

# ============================
#  SESSION STATE
# ============================
if 'search_results' not in st.session_state:
    st.session_state.search_results = None
if 'search_clicked' not in st.session_state:
    st.session_state.search_clicked = False

# ============================
#  DATABASE
# ============================
@st.cache_data
def load_database():
    try:
        with open(DB_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"industries": {}}

DB = load_database()

def get_all_industries():
    return list(DB.get("industries", {}).keys())

def get_categories_for_industry(industry):
    ind = DB.get("industries", {}).get(industry, {})
    return list(ind.get("categories", {}).keys())

def get_positions_for_category(industry, category):
    cat = DB.get("industries", {}).get(industry, {}).get("categories", {}).get(category, {})
    return list(cat.get("positions", {}).keys())

def get_position_data(industry, category, position):
    return DB.get("industries", {}).get(industry, {}).get("categories", {}).get(category, {}).get("positions", {}).get(position, {})

def get_company_scales():
    return DB.get("companyScales", ["小型", "中型", "大型"])

def get_business_types():
    return DB.get("businessTypes", [])

def get_departments():
    return DB.get("departments", [])

TOOL_DB = {
    'ChatGPT': {'cost': 20, 'learn': '3-5天', 'best': ['内容创作', '代码辅助', '数据分析'], 'difficulty': '低', 'free': True},
    'Claude': {'cost': 20, 'learn': '3-5天', 'best': ['长文档分析', '代码辅助', '学术写作'], 'difficulty': '低', 'free': True},
    'GitHub Copilot': {'cost': 19, 'learn': '1-2周', 'best': ['代码补全', '代码审查', '单元测试'], 'difficulty': '低', 'free': False},
    'Cursor': {'cost': 0, 'learn': '1-2周', 'best': ['AI编程', '代码重构', '项目理解'], 'difficulty': '低', 'free': True},
    '通义灵码': {'cost': 0, 'learn': '1-2周', 'best': ['中文编程', '代码生成', '注释生成'], 'difficulty': '低', 'free': True},
    'Midjourney': {'cost': 60, 'learn': '2-4周', 'best': ['创意设计', '品牌视觉', '概念艺术'], 'difficulty': '中', 'free': False},
    'Stable Diffusion': {'cost': 0, 'learn': '4-8周', 'best': ['定制化生成', '批量生产', '隐私项目'], 'difficulty': '高', 'free': True},
    'Figma': {'cost': 12, 'learn': '2-3周', 'best': ['UI设计', '产品原型', '协作设计'], 'difficulty': '低', 'free': True},
    'Canva': {'cost': 12, 'learn': '2-3天', 'best': ['营销物料', '社交媒体', '快速设计'], 'difficulty': '极低', 'free': True},
    '剪映': {'cost': 0, 'learn': '3-5天', 'best': ['短视频制作', '抖音内容', '快速剪辑'], 'difficulty': '极低', 'free': True},
    'CapCut': {'cost': 0, 'learn': '3-5天', 'best': ['海外短视频', 'TikTok', '移动剪辑'], 'difficulty': '极低', 'free': True},
    'Notion': {'cost': 8, 'learn': '1-2周', 'best': ['文档管理', '项目管理', '知识库'], 'difficulty': '低', 'free': True},
    'Notion AI': {'cost': 10, 'learn': '1-2周', 'best': ['AI写作', '内容总结', '智能问答'], 'difficulty': '低', 'free': False},
    '飞书': {'cost': 10, 'learn': '1-2周', 'best': ['团队协作', '办公协同', '文档管理'], 'difficulty': '低', 'free': True},
    '钉钉': {'cost': 10, 'learn': '1-2周', 'best': ['企业通讯', '考勤管理', '审批流程'], 'difficulty': '低', 'free': True},
    'Tableau': {'cost': 70, 'learn': '3-4周', 'best': ['数据可视化', '商业智能', '仪表盘'], 'difficulty': '中', 'free': False},
    'Power BI': {'cost': 49, 'learn': '3-4周', 'best': ['数据仪表盘', '报表分析', 'Excel集成'], 'difficulty': '中', 'free': False},
    'Python': {'cost': 0, 'learn': '8-12周', 'best': ['数据分析', '自动化脚本', '机器学习'], 'difficulty': '高', 'free': True},
    'SQL': {'cost': 0, 'learn': '4-6周', 'best': ['数据库查询', '数据分析', '报表生成'], 'difficulty': '中', 'free': True},
    'Gamma': {'cost': 20, 'learn': '1-2周', 'best': ['演示文稿', 'PPT制作', '内容展示'], 'difficulty': '低', 'free': True},
    'Tome': {'cost': 20, 'learn': '1-2周', 'best': ['故事化演示', '营销材料', '方案展示'], 'difficulty': '低', 'free': True},
    '神策数据': {'cost': 100, 'learn': '4-8周', 'best': ['用户行为分析', '数据驱动', '精细化运营'], 'difficulty': '高', 'free': False},
    'GrowingIO': {'cost': 80, 'learn': '4-8周', 'best': ['用户增长', '行为分析', '营销归因'], 'difficulty': '高', 'free': False},
    'Mixpanel': {'cost': 20, 'learn': '2-4周', 'best': ['产品分析', '用户漏斗', 'A/B测试'], 'difficulty': '中', 'free': True},
    'HubSpot': {'cost': 50, 'learn': '3-4周', 'best': ['客户管理', '营销自动化', '销售管理'], 'difficulty': '中', 'free': True},
    'Salesforce': {'cost': 100, 'learn': '6-8周', 'best': ['客户管理', '销售自动化', '企业CRM'], 'difficulty': '高', 'free': False},
    '文心一言': {'cost': 0, 'learn': '2-3天', 'best': ['中文内容', '知识问答', '创意写作'], 'difficulty': '低', 'free': True},
    '通义千问': {'cost': 0, 'learn': '2-3天', 'best': ['中文对话', '代码生成', '文档处理'], 'difficulty': '低', 'free': True},
    'Kimi': {'cost': 0, 'learn': '1-2天', 'best': ['长文档分析', '内容总结', '知识管理'], 'difficulty': '低', 'free': True},
    '豆包': {'cost': 0, 'learn': '1-2天', 'best': ['日常对话', '创意写作', '信息查询'], 'difficulty': '低', 'free': True},
    'Codeium': {'cost': 15, 'learn': '1-2周', 'best': ['代码补全', '多语言支持', 'IDE集成'], 'difficulty': '低', 'free': True},
    '文心快码': {'cost': 0, 'learn': '1-2周', 'best': ['代码生成', '百度生态', '中文注释'], 'difficulty': '低', 'free': True},
    '飞书多维表格': {'cost': 0, 'learn': '3-5天', 'best': ['数据管理', '项目管理', '协作表格'], 'difficulty': '低', 'free': True},
    '腾讯文档': {'cost': 0, 'learn': '1-2天', 'best': ['在线协作', '文档共享', '实时编辑'], 'difficulty': '低', 'free': True},
    '石墨文档': {'cost': 0, 'learn': '1-2天', 'best': ['在线协作', '表格处理', '幻灯片'], 'difficulty': '低', 'free': True},
    'Excel': {'cost': 0, 'learn': '1-2周', 'best': ['数据处理', '报表制作', '统计分析'], 'difficulty': '低', 'free': True},
    '问卷星': {'cost': 10, 'learn': '1-3天', 'best': ['问卷调查', '数据收集', '在线考试'], 'difficulty': '低', 'free': True},
    'XMind': {'cost': 10, 'learn': '1-3天', 'best': ['思维导图', '头脑风暴', '知识梳理'], 'difficulty': '低', 'free': True},
    'ProcessOn': {'cost': 10, 'learn': '1-3天', 'best': ['流程图', '组织架构', 'UML图'], 'difficulty': '低', 'free': True},
    'Coze': {'cost': 0, 'learn': '3-5天', 'best': ['AI Bot搭建', '自动化工作流', '智能客服'], 'difficulty': '低', 'free': True},
    'FastGPT': {'cost': 0, 'learn': '1-2周', 'best': ['知识库问答', 'AI应用搭建', '私有部署'], 'difficulty': '中', 'free': True},
    'WorkBuddy': {'cost': 0, 'learn': '1-2周', 'best': ['智能办公', '任务管理', '日程安排'], 'difficulty': '低', 'free': True},
}

DEPT_ADJUST = {
    '技术研发部': {'boost': ['GitHub Copilot', 'Cursor', '通义灵码', '文心快码', 'Codeium'], 'penalty': ['Canva', 'Midjourney', '剪映']},
    '产品设计部': {'boost': ['Figma', 'Midjourney', 'Canva', 'Stable Diffusion', 'Notion'], 'penalty': ['Tabnine']},
    '市场运营部': {'boost': ['ChatGPT', 'Canva', '剪映', 'Gamma', 'Tome', 'HubSpot', '神策数据'], 'penalty': ['GitHub Copilot', 'Cursor']},
    '销售部': {'boost': ['Salesforce', 'HubSpot', '飞书', '钉钉', 'ChatGPT'], 'penalty': ['Midjourney', 'Stable Diffusion']},
    '人力资源部': {'boost': ['企业微信', '问卷星', 'ChatGPT', 'Excel'], 'penalty': ['Tableau', 'Power BI']},
    '财务部': {'boost': ['Excel', 'Python', 'Tableau', 'Power BI', 'SQL'], 'penalty': ['Midjourney', '剪映', 'Canva']},
    '行政部': {'boost': ['飞书', '钉钉', '企业微信', '腾讯文档', 'Excel'], 'penalty': ['GitHub Copilot', 'Salesforce']},
    '客户服务部': {'boost': ['飞书', '钉钉', 'ChatGPT', 'Coze'], 'penalty': ['Midjourney', 'Tableau']},
    '数据中心': {'boost': ['Python', 'SQL', 'Tableau', '神策数据', 'Power BI', 'GrowingIO'], 'penalty': ['剪映', 'Canva']},
    '战略规划部': {'boost': ['Tableau', 'Power BI', 'Python', 'SQL', 'ChatGPT', 'Notion'], 'penalty': ['剪映', 'Canva']},
}

BIZ_ADJUST = {
    'ToB企业服务': {'boost': ['HubSpot', 'Salesforce', '飞书', '钉钉'], 'penalty': []},
    'ToC消费互联网': {'boost': ['神策数据', 'GrowingIO', 'Mixpanel', '剪映'], 'penalty': ['Salesforce']},
    '金融科技': {'boost': ['Python', 'SQL', 'Tableau', 'Power BI'], 'penalty': ['剪映', 'Midjourney']},
    '医疗健康': {'boost': ['Python', 'SQL'], 'penalty': []},
    '教育培训': {'boost': ['问卷星', 'Gamma', 'Tome'], 'penalty': []},
    '电商零售': {'boost': ['神策数据', 'GrowingIO', '剪映', 'Canva', 'Mixpanel'], 'penalty': ['Salesforce']},
    '文化娱乐': {'boost': ['剪映', 'Midjourney', 'Canva', 'CapCut', 'Runway'], 'penalty': ['Salesforce']},
    '智能制造': {'boost': ['Python', 'SQL'], 'penalty': ['剪映']},
    '新能源': {'boost': ['Python', 'SQL'], 'penalty': []},
    '人工智能': {'boost': ['Python', 'GitHub Copilot', 'Cursor', 'ChatGPT'], 'penalty': []},
}

SKILL_DB = {
    '前端开发工程师': [
        {'name': 'AI辅助编程', 'level': '进阶', 'duration': '2-3周', 'desc': '使用Copilot、Cursor等AI工具辅助前端开发', 'keys': ['代码生成', '智能补全', 'Bug修复']},
        {'name': '提示词工程', 'level': '入门', 'duration': '1-2周', 'desc': '编写有效的AI提示词，提升开发效率', 'keys': ['问题描述', '代码改写', '调试提示']},
        {'name': 'AI设计协作', 'level': '基础', 'duration': '1-2周', 'desc': '与AI生成的设计稿协作，理解设计意图', 'keys': ['设计理解', '设计还原', '像素级开发']},
    ],
    '后端开发工程师': [
        {'name': 'AI辅助编程', 'level': '进阶', 'duration': '2-3周', 'desc': '使用AI工具辅助Java/Python/Go开发', 'keys': ['代码生成', '单元测试', '优化重构']},
        {'name': 'AI数据库设计', 'level': '进阶', 'duration': '1-2周', 'desc': '利用AI辅助数据库设计与优化', 'keys': ['SQL生成', '索引优化', '查询分析']},
        {'name': 'AI安全审计', 'level': '进阶', 'duration': '2-3周', 'desc': '使用AI工具进行代码安全审计', 'keys': ['漏洞检测', '安全建议', '合规检查']},
    ],
    '全栈工程师': [
        {'name': 'AI全栈开发', 'level': '熟练', 'duration': '3-4周', 'desc': 'AI辅助完成前后端全栈开发', 'keys': ['AI编程', '架构设计', '快速迭代']},
        {'name': 'AI项目管理', 'level': '进阶', 'duration': '2-3周', 'desc': '使用AI工具进行项目管理和协作', 'keys': ['任务分配', '进度追踪', '文档生成']},
    ],
    '产品经理': [
        {'name': 'AI需求分析', 'level': '进阶', 'duration': '1-2周', 'desc': '使用ChatGPT分析用户需求，生成PRD', 'keys': ['需求挖掘', '用户画像', '竞品分析']},
        {'name': 'AI数据决策', 'level': '进阶', 'duration': '2-3周', 'desc': '利用AI工具辅助产品决策', 'keys': ['数据解读', 'A/B分析', '增长策略']},
        {'name': 'AI原型设计', 'level': '基础', 'duration': '1-2周', 'desc': '使用Figma AI快速生成产品原型', 'keys': ['原型制作', '交互设计', '需求可视化']},
    ],
    'UI设计师': [
        {'name': 'AI创意生成', 'level': '熟练', 'duration': '3-4周', 'desc': '精通Midjourney/Stable Diffusion生成设计素材', 'keys': ['提示词编写', '风格控制', '批量生成']},
        {'name': 'AI设计工具', 'level': '熟练', 'duration': '2-3周', 'desc': '熟练使用Figma AI、Canva等AI设计工具', 'keys': ['AI辅助设计', '效率优化', '设计系统']},
        {'name': 'AI设计审核', 'level': '进阶', 'duration': '2-3周', 'desc': '审核和优化AI生成的设计内容', 'keys': ['质量评估', '风格统一', '合规检查']},
    ],
    '新媒体运营': [
        {'name': 'AI内容创作', 'level': '熟练', 'duration': '2-3周', 'desc': '使用ChatGPT批量生成多平台内容', 'keys': ['选题策划', '文案生成', '多平台适配']},
        {'name': 'AI短视频制作', 'level': '熟练', 'duration': '2-3周', 'desc': '使用剪映/CapCut高效制作短视频', 'keys': ['视频剪辑', '特效制作', '节奏把控']},
        {'name': 'AI数据分析', 'level': '进阶', 'duration': '2-3周', 'desc': '利用AI工具分析内容数据优化运营', 'keys': ['数据解读', '用户分析', '内容优化']},
        {'name': 'AI社媒管理', 'level': '基础', 'duration': '1-2周', 'desc': '利用AI工具管理多平台社媒账号', 'keys': ['排期管理', '互动分析', '舆情监控']},
    ],
    '数据分析师': [
        {'name': 'AI数据分析', 'level': '熟练', 'duration': '3-4周', 'desc': '使用Python/SQL结合AI进行数据挖掘', 'keys': ['数据处理', '特征工程', '可视化']},
        {'name': 'AI报表自动化', 'level': '进阶', 'duration': '2-3周', 'desc': '利用AI实现报表自动化生成', 'keys': ['仪表盘', '定时报告', '异常预警']},
        {'name': 'AI商业洞察', 'level': '熟练', 'duration': '3-4周', 'desc': 'AI辅助生成商业洞察和决策建议', 'keys': ['趋势分析', '归因分析', '策略建议']},
    ],
    '市场经理': [
        {'name': 'AI营销策略', 'level': '熟练', 'duration': '2-3周', 'desc': '使用AI制定数据驱动的营销策略', 'keys': ['市场分析', '用户洞察', '策略制定']},
        {'name': 'AI营销自动化', 'level': '进阶', 'duration': '3-4周', 'desc': '利用HubSpot实现营销自动化', 'keys': ['线索管理', '邮件营销', '漏斗分析']},
        {'name': 'AI内容营销', 'level': '熟练', 'duration': '2-3周', 'desc': '使用AI批量化创作高质量营销内容', 'keys': ['内容策划', '文案创作', '多平台分发']},
    ],
    '品牌经理': [
        {'name': 'AI品牌设计', 'level': '进阶', 'duration': '2-3周', 'desc': '使用Midjourney辅助品牌视觉设计', 'keys': ['品牌视觉', '创意设计', '风格定义']},
        {'name': 'AI舆情分析', 'level': '进阶', 'duration': '2-3周', 'desc': '利用AI进行品牌舆情监控和分析', 'keys': ['舆情监控', '竞品分析', '声誉管理']},
    ],
    '电商运营': [
        {'name': 'AI选品分析', 'level': '熟练', 'duration': '2-3周', 'desc': '使用AI辅助电商选品分析', 'keys': ['市场分析', '竞品调研', '趋势预测']},
        {'name': 'AI营销自动化', 'level': '进阶', 'duration': '2-3周', 'desc': '利用AI自动优化电商广告投放', 'keys': ['广告优化', 'ROI分析', '用户画像']},
        {'name': 'AI内容运营', 'level': '熟练', 'duration': '2-3周', 'desc': '使用AI批量化创作商品内容', 'keys': ['内容创作', '视频制作', '图文设计']},
    ],
    '广告投放专员': [
        {'name': 'AI投放优化', 'level': '熟练', 'duration': '3-4周', 'desc': '使用AI优化广告投放策略和出价', 'keys': ['智能出价', '人群定向', '素材优化']},
        {'name': 'AI数据分析', 'level': '进阶', 'duration': '2-3周', 'desc': '利用AI分析投放数据提供优化建议', 'keys': ['数据解读', '归因分析', 'ROI提升']},
    ],
    'HR专员': [
        {'name': 'AI招聘辅助', 'level': '基础', 'duration': '1-2周', 'desc': '使用AI辅助简历筛选和候选人评估', 'keys': ['简历分析', '匹配度评分', '面试准备']},
        {'name': 'AI人事管理', 'level': '基础', 'duration': '1-2周', 'desc': '利用AI提高人事管理效率', 'keys': ['员工档案', '流程自动化', '数据分析']},
    ],
    '财务分析师': [
        {'name': 'AI财务分析', 'level': '进阶', 'duration': '2-3周', 'desc': '使用AI进行财务报表分析和预测', 'keys': ['报表分析', '预算预测', '风险识别']},
        {'name': 'AI Excel高级应用', 'level': '熟练', 'duration': '2-3周', 'desc': '利用AI辅助Excel高级数据处理', 'keys': ['VBA自动化', '数据透视', '可视化']},
    ],
}

def get_skills(position_name):
    return SKILL_DB.get(position_name, [
        {'name': 'AI基础应用', 'level': '入门', 'duration': '1-2周', 'desc': '掌握通用AI工具的基础操作', 'keys': ['工具使用', '基础提问', '结果筛选']},
        {'name': '提示词工程', 'level': '基础', 'duration': '1-2周', 'desc': '编写有效的AI提示词', 'keys': ['问题描述', '任务分解', '结果优化']},
    ])

def calc_tool_level(tool_name, company_scale, business_type, department):
    db = TOOL_DB.get(tool_name, {'cost': 10, 'free': True})
    di = DEPT_ADJUST.get(department, {'boost': [], 'penalty': []})
    bi = BIZ_ADJUST.get(business_type.replace('全部', ''), {'boost': [], 'penalty': []})
    score = 50
    if tool_name in di['boost']: score += 30
    if tool_name in di['penalty']: score -= 25
    if tool_name in bi['boost']: score += 20
    if tool_name in bi['penalty']: score -= 20
    if company_scale == '大型':
        score += 5 if not db['free'] else -5
    elif company_scale == '小型':
        score += 15 if db['free'] else (-10 if db['cost'] > 15 else 5)
    if score >= 75: return '必备'
    if score >= 50: return '推荐'
    return '可选'

def generate_recommendations(search_results, company_scale, business_type, department):
    tools = search_results.get('tools', [])
    scale_factor = {'小型': 0.6, '中型': 1.0, '大型': 1.5}
    factor = scale_factor.get(company_scale, 1.0)
    recommendations = []
    for tool in tools[:10]:
        db = TOOL_DB.get(tool, {'cost': 10, 'learn': '2-4周', 'best': ['通用'], 'difficulty': '中', 'free': True})
        level = calc_tool_level(tool, company_scale, business_type, department)
        recommendations.append({'tool': tool, 'category': TOOL_CATEGORIES.get(tool, '其他'), 'level': level, 'cost': db['cost'], 'est_cost': int(db['cost'] * factor), 'free': db['free'], 'learn': db['learn'], 'difficulty': db['difficulty'], 'best_for': db['best']})
    recommendations.sort(key=lambda x: {'必备': 0, '推荐': 1, '可选': 2}[x['level']])
    return recommendations

def generate_plan(tools, company_scale):
    essential = [t for t in tools if t['level'] == '必备']
    recommended = [t for t in tools if t['level'] == '推荐']
    optional = [t for t in tools if t['level'] == '可选']
    small_plan = [
        {'phase': '阶段一：基础搭建（第1-2周）', 'tasks': ['安装配置必备工具', '建立基础工作流', '个人技能培训'], 'tools': [t['tool'] for t in essential[:3]]},
        {'phase': '阶段二：能力深化（第3-4周）', 'tasks': ['优化使用技巧', '建立个人模板库', '扩展到推荐工具'], 'tools': [t['tool'] for t in essential[:5] + recommended[:2]]},
        {'phase': '阶段三：全面应用（第5-8周）', 'tasks': ['整合可选工具', '制定最佳实践', '持续优化迭代'], 'tools': [t['tool'] for t in essential + recommended[:3] + optional[:1]]},
    ]
    mid_plan = [
        {'phase': '阶段一：基础搭建（第1-2周）', 'tasks': ['安装配置必备工具', '建立基础工作流', '团队基础培训'], 'tools': [t['tool'] for t in essential[:3]]},
        {'phase': '阶段二：能力深化（第3-4周）', 'tasks': ['优化提示词模板', '建立质量标准', '扩展工具应用', '团队技能建设'], 'tools': [t['tool'] for t in essential]},
        {'phase': '阶段三：全面应用（第5-8周）', 'tasks': ['整合推荐工具', '建立最佳实践', '持续优化迭代', '跨部门推广'], 'tools': [t['tool'] for t in essential + recommended[:4]]},
    ]
    large_plan = [
        {'phase': '阶段一：基础搭建（第1-2周）', 'tasks': ['制定企业级使用规范', '安装配置必备工具', '组建AI工具管理团队'], 'tools': [t['tool'] for t in essential[:4]]},
        {'phase': '阶段二：团队培训（第3-4周）', 'tasks': ['全员AI工具培训', '建立知识管理体系', '试点应用与反馈'], 'tools': [t['tool'] for t in essential]},
        {'phase': '阶段三：全面推广（第5-8周）', 'tasks': ['全团队推广', '效果评估与优化', '建立最佳实践库', '持续迭代升级'], 'tools': [t['tool'] for t in essential + recommended]},
    ]
    return {'小型': small_plan, '中型': mid_plan, '大型': large_plan}.get(company_scale, mid_plan)

def calc_cost(tools, company_scale):
    factor = {'小型': 0.6, '中型': 1.0, '大型': 1.5}.get(company_scale, 1.0)
    essential = [t for t in tools if t['level'] == '必备']
    recommended = [t for t in tools if t['level'] == '推荐']
    es = sum(t['cost'] for t in essential)
    rs = sum(t['cost'] for t in recommended)
    return {'essential_monthly': int(es * factor), 'recommended_monthly': int(rs * factor), 'total_monthly': int((es + rs) * factor), 'total_annual': int((es + rs) * factor * 12), 'breakdown': [*[{'tool': t['tool'], 'cost': int(t['cost'] * factor), 'level': '必备'} for t in essential], *[{'tool': t['tool'], 'cost': int(t['cost'] * factor), 'level': '推荐'} for t in recommended]]}

# ============================
#  TOOL CATEGORY MAP
# ============================
TOOL_CATEGORIES = {
    'ChatGPT': 'AI助手', 'Claude': 'AI助手', '文心一言': 'AI助手', '通义千问': 'AI助手', 'Kimi': 'AI助手',
    '豆包': 'AI助手', '讯飞星火': 'AI助手', '腾讯混元': 'AI助手',
    'WorkBuddy': 'AI助手', 'OpenClaw': 'AI助手', 'Coze': 'AI助手', 'Trae': 'AI助手', 'FastGPT': 'AI助手',
    'Notion AI': '写作工具', '秘塔写作猫': '写作工具', '火山写作': '写作工具', 'Jasper': '写作工具', 'Grammarly': '写作工具',
    'Canva': '设计工具', 'Figma': '设计工具', 'Midjourney': '设计工具', 'Stable Diffusion': '设计工具',
    'Adobe Firefly': '设计工具', 'DALL-E': '设计工具', '创客贴': '设计工具', '稿定设计': '设计工具', 'Remove.bg': '设计工具',
    '剪映': '视频工具', 'CapCut': '视频工具', 'HeyGen': '视频工具', '腾讯智影': '视频工具', 'Runway': '视频工具', 'Pika': '视频工具',
    'Gamma': '演示工具', 'Tome': '演示工具', 'MindShow': '演示工具', '博思白板': '演示工具',
    'Tableau': '数据分析', 'Power BI': '数据分析', 'Python': '数据分析', 'SQL': '数据分析',
    '神策数据': '数据分析', 'GrowingIO': '数据分析', 'Mixpanel': '数据分析',
    'GitHub Copilot': '开发工具', 'Cursor': '开发工具', 'Codeium': '开发工具', '通义灵码': '开发工具', '文心快码': '开发工具', 'Tabnine': '开发工具',
    '飞书': '协作工具', '飞书多维表格': '协作工具', '钉钉': '协作工具', '企业微信': '协作工具', 'Notion': '协作工具', '印象笔记': '协作工具',
    'XMind': '思维导图', 'ProcessOn': '思维导图',
    '影刀': 'RPA工具', 'UiPath': 'RPA工具', 'Automation Anywhere': 'RPA工具',
    'HubSpot': '营销工具', 'Salesforce': '营销工具', 'Marketo': '营销工具',
    'SAP': '财务工具', 'Oracle': '财务工具', '用友': '财务工具', '金蝶': '财务工具',
    '问卷星': '教育工具', '腾讯文档': '教育工具', '石墨文档': '教育工具',
}

CATEGORY_COLORS = {
    'AI助手': '#00d26a', '写作工具': '#a371f7', '设计工具': '#ec4899',
    '视频工具': '#ff922b', '演示工具': '#f59e0b', '数据分析': '#00d26a',
    '开发工具': '#4dabf7', '协作工具': '#22c55e', '思维导图': '#d2a8ff',
    'RPA工具': '#f97316', '营销工具': '#69db7c', '财务工具': '#ef4444',
    '教育工具': '#06b6d4', '其他': '#9ca3af'
}

# ============================
#  SIDEBAR
# ============================
with st.sidebar:
    st.markdown("""
    <div class="brand-header">
        <div class="logo-icon">🤖</div>
        <div>
            <div class="brand-text">SectorAI</div>
            <div class="brand-sub">AI岗位工具配置</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-title'>🎯 第一步：选择岗位</div>", unsafe_allow_html=True)
    
    industries = get_all_industries()
    industry = st.selectbox("行业", industries, key="industry")
    
    categories = get_categories_for_industry(industry)
    category = st.selectbox("职位类别", categories, key="category")
    
    positions = get_positions_for_category(industry, category)
    position = st.selectbox("具体岗位", positions, key="position")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔍 搜索AI工具", type="primary", use_container_width=True):
        st.session_state.search_clicked = True
    
    st.markdown("---")
    st.markdown("<div style='color:#5a6078;font-size:11px;'>v4.0 · 2026-05-14</div>", unsafe_allow_html=True)

# ============================
#  MAIN CONTENT
# ============================
if st.session_state.get('search_clicked', False):
    with st.spinner("正在搜索..."):
        template = get_position_data(industry, category, position)
        if template:
            ai_tools = template.get('ai_tools', [])
            skills = template.get('skills', [])
            salary = template.get('salary_range', '面议')
            company_scales = template.get('company_scales', [])
            business_types = template.get('business_types', [])
            depts = template.get('departments', [])
            
            st.session_state.search_results = {
                'industry': industry, 'category': category, 'position': position,
                'salary': salary, 'tools': ai_tools, 'skills': skills,
                'compatible_scales': company_scales,
                'compatible_business': business_types,
                'compatible_departments': depts
            }
            st.success(f"✅ 搜索完成！匹配 {len(ai_tools)} 个AI工具")
        else:
            st.error("❌ 暂无该职位数据")

def handle_analyze():
    recs = generate_recommendations(st.session_state.search_results, st.session_state.company_scale, st.session_state.business_type, st.session_state.department)
    plan = generate_plan(recs, st.session_state.company_scale)
    cost = calc_cost(recs, st.session_state.company_scale)
    skills = get_skills(st.session_state.search_results.get('position', ''))
    st.session_state.analysis_results = {
        'company_scale': st.session_state.company_scale,
        'business_type': st.session_state.business_type,
        'department': st.session_state.department,
        'position': st.session_state.search_results.get('position', ''),
        'category': st.session_state.search_results.get('category', ''),
        'industry': st.session_state.search_results.get('industry', ''),
        'recommendations': recs,
        'plan': plan,
        'cost': cost,
        'skills': skills,
    }

# ============================
#  DISPLAY RESULTS
# ============================
if st.session_state.search_results:
    r = st.session_state.search_results
    
    st.markdown(f"""
    <div class="section-title">
        📊 岗位概览
        <span class="badge-live">实时数据</span>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    metrics = [
        ("行业", r['industry'], "↑ 活跃", "up"),
        ("职位类别", r['category'], "", ""),
        ("岗位", r['position'], "", ""),
        ("薪资范围", r['salary'], "↑ 竞争力", "up"),
    ]
    for col, (label, value, change, change_type) in zip([c1, c2, c3, c4], metrics):
        with col:
            change_html = f'<div class="metric-change {change_type}">{change}</div>' if change else ''
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                {change_html}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown(f"""
    <div class="section-title">
        🛠️ 第四层：AI工具推荐
    </div>
    """, unsafe_allow_html=True)
    
    if r['tools']:
        tools_by_category = {}
        for tool in r['tools']:
            category = TOOL_CATEGORIES.get(tool, '其他')
            if category not in tools_by_category:
                tools_by_category[category] = []
            tools_by_category[category].append(tool)
        
        for category, tools in tools_by_category.items():
            with st.expander(f"📦 {category} ({len(tools)}个工具)"):
                tool_cols = st.columns(2)
                for i, tool in enumerate(tools):
                    with tool_cols[i % 2]:
                        st.markdown(f"""
                        <div class="tool-tag">
                            <span>{tool}</span>
                        </div>
                        """, unsafe_allow_html=True)
    else:
        st.info("暂无匹配的AI工具")
    
    st.markdown("---")
    
    if r['skills']:
        st.markdown(f"""
        <div class="section-title">
            🎯 核心技能要求
        </div>
        """, unsafe_allow_html=True)
        skill_cols = st.columns(4)
        for i, skill in enumerate(r['skills']):
            with skill_cols[i % 4]:
                st.markdown(f"""
                <div class="skill-tag">
                    {skill}
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown(f"""
    <div class="section-title">
        🏢 第二步：企业配置分析
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        company_scale = st.selectbox("企业规模", get_company_scales(), key="company_scale", index=1)
    with c2:
        business_type = st.selectbox("业务类型", ["全部"] + get_business_types(), key="business_type")
    with c3:
        department = st.selectbox("所属部门", ["全部"] + get_departments(), key="department")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.button("🚀 开始分析", type="primary", key="analyze_button", on_click=handle_analyze)
    
    st.markdown("---")
    
    if st.session_state.get('analysis_results'):
        ar = st.session_state.analysis_results
        st.markdown("---")
        st.markdown(f"""
        <div class="section-title">
            📈 第二步：企业配置分析结果
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="analysis-summary">
            <div class="analysis-item"><span class="analysis-label">岗位：</span><span class="analysis-value">{ar['industry']} → {ar['category']} → {ar['position']}</span></div>
            <div class="analysis-item"><span class="analysis-label">规模：</span><span class="analysis-value">{ar['company_scale']}</span></div>
            <div class="analysis-item"><span class="analysis-label">业务：</span><span class="analysis-value">{ar['business_type']}</span></div>
            <div class="analysis-item"><span class="analysis-label">部门：</span><span class="analysis-value">{ar['department']}</span></div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("<div class='section-title'>🛠️ 推荐工具</div>", unsafe_allow_html=True)
        
        recs = ar['recommendations']
        c1, c2, c3 = st.columns(3)
        for i, rec in enumerate(recs):
            with [c1, c2, c3][i % 3]:
                lvl_color = {'必备': '#7c3aed', '推荐': '#f59e0b', '可选': '#9ca3af'}.get(rec['level'], '#9ca3af')
                free_tag = '🆓 免费' if rec['free'] else f"¥{rec['est_cost']}/月"
                st.markdown(f"""
                <div class="metric-card" style="margin-bottom:12px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                        <strong style="font-size:15px;">{rec['tool']}</strong>
                        <span style="background:{lvl_color}20;color:{lvl_color};padding:2px 8px;border-radius:10px;font-size:11px;font-weight:600;">{rec['level']}</span>
                    </div>
                    <div style="font-size:12px;color:#9b96b0;margin-bottom:4px;">{free_tag} · {rec['learn']} · {rec['difficulty']}</div>
                    <div style="font-size:11px;color:#6b6680;">{', '.join(rec['best_for'])}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("<div class='section-title'>📋 工具实施路径</div>", unsafe_allow_html=True)
        
        for phase in ar['plan']:
            if phase['tools']:
                with st.expander(f"🔹 {phase['phase']}"):
                    st.markdown(f"**任务：**")
                    for t in phase['tasks']:
                        st.markdown(f"- {t}")
                    st.markdown(f"**涉及工具：**{', '.join(phase['tools'])}")
        
        st.markdown("---")
        
        st.markdown("<div class='section-title'>💰 成本估算</div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'<div class="metric-card"><div class="metric-label">必备工具月成本</div><div class="metric-value">¥{ar["cost"]["essential_monthly"]}</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-card"><div class="metric-label">推荐工具月成本</div><div class="metric-value">¥{ar["cost"]["recommended_monthly"]}</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="metric-card"><div class="metric-label">年度总成本</div><div class="metric-value">¥{ar["cost"]["total_annual"]}</div></div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("<div class='section-title'>🎓 需要掌握的技能</div>", unsafe_allow_html=True)
        
        for skill in ar['skills']:
            with st.expander(f"📘 {skill['name']}（{skill['level']} · {skill['duration']}）"):
                st.markdown(f"""
                <div style="margin-bottom:8px;">{skill['desc']}</div>
                <div><strong>关键能力：</strong>{', '.join(skill['keys'])}</div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔄 重新搜索", use_container_width=True):
            st.session_state.search_results = None
            st.session_state.search_clicked = False
            st.session_state.analysis_results = None
            st.session_state.analyze_clicked = False
            st.rerun()
    with c2:
        if st.button("💾 导出报告", use_container_width=True):
            st.success("报告导出功能开发中...")

else:
    st.markdown("""
    <div class="landing-hero">
        <div class="hero-icon">🤖</div>
        <div class="hero-title">SectorAI 岗位工具配置系统</div>
        <div class="hero-subtitle">
            采用四层数据结构，精准匹配岗位与AI工具<br>
            行业 → 职位类别 → 具体岗位 → AI工具推荐
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    total_industries = len(DB.get("industries", {}))
    total_categories = sum(len(ind["categories"]) for ind in DB.get("industries", {}).values())
    total_positions = sum(len(cat["positions"]) for ind in DB.get("industries", {}).values() for cat in ind.get("categories", {}).values())
    total_tools = sum(len(pos.get("ai_tools", [])) for ind in DB.get("industries", {}).values() for cat in ind.get("categories", {}).values() for pos in cat.get("positions", {}).values())
    
    c1, c2, c3, c4 = st.columns(4)
    stats = [
        ("行业覆盖", total_industries, "↑ 持续更新", "up"),
        ("职位类别", total_categories, "", ""),
        ("岗位数量", total_positions, "↑ 增长中", "up"),
        ("AI工具条目", total_tools, "", ""),
    ]
    for col, (label, value, change, change_type) in zip([c1, c2, c3, c4], stats):
        with col:
            change_html = f'<div class="metric-change {change_type}">{change}</div>' if change else ''
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                {change_html}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("<div class='section-title'>🚀 快速开始</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="step-guide">
        <div style="display:flex;gap:16px;align-items:center;justify-content:center;flex-wrap:wrap;">
            <div class="step-item">
                <div class="step-circle">1</div>
                <div class="step-label">选择行业</div>
            </div>
            <div style="color:#2a3042;font-size:24px;">→</div>
            <div class="step-item">
                <div class="step-circle">2</div>
                <div class="step-label">选择类别</div>
            </div>
            <div style="color:#2a3042;font-size:24px;">→</div>
            <div class="step-item">
                <div class="step-circle">3</div>
                <div class="step-label">选择岗位</div>
            </div>
            <div style="color:#2a3042;font-size:24px;">→</div>
            <div class="step-item">
                <div class="step-circle active">4</div>
                <div class="step-label active">AI工具</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("<div class='footer-text'>🤖 SectorAI · AI岗位工具配置分析系统</div>", unsafe_allow_html=True)
