from flask import Blueprint, render_template, request, redirect, url_for, flash
import pyodbc

# Create a blueprint for managing raw materials and additives
quanlynguyenlieuphugia_bp = Blueprint('quanlynguyenlieuphugia', __name__, template_folder='templates/quanlynguyenlieuphugia')

# Helper function to get a database connection
def get_db_connection():
    connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=minhhoa;DATABASE=quanlykhopho;UID=sa;PWD=123"
    return pyodbc.connect(connection_string)

# Route to display raw materials
@quanlynguyenlieuphugia_bp.route('/nguyenlieu')
def quanly_nguyenlieu():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM QuanLyNguyenLieu")
    rows = cursor.fetchall()
    nguyenlieu = [{'id': row.ID, 'TenNguyenLieu': row.TenNguyenLieu} for row in rows]
    cursor.close()
    conn.close()
    return render_template('quanly_nguyenlieu.html', nguyenlieu=nguyenlieu)

# Route to display additives
@quanlynguyenlieuphugia_bp.route('/phugia')
def quanly_phugia():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM QuanLyPhuGia")
    rows = cursor.fetchall()
    phugia = [{'id': row.ID, 'TenPhuGia': row.TenPhuGia} for row in rows]
    cursor.close()
    conn.close()
    return render_template('quanly_phugia.html', phugia=phugia)

# Route to add a new raw material
@quanlynguyenlieuphugia_bp.route('/nguyenlieu/add', methods=['GET', 'POST'])
def add_nguyenlieu():
    if request.method == 'POST':
        TenNguyenLieu = request.form['TenNguyenLieu']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM QuanLyNguyenLieu WHERE TenNguyenLieu = ?", (TenNguyenLieu,))
        existing_nguyenlieu = cursor.fetchone()

        if existing_nguyenlieu:
            flash('Nguyên liệu đã tồn tại!', 'error')
        else:
            cursor.execute("INSERT INTO QuanLyNguyenLieu (TenNguyenLieu) VALUES (?)", (TenNguyenLieu,))
            conn.commit()
            flash('Nguyên liệu đã được thêm thành công!', 'success')

        cursor.close()
        conn.close()
        return redirect(url_for('quanlynguyenlieuphugia.quanly_nguyenlieu'))
    return render_template('addnguyenlieu.html')

# Route to add a new additive
@quanlynguyenlieuphugia_bp.route('/phugia/add', methods=['GET', 'POST'])
def add_phugia():
    if request.method == 'POST':
        TenPhuGia = request.form['TenPhuGia']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM QuanLyPhuGia WHERE TenPhuGia = ?", (TenPhuGia,))
        existing_phugia = cursor.fetchone()

        if existing_phugia:
            flash('Phụ gia đã tồn tại!', 'error')
        else:
            cursor.execute("INSERT INTO QuanLyPhuGia (TenPhuGia) VALUES (?)", (TenPhuGia,))
            conn.commit()
            flash('Phụ gia đã được thêm thành công!', 'success')

        cursor.close()
        conn.close()
        return redirect(url_for('quanlynguyenlieuphugia.quanly_phugia'))
    return render_template('addphugia.html')

# Route to delete a raw material
@quanlynguyenlieuphugia_bp.route('/nguyenlieu/delete/<int:id>')
def delete_nguyenlieu(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM QuanLyNguyenLieu WHERE ID = ?", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('quanlynguyenlieuphugia.quanly_nguyenlieu'))

# Route to delete an additive
@quanlynguyenlieuphugia_bp.route('/phugia/delete/<int:id>')
def delete_phugia(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM QuanLyPhuGia WHERE ID = ?", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('quanlynguyenlieuphugia.quanly_phugia'))
