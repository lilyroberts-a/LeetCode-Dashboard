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

progress = analytics.overall_progress(problem_stats_json, calendar_info_json, streak_json)


#print(progress)

#print(topic_analysis)
#stats = analytics.solved_topic_difficulty(total_qs)
#print(stats)

proportions = analytics.proportions(total_qs, skill_stats, problem_stats_json)
print(proportions)
