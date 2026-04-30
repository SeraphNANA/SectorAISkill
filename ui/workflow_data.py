# AI工具组合架构 - 不是简单使用步骤，而是最优解路径
AI_WORKFLOWS = {
    "Midjourney": {
        "workflow_name": "AI视觉创意全链路",
        "description": "利用大模型优化Prompt，结合工作流自动化，实现从需求到成品的智能化生产",
        "optimal_path": [
            {
                "step": 1,
                "phase": "需求分析",
                "tool": "ChatGPT/Claude",
                "action": "自然语言沟通，拆解视觉需求，提取核心关键词",
                "output": "结构化需求文档"
            },
            {
                "step": 2,
                "phase": "拆解竞品视觉结构",
                "tool": "Bolt/V0",
                "action": "AI自动拆解竞品视觉结构，提取设计模式、色彩体系、构图规律",
                "output": "竞品视觉分析报告"
            },
            {
                "step": 3,
                "phase": "Prompt优化（AI辅助）",
                "tool": "ChatGPT/Claude + Prompt优化器",
                "action": "基于角色-技能-流程-限制结构，AI辅助生成专业Prompt",
                "output": "优化后的Midjourney Prompt"
            },
            {
                "step": 4,
                "phase": "Midjourney生成初稿",
                "tool": "Midjourney",
                "action": "输入优化后的Prompt，批量生成概念图，利用--sref保持风格一致",
                "output": "10-20张初稿候选"
            },
            {
                "step": 5,
                "phase": "ComfyUI-Copilot一键创建工作流",
                "tool": "ComfyUI-Copilot/AutoGPT",
                "action": "通过自然语言描述，AI自动构建工作流架构，一键串联各节点",
                "output": "自动化工作流配置"
            },
            {
                "step": 6,
                "phase": "批量生成变体",
                "tool": "ComfyUI + ControlNet",
                "action": "基于初稿批量生成变体，保持构图一致性，自动调整风格参数",
                "output": "50+风格变体"
            },
            {
                "step": 7,
                "phase": "人工筛选",
                "tool": "设计师人工审核",
                "action": "设计师基于专业判断，从AI生成的候选中筛选最符合需求的方案",
                "output": "3-5张精选方案"
            },
            {
                "step": 8,
                "phase": "输出方案",
                "tool": "Photoshop AI/Firefly",
                "action": "对选定方案进行最终优化，调整细节，输出符合交付标准的成品",
                "output": "最终交付方案"
            }
        ],
        "key_insight": "核心变革：不再需要手动搭建ComfyUI节点，而是通过自然语言让ComfyUI-Copilot自动构建工作流架构，设计师只需专注创意决策", 
        "prompt_template": {
            "structure": "角色-技能-处理流程-输出限制-参考资料-样式",
            "example": """
【角色】你是一位资深视觉设计师，擅长品牌视觉系统构建
【技能】精通色彩理论、构图法则、品牌调性把控
【处理流程】
1. 分析品牌定位和目标受众
2. 提取核心视觉关键词
3. 构建视觉情绪板
4. 生成多版本概念图
【输出限制】
- 风格：现代简约，科技感
- 色彩：主色调#1a1a2e，辅色#667eea
- 构图：中心对称，留白30%
【参考资料】
- Apple品牌视觉规范
- Material Design设计系统
【样式】
--ar 16:9 --s 750 --c 15 --style raw
            """
        }
    },
    
    "Stable Diffusion": {
        "workflow_name": "本地化AI设计生产管线",
        "description": "利用开源生态，构建私有化、可定制的设计生产流程",
        "optimal_path": [
            {
                "step": 1,
                "phase": "模型选型",
                "tool": "Civitai/LiblibAI",
                "action": "根据项目需求选择基础模型+LoRA组合",
                "output": "模型配置方案"
            },
            {
                "step": 2,
                "phase": "Prompt构建",
                "tool": "Prompt助手/Tag反推",
                "action": "构建正向+负向Prompt，设置权重",
                "output": "优化Prompt"
            },
            {
                "step": 3,
                "phase": "ControlNet控制",
                "tool": "ControlNet + OpenPose",
                "action": "姿势/结构/深度控制，确保输出可控",
                "output": "控制参数配置"
            },
            {
                "step": 4,
                "phase": "批量生成",
                "tool": "ComfyUI/SD WebUI",
                "action": "设置采样器、步数、CFG，批量产出",
                "output": "批量候选图"
            },
            {
                "step": 5,
                "phase": "后处理优化",
                "tool": "ADetailer/Upscaler",
                "action": "面部修复、细节增强、超分辨率",
                "output": "高清成品"
            }
        ],
        "key_insight": "SD的核心优势在于可控性和私有化部署，适合对数据安全要求高的企业",
        "prompt_template": {
            "structure": "基础Prompt + LoRA触发词 + ControlNet参数 + 采样设置",
            "example": """
正向Prompt:
masterpiece, best quality, (photorealistic:1.4), 
1girl, solo, beautiful detailed eyes, 
<lora:add_detail:0.8>, <lora:filmgirl:0.6>

负向Prompt:
(worst quality:1.4), (low quality:1.4), 
(normal quality:1.4), lowres, bad anatomy

ControlNet:
- Module: openpose_full
- Model: control_v11p_sd15_openpose
- Weight: 1.0

采样设置:
- Sampler: DPM++ 2M Karras
- Steps: 30
- CFG: 7.0
            """
        }
    },
    
    "Runway": {
        "workflow_name": "AI视频智能生产链",
        "description": "从脚本到成片的全流程AI化，实现视频内容的快速迭代",
        "optimal_path": [
            {
                "step": 1,
                "phase": "脚本生成",
                "tool": "ChatGPT/Claude",
                "action": "生成视频脚本和分镜描述",
                "output": "视频脚本+分镜表"
            },
            {
                "step": 2,
                "phase": "素材准备",
                "tool": "Midjourney/SD",
                "action": "生成关键帧和参考图",
                "output": "视觉素材库"
            },
            {
                "step": 3,
                "phase": "视频生成",
                "tool": "Runway Gen-2",
                "action": "图生视频/文生视频，设置运动参数",
                "output": "原始视频片段"
            },
            {
                "step": 4,
                "phase": "视频编辑",
                "tool": "Runway视频编辑",
                "action": "剪辑、转场、特效添加",
                "output": "剪辑版视频"
            },
            {
                "step": 5,
                "phase": "后期增强",
                "tool": "Topaz Video AI",
                "action": "超分辨率、帧率提升、稳定化",
                "output": "最终成片"
            }
        ],
        "key_insight": "AI视频的核心是'图生视频'而非'文生视频'，先用AI生成高质量图片再转视频效果更佳",
        "prompt_template": {
            "structure": "画面描述 + 运动指令 + 风格参数",
            "example": """
画面描述:
A cinematic shot of a futuristic city at sunset, 
flying cars, neon lights reflecting on wet streets

运动指令:
Camera slowly panning right, subtle zoom in, 
vehicles moving smoothly

风格参数:
Style: Cinematic
Motion: 5/10
Camera: Pan Right
Duration: 4s
            """
        }
    },
    
    "Figma AI": {
        "workflow_name": "AI驱动设计协作流程",
        "description": "利用AI辅助设计决策，提升团队协作效率",
        "optimal_path": [
            {
                "step": 1,
                "phase": "需求分析",
                "tool": "ChatGPT + FigJam AI",
                "action": "AI辅助梳理需求，生成用户旅程图",
                "output": "需求文档+用户旅程"
            },
            {
                "step": 2,
                "phase": "设计生成",
                "tool": "Figma AI/Magician",
                "action": "AI生成设计稿、图标、图片",
                "output": "设计初稿"
            },
            {
                "step": 3,
                "phase": "组件优化",
                "tool": "Figma Auto Layout + AI",
                "action": "自动布局优化，响应式适配",
                "output": "组件库"
            },
            {
                "step": 4,
                "phase": "设计检查",
                "tool": "Figma AI/插件",
                "action": "一致性检查、可访问性检测",
                "output": "优化建议"
            },
            {
                "step": 5,
                "phase": "交付开发",
                "tool": "Figma Dev Mode",
                "action": "自动生成CSS/代码，标注切图",
                "output": "开发交付物"
            }
        ],
        "key_insight": "Figma AI的价值在于'设计辅助'而非'替代设计'，重点是提升协作和交付效率",
        "prompt_template": {
            "structure": "设计目标 + 约束条件 + 参考风格",
            "example": """
设计目标:
为SaaS产品创建仪表盘界面，展示数据分析结果

约束条件:
- 支持暗黑/明亮模式切换
- 适配桌面端和移动端
- 符合WCAG 2.1 AA标准

参考风格:
- Material Design 3
- Apple Design Resources
- 简洁现代，数据可视化优先
            """
        }
    },
    
    "Lovart/星流": {
        "workflow_name": "一句话生图智能工作流",
        "description": "极简操作，最大化AI理解能力，实现自然语言到视觉的直接转换",
        "optimal_path": [
            {
                "step": 1,
                "phase": "意图表达",
                "tool": "自然语言",
                "action": "用日常语言描述想要的画面",
                "output": "原始需求描述"
            },
            {
                "step": 2,
                "phase": "Prompt精炼",
                "tool": "AI Prompt优化器",
                "action": "AI自动优化为结构化Prompt",
                "output": "优化Prompt"
            },
            {
                "step": 3,
                "phase": "一键生成",
                "tool": "Lovart/星流",
                "action": "输入精炼后的Prompt，选择风格",
                "output": "4张候选图"
            },
            {
                "step": 4,
                "phase": "迭代优化",
                "tool": "自然语言反馈",
                "action": "用自然语言描述修改意见",
                "output": "优化版本"
            }
        ],
        "key_insight": "这类工具的核心是'自然语言理解'，Prompt工程比传统方式更简单，重点是清晰表达意图",
        "prompt_template": {
            "structure": "主体-场景-风格-质量-特殊效果",
            "example": """
主体：一只橘猫
场景：坐在窗台上，窗外是雨夜城市
风格：吉卜力动画风格，温暖治愈
质量：高清，细节丰富，毛发清晰
特殊效果：柔和的光线，雨滴在玻璃上

完整Prompt:
A cute orange cat sitting on a windowsill, 
rainy night city outside the window, 
Studio Ghibli style, warm and healing atmosphere, 
high quality, detailed fur, soft lighting, 
raindrops on the glass
            """
        }
    },
    
    "ChatGPT/Claude": {
        "workflow_name": "AI智能助手工作流",
        "description": "作为所有AI工具的中枢大脑，负责需求理解、Prompt优化、结果评估",
        "optimal_path": [
            {
                "step": 1,
                "phase": "需求接收",
                "tool": "自然语言",
                "action": "接收用户的自然语言需求",
                "output": "原始需求"
            },
            {
                "step": 2,
                "phase": "需求结构化",
                "tool": "ChatGPT/Claude",
                "action": "分析需求，提取关键要素，构建任务框架",
                "output": "结构化任务书"
            },
            {
                "step": 3,
                "phase": "工具选型",
                "tool": "AI决策系统",
                "action": "根据任务选择最优AI工具组合",
                "output": "工具配置方案"
            },
            {
                "step": 4,
                "phase": "Prompt生成",
                "tool": "AI Prompt工程师",
                "action": "为每个工具生成专业Prompt",
                "output": "工具专用Prompt"
            },
            {
                "step": 5,
                "phase": "结果评估",
                "tool": "AI质量评估",
                "action": "评估AI输出质量，提出优化建议",
                "output": "质量报告+优化建议"
            }
        ],
        "key_insight": "大模型是所有AI工具的'指挥官'，负责理解意图、分配任务、评估结果",
        "prompt_template": {
            "structure": "角色设定-任务描述-输出格式-质量要求",
            "example": """
角色设定:
你是一位资深AI工具专家，擅长根据需求选择最优工具组合

任务描述:
我需要为一个新品牌创建完整的视觉识别系统，包括：
1. 品牌Logo设计
2. 色彩系统定义
3. 应用场景展示

输出格式:
1. 工具推荐清单（含理由）
2. 每个工具的Prompt模板
3. 工作流执行顺序
4. 质量检查清单

质量要求:
- 品牌调性：科技、年轻、活力
- 目标受众：Z世代消费者
- 应用场景：App、网站、社交媒体
            """
        }
    }
}

# 技能矩阵 - 按岗位层级和技能维度
SKILL_MATRIX = {
    "设计总监": {
        "AI战略能力": {
            "工具选型": {"level": "专家", "priority": "核心"},
            "成本评估": {"level": "专家", "priority": "核心"},
            "团队规划": {"level": "专家", "priority": "核心"},
            "技术趋势判断": {"level": "高级", "priority": "重要"}
        },
        "Prompt工程": {
            "结构化Prompt设计": {"level": "专家", "priority": "核心"},
            "多工具Prompt适配": {"level": "专家", "priority": "核心"},
            "Prompt优化迭代": {"level": "高级", "priority": "重要"},
            "Prompt库建设": {"level": "高级", "priority": "重要"}
        },
        "工作流设计": {
            "工具串联架构": {"level": "专家", "priority": "核心"},
            "自动化流程设计": {"level": "高级", "priority": "核心"},
            "质量控制节点": {"level": "高级", "priority": "重要"},
            "效率优化": {"level": "高级", "priority": "重要"}
        },
        "AI工具应用": {
            "Midjourney高级应用": {"level": "专家", "priority": "核心"},
            "Stable Diffusion定制": {"level": "高级", "priority": "核心"},
            "ComfyUI工作流": {"level": "高级", "priority": "重要"},
            "Runway视频生成": {"level": "熟练", "priority": "重要"}
        },
        "团队管理": {
            "AI技能培训": {"level": "专家", "priority": "核心"},
            "工作分配": {"level": "专家", "priority": "核心"},
            "质量把控": {"level": "专家", "priority": "核心"},
            "知识沉淀": {"level": "高级", "priority": "重要"}
        }
    },
    
    "设计主管": {
        "AI战略能力": {
            "工具选型": {"level": "熟练", "priority": "重要"},
            "成本评估": {"level": "熟练", "priority": "重要"},
            "团队规划": {"level": "熟练", "priority": "重要"},
            "技术趋势判断": {"level": "进阶", "priority": "一般"}
        },
        "Prompt工程": {
            "结构化Prompt设计": {"level": "熟练", "priority": "核心"},
            "多工具Prompt适配": {"level": "熟练", "priority": "核心"},
            "Prompt优化迭代": {"level": "熟练", "priority": "重要"},
            "Prompt库建设": {"level": "进阶", "priority": "一般"}
        },
        "工作流设计": {
            "工具串联架构": {"level": "熟练", "priority": "核心"},
            "自动化流程设计": {"level": "熟练", "priority": "核心"},
            "质量控制节点": {"level": "熟练", "priority": "重要"},
            "效率优化": {"level": "进阶", "priority": "重要"}
        },
        "AI工具应用": {
            "Midjourney高级应用": {"level": "熟练", "priority": "核心"},
            "Stable Diffusion定制": {"level": "熟练", "priority": "核心"},
            "ComfyUI工作流": {"level": "进阶", "priority": "重要"},
            "Runway视频生成": {"level": "熟练", "priority": "重要"}
        },
        "团队管理": {
            "AI技能培训": {"level": "熟练", "priority": "核心"},
            "工作分配": {"level": "熟练", "priority": "核心"},
            "质量把控": {"level": "熟练", "priority": "核心"},
            "知识沉淀": {"level": "进阶", "priority": "一般"}
        }
    },
    
    "设计专员": {
        "AI战略能力": {
            "工具选型": {"level": "入门", "priority": "一般"},
            "成本评估": {"level": "入门", "priority": "一般"},
            "团队规划": {"level": "入门", "priority": "一般"},
            "技术趋势判断": {"level": "入门", "priority": "一般"}
        },
        "Prompt工程": {
            "结构化Prompt设计": {"level": "进阶", "priority": "核心"},
            "多工具Prompt适配": {"level": "进阶", "priority": "重要"},
            "Prompt优化迭代": {"level": "进阶", "priority": "重要"},
            "Prompt库建设": {"level": "入门", "priority": "一般"}
        },
        "工作流设计": {
            "工具串联架构": {"level": "进阶", "priority": "重要"},
            "自动化流程设计": {"level": "入门", "priority": "一般"},
            "质量控制节点": {"level": "进阶", "priority": "重要"},
            "效率优化": {"level": "入门", "priority": "一般"}
        },
        "AI工具应用": {
            "Midjourney高级应用": {"level": "进阶", "priority": "核心"},
            "Stable Diffusion定制": {"level": "进阶", "priority": "重要"},
            "ComfyUI工作流": {"level": "入门", "priority": "一般"},
            "Runway视频生成": {"level": "进阶", "priority": "重要"}
        },
        "团队管理": {
            "AI技能培训": {"level": "入门", "priority": "一般"},
            "工作分配": {"level": "入门", "priority": "一般"},
            "质量把控": {"level": "进阶", "priority": "重要"},
            "知识沉淀": {"level": "入门", "priority": "一般"}
        }
    }
}

# Prompt工程模板库
PROMPT_TEMPLATES = {
    "通用结构": {
        "name": "角色-技能-流程-限制-参考-样式",
        "template": """
【角色】{role}
【技能】{skills}
【处理流程】
{workflow}
【输出限制】
{constraints}
【参考资料】
{references}
【样式】
{style}
        """,
        "example": {
            "role": "你是一位资深视觉设计师，擅长品牌视觉系统构建",
            "skills": "精通色彩理论、构图法则、品牌调性把控",
            "workflow": "1. 分析品牌定位\n2. 提取视觉关键词\n3. 构建情绪板\n4. 生成多版本概念图",
            "constraints": "- 风格：现代简约\n- 色彩：主色#1a1a2e\n- 构图：中心对称",
            "references": "Apple品牌视觉规范、Material Design",
            "style": "--ar 16:9 --s 750 --c 15"
        }
    },
    
    "Midjourney专用": {
        "name": "Midjourney专业Prompt结构",
        "template": """
{subject}, {environment}, {lighting}, {style}, {quality}, {parameters}
        """,
        "example": {
            "subject": "a futuristic cityscape with flying vehicles",
            "environment": "neon-lit streets, rain-slicked surfaces",
            "lighting": "volumetric lighting, cinematic shadows",
            "style": "cyberpunk aesthetic, Blade Runner inspired",
            "quality": "hyper detailed, 8k, masterpiece",
            "parameters": "--ar 16:9 --s 750 --c 15 --style raw"
        }
    },
    
    "Stable Diffusion专用": {
        "name": "SD结构化Prompt",
        "template": """
正向: {positive_prompt}
负向: {negative_prompt}
LoRA: {lora_config}
ControlNet: {controlnet_config}
采样: {sampling_config}
        """,
        "example": {
            "positive_prompt": "masterpiece, best quality, 1girl, solo, detailed eyes",
            "negative_prompt": "worst quality, low quality, bad anatomy",
            "lora_config": "<lora:add_detail:0.8>",
            "controlnet_config": "openpose_full, weight:1.0",
            "sampling_config": "DPM++ 2M Karras, Steps:30, CFG:7.0"
        }
    },
    
    "视频生成专用": {
        "name": "AI视频Prompt结构",
        "template": """
画面: {visual_description}
运动: {motion_description}
相机: {camera_movement}
风格: {visual_style}
时长: {duration}
        """,
        "example": {
            "visual_description": "一个宁静的日式花园，樱花盛开",
            "motion_description": "花瓣轻轻飘落，微风吹拂",
            "camera_movement": "缓慢向右平移，轻微推进",
            "visual_style": "电影感，柔和对焦，黄金时段光线",
            "duration": "4秒"
        }
    }
}
