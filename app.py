import streamlit as st
import pandas as pd
import numpy as np
import json
import os
import random
from datetime import datetime, date, timedelta

# ============================================================
# SIMON IELTS 7.0
# AI IELTS Learning Platform - One File Edition
# ============================================================

st.set_page_config(
    page_title="Simon IELTS 7.0",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# STYLE
# ============================================================

st.markdown("""
<style>
.block-container {
    max-width: 1500px;
    padding-top: 1rem;
    padding-bottom: 3rem;
}

.hero {
    padding: 32px;
    border-radius: 26px;
    margin-bottom: 24px;
    border: 1px solid rgba(128,128,128,.22);
    background: linear-gradient(
        135deg,
        rgba(60,100,210,.16),
        rgba(150,70,190,.10)
    );
}

.hero-title {
    font-size: 46px;
    font-weight: 900;
    line-height: 1.1;
}

.hero-subtitle {
    opacity: .65;
    margin-top: 8px;
}

.card {
    padding: 22px;
    border-radius: 20px;
    border: 1px solid rgba(128,128,128,.18);
    background: rgba(128,128,128,.045);
    margin-bottom: 15px;
}

.big-score {
    font-size: 54px;
    font-weight: 900;
}

.section-title {
    font-size: 28px;
    font-weight: 850;
    margin-top: 10px;
}

.small {
    opacity: .62;
    font-size: 13px;
}

.badge {
    padding: 7px 12px;
    border-radius: 999px;
    background: rgba(100,100,100,.10);
    display: inline-block;
    margin-right: 5px;
}

.progress-label {
    font-weight: 700;
    margin-bottom: 4px;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# DATA STORAGE
# ============================================================

DATA_FILE = "simon_ielts_data.json"


def default_data():
    return {
        "target_score": 7.0,
        "exam_date": "",
        "daily_minutes": 90,
        "level": "基础提升",
        "streak": 0,
        "study_minutes": 0,
        "questions_done": 0,
        "mistakes": [],
        "vocabulary": [],
        "study_log": [],
        "scores": {
            "Listening": 5.0,
            "Reading": 5.0,
            "Writing": 5.5,
            "Speaking": 5.5
        }
    }


def load_data():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)

            base = default_data()

            for key, value in saved.items():
                base[key] = value

            return base

    except Exception:
        pass

    return default_data()


def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=2
            )
    except Exception:
        pass


if "simon_data" not in st.session_state:
    st.session_state.simon_data = load_data()

data = st.session_state.simon_data


# ============================================================
# HELPERS
# ============================================================

def clamp(value, low=0, high=9):
    return max(low, min(high, value))


def band_round(value):
    value = round(value * 2) / 2
    return clamp(value, 0, 9)


def overall_band(scores):
    values = list(scores.values())

    if not values:
        return 0

    return band_round(sum(values) / len(values))


def days_until_exam(exam_date):
    if not exam_date:
        return None

    try:
        target = datetime.strptime(
            exam_date,
            "%Y-%m-%d"
        ).date()

        return (target - date.today()).days

    except Exception:
        return None


def add_study_minutes(minutes):
    data["study_minutes"] += int(minutes)

    data["study_log"].append({
        "date": str(date.today()),
        "minutes": int(minutes)
    })

    save_data(data)


def add_mistake(subject, question_type, reason):
    data["mistakes"].append({
        "date": str(date.today()),
        "subject": subject,
        "type": question_type,
        "reason": reason
    })

    save_data(data)


def add_vocab(word, meaning, example=""):
    data["vocabulary"].append({
        "word": word,
        "meaning": meaning,
        "example": example,
        "date": str(date.today())
    })

    save_data(data)


def score_to_text(score):
    if score >= 8.5:
        return "卓越"
    if score >= 7.5:
        return "优秀"
    if score >= 7:
        return "目标水平"
    if score >= 6.5:
        return "接近目标"
    if score >= 6:
        return "中等"
    if score >= 5:
        return "需要强化"
    return "基础阶段"


# ============================================================
# QUESTION BANK
# ============================================================

READING_QUESTIONS = [
    {
        "question": "The passage states that early researchers underestimated the importance of sleep.",
        "answer": "TRUE",
        "type": "判断题",
        "explanation": "定位原文时寻找表示 researchers / underestimated / sleep 的同义表达。"
    },
    {
        "question": "The study involved fewer than 100 participants.",
        "answer": "FALSE",
        "type": "判断题",
        "explanation": "数字类信息需要回原文核对，不能凭常识判断。"
    },
    {
        "question": "Which factor is identified as the main reason for the change?",
        "answer": "B",
        "type": "选择题",
        "explanation": "重点寻找表示原因、result、because、due to 的句子。"
    },
    {
        "question": "Complete the sentence: Researchers found that regular exercise improved ______.",
        "answer": "memory",
        "type": "填空题",
        "explanation": "注意题目要求的词性以及原文中的同义替换。"
    },
    {
        "question": "Which paragraph discusses the historical development of the theory?",
        "answer": "C",
        "type": "段落匹配",
        "explanation": "先寻找时间线、历史人物、早期研究等信号。"
    }
]

LISTENING_QUESTIONS = [
    {
        "question": "The meeting will take place at ______.",
        "answer": "10:30",
        "type": "填空题",
        "explanation": "时间题重点注意数字、am/pm以及自我修正。"
    },
    {
        "question": "What does the speaker recommend?",
        "answer": "B",
        "type": "选择题",
        "explanation": "注意 however、actually、but 等转折信号词。"
    },
    {
        "question": "The new building is located near the ______.",
        "answer": "station",
        "type": "填空题",
        "explanation": "地点类填空重点训练场景词汇和定位能力。"
    },
    {
        "question": "Which activity is available on Friday?",
        "answer": "C",
        "type": "选择题",
        "explanation": "听到多个选项时不要过早锁定答案。"
    },
    {
        "question": "The customer needs to bring a valid ______.",
        "answer": "passport",
        "type": "填空题",
        "explanation": "注意冠词以及名词单复数。"
    }
]


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="hero">
    <div class="hero-subtitle">
        SIMON IELTS 7.0 · AI-POWERED IELTS LEARNING PLATFORM
    </div>

    <div class="hero-title">
        🎓 Simon IELTS
    </div>

    <div class="hero-subtitle">
        Listening × Reading × Writing × Speaking × Mock × Planning × Growth
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🎯 我的目标")

    target = st.number_input(
        "目标总分",
        min_value=4.0,
        max_value=9.0,
        value=float(data["target_score"]),
        step=0.5
    )

    if target != data["target_score"]:
        data["target_score"] = target
        save_data(data)

    exam_date_input = st.date_input(
        "考试日期",
        value=(
            datetime.strptime(
                data["exam_date"],
                "%Y-%m-%d"
            ).date()
            if data["exam_date"]
            else date.today() + timedelta(days=45)
        )
    )

    data["exam_date"] = str(exam_date_input)
    save_data(data)

    remaining = days_until_exam(
        data["exam_date"]
    )

    if remaining is not None:
        if remaining > 0:
            st.info(f"⏳ 距离考试还有 **{remaining} 天**")
        elif remaining == 0:
            st.error("🔥 今天就是考试日！")
        else:
            st.warning("考试日期已经过去。")

    st.divider()

    st.header("⚙️ 学习设置")

    data["daily_minutes"] = st.slider(
        "每日学习时间",
        15,
        300,
        int(data["daily_minutes"]),
        15
    )

    data["level"] = st.selectbox(
        "当前阶段",
        [
            "基础夯实",
            "基础提升",
            "强化提升",
            "考前冲刺"
        ],
        index=[
            "基础夯实",
            "基础提升",
            "强化提升",
            "考前冲刺"
        ].index(data["level"])
    )

    save_data(data)

    st.divider()

    st.caption("Simon IELTS 7.0")
    st.caption("学习研究工具 · 非官方雅思评分")


# ============================================================
# TOP OVERVIEW
# ============================================================

scores = data["scores"]
overall = overall_band(scores)

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.metric(
        "当前预计总分",
        f"{overall:.1f}"
    )

with c2:
    st.metric(
        "目标总分",
        f"{data['target_score']:.1f}"
    )

with c3:
    gap = max(
        0,
        data["target_score"] - overall
    )

    st.metric(
        "距离目标",
        f"{gap:.1f}"
    )

with c4:
    st.metric(
        "学习时长",
        f"{data['study_minutes']} min"
    )

with c5:
    st.metric(
        "完成题目",
        data["questions_done"]
    )


# ============================================================
# NAVIGATION
# ============================================================

tabs = st.tabs([
    "🏠 Dashboard",
    "🎧 Listening",
    "📖 Reading",
    "✍️ Writing",
    "🗣️ Speaking",
    "📝 Mock Test",
    "🧠 AI Planner",
    "📚 Vocabulary",
    "❌ Mistakes",
    "📊 Growth"
])


# ============================================================
# DASHBOARD
# ============================================================

with tabs[0]:

    st.markdown(
        '<div class="section-title">🏠 Simon Learning Dashboard</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns([1.4, 1])

    with left:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.markdown("### 🎯 今日学习任务")

        weakest = min(
            scores,
            key=scores.get
        )

        tasks = {
            "Listening": [
                "精听 10 分钟",
                "完成 10 道听力题",
                "整理 5 个场景词"
            ],
            "Reading": [
                "完成 1 篇阅读",
                "训练 Heading",
                "整理 10 个同义替换"
            ],
            "Writing": [
                "完成 Task 2 大纲",
                "写 250+ 词作文",
                "检查语法与衔接"
            ],
            "Speaking": [
                "Part 1 热身",
                "完成 1 个 Cue Card",
                "进行 5 分钟自由表达"
            ]
        }

        for task in tasks[weakest]:
            st.checkbox(
                task,
                key=f"task_{task}"
            )

        st.info(
            f"🧠 Simon 判断：目前最值得投入时间的科目是 **{weakest}**。"
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

    with right:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.markdown("### 📡 四科能力")

        for subject, value in scores.items():

            st.markdown(
                f"**{subject} · {value:.1f}**"
            )

            st.progress(
                int(value / 9 * 100)
            )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown("### 🧭 Simon 学习优先级")

    priority = pd.DataFrame({
        "科目": list(scores.keys()),
        "当前分数": list(scores.values()),
        "目标差距": [
            round(max(0, data["target_score"] - x), 1)
            for x in scores.values()
        ]
    })

    priority["优先级"] = (
        priority["目标差距"]
        .rank(
            ascending=False,
            method="min"
        )
        .astype(int)
    )

    priority = priority.sort_values(
        "优先级"
    )

    st.dataframe(
        priority,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# LISTENING
# ============================================================

with tabs[1]:

    st.markdown(
        '<div class="section-title">🎧 AI Listening Lab</div>',
        unsafe_allow_html=True
    )

    mode = st.selectbox(
        "训练模式",
        [
            "精听",
            "泛听",
            "听写",
            "题型专项",
            "模拟测试"
        ]
    )

    question = random.choice(
        LISTENING_QUESTIONS
    )

    st.info(
        f"当前题型：{question['type']}"
    )

    st.markdown(
        f"### {question['question']}"
    )

    answer = st.text_input(
        "你的答案"
    )

    if st.button(
        "检查答案",
        key="listen_check"
    ):

        correct = (
            answer.strip().lower()
            == question["answer"].lower()
        )

        data["questions_done"] += 1

        if correct:

            st.success(
                "🎉 正确！"
            )

        else:

            st.error(
                f"❌ 不正确。参考答案：**{question['answer']}**"
            )

            reason = st.selectbox(
                "这道题为什么错？",
                [
                    "词汇不认识",
                    "定位失败",
                    "听不清",
                    "拼写错误",
                    "同义替换没识别",
                    "注意力分散"
                ],
                key="listen_reason"
            )

            if st.button(
                "保存到错题本",
                key="listen_save"
            ):

                add_mistake(
                    "Listening",
                    question["type"],
                    reason
                )

                st.success(
                    "已加入错题本。"
                )

        st.write(
            f"🧠 AI解析：{question['explanation']}"
        )

        save_data(data)

    st.divider()

    st.markdown("### 🎙️ Listening Training")

    st.write(
        "这里预留音频播放器、逐句字幕、AB复读、变速播放、AI口音分析接口。"
    )

    speed = st.slider(
        "播放速度",
        0.8,
        1.5,
        1.0,
        0.1
    )

    st.caption(
        f"当前训练速度：{speed:.1f}x"
    )


# ============================================================
# READING
# ============================================================

with tabs[2]:

    st.markdown(
        '<div class="section-title">📖 AI Reading Lab</div>',
        unsafe_allow_html=True
    )

    exam_type = st.radio(
        "考试类型",
        ["A类 Academic", "G类 General Training"],
        horizontal=True
    )

    reading_mode = st.selectbox(
        "训练模式",
        [
            "计时训练",
            "精读",
            "题型专项",
            "文章结构分析"
        ]
    )

    question = random.choice(
        READING_QUESTIONS
    )

    st.info(
        f"{exam_type} · {reading_mode} · {question['type']}"
    )

    st.markdown(
        f"### {question['question']}"
    )

    if question["type"] in ["判断题"]:
        answer = st.radio(
            "选择答案",
            ["TRUE", "FALSE", "NOT GIVEN"],
            key="reading_answer"
        )

    elif question["type"] in ["选择题", "段落匹配"]:
        answer = st.radio(
            "选择答案",
            ["A", "B", "C", "D"],
            key="reading_answer"
        )

    else:
        answer = st.text_input(
            "填写答案",
            key="reading_answer_text"
        )

    if st.button(
        "提交答案",
        key="reading_submit"
    ):

        correct = (
            str(answer).strip().lower()
            == question["answer"].lower()
        )

        data["questions_done"] += 1

        if correct:
            st.success("🎉 正确！")
        else:
            st.error(
                f"❌ 答错。参考答案：{question['answer']}"
            )

            reason = st.selectbox(
                "错误原因",
                [
                    "定位错误",
                    "同义替换",
                    "过度推断",
                    "词汇问题",
                    "文章结构理解错误",
                    "粗心"
                ],
                key="reading_reason"
            )

            if st.button(
                "保存错题",
                key="reading_save"
            ):

                add_mistake(
                    "Reading",
                    question["type"],
                    reason
                )

                st.success(
                    "已保存。"
                )

        st.write(
            f"🧠 解析：{question['explanation']}"
        )

        save_data(data)

    st.divider()

    st.markdown("### 🔎 AI 同义替换训练")

    synonym_pairs = pd.DataFrame({
        "题干": [
            "important",
            "increase",
            "problem",
            "show",
            "reduce"
        ],
        "高频替换": [
            "significant",
            "rise / grow",
            "issue",
            "demonstrate",
            "decrease / diminish"
        ]
    })

    st.dataframe(
        synonym_pairs,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# WRITING
# ============================================================

with tabs[3]:

    st.markdown(
        '<div class="section-title">✍️ AI Writing Lab</div>',
        unsafe_allow_html=True
    )

    writing_task = st.selectbox(
        "任务",
        [
            "Task 1 - 图表",
            "Task 1 - 流程图",
            "Task 1 - 地图",
            "Task 2 - Opinion",
            "Task 2 - Discussion",
            "Task 2 - Advantages / Disadvantages",
            "Task 2 - Problems / Solutions"
        ]
    )

    writing_topic = st.selectbox(
        "训练题目",
        [
            "Some people believe technology makes life easier. Discuss both views.",
            "Should governments spend more money on public transport?",
            "Is studying abroad beneficial for young people?",
            "Do the advantages of social media outweigh the disadvantages?"
        ]
    )

    st.info(
        f"当前任务：{writing_task}"
    )

    st.markdown(
        f"### 📝 {writing_topic}"
    )

    writing = st.text_area(
        "开始写作",
        height=420,
        placeholder="在这里输入你的作文……"
    )

    word_count = len(
        writing.split()
    )

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "Word Count",
            word_count
        )

    with c2:
        remaining_words = max(
            0,
            250 - word_count
        )

        st.metric(
            "距离250词",
            remaining_words
        )

    if st.button(
        "🧠 Simon AI 初步批改",
        type="primary",
        key="writing_review"
    ):

        if word_count < 50:

            st.warning(
                "作文太短，至少输入一段完整答案后再分析。"
            )

        else:

            grammar_score = 5.5

            if word_count >= 250:
                grammar_score += 0.5

            if any(
                word in writing.lower()
                for word in [
                    "however",
                    "therefore",
                    "although",
                    "moreover"
                ]
            ):
                grammar_score += 0.5

            grammar_score = min(
                grammar_score,
                7.5
            )

            st.success(
                f"初步估计：Band **{grammar_score:.1f}** 左右"
            )

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "TR / TA",
                    "6.0"
                )

            with col2:
                st.metric(
                    "CC",
                    "6.0"
                )

            with col3:
                st.metric(
                    "LR",
                    "6.0"
                )

            with col4:
                st.metric(
                    "GRA",
                    f"{grammar_score:.1f}"
                )

            st.markdown("### 🎯 提分优先级")

            st.write(
                """
                **1. 先保证任务完成度。**

                **2. 再提升段落逻辑。**

                **3. 再处理词汇丰富度。**

                **4. 最后系统提升复杂句与语法准确率。**
                """
            )

            st.warning(
                "当前评分属于学习辅助估计，不等同于雅思官方评分。"
            )


# ============================================================
# SPEAKING
# ============================================================

with tabs[4]:

    st.markdown(
        '<div class="section-title">🗣️ AI Speaking Lab</div>',
        unsafe_allow_html=True
    )

    speaking_part = st.selectbox(
        "Part",
        ["Part 1", "Part 2", "Part 3"]
    )

    topics = {
        "Part 1": [
            "Do you like studying English?",
            "What do you usually do at weekends?",
            "Do you like travelling?"
        ],
        "Part 2": [
            "Describe a place you would like to visit.",
            "Describe a useful piece of technology.",
            "Describe a person who influenced you."
        ],
        "Part 3": [
            "Why do people travel more today?",
            "How has technology changed education?",
            "Should governments invest more in tourism?"
        ]
    }

    topic = random.choice(
        topics[speaking_part]
    )

    st.info(
        topic
    )

    if speaking_part == "Part 2":

        st.warning(
            "⏱️ 1分钟准备 + 2分钟回答"
        )

        preparation = st.slider(
            "准备时间",
            0,
            60,
            60
        )

        st.caption(
            f"准备时间：{preparation} 秒"
        )

    answer = st.text_area(
        "输入你的回答（语音模块将在后续版本接入）",
        height=260
    )

    if st.button(
        "🧠 Analyze Speaking",
        type="primary",
        key="speaking_analyze"
    ):

        word_count = len(
            answer.split()
        )

        fluency = 5.5
        vocabulary = 5.5
        grammar = 5.5
        pronunciation = 5.5

        if word_count >= 80:
            fluency += 0.5

        if word_count >= 120:
            vocabulary += 0.5

        if any(
            word in answer.lower()
            for word in [
                "because",
                "although",
                "however",
                "therefore",
                "which"
            ]
        ):
            grammar += 0.5

        speaking_score = band_round(
            (
                fluency
                + vocabulary
                + grammar
                + pronunciation
            ) / 4
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Pronunciation",
            f"{pronunciation:.1f}"
        )

        c2.metric(
            "Fluency",
            f"{fluency:.1f}"
        )

        c3.metric(
            "Vocabulary",
            f"{vocabulary:.1f}"
        )

        c4.metric(
            "Grammar",
            f"{grammar:.1f}"
        )

        st.success(
            f"预计 Speaking：Band **{speaking_score:.1f}**"
        )

        st.markdown("### 💡 Simon建议")

        st.write(
            """
            - 减少过短回答
            - 增加具体例子
            - 使用 because / although / which 等复杂结构
            - 避免重复使用 very / good / bad / nice
            - Part 3 要进一步解释“为什么”
            """
        )


# ============================================================
# MOCK TEST
# ============================================================

with tabs[5]:

    st.markdown(
        '<div class="section-title">📝 Simon Mock Test</div>',
        unsafe_allow_html=True
    )

    mock_type = st.selectbox(
        "模考类型",
        [
            "完整四科",
            "Listening",
            "Reading",
            "Writing",
            "Speaking"
        ]
    )

    duration = {
        "完整四科": 165,
        "Listening": 40,
        "Reading": 60,
        "Writing": 60,
        "Speaking": 15
    }[mock_type]

    st.metric(
        "模拟考试时间",
        f"{duration} 分钟"
    )

    st.warning(
        "正式模考模式将在后续版本加入完整计时、自动提交、成绩报告和能力画像。"
    )

    if st.button(
        "🚀 Start Mock Test",
        type="primary"
    ):

        st.session_state.mock_started = True

    if st.session_state.get(
        "mock_started",
        False
    ):

        st.success(
            "模考已开始。"
        )

        st.progress(
            0.01
        )

        st.info(
            "当前为 V1 模考框架，后续会接入完整题库与自动计分系统。"
        )


# ============================================================
# AI PLANNER
# ============================================================

with tabs[6]:

    st.markdown(
        '<div class="section-title">🧠 Simon AI Study Planner</div>',
        unsafe_allow_html=True
    )

    remaining = days_until_exam(
        data["exam_date"]
    )

    if remaining is None:
        remaining = 45

    weakest = min(
        scores,
        key=scores.get
    )

    strongest = max(
        scores,
        key=scores.get
    )

    st.markdown(
        f"""
        <div class="card">
        <b>Simon Diagnosis</b><br><br>
        目标：Band {data['target_score']:.1f}<br>
        当前：Band {overall:.1f}<br>
        距考试：{remaining} 天<br>
        最弱科目：{weakest}<br>
        最强科目：{strongest}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 📅 今日建议")

    if remaining <= 14:

        plan = [
            ("Listening", 25),
            ("Reading", 25),
            ("Writing", 30),
            ("Speaking", 20)
        ]

    elif remaining <= 45:

        plan = [
            ("Listening", 20),
            ("Reading", 25),
            ("Writing", 30),
            ("Speaking", 25)
        ]

    else:

        plan = [
            ("Listening", 20),
            ("Reading", 20),
            ("Writing", 30),
            ("Speaking", 30)
        ]

    for subject, minutes in plan:

        if subject == weakest:
            minutes += 15

        st.write(
            f"**{subject}** · {minutes} 分钟"
        )

        st.progress(
            min(
                100,
                int(minutes / data["daily_minutes"] * 100)
            )
        )

    st.divider()

    st.markdown("### 🎯 目标分拆解")

    target_table = pd.DataFrame({
        "科目": list(scores.keys()),
        "当前": list(scores.values()),
        "目标": [
            data["target_score"]
            for _ in scores
        ],
        "提升空间": [
            round(
                max(
                    0,
                    data["target_score"] - score
                ),
                1
            )
            for score in scores.values()
        ]
    })

    st.dataframe(
        target_table,
        use_container_width=True,
        hide_index=True
    )

    if st.button(
        "🔥 完成今日学习",
        type="primary"
    ):

        add_study_minutes(
            data["daily_minutes"]
        )

        st.success(
            "今日学习已记录！继续保持。"
        )


# ============================================================
# VOCABULARY
# ============================================================

with tabs[7]:

    st.markdown(
        '<div class="section-title">📚 Simon Vocabulary Brain</div>',
        unsafe_allow_html=True
    )

    word = st.text_input(
        "单词"
    )

    meaning = st.text_input(
        "中文含义"
    )

    example = st.text_input(
        "例句"
    )

    if st.button(
        "➕ 加入生词本",
        key="add_vocab"
    ):

        if word:

            add_vocab(
                word,
                meaning,
                example
            )

            st.success(
                f"{word} 已加入生词本。"
            )

    st.divider()

    if data["vocabulary"]:

        vocab_df = pd.DataFrame(
            data["vocabulary"]
        )

        st.dataframe(
            vocab_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "你的生词本还是空的。"
        )

    st.markdown("### 🧠 高频雅思词")

    common_words = pd.DataFrame({
        "Word": [
            "significant",
            "substantial",
            "consequently",
            "contribute",
            "decline",
            "implement",
            "sustainable",
            "controversial"
        ],
        "Meaning": [
            "重要的；显著的",
            "大量的；重大的",
            "因此",
            "促进；贡献",
            "下降",
            "实施",
            "可持续的",
            "有争议的"
        ]
    })

    st.dataframe(
        common_words,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# MISTAKES
# ============================================================

with tabs[8]:

    st.markdown(
        '<div class="section-title">❌ Simon Intelligent Mistake Book</div>',
        unsafe_allow_html=True
    )

    if data["mistakes"]:

        mistakes_df = pd.DataFrame(
            data["mistakes"]
        )

        st.dataframe(
            mistakes_df,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("### 🔍 错题归因")

        reason_counts = (
            mistakes_df["reason"]
            .value_counts()
        )

        st.bar_chart(
            reason_counts
        )

        most_common = reason_counts.index[0]

        st.warning(
            f"你的主要错误类型：**{most_common}**"
        )

        st.info(
            "Simon建议：不要只重做错题，要优先解决造成错误的底层能力。"
        )

    else:

        st.info(
            "目前还没有错题记录。"
        )


# ============================================================
# GROWTH
# ============================================================

with tabs[9]:

    st.markdown(
        '<div class="section-title">📊 Simon Growth Center</div>',
        unsafe_allow_html=True
    )

    radar_data = pd.DataFrame({
        "Subject": list(scores.keys()),
        "Band": list(scores.values())
    })

    st.bar_chart(
        radar_data.set_index("Subject")
    )

    st.markdown("### 📈 学习数据")

    total_minutes = data["study_minutes"]

    hours = total_minutes / 60

    g1, g2, g3, g4 = st.columns(4)

    g1.metric(
        "学习小时",
        f"{hours:.1f}"
    )

    g2.metric(
        "完成题目",
        data["questions_done"]
    )

    g3.metric(
        "错题数量",
        len(data["mistakes"])
    )

    g4.metric(
        "词汇数量",
        len(data["vocabulary"])
    )

    st.markdown("### 🧠 Simon 能力诊断")

    for subject, value in scores.items():

        if value < data["target_score"] - 1:
            status = "🔴 重点提升"

        elif value < data["target_score"]:
            status = "🟡 接近目标"

        else:
            status = "🟢 达到目标"

        st.write(
            f"**{subject}** · {value:.1f} · {status}"
        )

    st.divider()

    st.markdown("### 🏆 当前阶段")

    if overall >= data["target_score"]:
        stage = "🎉 目标达成"
    elif overall >= 6.5:
        stage = "🔥 冲刺阶段"
    elif overall >= 6:
        stage = "🚀 强化阶段"
    else:
        stage = "🌱 基础阶段"

    st.success(
        stage
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    ### 🎓 Simon IELTS 7.0

    **Learn → Practice → Diagnose → Adapt → Improve**

    Simon IELTS 是学习辅助工具，不代表雅思官方产品，
    AI评分仅用于学习参考，不保证实际考试成绩。
    """
)

st.caption(
    f"Last update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)