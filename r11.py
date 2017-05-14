data_set = {
    'Lisa Rose': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'Superman Returns': 3.5,
        'You, Me and Dupree': 2.5,
        'The Night Listener': 3.0
    },
    'Gene Seymour': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 1.5,
        'Superman Returns': 5.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 3.5
    },
    'Michael Phillips': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.0,
        'Superman Returns': 3.5,
        'The Night Listener': 4.0
    },
    'Claudia Puig': {
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'The Night Listener': 4.5,
        'Superman Returns': 4.0,
        'You, Me and Dupree': 2.5
    },
    'Mick LaSalle': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'Just My Luck': 2.0,
        'Superman Returns': 3.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 2.0
    },
    'Jack Matthews': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'The Night Listener': 3.0,
        'Superman Returns': 5.0,
        'You, Me and Dupree': 3.5
    },
    'Toby': {
        'Snakes on a Plane':4.5,
        'You, Me and Dupree':1.0,
        'Superman Returns':4.0
    }
}
import math
def euclidean_distance_my(preferences, person1, person2):
    shared_items = dict()
    score = 0
    for i in preferences[person1]:
        if i in preferences[person2]:
            shared_items[i] = 1
    if len(shared_items) != 0:
        sum_of_squares = 0
        for i in preferences[person1]:
            if i in preferences[person2]:
                sum_of_squares += (preferences[person1][i] - preferences[person2][i]) ** 2
        # print(sum_of_squares)
        score = 1 / (1 + sum_of_squares)
    return score


def pearson_correlation_score(preferences, person1, person2):
    shared_items = dict()
    score = 0
    for i in preferences[person1]:
        if i in preferences[person2]:
            shared_items[i] = 1
    n = len(shared_items)
    if n != 0:
        sum1, sum2 = 0, 0
        for i in shared_items:
            sum1 += preferences[person1][i]
            sum2 += preferences[person2][i]
        sum1_square, sum2_square = 0, 0
        for i in shared_items:
            sum1_square += preferences[person1][i] ** 2
            sum2_square += preferences[person2][i] ** 2
        sum_of_products = 0
        for i in shared_items:
            sum_of_products += (preferences[person1][i] * preferences[person2][i])
        numerator = sum_of_products - (sum1 * sum2) / n
        denominator = math.sqrt((sum1_square - (sum1 ** 2) / n) * (sum2_square - (sum2 ** 2) / n))
        if denominator != 0:
            score = numerator / denominator
    return score


def top_matches(preferences, person, number=5, similarity_metric=pearson_correlation_score):
    scores = list()
    for i in preferences:
        if i != person:
            scores.append((similarity_metric(preferences, person, i), i))
    scores.sort()
    scores.reverse()
    scores = scores[:number]
    return scores


def get_recommendations(preferences, person, similarity_metric=pearson_correlation_score):

    total, similarity_sum, rankings = dict(), dict(), list()
    for i in preferences:
        if i != person:
            similarity = similarity_metric(preferences, person, i)
            if similarity > 0:
                for j in preferences[i]:
                    if j not in preferences[person] or preferences[person][j] == 0:
                        total.setdefault(j, 0)
                        total[j] += preferences[i][j] * similarity
                        similarity_sum.setdefault(j, 0)
                        similarity_sum[j] += similarity
    for key, value in total.items():
        rankings.append((value / similarity_sum[key], key))
    rankings.sort()
    rankings.reverse()
    return rankings

def loadML(path1='u.item',path2='u.data'):
    movies={}
    for line in open(path1):
        (id,title)=line.split('|')[0:2]
        movies[id]=title

    preferences={}
    for line in open(path2):
        (user,movieid,rating,ts)=line.split('\t')
        preferences.setdefault(user,{})
        preferences[user][movies[movieid]]=float(rating)
    return preferences
preferences=loadML()
print(preferences['87'])
print(get_recommendations(preferences,'101')[0:15])
