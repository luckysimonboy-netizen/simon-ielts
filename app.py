import streamlit as st
import random
import time
from datetime import datetime, date

# ============================================================
# SIMON IELTS 7.0
# AI IELTS LEARNING OS
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
    max-width: 1450px;
    padding-top: 1.5rem;
}

.hero {
    padding: 32px;
    border-radius: 24px;
    border: 1px solid rgba(128,128,128,.25);
    background: linear-gradient(
        135deg,
        rgba(70,100,200,.16),
        rgba(150,70,180,.10)
    );
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 48px;
    margin-bottom: 5px;
}

.card {
    padding: 22px;
    border-radius: 18px;
    border: 1px solid rgba(128,128,128,.20);
    background: rgba(128,128,128,.05);
    margin-bottom: 15px;
}

.big-score {
    font-size: 64px;
    font-weight: 900;
}

.small-text {
    opacity: .65;
}

.question-box {
    padding: 20px;
    border-radius: 16px;
    border: 1px solid rgba(128,128,128,.2);
    margin: 15px 0;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "xp": 0,
    "streak": 0,
    "questions_done": 0,
    "correct": 0,
    "wrong": 0,
    "mistakes": [],
    "completed": [],
    "study_minutes": 0,
    "target_band": 7.0,
    "exam_date": None,
    "daily_minutes": 60,
    "last_activity": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# QUESTION BANK
# ============================================================

LISTENING_BANK = [
    {
        "id": "L001",
        "type": "choice",
        "difficulty": "Easy",
        "topic": "Accommodation",
        "question": "What does the student need to bring to the accommodation office?",
        "options": [
            "A. A passport photograph",
            "B. A copy of the rental agreement",
            "C. A university identity card",
            "D. A bank statement"
        ],
        "answer": "B",
        "explanation": "The key information is the copy of the rental agreement."
    },
    {
        "id": "L002",
        "type": "choice",
        "difficulty": "Medium",
        "topic": "University",
        "question": "Why has the lecture been moved to another room?",
        "options": [
            "A. The original room is being repaired.",
            "B. More students are expected.",
            "C. The lecturer requested better equipment.",
            "D. The original room is being used for an examination."
        ],
        "answer": "B",
        "explanation": "The larger room is required because more students are expected."
    },
    {
        "id": "L003",
        "type": "choice",
        "difficulty": "Medium",
        "topic": "Travel",
        "question": "What time will the tour leave the hotel?",
        "options": [
            "A. 7:15",
            "B. 7:30",
            "C. 7:45",
            "D. 8:00"
        ],
        "answer": "C",
        "explanation": "The tour is scheduled to leave at 7:45."
    },
    {
        "id": "L004",
        "type": "choice",
        "difficulty": "Hard",
        "topic": "Environment",
        "question": "What is the main purpose of the new recycling project?",
        "options": [
            "A. To reduce collection costs",
            "B. To increase public awareness",
            "C. To reduce the amount of waste sent to landfill",
            "D. To encourage businesses to recycle"
        ],
        "answer": "C",
        "explanation": "The central objective is reducing landfill waste."
    },
    {
        "id": "L005",
        "type": "choice",
        "difficulty": "Hard",
        "topic": "Education",
        "question": "What does the professor say is the biggest problem with the current study?",
        "options": [
            "A. The sample is too small.",
            "B. The research period is too short.",
            "C. The data was collected incorrectly.",
            "D. The participants were too similar."
        ],
        "answer": "A",
        "explanation": "The professor specifically identifies the sample size as the main limitation."
    }
]


READING_BANK = [
    {
        "id": "R001",
        "difficulty": "Easy",
        "topic": "Technology",
        "title": "The Changing Workplace",
        "passage": """
Remote work has become increasingly common in many industries. Improvements
in communication technology have made it possible for employees to collaborate
without being physically present in the same office. Some companies report
higher employee satisfaction because workers have greater flexibility.

However, remote work also creates challenges. New employees may find it
difficult to develop relationships with colleagues, and some managers worry
that communication can become less efficient. As a result, many organisations
are experimenting with hybrid systems that combine remote and office-based work.
""",
        "question": "What is one advantage of remote work mentioned in the passage?",
        "options": [
            "A. Employees require less training.",
            "B. Employees have greater flexibility.",
            "C. Managers have more control.",
            "D. Companies need fewer computers."
        ],
        "answer": "B",
        "explanation": "The passage directly states that workers have greater flexibility."
    },
    {
        "id": "R002",
        "difficulty": "Medium",
        "topic": "Environment",
        "title": "Urban Trees",
        "passage": """
Trees in cities provide several environmental benefits. They can reduce local
temperatures by providing shade and releasing water vapour. Trees can also
improve air quality by capturing certain pollutants.

Researchers have found that the location of urban trees is important.
Trees planted near heavily used roads may provide environmental benefits,
but they can also be exposed to high levels of pollution. Urban planners
therefore need to consider both environmental and social factors when
deciding where trees should be planted.
""",
        "question": "Why is the location of urban trees important?",
        "options": [
            "A. Trees grow faster in cities.",
            "B. Trees require different types of soil.",
            "C. Location affects their environmental impact.",
            "D. Urban trees are expensive to maintain."
        ],
        "answer": "C",
        "explanation": "The passage explains that location affects pollution exposure and benefits."
    },
    {
        "id": "R003",
        "difficulty": "Hard",
        "topic": "Psychology",
        "title": "Memory and Learning",
        "passage": """
Learning is often more effective when information is revisited at increasing
intervals rather than repeatedly studied in a single session. This approach,
known as spaced practice, encourages learners to retrieve information after
some time has passed.

Researchers have suggested that the difficulty of retrieval is important.
If information is completely forgotten, learning may become inefficient.
However, retrieving information with some effort can strengthen memory.
Effective study therefore requires a balance between repetition and challenge.
""",
        "question": "According to the passage, why can spaced practice improve learning?",
        "options": [
            "A. It eliminates the need for revision.",
            "B. It makes every study session easier.",
            "C. It encourages effortful retrieval.",
            "D. It allows students to study fewer subjects."
        ],
        "answer": "C",
        "explanation": "The passage links spaced practice with effortful retrieval, which strengthens memory."
    }
]


WRITING_BANK = [
    {
        "id": "W001",
        "type": "Task 2",
        "topic": "Education",
        "question": "Some people believe that university education should be free for everyone. To what extent do you agree or disagree?",
        "ideas": [
            "Equal access to education",
            "Government spending",
            "Economic benefits of higher education",
            "Alternative funding models"
        ]
    },
    {
        "id": "W002",
        "type": "Task 2",
        "topic": "Technology",
        "question": "Some people think that technology makes life more complicated rather than easier. Discuss both views and give your own opinion.",
        "ideas": [
            "Convenience and efficiency",
            "Information overload",
            "Digital dependence",
            "Balance between technology and traditional methods"
        ]
    },
    {
        "id": "W003",
        "type": "Task 2",
        "topic": "Environment",
        "question": "Many environmental problems are caused by individuals, while others believe governments and large companies are responsible. Discuss both views.",
        "ideas": [
            "Individual consumption",
            "Government regulation",
            "Corporate responsibility",
            "Combined responsibility"
        ]
    },
    {
        "id": "W004",
        "type": "Task 2",
        "topic": "Work",
        "question": "More people are choosing to work from home. Do the advantages of this development outweigh the disadvantages?",
        "ideas": [
            "Flexible schedules",
            "Reduced commuting",
            "Isolation",
            "Communication difficulties"
        ]
    }
]


SPEAKING_BANK = [
    {
        "id": "S001",
        "part": "Part 1",
        "topic": "Hometown",
        "questions": [
            "Where is your hometown?",
            "What do you like most about your hometown?",
            "Has your hometown changed much in recent years?"
        ]
    },
    {
        "id": "S002",
        "part": "Part 2",
        "topic": "Person",
        "cue_card": "Describe a person who has influenced you.",
        "points": [
            "Who the person is",
            "How you know this person",
            "What this person has done",
            "Why this person influenced you"
        ]
    },
    {
        "id": "S003",
        "part": "Part 3",
        "topic": "Education",
        "questions": [
            "How has education changed in recent decades?",
            "Should schools teach more practical skills?",
            "What role will technology play in future education?"
        ]
    }
]


VOCABULARY_BANK = [
    {
        "word": "allocate",
        "meaning": "分配；拨出",
        "example": "The government should allocate more money to education.",
        "synonyms": ["distribute", "assign"]
    },
    {
        "word": "significant",
        "meaning": "重要的；显著的",
        "example": "There has been a significant increase in demand.",
        "synonyms": ["considerable", "substantial"]
    },
    {
        "word": "consequently",
        "meaning": "因此；结果",
        "example": "The population increased and consequently housing became more expensive.",
        "synonyms": ["therefore", "as a result"]
    },
    {
        "word": "sustainable",
        "meaning": "可持续的",
        "example": "Cities need to develop sustainable transport systems.",
        "synonyms": ["viable", "environmentally responsible"]
    },
    {
        "word": "enhance",
        "meaning": "提高；增强",
        "example": "Technology can enhance the learning experience.",
        "synonyms": ["improve", "strengthen"]
    },
    {
        "word": "inevitable",
        "meaning": "不可避免的",
        "example": "Some degree of change is inevitable.",
        "synonyms": ["unavoidable", "certain"]
    },
    {
        "word": "controversial",
        "meaning": "有争议的",
        "example": "The proposal remains controversial.",
        "synonyms": ["debatable", "disputed"]
    },
    {
        "word": "deteriorate",
        "meaning": "恶化",
        "example": "Air quality may deteriorate during the winter.",
        "synonyms": ["worsen", "decline"]
    }
]


GRAMMAR_BANK = [
    {
        "question": "If governments ___ more money on public transport, traffic congestion could decrease.",
        "options": ["spend", "spent", "will spend", "have spent"],
        "answer": "spent",
        "explanation": "This is a second conditional: If + past simple, would/could + verb."
    },
    {
        "question": "The number of people using public transport ___ increased significantly.",
        "options": ["have", "has", "are", "were"],
        "answer": "has",
        "explanation": "The subject 'The number' is singular."
    },
    {
        "question": "The report, ___ was published last week, received considerable attention.",
        "options": ["who", "where", "which", "what"],
        "answer": "which",
        "explanation": "Which introduces a non-defining relative clause referring to the report."
    },
    {
        "question": "Many students find it difficult ___ academic vocabulary.",
        "options": ["to acquire", "acquiring", "acquire", "acquired"],
        "answer": "to acquire",
        "explanation": "The structure is find it difficult to do something."
    }
]


# ============================================================
# FUNCTIONS
# ============================================================

def add_xp(amount):
    st.session_state.xp += amount


def record_answer(question_id, correct, subject, question_text):
    st.session_state.questions_done += 1

    if correct:
        st.session_state.correct += 1
        add_xp(10)
    else:
        st.session_state.wrong += 1
        add_xp(3)

        mistake = {
            "id": question_id,
            "subject": subject,
            "question": question_text,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        if mistake not in st.session_state.mistakes:
            st.session_state.mistakes.append(mistake)


def accuracy():
    total = st.session_state.questions_done

    if total == 0:
        return 0

    return st.session_state.correct / total


def listening_band(correct):
    table = [
        (39, 9.0),
        (37, 8.5),
        (35, 8.0),
        (32, 7.5),
        (30, 7.0),
        (26, 6.5),
        (23, 6.0),
        (18, 5.5),
        (16, 5.0),
        (13, 4.5),
        (10, 4.0)
    ]

    for minimum, band in table:
        if correct >= minimum:
            return band

    return 4.0


def reading_band(correct, academic=True):
    table = [
        (39, 9.0),
        (37, 8.5),
        (35, 8.0),
        (33, 7.5),
        (30, 7.0),
        (27, 6.5),
        (23, 6.0),
        (19, 5.5),
        (15, 5.0),
        (13, 4.5),
        (10, 4.0)
    ]

    if not academic:
        table = [
            (40, 9.0),
            (39, 8.5),
            (37, 8.0),
            (36, 7.5),
            (34, 7.0),
            (32, 6.5),
            (30, 6.0),
            (27, 5.5),
            (23, 5.0),
            (19, 4.5)
        ]

    for minimum, band in table:
        if correct >= minimum:
            return band

    return 4.0


def writing_estimate(text):
    words = len(text.split())

    if words < 100:
        return 4.5

    if words < 180:
        return 5.5

    if words < 230:
        return 6.0

    if words < 280:
        return 6.5

    if words < 330:
        return 7.0

    return 7.5


def overall_band(scores):
    valid = [x for x in scores if x is not None]

    if not valid:
        return None

    value = sum(valid) / len(valid)

    rounded = round(value * 2) / 2

    return rounded


def level_from_xp(xp):
    return 1 + xp // 100


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="hero">
    <div class="small-text">SIMON IELTS 7.0 · AI IELTS LEARNING OS</div>
    <h1>🎓 Simon IELTS</h1>
    <div class="small-text">
        Listening × Reading × Writing × Speaking × Vocabulary × Grammar
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🎯 我的目标")

    target = st.selectbox(
        "目标分数",
        [6.0, 6.5, 7.0, 7.5, 8.0],
        index=2
    )

    st.session_state.target_band = target

    exam = st.date_input(
        "考试日期",
        value=date.today()
    )

    st.session_state.exam_date = exam

    daily = st.slider(
        "每天学习时间",
        15,
        240,
        st.session_state.daily_minutes,
        15
    )

    st.session_state.daily_minutes = daily

    st.divider()

    st.metric(
        "🏆 Level",
        level_from_xp(st.session_state.xp)
    )

    st.metric(
        "⭐ XP",
        st.session_state.xp
    )

    st.metric(
        "🔥 连续学习",
        st.session_state.streak
    )

    st.divider()

    st.caption("Simon IELTS 7.0")
    st.caption("原创练习题库 · 学习研究工具")


# ============================================================
# NAVIGATION
# ============================================================

pages = [
    "🏠 Dashboard",
    "🎧 Listening",
    "📖 Reading",
    "✍️ Writing",
    "🗣️ Speaking",
    "🧠 Vocabulary",
    "📝 Grammar",
    "🧪 Mock Test",
    "❌ 错题本",
    "📊 学习数据",
    "📅 AI学习计划"
]

page = st.sidebar.radio(
    "功能",
    pages
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.title("🏠 Simon Learning Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "目标",
            f"{st.session_state.target_band:.1f}"
        )

    with c2:
        st.metric(
            "完成题目",
            st.session_state.questions_done
        )

    with c3:
        st.metric(
            "正确率",
            f"{accuracy() * 100:.1f}%"
        )

    with c4:
        st.metric(
            "XP",
            st.session_state.xp
        )

    st.divider()

    st.subheader("🚀 今天开始学习")

    cols = st.columns(4)

    cols[0].info("🎧 Listening\n\n训练定位、同义替换和细节捕捉。")

    cols[1].info("📖 Reading\n\n训练定位、判断和长难句。")

    cols[2].info("✍️ Writing\n\n训练 Task 1 / Task 2。")

    cols[3].info("🗣️ Speaking\n\n训练 Part 1 / 2 / 3。")

    st.divider()

    st.subheader("🎯 7.0 核心策略")

    st.write("""
    **不要盲目刷题。**

    Simon IELTS 会把训练拆成：

    1. 做题
    2. 判断对错
    3. 分析错误
    4. 找薄弱点
    5. 针对训练
    6. 再测试
    """)

    if st.session_state.questions_done > 0:

        st.subheader("📈 当前学习状态")

        if accuracy() >= 0.85:
            st.success("当前正确率很好，可以开始提高题目难度。")
        elif accuracy() >= 0.70:
            st.info("基础正在形成，继续针对薄弱题型训练。")
        else:
            st.warning("建议先减少盲目刷题，加强错题和基础能力。")


# ============================================================
# LISTENING
# ============================================================

elif page == "🎧 Listening":

    st.title("🎧 AI Listening Training")

    difficulty = st.selectbox(
        "难度",
        ["全部", "Easy", "Medium", "Hard"]
    )

    topic = st.selectbox(
        "场景",
        ["全部"] + sorted(
            list(set(q["topic"] for q in LISTENING_BANK))
        )
    )

    pool = LISTENING_BANK.copy()

    if difficulty != "全部":
        pool = [
            q for q in pool
            if q["difficulty"] == difficulty
        ]

    if topic != "全部":
        pool = [
            q for q in pool
            if q["topic"] == topic
        ]

    if "listening_question" not in st.session_state:
        st.session_state.listening_question = random.choice(pool)

    q = st.session_state.listening_question

    st.markdown(
        f"### {q['topic']} · {q['difficulty']}"
    )

    st.write(q["question"])

    answer = st.radio(
        "选择答案",
        q["options"],
        key=f"listen_{q['id']}"
    )

    if st.button("提交答案", type="primary"):

        selected = answer[0]
        correct = selected == q["answer"]

        record_answer(
            q["id"],
            correct,
            "Listening",
            q["question"]
        )

        if correct:
            st.success("🎉 Correct!")
        else:
            st.error(
                f"❌ 正确答案：{q['answer']}"
            )

        st.info(q["explanation"])

    if st.button("➡️ 下一题"):

        st.session_state.listening_question = random.choice(pool)
        st.rerun()

    st.divider()

    st.subheader("🎯 Listening 训练方法")

    st.write("""
    **第一遍：** 不看文字，模拟考试。

    **第二遍：** 定位关键词。

    **第三遍：** 分析同义替换。

    **第四遍：** 精听错误句。

    **第五遍：** 跟读模仿。
    """)


# ============================================================
# READING
# ============================================================

elif page == "📖 Reading":

    st.title("📖 AI Reading Training")

    academic = st.toggle(
        "Academic A类",
        value=True
    )

    difficulty = st.selectbox(
        "难度",
        ["全部", "Easy", "Medium", "Hard"]
    )

    pool = READING_BANK.copy()

    if difficulty != "全部":

        pool = [
            q for q in pool
            if q["difficulty"] == difficulty
        ]

    if "reading_question" not in st.session_state:
        st.session_state.reading_question = random.choice(pool)

    q = st.session_state.reading_question

    st.subheader(q["title"])

    st.markdown(q["passage"])

    st.divider()

    st.write(
        f"### Question\n{q['question']}"
    )

    answer = st.radio(
        "选择答案",
        q["options"],
        key=f"read_{q['id']}"
    )

    if st.button("提交答案", type="primary"):

        selected = answer[0]
        correct = selected == q["answer"]

        record_answer(
            q["id"],
            correct,
            "Reading",
            q["question"]
        )

        if correct:
            st.success("🎉 Correct!")
        else:
            st.error(
                f"❌ 正确答案：{q['answer']}"
            )

        st.info(q["explanation"])

    if st.button("➡️ 下一题"):

        st.session_state.reading_question = random.choice(pool)
        st.rerun()

    st.divider()

    st.subheader("🔍 Reading 三步法")

    st.write("""
    **1. 定位：** 找关键词。

    **2. 对照：** 找原文对应信息。

    **3. 判断：** 特别注意同义替换和逻辑关系。
    """)


# ============================================================
# WRITING
# ============================================================

elif page == "✍️ Writing":

    st.title("✍️ AI Writing Studio")

    task = st.selectbox(
        "Task",
        ["Task 2", "Task 1"]
    )

    if task == "Task 2":

        q = random.choice(WRITING_BANK)

        st.info(q["question"])

        st.caption(
            f"Topic: {q['topic']}"
        )

        essay = st.text_area(
            "在这里写作文",
            height=450
        )

        words = len(essay.split())

        c1, c2 = st.columns(2)

        c1.metric(
            "Word Count",
            words
        )

        if st.button(
            "🧠 Simon AI Pre-check",
            type="primary"
        ):

            estimate = writing_estimate(essay)

            st.subheader(
                f"📊 初步 Band：{estimate:.1f}"
            )

            if words < 250:
                st.warning(
                    "Task 2 建议至少完成 250 词。"
                )
            else:
                st.success(
                    "字数达到 Task 2 基本要求。"
                )

            st.markdown("### TR / TA")

            if words >= 250:
                st.write("✓ 已达到基本篇幅要求。")
            else:
                st.write("⚠️ 论点可能缺少充分展开。")

            st.markdown("### CC")
            st.write(
                "检查段落结构、逻辑关系和连接方式。"
            )

            st.markdown("### LR")
            st.write(
                "检查词汇准确性、搭配和重复表达。"
            )

            st.markdown("### GRA")
            st.write(
                "检查句子结构、从句、时态和语法准确性。"
            )

            st.info(
                "这是规则型预评估，不等同于雅思官方评分。"
            )

        st.subheader("💡 Simon Idea Generator")

        for idea in q["ideas"]:
            st.markdown(f"• {idea}")

    else:

        st.info(
            "Task 1 模块已预留完整结构："
            "折线图、柱状图、饼图、表格、地图、流程图。"
        )

        st.text_area(
            "Task 1 作答区",
            height=400
        )


# ============================================================
# SPEAKING
# ============================================================

elif page == "🗣️ Speaking":

    st.title("🗣️ AI Speaking Lab")

    part = st.selectbox(
        "Part",
        ["Part 1", "Part 2", "Part 3"]
    )

    matching = [
        q for q in SPEAKING_BANK
        if q["part"] == part
    ]

    q = random.choice(matching)

    st.subheader(
        f"{q['topic']} · {q['part']}"
    )

    if part == "Part 2":

        st.info(q["cue_card"])

        st.markdown("### You should say:")

        for point in q["points"]:
            st.markdown(f"• {point}")

        st.write("⏱️ Preparation: 1 minute")

        if st.button("开始准备"):
            st.session_state.speaking_start = time.time()

        st.text_area(
            "你的回答记录",
            height=300
        )

    else:

        for index, question in enumerate(
            q["questions"],
            1
        ):

            st.markdown(
                f"### {index}. {question}"
            )

            st.text_area(
                "你的回答",
                key=f"speaking_{q['id']}_{index}",
                height=120
            )

    st.divider()

    st.subheader("🎯 Speaking 四项能力")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Fluency", "待评估")
    c2.metric("Pronunciation", "待评估")
    c3.metric("Vocabulary", "待评估")
    c4.metric("Grammar", "待评估")

    st.caption(
        "后续可接入语音识别与发音分析 API。"
    )


# ============================================================
# VOCABULARY
# ============================================================

elif page == "🧠 Vocabulary":

    st.title("🧠 Simon Vocabulary Lab")

    mode = st.radio(
        "学习模式",
        ["浏览", "测试"]
    )

    if mode == "浏览":

        for word in VOCABULARY_BANK:

            with st.expander(
                word["word"]
            ):

                st.write(
                    f"**意思：** {word['meaning']}"
                )

                st.write(
                    f"**例句：** {word['example']}"
                )

                st.write(
                    "**同义词：** "
                    + ", ".join(word["synonyms"])
                )

    else:

        if "vocab_question" not in st.session_state:
            st.session_state.vocab_question = random.choice(
                VOCABULARY_BANK
            )

        q = st.session_state.vocab_question

        st.markdown(
            f"### What does **{q['word']}** mean?"
        )

        options = [
            q["meaning"],
            "完全不同的含义",
            "一种语法结构",
            "一种时间表达"
        ]

        random.shuffle(options)

        answer = st.radio(
            "选择",
            options
        )

        if st.button(
            "提交",
            type="primary"
        ):

            if answer == q["meaning"]:

                st.success("🎉 Correct!")
                add_xp(10)

            else:

                st.error(
                    f"答案：{q['meaning']}"
                )

        if st.button("下一词"):

            st.session_state.vocab_question = random.choice(
                VOCABULARY_BANK
            )

            st.rerun()


# ============================================================
# GRAMMAR
# ============================================================

elif page == "📝 Grammar":

    st.title("📝 Simon Grammar Lab")

    if "grammar_question" not in st.session_state:

        st.session_state.grammar_question = random.choice(
            GRAMMAR_BANK
        )

    q = st.session_state.grammar_question

    st.markdown(
        f"### {q['question']}"
    )

    answer = st.radio(
        "选择",
        q["options"]
    )

    if st.button(
        "提交",
        type="primary"
    ):

        if answer == q["answer"]:

            st.success("🎉 Correct!")
            add_xp(10)

        else:

            st.error(
                f"正确答案：{q['answer']}"
            )

        st.info(
            q["explanation"]
        )

    if st.button("下一题"):

        st.session_state.grammar_question = random.choice(
            GRAMMAR_BANK
        )

        st.rerun()


# ============================================================
# MOCK TEST
# ============================================================

elif page == "🧪 Mock Test":

    st.title("🧪 Simon Mock Test")

    st.info(
        "这是训练版模考引擎。正式版本可以继续扩展为完整 Listening + Reading + Writing 连续计时考试。"
    )

    mock_type = st.selectbox(
        "模考类型",
        [
            "Listening",
            "Reading",
            "Writing"
        ]
    )

    if mock_type == "Listening":

        number = st.slider(
            "题目数量",
            1,
            len(LISTENING_BANK),
            len(LISTENING_BANK)
        )

        if st.button(
            "开始 Listening Mock",
            type="primary"
        ):

            questions = random.sample(
                LISTENING_BANK,
                number
            )

            score = 0

            for q in questions:

                st.markdown(
                    f"### {q['question']}"
                )

                answer = st.radio(
                    "答案",
                    q["options"],
                    key=f"mock_{q['id']}"
                )

                if answer[0] == q["answer"]:
                    score += 1

            if st.button("提交模考"):

                band = listening_band(score)

                st.success(
                    f"正确 {score}/{number}"
                )

                st.metric(
                    "Estimated Band",
                    band
                )

    elif mock_type == "Reading":

        st.info(
            "Reading Mock 使用当前 Reading 题库生成训练卷。"
        )

        if st.button(
            "生成 Reading Mock",
            type="primary"
        ):

            st.session_state.mock_reading = random.sample(
                READING_BANK,
                len(READING_BANK)
            )

        if "mock_reading" in st.session_state:

            answers = {}

            for q in st.session_state.mock_reading:

                st.markdown(
                    f"### {q['question']}"
                )

                answers[q["id"]] = st.radio(
                    "答案",
                    q["options"],
                    key=f"rm_{q['id']}"
                )

            if st.button("提交 Reading Mock"):

                score = 0

                for q in st.session_state.mock_reading:

                    if answers[q["id"]][0] == q["answer"]:
                        score += 1

                st.success(
                    f"正确 {score}/{len(st.session_state.mock_reading)}"
                )

    else:

        st.subheader("Writing Mock")

        q = random.choice(WRITING_BANK)

        st.info(q["question"])

        essay = st.text_area(
            "Essay",
            height=500
        )

        if st.button(
            "提交 Writing Mock",
            type="primary"
        ):

            band = writing_estimate(essay)

            st.metric(
                "Estimated Band",
                band
            )


# ============================================================
# MISTAKES
# ============================================================

elif page == "❌ 错题本":

    st.title("❌ Simon Mistake Book")

    if not st.session_state.mistakes:

        st.success(
            "🎉 目前没有错题。继续保持！"
        )

    else:

        st.metric(
            "错题数量",
            len(st.session_state.mistakes)
        )

        for mistake in reversed(
            st.session_state.mistakes
        ):

            with st.expander(
                f"{mistake['subject']} · {mistake['id']}"
            ):

                st.write(
                    mistake["question"]
                )

                st.caption(
                    mistake["date"]
                )

        if st.button(
            "清空错题本"
        ):

            st.session_state.mistakes = []
            st.rerun()


# ============================================================
# DATA
# ============================================================

elif page == "📊 学习数据":

    st.title("📊 Learning Analytics")

    total = st.session_state.questions_done
    correct = st.session_state.correct
    wrong = st.session_state.wrong

    c1, c2, c3 = st.columns(3)

    c1.metric("做题量", total)
    c2.metric("正确", correct)
    c3.metric("错误", wrong)

    st.divider()

    st.subheader("🎯 正确率")

    st.progress(
        min(accuracy(), 1.0)
    )

    st.write(
        f"{accuracy() * 100:.1f}%"
    )

    st.subheader("🏆 XP")

    st.progress(
        (st.session_state.xp % 100) / 100
    )

    st.write(
        f"Level {level_from_xp(st.session_state.xp)}"
    )

    st.divider()

    st.subheader("🧠 7.0 能力要求")

    targets = {
        "Listening": 30,
        "Reading": 30,
        "Writing": 6.5,
        "Speaking": 6.5
    }

    for skill, target_score in targets.items():

        st.write(
            f"**{skill}** → 目标 {target_score}"
        )

        st.progress(
            min(
                accuracy(),
                1.0
            )
        )


# ============================================================
# STUDY PLAN
# ============================================================

elif page == "📅 AI学习计划":

    st.title("📅 Simon AI Study Planner")

    if st.session_state.exam_date:

        days = (
            st.session_state.exam_date
            - date.today()
        ).days

        if days < 0:
            days = 0

        st.metric(
            "距离考试",
            f"{days} 天"
        )

        st.subheader(
            f"🎯 目标 Band {st.session_state.target_band}"
        )

        if days > 60:

            phase = "基础夯实"

        elif days > 30:

            phase = "强化提升"

        elif days > 14:

            phase = "专项突破"

        else:

            phase = "考前冲刺"

        st.info(
            f"当前阶段：**{phase}**"
        )

    else:

        days = 30

    st.divider()

    st.subheader("📚 今日任务")

    minutes = st.session_state.daily_minutes

    tasks = [
        (
            "🎧 Listening",
            max(10, int(minutes * 0.25)),
            "精听 + 错题分析"
        ),
        (
            "📖 Reading",
            max(10, int(minutes * 0.25)),
            "定位 + 同义替换"
        ),
        (
            "✍️ Writing",
            max(10, int(minutes * 0.30)),
            "Task 2 / 句型升级"
        ),
        (
            "🗣️ Speaking",
            max(5, int(minutes * 0.15)),
            "Part 2 + Part 3"
        ),
        (
            "🧠 Vocabulary",
            max(5, int(minutes * 0.05)),
            "复习 + 新词"
        )
    ]

    for name, mins, task in tasks:

        st.markdown(
            f"### {name}"
        )

        st.write(
            f"⏱️ {mins} 分钟 · {task}"
        )

    st.divider()

    st.subheader("🔥 Simon Rule")

    st.success(
        "每天不要追求刷最多题，而要追求真正消灭一个薄弱点。"
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Simon IELTS 7.0 · AI IELTS Learning OS"
)

st.caption(
    "原创练习内容仅用于学习研究。"
)

st.caption(
    "本工具不是 IELTS 官方产品，也不代表官方评分结果。"
)