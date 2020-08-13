import json

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase

from students.models import Student
from students.views import students_view


class StudentAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.user = User.objects.create(username="admin")

    #
    # def tearDown(self) -> None:
    #     Student.objects.all().delete()

    def test_add_new_student(self):
        student = {
            "first_name": "john",
            "last_name": "smith",
            "student_id": 55175498,
            "date_of_birth": "08/02/2010",
            "school_grade": 5,
            "student_average": 85
        }
        request = self.factory.post('/students/', data=student, format='json')
        force_authenticate(request, user=self.user)
        response = students_view(request)
        found_user = Student.objects.get(student_id=55175498)

        assert found_user

    def test_delete_new_student(self):
        student = {
            "first_name": "john",
            "last_name": "smith",
            "student_id": 55175498,
            "date_of_birth": "08/02/2010",
            "school_grade": 5,
            "student_average": 85
        }
        request = self.factory.post('/students/', data=student, format='json')
        force_authenticate(request, user=self.user)
        response = students_view(request)

        request_del = self.factory.delete('/students/', data=student, format='json')
        force_authenticate(request_del, user=self.user)
        response_del = students_view(request_del)

        with self.assertRaises(Student.DoesNotExist):
            Student.objects.get(student_id=55175498)

    def test_avg_grade(self):
        student_one = {
            "first_name": "john",
            "last_name": "smith",
            "student_id": 55175498,
            "date_of_birth": "08/02/2010",
            "school_grade": 5,
            "student_average": 80
        }

        student_two = {
            "first_name": "john",
            "last_name": "smith",
            "student_id": 55175499,
            "date_of_birth": "08/02/2010",
            "school_grade": 5,
            "student_average": 50
        }

        student_three = {
            "first_name": "john",
            "last_name": "smith",
            "student_id": 55175497,
            "date_of_birth": "08/02/2010",
            "school_grade": 5,
            "student_average": 30
        }

        students = [student_one, student_two, student_three]

        for student in students:
            request = self.factory.post('/students/', data=student, format='json')
            force_authenticate(request, user=self.user)
            response = students_view(request)

        request = self.factory.get('/students/', {"grade": 5}, format='json')
        force_authenticate(request, user=self.user)
        response = students_view(request)

        resp_dict = json.loads(response.content)

        assert resp_dict['average'] == 53

    def test_stdDev(self):
        student_one = {
            "first_name": "john",
            "last_name": "smith",
            "student_id": 55175498,
            "date_of_birth": "08/02/2010",
            "school_grade": 5,
            "student_average": 80
        }

        student_two = {
            "first_name": "john",
            "last_name": "smith",
            "student_id": 55175499,
            "date_of_birth": "08/02/2010",
            "school_grade": 5,
            "student_average": 50
        }

        student_three = {
            "first_name": "john",
            "last_name": "smith",
            "student_id": 55175497,
            "date_of_birth": "08/02/2010",
            "school_grade": 5,
            "student_average": 30
        }

        students = [student_one, student_two, student_three]

        for student in students:
            request = self.factory.post('/students/', data=student, format='json')
            force_authenticate(request, user=self.user)
            response = students_view(request)

        request = self.factory.get('/students/', {"grade": 5, 'stdDev': 'yes'}, format='json')
        force_authenticate(request, user=self.user)
        response = students_view(request)

        resp_dict = json.loads(response.content)

        assert resp_dict['std_dev'] == 20.55

    def test_delete_all(self):
        student = {
            "first_name": "john",
            "last_name": "smith",
            "student_id": 55175498,
            "date_of_birth": "08/02/2010",
            "school_grade": 5,
            "student_average": 85
        }
        request = APIRequestFactory().post('/students/', data=student, format='json')
        force_authenticate(request, user=self.user)
        response = students_view(request)

        request_del = APIRequestFactory().delete('/students/')
        force_authenticate(request_del, user=self.user)
        response_del = students_view(request_del)

        assert not Student.objects.all()

    def test_students_sort_last_name(self):
        student_one = {
            "first_name": "john",
            "last_name": "zba",
            "student_id": 55175498,
            "date_of_birth": "08/02/2010",
            "school_grade": 5,
            "student_average": 80
        }

        student_two = {
            "first_name": "john",
            "last_name": "abc",
            "student_id": 55175499,
            "date_of_birth": "08/02/2010",
            "school_grade": 5,
            "student_average": 50
        }

        student_three = {
            "first_name": "john",
            "last_name": 'bce',
            "student_id": 55175497,
            "date_of_birth": "08/02/2010",
            "school_grade": 5,
            "student_average": 30
        }

        students = [student_one, student_two, student_three]

        for student in students:
            request = self.factory.post('/students/', data=student, format='json')
            force_authenticate(request, user=self.user)
            response = students_view(request)

        request = self.factory.get('/students/', {'sorted_last_name': 'yes'})
        force_authenticate(request, user=self.user)
        response = students_view(request)

        resp_list = json.loads(response.content)

        assert resp_list[0]['last_name'] == 'abc'
        assert resp_list[1]['last_name'] == 'bce'
        assert resp_list[2]['last_name'] == 'zba'

    def test_students_sort_age(self):
        student_one = {
            "first_name": "john",
            "last_name": "zba",
            "student_id": 55175498,
            "date_of_birth": "08/02/1999",
            "school_grade": 5,
            "student_average": 80
        }

        student_two = {
            "first_name": "john",
            "last_name": "abc",
            "student_id": 55175499,
            "date_of_birth": "08/02/1988",
            "school_grade": 5,
            "student_average": 50
        }

        student_three = {
            "first_name": "john",
            "last_name": 'bce',
            "student_id": 55175497,
            "date_of_birth": "08/02/2005",
            "school_grade": 5,
            "student_average": 30
        }

        students = [student_one, student_two, student_three]

        for student in students:
            request = self.factory.post('/students/', data=student, format='json')
            force_authenticate(request, user=self.user)
            response = students_view(request)

        request = self.factory.get('/students/', {'sorted_age': 'yes'})
        force_authenticate(request, user=self.user)
        response = students_view(request)

        resp_list = json.loads(response.content)

        assert resp_list[0]['date_of_birth'] == '2005-02-08'
        assert resp_list[1]['date_of_birth'] == '1999-02-08'
        assert resp_list[2]['date_of_birth'] == '1988-02-08'

    def test_students_sort_grade(self):
        student_one = {
            "first_name": "john",
            "last_name": "zba",
            "student_id": 55175498,
            "date_of_birth": "08/02/1999",
            "school_grade": 8,
            "student_average": 80
        }

        student_two = {
            "first_name": "john",
            "last_name": "abc",
            "student_id": 55175499,
            "date_of_birth": "08/02/1988",
            "school_grade": 10,
            "student_average": 50
        }

        student_three = {
            "first_name": "john",
            "last_name": 'bce',
            "student_id": 55175497,
            "date_of_birth": "08/02/2005",
            "school_grade": 9,
            "student_average": 30
        }

        students = [student_one, student_two, student_three]

        for student in students:
            request = self.factory.post('/students/', data=student, format='json')
            force_authenticate(request, user=self.user)
            response = students_view(request)

        request = self.factory.get('/students/', {'sorted_grade': 'yes'})
        force_authenticate(request, user=self.user)
        response = students_view(request)

        resp_list = json.loads(response.content)

        assert resp_list[0]['school_grade'] == 10
        assert resp_list[1]['school_grade'] == 9
        assert resp_list[2]['school_grade'] == 8

    def test_students_detail(self):
        student_one = {
            "first_name": "john",
            "last_name": "zba",
            "student_id": 55175498,
            "date_of_birth": "08/02/1999",
            "school_grade": 8,
            "student_average": 80
        }

        request = self.factory.post('/students/', data=student_one, format='json')
        force_authenticate(request, user=self.user)
        response = students_view(request)

        format_date_of_birth = '1999-02-08'
        student_one["date_of_birth"] = format_date_of_birth

        request = self.factory.get('/students/', {"student_id": 55175498}, format='json')
        force_authenticate(request, user=self.user)
        response = students_view(request)

        resp_json = json.loads(response.content)

        assert resp_json == student_one


class StudentModelTestCase(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.user = User.objects.create(username="admin")

    def test_first_name_empty(self):
        student = {
            "first_name": "",
            "last_name": "smith",
            "student_id": 55175498,
            "date_of_birth": "08/02/2010",
            "school_grade": 5,
            "student_average": 85
        }
        request = self.factory.post('/students/', data=student, format='json')
        force_authenticate(request, user=self.user)
        response = students_view(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_last_name_empty(self):
        student = {
            "first_name": "john",
            "last_name": "",
            "student_id": 55175498,
            "date_of_birth": "08/02/2010",
            "school_grade": 5,
            "student_average": 85
        }
        request = self.factory.post('/students/', data=student, format='json')
        force_authenticate(request, user=self.user)
        response = students_view(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_student_id_length_wrong(self):
        student = {
            "first_name": "john",
            "last_name": "smith",
            "student_id": 5517549,
            "date_of_birth": "08/02/2010",
            "school_grade": 5,
            "student_average": 85
        }
        request = self.factory.post('/students/', data=student, format='json')
        force_authenticate(request, user=self.user)
        response = students_view(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_student_id_length_not_unique(self):
        student = {
            "first_name": "john",
            "last_name": "smith",
            "student_id": 55175495,
            "date_of_birth": "08/02/2010",
            "school_grade": 5,
            "student_average": 85
        }
        request = self.factory.post('/students/', data=student, format='json')
        force_authenticate(request, user=self.user)
        response = students_view(request)

        request = self.factory.post('/students/', data=student, format='json')
        force_authenticate(request, user=self.user)
        second_response = students_view(request)

        assert second_response.status_code == status.HTTP_400_BAD_REQUEST

    def test_date_of_birth_wrong_format(self):
        student = {
            "first_name": "john",
            "last_name": "smith",
            "student_id": 55175495,
            "date_of_birth": "2010/08/02",
            "school_grade": 5,
            "student_average": 85
        }
        request = self.factory.post('/students/', data=student, format='json')
        force_authenticate(request, user=self.user)
        response = students_view(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_school_grade_wrong_value(self):
        student = {
            "first_name": "john",
            "last_name": "smith",
            "student_id": 55175495,
            "date_of_birth": "2010/08/02",
            "school_grade": 13,
            "student_average": 85
        }
        request = self.factory.post('/students/', data=student, format='json')
        force_authenticate(request, user=self.user)
        response = students_view(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_student_average_wrong_value(self):
        student = {
            "first_name": "john",
            "last_name": "smith",
            "student_id": 55175495,
            "date_of_birth": "2010/08/02",
            "school_grade": 13,
            "student_average": 101
        }
        request = self.factory.post('/students/', data=student, format='json')
        force_authenticate(request, user=self.user)
        response = students_view(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
