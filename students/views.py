from datetime import datetime

from django.db.models import StdDev, Avg
from django.forms import model_to_dict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes

from students.models import Student
from students.serializers import StudentSerializer, StudentGradeAggSerializer


@api_view(['GET', 'POST', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@csrf_exempt
def students_view(request):
    request_data = request.data

    if request.method == 'GET':
        grade = request.GET.get("grade")
        std_dev = request.GET.get("stdDev")
        sorted_last_name = request.GET.get("sorted_last_name")
        sorted_age = request.GET.get("sorted_age")
        sorted_grade = request.GET.get("sorted_grade")
        student_id = request.GET.get("student_id")

        if student_id:
            try:
                student = Student.objects.get(student_id=student_id)
            except Student.DoesNotExist:
                return JsonResponse({"student": "Not Found"}, status=404)

            serializer = StudentSerializer(student)

        elif grade:
            students = Student.objects.filter(school_grade=grade)
            num_students = len(students)

            students_avg_grade = students.aggregate(average=Avg('student_average'))

            res_json = {"num_students": num_students,
                        "school_grade": grade}

            res_json.update(students_avg_grade)

            if std_dev:
                students_stdDev = students.aggregate(std_dev=StdDev('student_average'))
                students_stdDev['std_dev'] = round(students_stdDev['std_dev'], 2)
                res_json.update(students_stdDev)

            serializer = StudentGradeAggSerializer(res_json)

        else:
            if sorted_last_name:
                students = Student.objects.order_by("last_name").all()

            elif sorted_age:
                students = Student.objects.order_by("-date_of_birth").all()

            elif sorted_grade:
                students = Student.objects.order_by("-school_grade").all()

            else:
                students = Student.objects.all()

            serializer = StudentSerializer(students, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        serializer = StudentSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return_json = dict(serializer.data)
            return_json["created_at"] = datetime.now()
            return JsonResponse(return_json, status=201)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        student_id = request.GET.get("student_id")
        if student_id:
            try:
                student = Student.objects.get(student_id=student_id)
            except Student.DoesNotExist:
                return JsonResponse({"student": "Not Found"}, status=404)

            student.delete()
            return_json = model_to_dict(student)
            del return_json["id"]
            return_json["deleted_at"] = datetime.now()

        else:
            Student.objects.all().delete()
            return_json = {"num_students": 0}

        return JsonResponse(return_json, status=204)
