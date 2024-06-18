#!/usr/bin/env python3
"""This function returns all students sorted by average score"""


def top_students(mongo_collection):
    """returns the avg score of all students (sorted)"""
    documents = mongo_collection.find({})

    students = []

    for doc in documents:
        name = doc["name"]
        topics = doc["topics"]

        total_score = sum(topic['score'] for topic in topics)
        avg_score = total_score / len(topics) if topics else 0

        mongo_collection.update_one(
                {'_id': doc['_id']},
                {"$set": {'averageScore': avg_score}}
                )

        students.append({
            'name': name,
            'averageScore': avg_score
            })
    sorted_students = sorted(students, key=lambda x: x['averageScore'], reverse = True)
    return sorted_students
