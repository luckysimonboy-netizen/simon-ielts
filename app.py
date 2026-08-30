import streamlit as st
import random
import time
from datetime import date, datetime

# =========================
# IELTS MASTER V4
# =========================

st.set_page_config(
    page_title="IELTS Master V4",
    page_icon="🎓",
    layout="wide"
)

# ---------- Session ----------
defaults = {
    "page": "Dashboard",
    "name": "",
    "goal": 6.5,
    "bands": {},
    "history": [],
    "mistakes": [],
    "timer_end": None,
    "streak": 0,
    "last_day": None,
    "writing_count": 0,
    "speaking_count": 0,
    "vocab_score": 0,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ---------- Functions ----------
def mark_study():
    today = date.today().isoformat()

    if st.session_state.last_day != today:
        st.session_state.streak += 1
        st.session_state.last_day = today


def start_timer(minutes):
    st.session_state.timer_end = time.time() + minutes * 60


def show_timer():
    if st.session_state.timer_end is None:
        return

    remaining = max(
        0,
        int(st.session_state.timer_end - time.time())
    )

    if remaining == 0:
        st.session_state.timer_end = None
        st.error("⏰ Time is up!")
    else:
        minutes = remaining // 60
        seconds = remaining % 60

        st.warning(
            f"⏱️ Time remaining: "
            f"**{minutes:02d}:{seconds:02d}**"
        )


def estimate_band(correct, total):
    if total == 0:
        return 0

    ratio = correct / total

    if ratio >= 0.95:
        return 9.0
    elif ratio >= 0.90:
        return 8.5
    elif ratio >= 0.80:
        return 7.5
    elif ratio >= 0.70:
        return 6.5
    elif ratio >= 0.60:
        return 6.0
    elif ratio >= 0.50:
        return 5.5
    elif ratio >= 0.40:
        return 5.0
    elif ratio >= 0.30:
        return 4.5
    else:
        return 4.0


def save_result(skill, score, detail):
    st.session_state.bands[skill] = score

    st.session_state.history.append({
        "Time": datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        ),
        "Skill": skill,
        "Band": score,
        "Detail": detail
    })


# =========================
# DATA
# =========================

READING = [
    {
        "title": "Urban Green Spaces",
        "text": """
Urban parks have changed considerably over the last two centuries.

Early public parks were often created to provide attractive scenery
and cleaner air for residents of crowded industrial cities.

Today, urban green spaces have a much wider purpose.

Trees can lower surface temperatures and provide shade.
Plants may help manage rainwater and create habitats for insects
and birds.

Parks can also encourage walking, exercise and social interaction.

However, parks require funding and maintenance.
Attractive green areas may sometimes be followed by rising
property prices.

Modern planning therefore considers accessibility and inclusion.
        """,
        "questions": [
            {
                "q": "Early parks were partly created to provide:",
                "options": [
                    "Cleaner air and scenery",
                    "Factories",
                    "Shopping centres",
                    "Private housing"
                ],
                "answer": 0
            },
            {
                "q": "Trees can help:",
                "options": [
                    "Increase traffic",
                    "Lower surface temperatures",
                    "Remove parks",
                    "Increase pollution"
                ],
                "answer": 1
            },
            {
                "q": "Parks can encourage:",
                "options": [
                    "Exercise",
                    "Factory work",
                    "Traffic",
                    "Higher pollution"
                ],
                "answer": 0
            },
            {
                "q": "A possible problem is:",
                "options": [
                    "Rising property prices",
                    "Less sunlight",
                    "More factories",
                    "Fewer buildings"
                ],
                "answer": 0
            },
            {
                "q": "Modern planning considers:",
                "options": [
                    "Accessibility",
                    "Cars only",
                    "Factories only",
                    "Private ownership only"
                ],
                "answer": 0
            }
        ]
    },

    {
        "title": "Public Transport",
        "text": """
Cities are investing in public transport as populations grow.

Rail systems, buses and cycling networks can move large numbers
of people while using less urban space than private cars.

Infrastructure is expensive and new rail lines can take years
to build.

Nevertheless, reliable transport can create long-term economic
benefits by connecting workers with employment and reducing
congestion.

Technology is changing transport too.

Real-time information helps passengers plan journeys, while
electronic ticketing can reduce queues.
        """,
        "questions": [
            {
                "q": "Public transport can use less space than:",
                "options": [
                    "Private cars",
                    "Walking",
                    "Cycling",
                    "Trains"
                ],
                "answer": 0
            },
            {
                "q": "Infrastructure can be:",
                "options": [
                    "Free",
                    "Expensive",
                    "Unnecessary",
                    "Temporary"
                ],
                "answer": 1
            },
            {
                "q": "Reliable transport can:",
                "options": [
                    "Reduce congestion",
                    "Increase pollution",
                    "Remove jobs",
                    "Stop technology"
                ],
                "answer": 0
            },
            {
                "q": "Real-time information helps passengers:",
                "options": [
                    "Plan journeys",
                    "Buy houses",
                    "Build trains",
                    "Avoid transport"
                ],
                "answer": 0
            },
            {
                "q": "Electronic ticketing can:",
                "options": [
                    "Increase queues",
                    "Reduce queues",
                    "Remove buses",
                    "Increase pollution"
                ],
                "answer": 1
            }
        ]
    }
]


LISTENING = [
    {
        "title": "Language Centre",
        "transcript": """
The student wants to improve speaking because lectures are easy
to understand but presentations make the student nervous.

A presentation workshop runs on Thursday afternoon.

However, the student has a laboratory class on Thursday.

The adviser recommends a discussion group on Tuesday morning.

Registration closes this Friday.

There is no fee for enrolled students.
        """,
        "questions": [
            {
                "q": "What skill does the student want to improve?",
                "options": [
                    "Speaking",
                    "Reading",
                    "Writing",
                    "Grammar"
                ],
                "answer": 0
            },
            {
                "q": "When is the presentation workshop?",
                "options": [
                    "Monday",
                    "Tuesday",
                    "Thursday afternoon",
                    "Friday"
                ],
                "answer": 2
            },
            {
                "q": "Why can't the student attend?",
                "options": [
                    "Cost",
                    "Laboratory class",
                    "Work",
                    "Travel"
                ],
                "answer": 1
            },
            {
                "q": "When is the discussion group?",
                "options": [
                    "Monday morning",
                    "Tuesday morning",
                    "Thursday afternoon",
                    "Friday morning"
                ],
                "answer": 1
            },
            {
                "q": "When does registration close?",
                "options": [
                    "Today",
                    "Monday",
                    "This Friday",
                    "Next month"
                ],
                "answer": 2
            }
        ]
    }
]


VOCABULARY = [
    ("crucial", "extremely important"),
    ("allocate", "give a particular amount of time or money"),
    ("substantial", "large in amount"),
    ("deteriorate", "become worse"),
    ("enhance", "improve something"),
    ("contribute", "help cause something"),
    ("sustainable", "able to continue without serious harm"),
    ("perspective", "a particular way of viewing something"),
    ("implement", "put a plan into action"),
    ("inevitable", "certain to happen"),
    ("mitigate", "reduce a harmful effect"),
    ("coherent", "logical and well organised"),
]


PART1 = {
    "Study": [
        "What are you studying?",
        "Why did you choose it?",
        "What do you enjoy most about it?"
    ],
    "Hometown": [
        "Where is your hometown?",
        "What do you like about it?",
        "Has it changed much?"
    ],
    "Technology": [
        "What technology do you use every day?",
        "Do you like new technology?",
        "What technology would you like to learn?"
    ]
}


PART2 = [
    "Describe a useful website you often use.",
    "Describe a place you enjoy visiting.",
    "Describe a skill you would like to learn.",
    "Describe an important decision you have made.",
    "Describe a memorable journey."
]


PART3 = [
    "Why do people find change difficult?",
    "How can schools prepare students for future jobs?",
    "Does technology always improve people's lives?",
    "What are the advantages and disadvantages of large cities?"
]


# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.title("🎓 IELTS Master V4")

    st.session_state.name = st.text_input(
        "Your name",
        st.session_state.name
    )

    st.session_state.goal = st.select_slider(
        "Target Band",
        options=[
            5.0,
            5.5,
            6.0,
            6.5,
            7.0,
            7.5,
            8.0,
            8.5,
            9.0
        ],
        value=st.session_state.goal
    )

    st.divider()

    pages = [
        "Dashboard",
        "📖 Reading",
        "🎧 Listening",
        "✍️ Writing",
        "🗣️ Speaking",
        "📚 Vocabulary",
        "📊 Progress",
        "❌ Mistake Book"
    ]

    for page in pages:
        if st.button(
            page,
            use_container_width=True
        ):
            st.session_state.page = page
            st.rerun()

    st.divider()

    st.metric(
        "🔥 Study streak",
        f"{st.session_state.streak} day(s)"
    )


# =========================
# DASHBOARD
# =========================

if st.session_state.page == "Dashboard":

    mark_study()

    st.title("🎓 IELTS Master V4")

    if st.session_state.name:
        st.subheader(
            f"Welcome back, {st.session_state.name} 👋"
        )

    st.write(
        "Your complete IELTS practice dashboard."
    )

    st.divider()

    cols = st.columns(4)

    for col, skill in zip(
        cols,
        ["Reading", "Listening", "Writing", "Speaking"]
    ):
        value = st.session_state.bands.get(
            skill,
            "—"
        )

        col.metric(
            skill,
            value
        )

    st.divider()

    values = list(
        st.session_state.bands.values()
    )

    if values:

        average = sum(values) / len(values)

        st.subheader(
            f"🎯 Current average: {average:.1f}"
        )

        st.progress(
            min(average / 9, 1)
        )

        gap = max(
            0,
            st.session_state.goal - average
        )

        st.write(
            f"Target: **{st.session_state.goal:.1f}**"
        )

        st.write(
            f"Remaining gap: **{gap:.1f}**"
        )

    else:

        st.info(
            "Complete your first practice test "
            "to establish a baseline."
        )

    st.divider()

    st.subheader("🚀 Recommended routine")

    st.write(
        """
        **10 min Reading**
        → **10 min Listening**
        → **10 min Vocabulary**
        → **10 min Speaking**
        """
    )


# =========================
# READING
# =========================

elif st.session_state.page == "📖 Reading":

    mark_study()

    st.title("📖 IELTS Reading")

    passage = st.selectbox(
        "Choose passage",
        READING,
        format_func=lambda x: x["title"]
    )

    if st.button(
        "⏱️ Start 20-minute timer"
    ):
        start_timer(20)

    show_timer()

    st.subheader(
        passage["title"]
    )

    st.write(
        passage["text"]
    )

    st.divider()

    answers = []

    for i, question in enumerate(
        passage["questions"]
    ):

        answer = st.radio(
            f"{i + 1}. {question['q']}",
            question["options"],
            index=None,
            key=f"reading_{passage['title']}_{i}"
        )

        answers.append(answer)

    if st.button(
        "✅ Submit Reading",
        type="primary"
    ):

        correct = 0

        for answer, question in zip(
            answers,
            passage["questions"]
        ):

            if (
                answer
                == question["options"][
                    question["answer"]
                ]
            ):
                correct += 1

        total = len(
            passage["questions"]
        )

        score = estimate_band(
            correct,
            total
        )

        save_result(
            "Reading",
            score,
            f"{correct}/{total}"
        )

        st.success(
            f"Score: **{correct}/{total}**"
        )

        st.success(
            f"Estimated practice Band: **{score}**"
        )

        for answer, question in zip(
            answers,
            passage["questions"]
        ):

            correct_answer = question[
                "options"
            ][question["answer"]]

            if answer != correct_answer:

                st.session_state.mistakes.append(
                    {
                        "skill": "Reading",
                        "question": question["q"],
                        "answer": correct_answer
                    }
                )


# =========================
# LISTENING
# =========================

elif st.session_state.page == "🎧 Listening":

    mark_study()

    st.title("🎧 IELTS Listening")

    section = st.selectbox(
        "Choose section",
        LISTENING,
        format_func=lambda x: x["title"]
    )

    st.info(
        "For realistic practice, use your own recording. "
        "The transcript is available for study."
    )

    audio = st.file_uploader(
        "Upload audio",
        type=[
            "mp3",
            "wav",
            "m4a"
        ]
    )

    if audio:
        st.audio(audio)

    if st.checkbox(
        "Show transcript"
    ):
        st.write(
            section["transcript"]
        )

    st.divider()

    answers = []

    for i, question in enumerate(
        section["questions"]
    ):

        answer = st.radio(
            f"{i + 1}. {question['q']}",
            question["options"],
            index=None,
            key=f"listen_{section['title']}_{i}"
        )

        answers.append(answer)

    if st.button(
        "✅ Submit Listening",
        type="primary"
    ):

        correct = 0

        for answer, question in zip(
            answers,
            section["questions"]
        ):

            if (
                answer
                == question["options"][
                    question["answer"]
                ]
            ):
                correct += 1

        total = len(
            section["questions"]
        )

        score = estimate_band(
            correct,
            total
        )

        save_result(
            "Listening",
            score,
            f"{correct}/{total}"
        )

        st.success(
            f"Score: **{correct}/{total}**"
        )

        st.success(
            f"Estimated practice Band: **{score}**"
        )


# =========================
# WRITING
# =========================

elif st.session_state.page == "✍️ Writing":

    mark_study()

    st.title("✍️ IELTS Writing")

    task = st.selectbox(
        "Choose task",
        [
            "Task 1 — Academic",
            "Task 1 — General Training",
            "Task 2 — Essay"
        ]
    )

    if task == "Task 2 — Essay":

        prompt = """
Some people believe that students should study
only subjects that are useful for their future careers.

Others believe that students should study
a wide range of subjects.

Discuss both views and give your own opinion.
        """

        minimum = 250

    elif task == "Task 1 — Academic":

        prompt = """
The chart below shows changes in the percentage
of people using different forms of transport.

Summarise the main features and make comparisons
where relevant.
        """

        minimum = 150

    else:

        prompt = """
Write a letter to a friend who is visiting your city.

Recommend a place to visit and explain
what they can do there.
        """

        minimum = 150

    st.info(prompt)

    if st.button(
        "⏱️ Start 40-minute timer"
    ):
        start_timer(40)

    show_timer()

    essay = st.text_area(
        "Write your answer",
        height=450,
        placeholder=(
            "Introduction...\n\n"
            "Body paragraph 1...\n\n"
            "Body paragraph 2...\n\n"
            "Conclusion..."
        )
    )

    words = len(
        essay.split()
    )

    st.write(
        f"**Word count: {words}**"
    )

    if st.button(
        "🔎 Analyse writing",
        type="primary"
    ):

        if not essay.strip():

            st.error(
                "Please write something first."
            )

        else:

            st.session_state.writing_count += 1

            paragraphs = [
                x
                for x in essay.split("\n")
                if x.strip()
            ]

            sentences = [
                x
                for x in essay
                .replace("!", ".")
                .replace("?", ".")
                .split(".")
                if x.strip()
            ]

            linking_words = [
                "however",
                "therefore",
                "moreover",
                "furthermore",
                "although",
                "while",
                "whereas",
                "consequently"
            ]

            used = [
                word
                for word in linking_words
                if word in essay.lower()
            ]

            score = 6.0

            if words >= minimum:
                score += 0.5
            else:
                score -= 0.5

            if len(paragraphs) >= 4:
                score += 0.5

            if len(sentences) >= 10:
                score += 0.5

            score = max(
                4.0,
                min(
                    8.0,
                    round(score * 2) / 2
                )
            )

            save_result(
                "Writing",
                score,
                f"{words} words"
            )

            st.success(
                f"Practice estimate: **Band {score}**"
            )

            if words >= minimum:
                st.success(
                    "✅ Word-count target met."
                )
            else:
                st.warning(
                    "⚠️ Your answer is below "
                    "the recommended word count."
                )

            if len(paragraphs) >= 4:
                st.success(
                    "✅ Paragraph structure looks good."
                )
            else:
                st.warning(
                    "⚠️ Develop clearer paragraphs."
                )

            if used:
                st.success(
                    "🔗 Linking words detected: "
                    + ", ".join(used)
                )
            else:
                st.warning(
                    "🔗 Try using more cohesive devices."
                )

            st.info(
                "This is automated practice feedback, "
                "not an official IELTS examiner score."
            )


# =========================
# SPEAKING
# =========================

elif st.session_state.page == "🗣️ Speaking":

    mark_study()

    st.title("🗣️ IELTS Speaking")

    part = st.selectbox(
        "Choose part",
        [
            "Part 1",
            "Part 2",
            "Part 3"
        ]
    )

    if part == "Part 1":

        topic = st.selectbox(
            "Topic",
            list(PART1.keys())
        )

        for question in PART1[topic]:
            st.markdown(
                f"**{question}**"
            )

        st.info(
            "Try to answer each question "
            "for 20–30 seconds."
        )

    elif part == "Part 2":

        prompt = random.choice(
            PART2
        )

        st.subheader(
            "🎫 Cue Card"
        )

        st.write(
            prompt
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "⏱️ 1-minute preparation"
            ):
                start_timer(1)

        with col2:

            if st.button(
                "🗣️ 2-minute speaking"
            ):
                start_timer(2)
                st.session_state.speaking_count += 1

        show_timer()

    else:

        for question in PART3:

            st.markdown(
                f"**{question}**"
            )

        st.info(
            "Aim for 40–60 seconds per answer."
        )

    st.divider()

    st.subheader(
        "📊 Self assessment"
    )

    fluency = st.slider(
        "Fluency",
        1,
        9,
        6
    )

    vocabulary = st.slider(
        "Vocabulary",
        1,
        9,
        6
    )

    grammar = st.slider(
        "Grammar",
        1,
        9,
        6
    )

    pronunciation = st.slider(
        "Pronunciation",
        1,
        9,
        6
    )

    if st.button(
        "Save speaking result"
    ):

        score = round(
            (
                fluency
                + vocabulary
                + grammar
                + pronunciation
            ) / 4 * 2
        ) / 2

        save_result(
            "Speaking",
            score,
            "Self assessment"
        )

        st.success(
            f"Practice Band: **{score}**"
        )


# =========================
# VOCABULARY
# =========================

elif st.session_state.page == "📚 Vocabulary":

    mark_study()

    st.title(
        "📚 IELTS Vocabulary"
    )

    search = st.text_input(
        "Search vocabulary"
    )

    filtered = [
        item
        for item in VOCABULARY
        if (
            not search
            or search.lower() in item[0].lower()
            or search.lower() in item[1].lower()
        )
    ]

    for word, meaning in filtered:

        with st.expander(
            f"**{word}** — {meaning}"
        ):

            st.write(
                f"Example: This is a **{word}** issue."
            )

    st.divider()

    st.subheader(
        "🧠 Vocabulary Quiz"
    )

    word, meaning = random.choice(
        VOCABULARY
    )

    wrong = random.sample(
        [
            item[1]
            for item in VOCABULARY
            if item[0] != word
        ],
        3
    )

    choices = [
        meaning
    ] + wrong

    random.shuffle(
        choices
    )

    answer = st.radio(
        f"What does **{word}** mean?",
        choices,
        index=None
    )

    if st.button(
        "Check answer"
    ):

        if answer == meaning:

            st.success(
                "🎉 Correct!"
            )

        else:

            st.error(
                f"Correct answer: {meaning}"
            )


# =========================
# PROGRESS
# =========================

elif st.session_state.page == "📊 Progress":

    st.title(
        "📊 Progress Centre"
    )

    cols = st.columns(4)

    for col, skill in zip(
        cols,
        [
            "Reading",
            "Listening",
            "Writing",
            "Speaking"
        ]
    ):

        col.metric(
            skill,
            st.session_state.bands.get(
                skill,
                "—"
            )
        )

    st.divider()

    if st.session_state.bands:

        average = sum(
            st.session_state.bands.values()
        ) / len(
            st.session_state.bands
        )

        st.subheader(
            f"Overall practice average: {average:.1f}"
        )

        st.progress(
            min(
                average / 9,
                1
            )
        )

        st.write(
            f"Target Band: **{st.session_state.goal}**"
        )

    if st.session_state.history:

        st.subheader(
            "Practice history"
        )

        st.dataframe(
            st.session_state.history,
            use_container_width=True
        )

        st.line_chart(
            [
                x["Band"]
                for x in st.session_state.history
            ]
        )

    else:

        st.info(
            "Complete some practice first."
        )


# =========================
# MISTAKE BOOK
# =========================

elif st.session_state.page == "❌ Mistake Book":

    st.title(
        "❌ Mistake Book"
    )

    if not st.session_state.mistakes:

        st.success(
            "No mistakes recorded yet. 🎉"
        )

    else:

        st.write(
            f"Total mistakes: "
            f"**{len(st.session_state.mistakes)}**"
        )

        for i, mistake in enumerate(
            reversed(
                st.session_state.mistakes
            ),
            1
        ):

            with st.expander(
                f"{i}. {mistake['skill']}"
            ):

                st.write(
                    "**Question:**",
                    mistake["question"]
                )

                st.write(
                    "**Correct answer:**",
                    mistake["answer"]
                )


# =========================
# FOOTER
# =========================

st.divider()

st.caption(
    "IELTS Master V4 · Independent practice tool · "
    "Not affiliated with IELTS, IDP, British Council or Cambridge."
)