import streamlit as st
import random

st.set_page_config(
    page_title="Simon IELTS",
    page_icon="🎓",
    layout="wide"
)

# ---------- CSS ----------
st.markdown("""
<style>
.main-title {
    font-size: 48px;
    font-weight: 800;
}
.subtitle {
    font-size: 20px;
    color: #666;
}
.card {
    padding: 25px;
    border-radius: 18px;
    border: 1px solid #ddd;
    margin-bottom: 20px;
}
.score {
    font-size: 42px;
    font-weight: 800;
}
</style>
""", unsafe_allow_html=True)

# ---------- Data ----------
reading_questions = [
    {
        "question": "What is one major advantage of learning a foreign language?",
        "options": [
            "It makes people taller",
            "It improves communication",
            "It eliminates exams",
            "It reduces sleep"
        ],
        "answer": "It improves communication"
    },
    {
        "question": "Which skill is particularly important for IELTS Speaking?",
        "options": [
            "Memorising every answer",
            "Speaking naturally and clearly",
            "Writing long essays",
            "Reading silently"
        ],
        "answer": "Speaking naturally and clearly"
    },
    {
        "question": "What should an IELTS essay normally contain?",
        "options": [
            "Only one paragraph",
            "An introduction, body paragraphs and a conclusion",
            "Only examples",
            "Only personal stories"
        ],
        "answer": "An introduction, body paragraphs and a conclusion"
    }
]

speaking_topics = [
    "Describe a person who has influenced you.",
    "Describe a place you would like to visit.",
    "Describe an important decision you made.",
    "Describe a skill you would like to learn.",
    "Describe a memorable day in your life.",
    "Describe a book or film you enjoyed.",
    "Describe something useful you bought.",
    "Describe a country you would like to live in."
]

vocabulary = [
    ("significant", "重要的", "The government made a significant investment."),
    ("contribute", "贡献", "Education can contribute to economic growth."),
    ("consequence", "后果", "Every decision has consequences."),
    ("environment", "环境", "We should protect the environment."),
    ("beneficial", "有益的", "Exercise is beneficial to our health."),
    ("essential", "必要的", "Good communication is essential."),
    ("increase", "增加", "The number of students has increased."),
    ("decline", "下降", "The birth rate has declined."),
    ("maintain", "维持", "It is difficult to maintain a balance."),
    ("opportunity", "机会", "Education provides more opportunities.")
]

# ---------- Sidebar ----------
st.sidebar.title("🎓 Simon IELTS")

page = st.sidebar.radio(
    "Menu",
    [
        "🏠 Home",
        "📖 Reading",
        "🎧 Listening",
        "✍️ Writing",
        "🗣️ Speaking",
        "📚 Vocabulary",
        "📝 Mock Test",
        "📊 My Progress"
    ]
)

# ---------- Home ----------
if page == "🏠 Home":

    st.markdown(
        '<div class="main-title">Simon IELTS 🎓</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Complete IELTS Practice Platform</div>',
        unsafe_allow_html=True
    )

    st.write("")
    st.success("Welcome! Let's improve your IELTS score step by step.")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Reading", "4.0", "Target 6.5")

    with col2:
        st.metric("Listening", "4.5", "Target 6.5")

    with col3:
        st.metric("Writing", "5.5", "Target 6.5")

    with col4:
        st.metric("Speaking", "5.5", "Target 6.5")

    st.divider()

    st.subheader("🚀 Start Practising")

    a, b = st.columns(2)

    with a:
        st.info("""
        ### 📖 Reading
        Practise reading questions and improve your accuracy.
        """)

        st.info("""
        ### 🎧 Listening
        Train your listening comprehension and vocabulary.
        """)

    with b:
        st.info("""
        ### ✍️ Writing
        Practise Task 1 and Task 2 with IELTS-style questions.
        """)

        st.info("""
        ### 🗣️ Speaking
        Practise Part 1, Part 2 and Part 3 questions.
        """)

# ---------- Reading ----------
elif page == "📖 Reading":

    st.title("📖 IELTS Reading Practice")

    st.write("Choose the best answer for each question.")

    score = 0

    for i, q in enumerate(reading_questions):

        st.subheader(f"Question {i + 1}")

        answer = st.radio(
            q["question"],
            q["options"],
            key=f"reading_{i}"
        )

        if st.button(f"Check Question {i + 1}", key=f"check_{i}"):

            if answer == q["answer"]:
                st.success("✅ Correct!")
                score += 1
            else:
                st.error(f"❌ Incorrect. Correct answer: {q['answer']}")

    st.divider()

    st.caption(
        "Tip: Don't translate every word. Focus on keywords and meaning."
    )

# ---------- Listening ----------
elif page == "🎧 Listening":

    st.title("🎧 IELTS Listening")

    st.info(
        "The listening section will be expanded with audio files and "
        "full IELTS-style tests in the next version."
    )

    st.subheader("Listening Strategy")

    strategies = [
        "Read the questions before the audio starts.",
        "Underline important keywords.",
        "Pay attention to numbers, names and dates.",
        "Do not panic if you miss one answer.",
        "Check spelling carefully."
    ]

    for strategy in strategies:
        st.write("✅", strategy)

# ---------- Writing ----------
elif page == "✍️ Writing":

    st.title("✍️ IELTS Writing")

    task = st.selectbox(
        "Choose a task",
        ["Task 1", "Task 2"]
    )

    if task == "Task 1":

        st.subheader("IELTS Academic Task 1")

        st.write("""
        The chart below shows changes in the number of people using
        different forms of transportation.
        """)

        st.text_area(
            "Write your answer here:",
            height=300
        )

        st.button("Submit Writing")

        st.caption(
            "Target: at least 150 words."
        )

    else:

        st.subheader("IELTS Writing Task 2")

        topic = st.selectbox(
            "Choose a topic",
            [
                "Technology",
                "Education",
                "Environment",
                "Health",
                "Government",
                "Work",
                "Society"
            ]
        )

        questions = {
            "Technology":
            "Some people think technology makes life easier. "
            "To what extent do you agree or disagree?",

            "Education":
            "Some people believe university education should be free. "
            "To what extent do you agree or disagree?",

            "Environment":
            "Environmental problems are becoming increasingly serious. "
            "What are the causes and solutions?",

            "Health":
            "Many people today live unhealthy lifestyles. "
            "What are the causes and what can be done?",

            "Government":
            "Governments should spend more money on public services "
            "than on the arts. To what extent do you agree?",

            "Work":
            "Some people prefer working from home. "
            "Discuss the advantages and disadvantages.",

            "Society":
            "Some people believe modern society is becoming less friendly. "
            "Do you agree or disagree?"
        }

        st.info(questions[topic])

        essay = st.text_area(
            "Write your essay:",
            height=450
        )

        word_count = len(essay.split())

        st.write(f"**Word count: {word_count}**")

        if word_count >= 250:
            st.success("✅ Good length for Task 2.")
        elif word_count > 0:
            st.warning("⚠️ Try to reach at least 250 words.")

        st.button("Submit Essay")

# ---------- Speaking ----------
elif page == "🗣️ Speaking":

    st.title("🗣️ IELTS Speaking")

    part = st.selectbox(
        "Choose Speaking Part",
        ["Part 1", "Part 2", "Part 3"]
    )

    if part == "Part 1":

        topics = [
            "Do you enjoy studying English?",
            "What do you usually do in your free time?",
            "Do you like travelling?",
            "What kind of music do you enjoy?",
            "Do you prefer studying alone or with others?"
        ]

        st.subheader("Part 1 Questions")

        for question in topics:
            st.write("•", question)

    elif part == "Part 2":

        st.subheader("Part 2 Cue Card")

        topic = random.choice(speaking_topics)

        st.info(topic)

        st.write("⏱️ Preparation time: 1 minute")
        st.write("🗣️ Speaking time: 1–2 minutes")

        if st.button("New Topic"):
            st.rerun()

    else:

        st.subheader("Part 3 Discussion")

        questions = [
            "Why do people travel more nowadays?",
            "How has technology changed education?",
            "What makes a good teacher?",
            "Should governments invest more in education?",
            "How might society change in the future?"
        ]

        for question in questions:
            st.write("•", question)

# ---------- Vocabulary ----------
elif page == "📚 Vocabulary":

    st.title("📚 IELTS Vocabulary")

    search = st.text_input("Search vocabulary")

    for word, meaning, example in vocabulary:

        if not search or search.lower() in word.lower():

            with st.container(border=True):

                st.subheader(word)

                st.write(f"**中文：** {meaning}")
                st.write(f"**Example:** {example}")

# ---------- Mock Test ----------
elif page == "📝 Mock Test":

    st.title("📝 IELTS Mini Mock Test")

    st.write(
        "This mini test gives you a quick estimate of your current performance."
    )

    questions = reading_questions

    answers = []

    for i, q in enumerate(questions):

        answer = st.radio(
            f"{i + 1}. {q['question']}",
            q["options"],
            key=f"mock_{i}"
        )

        answers.append(answer)

    if st.button("Submit Mock Test"):

        score = sum(
            answers[i] == questions[i]["answer"]
            for i in range(len(questions))
        )

        st.success(
            f"You scored {score}/{len(questions)}"
        )

        if score == len(questions):
            st.balloons()
            st.write("🔥 Excellent!")

        elif score >= 2:
            st.write("👍 Good job! Keep practising.")

        else:
            st.write("💪 Keep practising. You will improve.")

# ---------- Progress ----------
elif page == "📊 My Progress":

    st.title("📊 My IELTS Progress")

    st.subheader("Current Scores")

    scores = {
        "Listening": 4.5,
        "Reading": 4.0,
        "Writing": 5.5,
        "Speaking": 5.5
    }

    for skill, score in scores.items():

        st.write(f"### {skill}")

        st.progress(score / 9)

        st.write(f"Band {score}")

    st.divider()

    st.subheader("🎯 Target")

    st.write("Overall target: **Band 6.5**")

    st.info(
        "Keep practising every day. Consistency matters more than "
        "studying for many hours once in a while."
    )

st.sidebar.divider()
st.sidebar.caption("Simon IELTS • Built with Streamlit")