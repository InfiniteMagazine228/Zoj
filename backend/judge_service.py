import os
import subprocess
import shutil
from sqlalchemy.orm import sessionmaker
from database import engine
from models import Submission, Problem, TestCase
from config import SUBMISSION_DIR

SessionLocal = sessionmaker(bind=engine)

def compare_output(expected: str, actual: str) -> bool:
    """So sánh output: trim khoảng trắng đầu cuối và các dòng."""
    exp_lines = expected.strip().split('\n')
    act_lines = actual.strip().split('\n')
    if len(exp_lines) != len(act_lines):
        return False
    for e, a in zip(exp_lines, act_lines):
        if e.strip() != a.strip():
            return False
    return True

def run_judge(submission_id: int):
    db = SessionLocal()
    try:
        submission = db.query(Submission).filter(Submission.id == submission_id).first()
        if not submission: return

        problem = db.query(Problem).filter(Problem.id == submission.problem_id).first()
        test_cases = db.query(TestCase).filter(TestCase.problem_id == problem.id).all()

        submission.status = "Judging"
        db.commit()

        # 1. Tạo thư mục tạm
        temp_dir = os.path.join(SUBMISSION_DIR, str(submission_id))
        os.makedirs(temp_dir, exist_ok=True)

        # 2. Ghi source code
        ext = ".py" if submission.language == "python" else ".cpp"
        src_path = os.path.join(temp_dir, f"main{ext}")
        with open(src_path, "w") as f:
            f.write(submission.source_code)

        passed_tests = 0
        total_tests = len(test_cases)
        final_status = "Accepted"
        runtime_ms = 0
        is_compile_error = False

        for tc in test_cases:
            inp_path = os.path.join(temp_dir, "input.txt")
            out_path = os.path.join(temp_dir, "output.txt")
            
            # Copy test case vào thư mục tạm
            shutil.copy(tc.input_file, inp_path)
            
            # Tạo file output trống
            with open(out_path, "w") as f: pass

            # 3. Chạy Docker Sandbox
            cmd = [
                "docker", "run", "--rm",
                "--network", "none",
                "--memory", "256m",
                "--cpus", "1",
                "-v", f"{temp_dir}:/app",
                "oj-judge:latest",
                "/runner.sh", submission.language, "input.txt", str(problem.time_limit)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Xử lý kết quả
            if "COMPILE_ERROR" in result.stderr or "COMPILE_ERROR" in result.stdout:
                final_status = "Compile Error"
                is_compile_error = True
                break
            
            if result.returncode == 124: # Timeout exit code
                final_status = "Time Limit Exceeded"
                break
            
            if result.returncode != 0:
                final_status = "Runtime Error"
                break
                
            # Đọc output thực tế
            with open(out_path, "r") as f:
                actual_out = f.read()
            with open(tc.output_file, "r") as f:
                expected_out = f.read()
                
            if compare_output(expected_out, actual_out):
                passed_tests += 1
            else:
                final_status = "Wrong Answer"
                break

        if is_compile_error:
            score = 0.0
        else:
            score = (passed_tests / total_tests) * 100 if total_tests > 0 else 0.0
            if score < 100 and final_status == "Accepted":
                final_status = "Wrong Answer"

        submission.status = final_status
        submission.score = score
        submission.runtime = runtime_ms
        db.commit()

    except Exception as e:
        print(f"Judge Error: {e}")
        submission.status = "System Error"
        db.commit()
    finally:
        # 4. Tự động xóa thư mục tạm sau khi chấm
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        db.close()
