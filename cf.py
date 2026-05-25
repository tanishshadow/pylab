from collections import Counter

import matplotlib.pyplot as plt
import requests
import streamlit as st


CF_API = "https://codeforces.com/api"

TOPIC_ALIASES = {
    "arrays": {"array", "implementation"},
    "dp": {"dp", "dynamic programming"},
    "graphs": {"graphs", "graph", "dfs and similar", "dsu", "shortest paths"},
    "binary search": {"binary search", "ternary search"},
    "greedy": {"greedy"},
}


def fetch_cf(endpoint, params):
    try:
        response = requests.get(f"{CF_API}/{endpoint}", params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as exc:
        raise RuntimeError(f"Codeforces API error: {exc}") from exc

    if data.get("status") != "OK":
        raise RuntimeError(data.get("comment", "Could not load Codeforces data."))

    return data["result"]


def get_profile(handle):
    user = fetch_cf("user.info", {"handles": handle})[0]
    return {
        "rating": user.get("rating", 0),
        "max_rating": user.get("maxRating", 0),
        "rank": user.get("rank", "Unrated").title(),
    }


def get_rating_history(handle):
    return fetch_cf("user.rating", {"handle": handle})


def get_submissions(handle):
    return fetch_cf("user.status", {"handle": handle})


def summarize_submissions(submissions):
    solved = set()
    tag_counter = Counter()
    difficulty_counter = Counter()

    for submission in submissions:
        if submission.get("verdict") != "OK":
            continue

        problem = submission.get("problem", {})
        problem_key = (
            problem.get("contestId"),
            problem.get("index"),
            problem.get("name"),
        )
        if problem_key in solved:
            continue

        solved.add(problem_key)

        for tag in problem.get("tags", []):
            tag_counter[tag.lower()] += 1

        rating = problem.get("rating")
        if rating:
            lower = (rating // 200) * 200
            difficulty_counter[f"{lower}-{lower + 200}"] += 1

    return tag_counter, difficulty_counter


def topic_strengths(tags):
    strengths = {}
    for display_name, aliases in TOPIC_ALIASES.items():
        strengths[display_name] = sum(tags.get(alias, 0) for alias in aliases)
    return strengths


def weak_topics(strengths):
    weak = []
    if strengths.get("graphs", 0) < 5:
        weak.append("Graphs")
    if strengths.get("dp", 0) < 5:
        weak.append("Dynamic Programming")
    return weak


def draw_rating_graph(history):
    fig, ax = plt.subplots(figsize=(8, 4))
    ratings = [contest["newRating"] for contest in history]
    contests = list(range(1, len(ratings) + 1))

    ax.plot(contests, ratings, marker="o", linewidth=2)
    ax.set_title("Codeforces Rating History")
    ax.set_xlabel("Contest")
    ax.set_ylabel("Rating")
    ax.grid(True, alpha=0.25)

    return fig


def draw_difficulty_graph(values):
    fig, ax = plt.subplots(figsize=(8, 4))
    labels = list(values.keys())
    counts = list(values.values())

    ax.bar(labels, counts)
    ax.set_title("Codeforces Difficulty Distribution")
    ax.set_ylabel("Solved")
    ax.tick_params(axis="x", rotation=35)

    return fig


st.set_page_config(page_title="Codeforces Analytics", layout="wide")
st.title("Codeforces Analytics")

with st.form("cf_handle_form"):
    handle = st.text_input("Codeforces handle")
    analyze = st.form_submit_button("Analyze")

if analyze:
    if not handle:
        st.warning("Enter a Codeforces handle.")
        st.stop()

    try:
        handle = handle.strip()
        with st.spinner("Fetching Codeforces data..."):
            profile = get_profile(handle)
            history = get_rating_history(handle)
            submissions = get_submissions(handle)
            tags, difficulties = summarize_submissions(submissions)
            strengths = topic_strengths(tags)

        st.header("Profile Overview")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Rating", profile["rating"])
        col2.metric("Max", profile["max_rating"])
        col3.metric("Rank", profile["rank"])
        col4.metric("Contests", len(history))

        st.header("Rating Graph")
        if history:
            st.pyplot(draw_rating_graph(history))
        else:
            st.info("No contest history found.")

        st.header("Difficulty Distribution")
        if difficulties:
            sorted_difficulties = dict(
                sorted(difficulties.items(), key=lambda item: int(item[0].split("-")[0]))
            )
            st.pyplot(draw_difficulty_graph(sorted_difficulties))
        else:
            st.info("No rated solved problems found.")

        st.header("Basic Topic Strengths")
        for topic, count in strengths.items():
            st.write(f"{topic.title()}: {count}")

        st.header("Weak Areas")
        weak = weak_topics(strengths)
        if weak:
            for topic in weak:
                st.write(f"- {topic}")
        else:
            st.success("No weak areas found by the simple rules.")

    except RuntimeError as exc:
        st.error(str(exc))
