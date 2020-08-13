Architecture: this project uses Django + Django Rest Framework the latest versions up-do-date. They provide an easy and fast way to create efficient and customizable API's. As a deployment service Docker is used.



**HOW TO RUN**: 

`$ docker build . -t drf_robot  `

`$ docker run -p 8080:8080 drf_robot`

- Go to http://0.0.0.0:8080/students and make sure you cannot access it without token

- Go to http://0.0.0.0:8080/token and get a token

- Copy your token. With the next requests you have to include "Authorization: Token b224693dec64a566abab77dec2c04490b0880d74" (the token itself would be different) inside your Postman (or other requests tools) headers.

Available requests:


**GET**:

- http://0.0.0.0:8000/token/

RESPONSE:
> {
    "token": "b224693dec64a566abab77dec2c04490b0880d74"
}

- http://0.0.0.0:8000/students?student_id=97125439

RESPONSE:
> {
    "first_name": "jack",
    "last_name": "smith",
    "student_id": 97125439,
    "date_of_birth": "2003-02-01",
    "school_grade": 12,
    "student_average": 55
}

- http://0.0.0.0:8000/students?grade=12

RESPONSE:
> {
    "school_grade": 12,
    "num_students": 3,
    "average": 63
}

- http://0.0.0.0:8000/students?grade=12&stdDev=yes

RESPONSE:
> {
    "school_grade": 12,
    "num_students": 3,
    "average": 63,
    "std_dev": 8.5
}

- http://0.0.0.0:8000/students?sorted_last_name=yes

RESPONSE:
>[
    {
        "first_name": "jack",
        "last_name": "bams",
        "student_id": 97125432,
        "date_of_birth": "2003-02-01",
        "school_grade": 12,
        "student_average": 75
    },
    {
        "first_name": "jack",
        "last_name": "smith",
        "student_id": 97125439,
        "date_of_birth": "2003-02-01",
        "school_grade": 12,
        "student_average": 55
    },
    {
        "first_name": "jack",
        "last_name": "zillin",
        "student_id": 97125422,
        "date_of_birth": "2003-02-01",
        "school_grade": 12,
        "student_average": 60
    }
]

- http://0.0.0.0:8000/students?sorted_age=yes

RESPONSE:

> [
    {
        "first_name": "jack",
        "last_name": "smith",
        "student_id": 97125439,
        "date_of_birth": "2005-02-01",
        "school_grade": 12,
        "student_average": 55
    },
    {
        "first_name": "jack",
        "last_name": "bams",
        "student_id": 97125432,
        "date_of_birth": "2004-02-01",
        "school_grade": 12,
        "student_average": 75
    },
    {
        "first_name": "jack",
        "last_name": "zillin",
        "student_id": 97125422,
        "date_of_birth": "2003-02-01",
        "school_grade": 12,
        "student_average": 60
    }
]

- http://0.0.0.0:8000/students?sorted_grade=yes

RESPONSE:

> [
    {
        "first_name": "jack",
        "last_name": "smith",
        "student_id": 97125439,
        "date_of_birth": "2003-02-01",
        "school_grade": 12,
        "student_average": 55
    },
    {
        "first_name": "jack",
        "last_name": "bams",
        "student_id": 97125432,
        "date_of_birth": "2003-02-01",
        "school_grade": 11,
        "student_average": 75
    },
    {
        "first_name": "jack",
        "last_name": "zillin",
        "student_id": 97125422,
        "date_of_birth": "2003-02-01",
        "school_grade": 10,
        "student_average": 60
    }
]

- http://0.0.0.0:8000/students/

RESPONSE:
> [
    {
        "first_name": "jack",
        "last_name": "smith",
        "student_id": 97125439,
        "date_of_birth": "2003-02-01",
        "school_grade": 12,
        "student_average": 55
    },
    {
        "first_name": "jack",
        "last_name": "bams",
        "student_id": 97125432,
        "date_of_birth": "2003-02-01",
        "school_grade": 12,
        "student_average": 75
    },
    {
        "first_name": "jack",
        "last_name": "zillin",
        "student_id": 97125422,
        "date_of_birth": "2003-02-01",
        "school_grade": 12,
        "student_average": 60
    }
]


**POST**:

- http://0.0.0.0:8000/students/

BODY: 
> {
    "first_name": "jack",
    "last_name": "zillin",
    "student_id": 97125420,
    "date_of_birth": "02/01/2003",
    "school_grade": 12,
    "student_average": 60
}

RESPONSE: 

> {
    "first_name": "jack",
    "last_name": "zillin",
    "student_id": 97125420,
    "date_of_birth": "2003-01-02",
    "school_grade": 12,
    "student_average": 60,
    "created_at": "2020-08-13T09:29:06.487"
}

**DELETE**:

- http://0.0.0.0:8000/students/?student_id=97125420

RESPONSE:
> {
    "first_name": "jack",
    "last_name": "zillin",
    "student_id": 97125420,
    "date_of_birth": "2003-01-02",
    "school_grade": 12,
    "student_average": 60,
    "deleted_at": "2020-08-13T09:33:34.154"
}

- http://0.0.0.0:8000/students/

RESPONSE:
> {
    "num_students": 0
}


Running tests:
`$ python manage.py tests`