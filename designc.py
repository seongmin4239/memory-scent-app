import streamlit as st

st.set_page_config(page_title="기억 기반 향수 추천", layout="centered")

# 세션 초기화
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.answers = {}

# 단계별 질문 데이터
questions = [
    {
        "key": "emotion",
        "title": "1단계: 지금 떠오르는 감정은 무엇인가요?",
        "options": ["기쁨", "슬픔", "그리움", "설렘", "평온함", "분노", "불안"]
    },
    {
        "key": "time",
        "title": "2단계: 그 기억은 언제였나요?",
        "options": ["아침", "낮", "저녁", "밤"]
    },
    {
        "key": "person",
        "title": "3단계: 그 기억 속 함께한 사람은 누구였나요?",
        "options": ["혼자", "친구", "연인", "가족", "낯선 사람"]
    },
    {
        "key": "place",
        "title": "4단계: 그 기억은 어디에서 있었나요?",
        "options": ["자연", "도시", "실내 공간", "교통수단", "바닷가", "산", "학교", "카페"]
    },
    {
        "key": "core",
        "title": "5단계: 그 감정의 핵심은 무엇인가요?",
        "options": ["위로", "자유", "두근거림", "회복", "몰입", "도피", "정체성", "기다림"]
    },
    {
        "key": "scent",
        "title": "6단계: 선호하는 향의 무드는 어떤가요?",
        "options": ["가볍고 상큼한", "무겁고 진한", "따뜻하고 부드러운", "차갑고 깔끔한", "달콤하고 중성적인"]
    }
]

# 다음 단계로 이동
def next_step(key, value):
    st.session_state.answers[key] = value
    st.session_state.step += 1

# UI
st.title("✈️ 기억 기반 향수 추천 플랫폼")

# 현재 단계
if st.session_state.step < len(questions):
    q = questions[st.session_state.step]
    st.subheader(q["title"])
    cols = st.columns(3)
    for i, option in enumerate(q["options"]):
        if cols[i % 3].button(option):
            next_step(q["key"], option)
else:
    st.success("향수 추천 결과")
    st.markdown("🎟️ **당신의 기억을 기반으로 추천된 향수는...**")
    st.markdown("### 🧴 Jo Malone English Pear & Freesia")
    st.caption("예시 결과입니다. 나중에 데이터 기반 매칭 로직으로 바꿀 수 있어요.")
    st.markdown("---")
    st.markdown("당신의 선택")
    for key, value in st.session_state.answers.items():
        st.markdown(f"- **{key}**: {value}")

    if st.button("다시 시작하기"):
        st.session_state.step = 0
        st.session_state.answers = {}
