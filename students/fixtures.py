# from random import randint
#
# from faker import Faker
#
# random_ids = range(97125430, 97125439)
#
#
# def get_ten_students():
#     fake = Faker()
#
#     students = []
#
#     for student_id in random_ids:
#         person = fake.name().split(" ", 1)
#         first_name = person[0]
#         last_name = person[1]
#         student_grade = randint(1, 13)
#         student_average = randint(0, 101)
#
#         student = {
#             "first_name": first_name,
#             "last_name": last_name,
#             "student_id": student_id,
#             "date_of_birth": "2003-02-01",
#             "school_grade": student_grade,
#             "student_average": student_average
#         }
#         students.append(student)
