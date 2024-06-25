from flask import Blueprint, render_template, request, redirect, url_for, session
import pyodbc
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

loginregister_bp = Blueprint('loginregister', __name__, template_folder='templates')

connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=minhhoa;DATABASE=quanlykhopho;UID=sa;PWD=123"

@loginregister_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute("SELECT ID, MatKhau, Quyen, isActive FROM TaiKhoan WHERE TenDangNhap = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user.MatKhau, password):
            if user.isActive:
                session['user_id'] = user.ID
                session['TenDangNhap'] = username
                session['Quyen'] = user.Quyen
                return render_template('index.html', message={'title': 'Đăng nhập thành công', 'body': f'Bạn đã đăng nhập thành công với quyền {user.Quyen}'})
            else:
                message = {'title': 'Đăng ký thành công', 'body': 'Tài khoản của bạn đã được tạo thành công và đang chờ kích hoạt.'}
                return render_template('login.html',message = {'body': 'Tài khoản chưa được kích hoạt'}
)
        else:
            return render_template('login.html', message={ 'body': 'Tên đăng nhập hoặc mật khẩu không đúng'})

    return render_template('login.html')

@loginregister_bp.route('/register', methods=['GET', 'POST'])
def register():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        hoten = request.form['hoten']
        email = request.form['email']
        quyen = request.form['quyen']
        ngay_tao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO TaiKhoan (TenDangNhap, MatKhau, HoTen, Email, Quyen, NgayTao, isActive) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (username, password, hoten, email, quyen, ngay_tao, 0))
            conn.commit()
            message = {'title': 'Đăng ký thành công', 'body': 'Tài khoản của bạn đã được tạo thành công và đang chờ kích hoạt.'}
        except Exception as e:
            conn.rollback()
            message = {'title': 'Đăng ký thất bại', 'body': 'Có lỗi xảy ra. Vui lòng thử lại.'}
        finally:
            conn.close()

    return render_template('register.html', message=message)

@loginregister_bp.route('/account_management')
def account_management():
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute('SELECT ID, TenDangNhap, HoTen, Email, Quyen, isActive FROM TaiKhoan')
    accounts = cursor.fetchall()
    conn.close()
    return render_template('quanlytaikhoan/danhsachtaikhoan.html', accounts=accounts)
@loginregister_bp.route('/edit_taikhoan/<int:id>', methods=['GET', 'POST'])
def edit_taikhoan(id):
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    if request.method == 'POST':
        ten_dang_nhap = request.form['TenDangNhap']
        ho_ten = request.form['HoTen']
        email = request.form['Email']
        quyen = request.form['Quyen']
        is_active = request.form.get('isActive') == 'on'
        mat_khau = request.form['MatKhau']

        # Update the fields except the password
        cursor.execute("""
            UPDATE TaiKhoan 
            SET TenDangNhap = ?, HoTen = ?, Email = ?, Quyen = ?, isActive = ? 
            WHERE ID = ?
        """, (ten_dang_nhap, ho_ten, email, quyen, is_active, id))

        # Update the password only if it's provided
        if mat_khau:
            hashed_password = generate_password_hash(mat_khau)
            cursor.execute("UPDATE TaiKhoan SET MatKhau = ? WHERE ID = ?", (hashed_password, id))

        conn.commit()
        conn.close()
        return redirect(url_for('loginregister.account_management'))

    cursor.execute("SELECT ID, TenDangNhap, HoTen, Email, Quyen, isActive FROM TaiKhoan WHERE ID = ?", (id,))
    taikhoan = cursor.fetchone()
    conn.close()
    return render_template('quanlytaikhoan/edit_taikhoan.html', taikhoan=taikhoan)


@loginregister_bp.route('/delete_taikhoan/<int:id>')
def delete_taikhoan(id):
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM TaiKhoan WHERE ID = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('loginregister.account_management'))

@loginregister_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('loginregister.login'))