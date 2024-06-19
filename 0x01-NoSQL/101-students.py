#!/usr/bin/env python3

"""Returns all students sorted by average score"""

def top_students(mongo_collection):
    """
    Returns all students sorted by average score.
    
    :param mongo_collection: pymongo collection object
    :return: list of students with their average score, sorted by average score
    """

    # Calculate the average score for each student and add it as a field 'averageScore'
    students = mongo_collection.aggregate([
        {
            "$project": {
                "name": 1,
                "topics": 1,
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {
            "$sort": {
                "averageScore": -1
            }
        }
    ])
    
    return students
