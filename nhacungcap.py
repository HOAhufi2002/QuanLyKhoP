from flask import Blueprint, render_template, request, redirect, url_for
import pyodbc

nhacungcap_bp = Blueprint('nhacungcap', __name__, template_folder='templates/nhacungcap')

connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=minhhoa;DATABASE=quanlykhopho;UID=sa;PWD=123"

@nhacungcap_bp.route('/')
def quanly_nhacungcap():
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM NhaCungCap")
    nhacungcap = cursor.fetchall()
    conn.close()
    return render_template('quanly_nhacungcap.html', nhacungcap=nhacungcap)

@nhacungcap_bp.route('/add', methods=['GET', 'POST'])
def add_nhacungcap():
    if request.method == 'POST':
        ten = request.form['ten']
        diachi = request.form['diachi']
        sodienthoai = request.form['sodienthoai']
        email = request.form['email']
        loai_nguyenlieu = request.form['loai_nguyenlieu']

        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO NhaCungCap (TenNhaCungCap, DiaChi, SoDienThoai, Email, LoaiNguyenLieu) VALUES (?, ?, ?, ?, ?)",
                       (ten, diachi, sodienthoai, email, loai_nguyenlieu))
        conn.commit()
        conn.close()

        return redirect(url_for('nhacungcap.quanly_nhacungcap'))

    return render_template('add_nhacungcap.html')

@nhacungcap_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_nhacungcap(id):
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM NhaCungCap WHERE ID = ?", id)
    nhacungcap = cursor.fetchone()

    if request.method == 'POST':
        ten = request.form['ten']
        diachi = request.form['diachi']
        sodienthoai = request.form['sodienthoai']
        email = request.form['email']
        loai_nguyenlieu = request.form['loai_nguyenlieu']

        cursor.execute("UPDATE NhaCungCap SET TenNhaCungCap = ?, DiaChi = ?, SoDienThoai = ?, Email = ?, LoaiNguyenLieu = ? WHERE ID = ?",
                       (ten, diachi, sodienthoai, email, loai_nguyenlieu, id))
        conn.commit()
        conn.close()

        return redirect(url_for('nhacungcap.quanly_nhacungcap'))

    conn.close()
    return render_template('edit_nhacungcap.html', nhacungcap=nhacungcap)

@nhacungcap_bp.route('/delete/<int:id>', methods=['GET'])
def delete_nhacungcap(id):
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM NhaCungCap WHERE ID = ?", id)
    conn.commit()
    conn.close()
    return redirect(url_for('nhacungcap.quanly_nhacungcap'))
