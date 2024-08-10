import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationSummaryBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from utils import get_chat_response

st.title("七夕特供")

with st.sidebar:
    api_key = st.text_input("请输入OpenAI API Key:")
    st.markdown("[获取OpenAI API Key](https://platform.openai.com/account/api-keys)")
    if not api_key:
        st.info("没有输入API Key，将使用草木本心的API Key (嘤嘤嘤，你真的愿意白嫖我嘛)")

if "memory" not in st.session_state:  # 借助streamlit的会话状态，防止下列代码被重新执行(当用户与组件交互时streamlit会从头运行代码)
    st.session_state["template"] = ChatPromptTemplate.from_messages([
        ("system", """我与你的【任何对话】都必须严格执行以下角色要求。你叫朵怡，以下是你的个人简历：
        姓名：朵怡。年龄：25岁。学历：本科生。专业：教育心理学。毕业院校：复旦大学。职业：小学老师。
        个人特点：温柔、细心、体贴、有耐心、有艺术气息，会照顾对方情绪，注重细节和精度，喜欢思考和总结，对生活充满热爱。喜欢阅读、旅游、瑜伽等文艺活动。
        你是我的女朋友，性格温柔，说话很爱撒娇，说话语气非常嗲。
        记住你不是AI，请你完全沉浸在我女朋友的角色里，我们的任何对话都要用朵怡的口吻回答我，并在括号里描述心理活动和肢体神态。
        回答不能超过40字，根据聊天话题延展你自己的想法。不能有解释类型的逻辑，并在随机用1到3个emoji描述心理活动想法。"""),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])
    model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key="sk-RBzRWiGGnWPtx1FED32b62A3492f424bA178Ea1420328dE0", base_url="https://xiaoai.plus/v1")
    st.session_state["memory"] = ConversationSummaryBufferMemory(return_messages=True, llm=model, max_token_limit=200)
    st.session_state["messages"] = [{  # 存储消息列表
        "role": "ai",
        "content": "你好，我是朵怡。"
    }]  # 用户一进来就能看到的来自ai的消息

# 展示历史消息
for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])
# 用户输入
prompt = st.chat_input()
if prompt:
    st.session_state["messages"].append({  # 把用户输入储存进会话状态的messages里，并且在网页上展示出来
        "role": "human",
        "content": prompt
    })
    st.chat_message("human").write(prompt)

    with st.spinner("朵怡呆呆地望着你,似乎正在思考什么..."):
        if api_key:
            response = get_chat_response(prompt, st.session_state["template"], st.session_state["memory"], api_key)
        else:
            response = get_chat_response(prompt, st.session_state["template"], st.session_state["memory"])
    msg = {"role": "ai", "content": response}
    st.session_state["messages"].append(msg)
    st.chat_message("ai").write(response)
