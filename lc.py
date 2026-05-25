import matplotlib.pyplot as plt
import requests
import streamlit as st


LC_GRAPHQL = "https://leetcode.com/graphql"


def get_profile(username):
    query = """
    query userProfile($username: String!) {
      matchedUser(username: $username) {
        username
        submitStatsGlobal {
          acSubmissionNum {
            difficulty
            count
          }
        }
      }
    }
    """

    try:
        response = requests.post(
            LC_GRAPHQL,
            json={"query": query, "variables": {"username": username}},
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as exc:
        raise RuntimeError(f"LeetCode API error: {exc}") from exc

    user = data.get("data", {}).get("matchedUser")
    if not user:
        raise RuntimeError("Could not load LeetCode profile.")

    solved = {"All": 0, "Easy": 0, "Medium": 0, "Hard": 0}
    for item in user["submitStatsGlobal"]["acSubmissionNum"]:
        solved[item["difficulty"]] = item["count"]

    return {
        "username": user["username"],
        "total": solved["All"],
        "easy": solved["Easy"],
        "medium": solved["Medium"],
        "hard": solved["Hard"],
    }


def draw_difficulty_graph(profile):
    fig, ax = plt.subplots(figsize=(7, 4))
    labels = ["Easy", "Medium", "Hard"]
    counts = [profile["easy"], profile["medium"], profile["hard"]]

    ax.bar(labels, counts, color=["#22c55e", "#f59e0b", "#ef4444"])
    ax.set_title("LeetCode Difficulty Distribution")
    ax.set_ylabel("Solved")

    return fig


st.set_page_config(page_title="LeetCode Analytics", layout="centered")
st.title("LeetCode Analytics")

with st.form("lc_username_form"):
    username = st.text_input("LeetCode username")
    analyze = st.form_submit_button("Analyze")

if analyze:
    if not username:
        st.warning("Enter a LeetCode username.")
        st.stop()

    try:
        with st.spinner("Fetching LeetCode data..."):
            profile = get_profile(username.strip())

        st.header("Profile Overview")
        col1, col2 = st.columns(2)
        col1.metric("Solved", profile["total"])
        col2.metric("Username", profile["username"])

        col1, col2, col3 = st.columns(3)
        col1.metric("Easy", profile["easy"])
        col2.metric("Medium", profile["medium"])
        col3.metric("Hard", profile["hard"])

        st.header("Difficulty Distribution")
        st.pyplot(draw_difficulty_graph(profile))

    except RuntimeError as exc:
        st.error(str(exc))
