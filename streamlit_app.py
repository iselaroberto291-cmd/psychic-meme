import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# --- 1. 页面配置 ---
st.set_page_config(page_title="影视硬盘助手", page_icon="🎬", layout="centered")

# 注入 CSS 尝试防止翻译插件干扰
st.markdown('<div class="notranslate">', unsafe_allow_html=True)

st.title("🎬 硬盘影片信息快速识别工具")
st.markdown("上传一张剧照，我帮你找回硬盘里的记忆。")

# --- 2. 侧边栏配置 ---
with st.sidebar:
    st.header("⚙️ 设置")
    # 使用 session_state 保持 API Key 状态
    api_key = st.text_input("请输入 Gemini API Key", type="password", key="api_key_input")
    if api_key:
        genai.configure(api_key=api_key)
    
    st.divider()
    st.info("💡 提示：本工具使用 Gemini 1.5 Flash 模型，识别速度快且支持多模态理解。")
    st.caption("没有 Key？请前往 [Google AI Studio](https://aistudio.google.com/) 申请。")

# --- 3. 核心功能 ---
# 增加 key 确保上传组件状态稳定
uploaded_file = st.file_uploader("选择剧照 (JPG/PNG/WebP)...", type=["jpg", "jpeg", "png", "webp"], key="movie_uploader")

if uploaded_file is not None:
    try:
        # 打开图片
        image = Image.open(uploaded_file)
        
        # 使用列布局美化界面
        col1, col2 = st.columns([1, 1])
        with col1:
            st.image(image, caption='已上传的剧照', use_container_width=True)
        
        with col2:
            st.write("🔍 **识别准备就绪**")
            st.write("点击下方按钮开始分析。")
            identify_btn = st.button("🚀 开始识别", key="start_ai_btn")

        # 设定 AI 的角色和任务
        prompt = """
        你是一个专业的影视库助手。请根据这张图片识别以下内容：
        1. 识别影片内容：确认该剧照属于哪部电影或电视剧（包括上映年份）。
        2. 角色与演员：列出图片中出现的关键角色名称及其对应的演员姓名（格式：角色名 - 演员名）。
        3. 视频剧情简介：总结该影片的剧情大纲（300字以内）。
        
        要求：请用中文回复，使用 Markdown 格式，让排版美观（例如使用加粗、列表）。
        """

        if identify_btn:
            if not api_key:
                st.warning("⚠️ 请先在左侧侧边栏输入 API Key！")
            else:
                with st.spinner('AI 正在翻阅影视库，请稍候...'):
                    # 运行 Gemini 1.5 Flash 模型
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # 增加流式传输或直接获取结果
                    response = model.generate_content([prompt, image])
                    
                    if response.text:
                        st.success("✅ 识别成功！")
                        st.divider()
                        # 结果展示区
                        st.markdown(response.text)
                    else:
                        st.error("❌ AI 未能返回有效结果，可能是由于内容安全过滤。")
                        
    except Exception as e:
        # 捕获具体的错误类型
        error_msg = str(e)
        if "API_KEY_INVALID" in error_msg:
            st.error("❌ API Key 无效，请检查输入是否正确。")
        elif "quota" in error_msg.lower():
            st.error("❌ API 配额已耗尽，请稍后再试或更换 Key。")
        else:
            st.error(f"❌ 运行出错：{error_msg}")

# --- 4. 底部提示 ---
st.divider()
st.caption("建议：使用包含主角面部或经典场景的清晰剧照以获得最佳识别效果。")
st.markdown('</div>', unsafe_allow_html=True) # 结束屏蔽翻译区域
