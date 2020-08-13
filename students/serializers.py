from rest_framework import serializers
from students.models import Student, SCHOOL_GRADE_CHOICES, STUDENT_AVERAGE_CHOICES

STUDENT_ID_LEN = 8

date_of_birth_frmt = ["%d/%m/%Y"]


class StudentSerializer(serializers.Serializer):
    first_name = serializers.CharField(allow_blank=False)
    last_name = serializers.CharField(allow_blank=False)
    student_id = serializers.IntegerField()
    date_of_birth = serializers.DateField(input_formats=date_of_birth_frmt)
    school_grade = serializers.ChoiceField(choices=SCHOOL_GRADE_CHOICES)
    student_average = serializers.ChoiceField(choices=STUDENT_AVERAGE_CHOICES)

    def validate(self, data):
        if len(str(data['student_id'])) != STUDENT_ID_LEN:
            raise serializers.ValidationError("Students id should be len 8")

        if Student.objects.filter(student_id=data["student_id"]).exists():
            raise serializers.ValidationError("Students id should be unique")

        return data

    def create(self, validated_data):
        return Student.objects.create(**validated_data)


class StudentGradeAggSerializer(StudentSerializer):
    first_name = None
    last_name = None
    student_id = None
    date_of_birth = None
    student_average = None
    num_students = serializers.IntegerField()
    average = serializers.IntegerField()
    std_dev = serializers.FloatField(required=False)
