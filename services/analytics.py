from datetime import datetime
import json

class QuestionAnalytics:

    def __init__(self, username):
        self.username = username

    def datetime_conversion(self, problems_by_day):
        calendar = {}

        for timestamp in problems_by_day:
            date = datetime.fromtimestamp(int(timestamp)).strftime("%d/%m/%Y")
            calendar[date] = problems_by_day[timestamp]

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



class SplittingTags:

    def __init__(self, difficulty):
        self.difficulty = difficulty

        self.dict = {}

    def splitting(self):

        for mini_dict in self.difficulty:
            self.dict[mini_dict["tagName"]] = mini_dict["problemsSolved"]

        return self.dict

        
