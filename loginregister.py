from flask import Blueprint, render_template, request, redirect, url_for, session
import pyodbc
from datetime import datetime

loginregister_bp = Blueprint('loginregister', __name__, template_folder='templates')

connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=minhhoa;DATABASE=quanlykhopho;UID=sa;PWD=123"

@loginregister_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute("SELECT ID, Quyen FROM TaiKhoan WHERE TenDangNhap = ? AND MatKhau = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user.ID
            session['TenDangNhap'] = username
            session['Quyen'] = user.Quyen
            return render_template('index.html', message={'title': 'Đăng nhập thành công', 'body': f'Bạn đã đăng nhập thành công với quyền {user.Quyen}'})
        else:
            return render_template('login.html', message={'title': 'Đăng nhập thất bại', 'body': 'Tên đăng nhập hoặc mật khẩu không đúng'})

    return render_template('login.html')

@loginregister_bp.route('/register', methods=['GET', 'POST'])
def register():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hoten = request.form['hoten']
        email = request.form['email']
        quyen = request.form['quyen']
        ngay_tao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO TaiKhoan (TenDangNhap, MatKhau, HoTen, Email, Quyen, NgayTao) VALUES (?, ?, ?, ?, ?, ?)",
                           (username, password, hoten, email, quyen, ngay_tao))
            conn.commit()
            message = {'title': 'Đăng ký thành công', 'body': 'Tài khoản của bạn đã được tạo thành công .'}
        except Exception as e:
            conn.rollback()
            message = {'title': 'Đăng ký thất bại', 'body': 'Có lỗi xảy ra. Vui lòng thử lại.'}
        finally:
            conn.close()

    return render_template('register.html', message=message)


@loginregister_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('loginregister.login'))
