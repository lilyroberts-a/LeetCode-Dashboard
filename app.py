from flask import Flask, render_template, request

from services.analytics import QuestionAnalytics
from services.leetcode_api import LeetCodeAPI

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analytics")
def analytics():

    username = request.args.get("username")

    profile = LeetCodeAPI(username)
    analytics = QuestionAnalytics(username)

    #client_profile = profile.get_profile()
    #language_stats = profile.get_language_stats()
    problem_stats = profile.get_problem_stats()
    streak = profile.get_streak_info()
    skill_stats = profile.get_skill_stats()
    total_questions, count = profile.get_total_questions()
    calendar_info = profile.get_profile_calendar()

    solved_data = profile.get_solved_questions()
    solved_questions = solved_data["data"]["recentAcSubmissionList"]
    print(count)
    




    calendar, solved_difficulty, streak = analytics.overall_progress(
        problem_stats,
        calendar_info,
        streak
    )

    difficulty_proportions, topic_proportions = analytics.proportions(
        total_questions,
        skill_stats,
        problem_stats
    )

    difficulty_counts, topic_counts = analytics.qs_by_topic_and_difficulty(
        total_questions
    )

    difficulty_by_topic = analytics.difficulty_by_topic(
        total_questions,
        solved_questions
    )

    topics_solved = len(difficulty_by_topic)
    total_topics = len(topic_counts)



    return render_template(
        "analytics.html",
        calendar=calendar,
        difficulty_proportions=difficulty_proportions,
        difficulty=solved_difficulty,
        topic_proportions=topic_proportions,
        streak=streak,
        questions_by_day=calendar,
        difficulty_by_topic=difficulty_by_topic,
        topic_counts=topic_counts,
        difficulty_counts=difficulty_counts,
        topics_solved=topics_solved,
        total_topics=total_topics,
        total_questions=len(total_questions)

    )


if __name__ == "__main__":
    app.run(debug=True)