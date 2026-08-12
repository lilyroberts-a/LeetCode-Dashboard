from services.problems import *
from services.leetcode_api import *

from services.analytics import *

#username = input("Enter your username: ")


profile = LeetCodeAPI(username="lilyroberts_99")
client_profile_json = profile.get_profile()
language_stats_json = profile.get_language_stats()
problem_stats_json = profile.get_problem_stats()
streak_json = profile.get_streak_info()
skill_stats = profile.get_skill_stats()
total_qs = profile.get_total_questions()

analytics = QuestionAnalytics(username="lilyroberts_99")

calendar_info_json = profile.get_profile_calendar()
#print(total_qs)
#new = analytics.difficulty_by_topic(total_qs)


calendar, solved_difficulty, streak = analytics.overall_progress(problem_stats_json, calendar_info_json, streak_json)
##

#print(progress)

#print(topic_analysis)
#stats = analytics.solved_topic_difficulty(total_qs)
#print(stats)

#proportions = analytics.proportions(total_qs, skill_stats, problem_stats_json)
#print(proportions)
#print(new)
#print(problem_stats_json)
#solved = profile.get_solved_questions()
#print(solved)
solved_data = profile.get_solved_questions()

solved_questions = solved_data["data"]["recentAcSubmissionList"]

new = analytics.difficulty_by_topic(
    total_qs,
    solved_questions
)

print(new)