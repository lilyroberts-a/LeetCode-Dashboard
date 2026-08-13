from datetime import datetime, timedelta
import json

from collections import defaultdict

class QuestionAnalytics:

    def __init__(self, username):
        self.username = username

    def datetime_conversion(self, problems_by_day):

        calendar = {}

        for timestamp in problems_by_day:
            date_string = datetime.fromtimestamp(
                int(timestamp)
            ).strftime("%d/%m/%Y")

            calendar[date_string] = problems_by_day[timestamp]

        if calendar:

            start_date = datetime.strptime(
                min(
                    calendar.keys(),
                    key=lambda x: datetime.strptime(x, "%d/%m/%Y")
                ),
                "%d/%m/%Y"
            ).date()

            end_date = datetime.today().date()

            current_date = start_date

            while current_date <= end_date:

                date_string = current_date.strftime("%d/%m/%Y")

                if date_string not in calendar:
                    calendar[date_string] = 0

                current_date += timedelta(days=1)

        calendar = dict(sorted(
            calendar.items(),
            key=lambda x: datetime.strptime(x[0], "%d/%m/%Y")
        ))

        return calendar

    def get_solved_counts(self, problem_stats_json):
        solved = problem_stats_json["data"]["matchedUser"]["submitStatsGlobal"]["acSubmissionNum"]

        return {
        "All": solved[0]["count"],
        "Easy": solved[1]["count"],
        "Medium": solved[2]["count"],
        "Hard": solved[3]["count"]
    }

    def overall_progress(self, problem_stats_json, calendar_info_json, streak_json):

        solved_difficulty = self.get_solved_counts(problem_stats_json)

        

        problems_by_day = calendar_info_json["data"]["matchedUser"]["userCalendar"]["submissionCalendar"]

        problems_by_day = json.loads(problems_by_day)

        streak = streak_json["data"]#["streakCounter"]

        calendar = self.datetime_conversion(problems_by_day)

        return(calendar, solved_difficulty, streak)

    def skill_analysis(self, skill_stats):

        #number of topic tags completed by difficulty

        advanced_tagnames = skill_stats["data"]["matchedUser"]["tagProblemCounts"]["advanced"]
        intermediate_tagnames = skill_stats["data"]["matchedUser"]["tagProblemCounts"]["intermediate"]
        fundamental_tagnames = skill_stats["data"]["matchedUser"]["tagProblemCounts"]["fundamental"]

        advanced = SplittingTags(difficulty=advanced_tagnames)
        advanced_skills = advanced.splitting()

        intermediate = SplittingTags(difficulty=intermediate_tagnames)
        intermediate_skills = intermediate.splitting()

        fundamental = SplittingTags(difficulty=fundamental_tagnames)
        fundamental_skills = fundamental.splitting()

        dicts = (advanced_skills, intermediate_skills, fundamental_skills)
        combined = {}

        #total number of topics completed combined
        for dictionary in dicts:
            for key, value in dictionary.items():
                combined[key] = combined.get(key, 0) + value


        return combined, advanced_skills, intermediate_skills, fundamental_skills


    def proportions(self, total_qs, skill_stats, problem_stats_json):

        total_difficulty_counts, total_topic_counts = self.qs_by_topic_and_difficulty(total_qs)

        total_difficulty_counts["All"] = len(total_qs)

        completed_topic_combined, advanced_skills, intermediate_skills, fundamental_skills  = self.skill_analysis(skill_stats)

        solved_difficulty = self.get_solved_counts(problem_stats_json)

        dif_prop = {}

        for key in solved_difficulty:
            dif_prop[key] = round((solved_difficulty[key]/ total_difficulty_counts[key])*100, 2)

        topic_prop = {}

        for key in completed_topic_combined:
            topic_prop[key] = round((completed_topic_combined[key] / total_topic_counts[key])*100, 2)


        return dif_prop, topic_prop

    def qs_by_topic_and_difficulty(self, total_qs):

        difficulty_counts = {}
        topic_counts = {}

        for question in total_qs:

            # total questions by difficulty
            difficulty = question["difficulty"]
            difficulty_counts[difficulty] = difficulty_counts.get(difficulty, 0) + 1

            # total topic tags
            for tag in question["topicTags"]:
                topic = tag["name"]
                topic_counts[topic] = topic_counts.get(topic, 0) + 1

        return difficulty_counts, topic_counts

    def difficulty_by_topic(self, total_qs, solved_questions):

        # Get the slugs of solved questions
        solved_slugs = {
            question["titleSlug"]
            for question in solved_questions
        }

        difficulty_by_topic = defaultdict(lambda: {
            "Easy": 0,
            "Medium": 0,
            "Hard": 0
        })

        for question in total_qs:

            if question["titleSlug"] not in solved_slugs:
                continue

            difficulty = question["difficulty"]

            for topic in question["topicTags"]:
                topic_name = topic["name"]

                difficulty_by_topic[topic_name][difficulty] += 1

        return dict(difficulty_by_topic)

            


class SplittingTags:

    def __init__(self, difficulty):
        self.difficulty = difficulty

        self.dict = {}

    def splitting(self):

        for mini_dict in self.difficulty:
            self.dict[mini_dict["tagName"]] = mini_dict["problemsSolved"]

        return self.dict

        
