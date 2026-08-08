import requests
import json
import os

class LeetCodeAPI:

    def __init__(self, username):
        self.username = username

        self.url = "https://leetcode.com/graphql"


    def _query(self, query, variables):

        response = requests.post(
            self.url,
            json={
                "query": query,
                "variables": variables
            }
        )
        return response.json()

    def get_profile(self):

        query = """
        query userPublicProfile($username: String!) {
            matchedUser(username: $username) {
                username
                profile {
                    ranking
                    realName
                    countryName
                    company
                    jobTitle
                }
            }
        }
        """

        variables = {
            "username": self.username
        }

        return self._query(query, variables)

    def get_language_stats(self):

        query = """
        query languageStats($username: String!) {
            matchedUser(username: $username) {
                languageProblemCount {
                    languageName
                    problemsSolved
                }
            }
        }
        """

        variables = {
            "username": self.username
        }

        return self._query(query, variables)

    def get_problem_stats(self):

        query = """
        query userProblemsSolved($username: String!) {
            allQuestionsCount {
                difficulty
                count
            }
            matchedUser(username: $username) {
                problemsSolvedBeatsStats {
                    difficulty
                    percentage
                }
                submitStatsGlobal {
                    acSubmissionNum {
                        difficulty
                        count
                    }
                }
                tagProblemCounts {
                    advanced {
                        tagName
                        tagSlug
                        problemsSolved
                    }
                    intermediate {
                        tagName
                        tagSlug
                        problemsSolved
                    }
                    fundamental {
                        tagName
                        tagSlug
                        problemsSolved
                    }
                }
            }
        }
        """

        variables = {
            "username": self.username
        }

        return self._query(query, variables)

    def get_profile_calendar(self):
        query = """
        query userProfileCalendar($username: String!, $year: Int) {
            matchedUser(username: $username) {
                userCalendar(year: $year) {
                activeYears
                streak
                totalActiveDays
                dccBadges {
                    timestamp
                    badge {
                        name
                        icon
                    }
                }
                submissionCalendar
                }
            }
        }
        """
        variables = {
            "username": self.username
        }

        return self._query(query, variables)

    def get_streak_info(self):
        query = """
        query getStreakCounter {
            streakCounter {
                streakCount
                daysSkipped
                currentDayCompleted
            }
        }
        """

        variables = {
            "username": self.username
        }

        return self._query(query, variables)

    def get_skill_stats(self):

        query = """
        query skillStats($username: String!) {
            matchedUser(username: $username) {
                tagProblemCounts {
                    advanced {
                        tagName
                        tagSlug
                        problemsSolved
                    }
                    intermediate {
                        tagName
                        tagSlug
                        problemsSolved
                    }
                    fundamental {
                        tagName
                        tagSlug
                        problemsSolved
                    }
                }
            }
        }
        """

        variables = {
            "username": self.username
        }

        return self._query(query, variables)


    def get_total_questions(self):

        cache_file = "all_questions.json"

        if os.path.exists(cache_file):
            with open(cache_file, "r") as f:
                return json.load(f)

        query = """
        query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
        problemsetQuestionList: questionList(
            categorySlug: $categorySlug
            limit: $limit
            skip: $skip
            filters: $filters
        ) {
            total: totalNum
            questions: data {
            acRate
            difficulty
            isFavor
            status
            title
            titleSlug
            topicTags {
                name
            }
            }
        }
        }
        """

        all_questions = []
        skip = 0
        limit = 100

        while True:

        
            variables = {
                "categorySlug": "",
                "skip": skip,
                "limit": limit,
                "filters":{}
            }

            response = self._query(query, variables)

            data = response["data"]["problemsetQuestionList"]

            questions = data["questions"]

            all_questions.extend(questions)

            if len(all_questions) >= data["total"]:
                break

            skip += limit

            with open(cache_file, "w") as f:
                json.dump(all_questions, f)

        return all_questions