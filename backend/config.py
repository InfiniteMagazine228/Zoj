import os

SECRET_KEY = "sb_secret_dynWYojIERgDRXzFQ5JoFQ_qZVYKMaW"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 # 1 day

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TESTCASE_DIR = os.path.join(BASE_DIR, "..", "testcases")
SUBMISSION_DIR = os.path.join(BASE_DIR, "..", "submissions")
UPLOAD_DIR = os.path.join(BASE_DIR, "..", "uploads")

# Đảm bảo các thư mục tồn tại
os.makedirs(TESTCASE_DIR, exist_ok=True)
os.makedirs(SUBMISSION_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)
