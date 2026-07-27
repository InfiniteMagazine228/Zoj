Mini Online Judge (OJ)
Hệ thống chấm bài lập trình tự động dành cho trường học. Hỗ trợ Python 3.12 và C++20.

Tính năng
Đăng nhập / Đăng ký (Học sinh / Giáo viên)
Giáo viên: Tạo bài tập, upload test case (.in, .out)
Học sinh: Xem bài, viết code trực tiếp (Monaco Editor) hoặc upload file (.py, .cpp), nộp bài.
Chấm bài tự động bằng Docker Sandbox (Cách ly network, giới hạn CPU/RAM).
Trạng thái: Accepted, Wrong Answer, Runtime Error, Compile Error, Time Limit Exceeded.
Điểm số tính theo tỷ lệ test case đúng.
Công nghệ
Backend: FastAPI, SQLAlchemy, SQLite, JWT Auth
Frontend: HTML, CSS, Bootstrap 5, Javascript, Monaco Editor
Judge System: Docker, Python Sandbox
Cài đặt và Chạy
Yêu cầu
Docker
Docker Compose
Bước 1: Build image Judge Sandbox
Chạy lệnh sau để build image dùng cho việc chấm bài:

docker-compose build judge
Bước 2: Chạy hệ thống
bash

docker-compose up -d api
Hệ thống API và Frontend sẽ chạy tại: http://localhost:8000

Bước 3: Sử dụng
Mở trình duyệt và truy cập http://localhost:8000/login.html
Đăng nhập bằng tài khoản giáo viên mặc định (hoặc tự đăng ký):
Username: teacher
Password: teacher
(Lưu ý: Tạo tài khoản teacher bằng cách đổi role='teacher' trong DB hoặc sửa code register tạm thời)
Tạo bài tập mới, upload test case (các file .in và .out xen kẽ, tên theo thứ tự: 0.in, 0.out, 1.in, 1.out...).
Đăng xuất, đăng ký tài khoản học sinh.
Vào danh sách bài, chọn bài, code và Submit.
