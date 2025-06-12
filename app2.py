# import streamlit as st
# import pandas as pd
# import random
# import time

# # 페이지 설정
# st.set_page_config(page_title="향기로 떠나는 기억 여행", layout="wide")

# @st.cache_data
# def load_data():
#     return pd.read_csv("de_perList.csv", encoding="cp949")

# perfumes = load_data()
# user_choices = {}

# # 카드 버튼 함수
# def big_card(label, key):
#     return st.button(label, key=key)

# # 단계 초기화
# if "step" not in st.session_state:
#     st.session_state.step = 1

# st.title("🛫 향기로 떠나는 기억 여행")

# # GATE 1~6
# if st.session_state.step == 1:
#     st.subheader("Gate 1: 어떤 장면이 기억에 남아있나요?")
#     scenes = ["햇살이 스며드는 방", "비 오는 거리", "숲속 오솔길", "노을진 바닷가"]
#     for i, scene in enumerate(scenes):
#         if big_card(scene, f"scene_{i}"):
#             user_choices["scene"] = scene
#             st.session_state.step += 1

# elif st.session_state.step == 2:
#     st.subheader("Gate 2: 그 기억의 감정은?")
#     emotions = ["설렘", "그리움", "평온함", "고요한 외로움"]
#     for i, emo in enumerate(emotions):
#         if big_card(emo, f"emotion_{i}"):
#             user_choices["emotion"] = emo
#             st.session_state.step += 1

# elif st.session_state.step == 3:
#     st.subheader("Gate 3: 언제의 기억인가요?")
#     times = ["이른 아침", "정오", "해질녘", "깊은 밤"]
#     for i, time in enumerate(times):
#         if big_card(time, f"time_{i}"):
#             user_choices["time"] = time
#             st.session_state.step += 1

# elif st.session_state.step == 4:
#     st.subheader("Gate 4: 누구와 함께였나요?")
#     people = ["혼자", "친구", "연인", "가족"]
#     for i, person in enumerate(people):
#         if big_card(person, f"person_{i}"):
#             user_choices["person"] = person
#             st.session_state.step += 1

# elif st.session_state.step == 5:
#     st.subheader("Gate 5: 그 장소의 느낌은?")
#     places = ["도심", "자연", "해변", "산책로"]
#     for i, place in enumerate(places):
#         if big_card(place, f"place_{i}"):
#             user_choices["place"] = place
#             st.session_state.step += 1

# elif st.session_state.step == 6:
#     st.subheader("Gate 6: 선호하는 향의 톤은?")
#     tones = ["우디", "시트러스", "플로럴", "스파이시"]
#     for i, tone in enumerate(tones):
#         if big_card(tone, f"tone_{i}"):
#             user_choices["tone"] = tone
#             st.session_state.step += 1

# elif st.session_state.step == 7:
#     st.subheader("📦 탑승 준비 완료!")
#     st.markdown("🛫 **당신의 향기 여행을 준비 중입니다...**")

#     with st.spinner("기억을 분석 중..."):
#         st.markdown("---")
#         st.markdown("### ✈️ 당신의 응답 요약:")
#         for key, value in user_choices.items():
#             st.markdown(f"- **{key}**: {value}")
#         time.sleep(5)
#     st.session_state.step += 1

# elif st.session_state.step == 8:
#     st.success("🧳 추천 향수가 도착했습니다!")
#     tone = user_choices.get("tone", "")

#     # 조건에 맞는 향수 필터링
#     filtered = perfumes[perfumes["향조"].str.contains(tone, na=False, case=False)]

#     if filtered.empty:
#         st.warning("조건에 맞는 향수가 없습니다. 다시 시도해주세요.")
#     else:
#         selected = filtered.sample(1).iloc[0]
#         st.markdown(f"### 🎁 추천 향수: {selected['브랜드']} - {selected['이름']}")
#         st.markdown(f"- 🌿 향조: {selected['향조']}")
#         st.markdown(f"- 💧 지속력: {selected['지속력']}")
#         st.markdown(f"- 📦 크기: {selected['크기']} / 무게: {selected['무게']}")
#         st.markdown(f"- 🎨 컬러: {selected['컬러']}")
#         st.markdown(f"- 🧴 사용처: {selected['사용처']}")
#         st.markdown(f"- 🧵 재질: {selected['재질']}")

#         # 페어링 향수 (다른 브랜드 중에서)
#         others = perfumes[perfumes["브랜드"] != selected["브랜드"]]
#         if not others.empty:
#             pair = others.sample(1).iloc[0]
#             st.markdown("---")
#             st.markdown(f"### 🔗 페어링 향수: {pair['브랜드']} - {pair['이름']}")
#             st.markdown(f"- 🌿 향조: {pair['향조']}")








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
