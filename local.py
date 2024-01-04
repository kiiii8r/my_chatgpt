import json
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import (SystemMessage, HumanMessage, AIMessage)

def main():
    # JSONファイルからAPIキーを読み込む
    with open('/Users/kii/work/python_study/chat_gpt/ai_chat/config.json') as config_file:
        config = json.load(config_file)
        
    # ページ設定
    init_page()

    # モデルの選択
    llm = select_model()
    
    # プラグインの選択
    plugin = select_contents(llm)
    
    if plugin == "なし":
        # メッセージの初期化
        init_messages()
    
        # ユーザーの入力を監視
        if user_input := st.chat_input("聞きたいことを入力してね！"):
            st.session_state.messages.append(HumanMessage(content=user_input))
            with st.spinner("ChatGPT が考えています ..."):
                response = llm(st.session_state.messages)
            st.session_state.messages.append(AIMessage(content=response.content))

        
        # チャット履歴の表示
        messages = st.session_state.get('messages', [])
        for message in messages:
            if isinstance(message, AIMessage):
                with st.chat_message('assistant'):
                    st.markdown(message.content)
            elif isinstance(message, HumanMessage):
                with st.chat_message('user'):
                    st.markdown(message.content)
            else:  # isinstance(message, SystemMessage):
                st.write(f"System message: {message.content}")
            
        
def init_page():
    st.set_page_config(
        page_title="My ChatGPT",
        page_icon="⚙️"
    )
    st.header("My ChatGPT")
    st.sidebar.title("ChatGPT")
        
        
def init_messages():
    clear_button = st.sidebar.button("Clear chat history", key="clear")
    if clear_button or "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="何かお役に立てることはありますか？")
        ]
    st.session_state.cost = []
        
        
def select_model():
    # サイドバーにモデル選択のラジオボタンを追加
    model = st.sidebar.radio("モデルを選択", ["GPT-3.5", "GPT-4"])
    if model == "GPT-3.5":
        model_name = "gpt-3.5-turbo-0613"
    else:
        model_name = "gpt-4"
        
    # サイドバーにスライダーを追加、temperatureの値を選択可能にする
    # 初期値は0.0、最小値は0.0、最大値は2.0、ステップは0.1
    temperature = st.sidebar.slider("サンプリング温度", 0.0, 2.0, 0.0, 0.1)
    
    st.sidebar.markdown("## Costs")
    st.sidebar.markdown("**Total cost**")
    # st.sidebar.markdown(cb.total_cost)

    return ChatOpenAI(api_key=config['OPENAI_API_KEY'], temperature=temperature, model_name=model_name)        


def select_contents(llm):
    # サイドバーにモデル選択のラジオボタンを追加
    plugin = st.sidebar.selectbox("プラグイン", ["なし", "WEBサイト要約", "Youtube動画要約", "PDF質問"])
    if plugin == "WEBサイト要約":
        plugin.web_summarize(llm)
    elif plugin == "Youtube動画要約":
        plugin.youtube_summarize(llm)
    elif plugin == "PDF質問":
        plugin.pdf_question(llm)
    return plugin
    
    

if __name__ == '__main__':
    main()