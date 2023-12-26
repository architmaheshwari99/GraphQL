employers_data = [
    {"id": 1, "name": "MetaTechA", "contact_email": "contact@company-a.com", "industry": "Tech"},
    {"id": 2, "name": "MoneySoftB", "contact_email": "contact@company-b.com", "industry": "Finance"},
]

jobs_data = [
    {"id": 1, "title": "Software Engineer", "description": "Develop web applications", "employer_id": 1},
    {"id": 2, "title": "Data Analyst", "description": "Analyze data and create reports", "employer_id": 1},
    {"id": 3, "title": "Accountant", "description": "Manage financial records", "employer_id": 2},
    {"id": 4, "title": "Manager", "description": "Manage people who manage records", "employer_id": 2},
]

users_data = [
    {"username": "arcmahes1", "email": "abc1", "password": "abc1", "role": "staff"},
    {"username": "arcmahes2", "email": "abc2", "password": "abc2", "role": "user"},
    {"username": "arcmahes3", "email": "abc3", "password": "abc3", "role": "admin"},
]

job_applications = [
    {"job_id": 1, "user_id": 1},
    {"job_id": 2, "user_id": 1},
    {"job_id": 3, "user_id": 1},
    {"job_id": 3, "user_id": 2},
    {"job_id": 3, "user_id": 3},
]