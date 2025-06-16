import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="메타적 기억 기반 향수 추천",
    layout="centered",
)

# 세션 스테이트 초기화
if "step" not in st.session_state:
    st.session_state.update({
        "step": 1,
        "memory_name": "",
        "location": "",
        "time_of_day": "",
        "people": "",
        "emotion": "",
        "top_ratio": 30,
        "mid_ratio": 40,
        "base_ratio": 30
    })

# ❶ 데이터 로드 (엑셀)
@st.cache_data
def load_perfumes():
    return pd.read_excel("디컨_향수List.xlsx")

perfumes = load_perfumes()

# 1단계: 기억 이름 입력하기
if st.session_state.step == 1:
    st.header("1단계: 기억 이름 입력하기")
    name = st.text_input("당신의 기억에 이름을 붙여보세요", value=st.session_state.memory_name)
    if st.button("다음"):
        if name.strip():
            st.session_state.memory_name = name.strip()
            st.session_state.step = 2
        else:
            st.warning("기억 이름을 입력해 주세요.")

# 2단계: 지도에서 장소 선택하기
elif st.session_state.step == 2:
    st.header("2단계: 지도에서 장소 선택하기")
    col1, col2, col3, col4 = st.columns(4)
    for col, loc in zip([col1, col2, col3, col4], ["산", "바다", "도심", "숲"]):
        if col.button(loc):
            st.session_state.location = loc
            st.session_state.step = 3

# 3단계: 시간대 고르기
elif st.session_state.step == 3:
    st.header("3단계: 시간대 고르기")
    times = ["이른 아침", "정오", "해질녘", "깊은 밤"]
    choice = st.selectbox("시간대를 선택하세요", times,
                          index=times.index(st.session_state.time_of_day)
                          if st.session_state.time_of_day in times else 0)
    if st.button("다음"):
        st.session_state.time_of_day = choice
        st.session_state.step = 4

# 4단계: 인원 수 고르기
elif st.session_state.step == 4:
    st.header("4단계: 인원 수 고르기")
    people_opts = ["혼자", "친구", "연인", "가족"]
    choice = st.selectbox("누구와 함께였나요?", people_opts,
                          index=people_opts.index(st.session_state.people)
                          if st.session_state.people in people_opts else 0)
    if st.button("다음"):
        st.session_state.people = choice
        st.session_state.step = 5

# 5단계: 감정 고르기
elif st.session_state.step == 5:
    st.header("5단계: 감정 고르기")
    emotions = ["설렘", "그리움", "평온함", "불안", "두근거림"]
    choice = st.selectbox("어떤 감정이었나요?", emotions,
                          index=emotions.index(st.session_state.emotion)
                          if st.session_state.emotion in emotions else 0)
    if st.button("다음"):
        st.session_state.emotion = choice
        st.session_state.step = 6

# 6단계: 탑·미들·베이스 비율 고르기
elif st.session_state.step == 6:
    st.header("6단계: 탑·미들·베이스 비율 고르기")
    st.markdown("총합이 100이 되도록 비율을 조절하세요.")
    top = st.slider("탑 노트 비율", 0, 100, st.session_state.top_ratio)
    mid = st.slider("미들 노트 비율", 0, 100 - top, st.session_state.mid_ratio)
    base = 100 - top - mid
    st.write(f"베이스 노트 비율: {base}%")
    if st.button("추천 받기"):
        st.session_state.top_ratio = top
        st.session_state.mid_ratio = mid
        st.session_state.base_ratio = base
        st.session_state.step = 7

# 7단계: 추천 결과
else:
    st.header("🎉 추천 향수 결과 🎉")
    st.markdown(f"- **기억 이름:** {st.session_state.memory_name}")
    st.markdown(f"- **장소:** {st.session_state.location}")
    st.markdown(f"- **시간대:** {st.session_state.time_of_day}")
    st.markdown(f"- **함께한 사람:** {st.session_state.people}")
    st.markdown(f"- **감정:** {st.session_state.emotion}")
    st.markdown(f"- **탑·미들·베이스 비율:** {st.session_state.top_ratio}% / {st.session_state.mid_ratio}% / {st.session_state.base_ratio}%")

    # 간단 랜덤 추천 예시
    main = perfumes.sample(1).iloc[0]
    st.subheader(f"추천 향수: {main['브랜드']} - {main['이름']}")
    st.markdown(f"- 주요 노트: {main.get('주향','')}")
    st.markdown(f"- 지속력: {main.get('지속력','')}")

    st.subheader("페어링 향수")
    pair = perfumes.drop(main.name).sample(1).iloc[0]
    st.markdown(f"- {pair['브랜드']} - {pair['이름']} (주요 노트: {pair.get('주향','')})")
