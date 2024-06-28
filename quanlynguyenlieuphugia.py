from flask import Blueprint, render_template, request, redirect, url_for
import pyodbc

connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=Hiep\\SQLEXPRESS;DATABASE=quanlykhopho;Trusted_Connection=yes;"
conn = pyodbc.connect(connection_string)

quanlynguyenlieuphugia_bp = Blueprint('quanlynguyenlieuphugia', __name__, template_folder='templates/quanlynguyenlieuphugia')

@quanlynguyenlieuphugia_bp.route('/nguyenlieu')
def quanly_nguyenlieu():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM QuanLyNguyenLieu")
    rows = cursor.fetchall()
    nguyenlieu = []
    for row in rows:
        nguyenlieu.append({
            'id': row.ID,
            'TenNguyenLieu': row.TenNguyenLieu
        })
    cursor.close()
    return render_template('quanly_nguyenlieu.html', nguyenlieu=nguyenlieu)

@quanlynguyenlieuphugia_bp.route('/phugia')
def quanly_phugia():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM QuanLyPhuGia")
    rows = cursor.fetchall()
    phugia = []
    for row in rows:
        phugia.append({
            'id': row.ID,
            'TenPhuGia': row.TenPhuGia
        })
    cursor.close()
    return render_template('quanly_phugia.html', phugia=phugia)

@quanlynguyenlieuphugia_bp.route('/nguyenlieu/add', methods=['GET', 'POST'])
def add_nguyenlieu():
    if request.method == 'POST':
        TenNguyenLieu = request.form['TenNguyenLieu']

        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO QuanLyNguyenLieu (TenNguyenLieu)
            VALUES (?)
        """, (TenNguyenLieu,))
        conn.commit()
        cursor.close()
        return redirect(url_for('quanlynguyenlieuphugia.quanly_nguyenlieu'))
    return render_template('addnguyenlieu.html')

@quanlynguyenlieuphugia_bp.route('/phugia/add', methods=['GET', 'POST'])
def add_phugia():
    if request.method == 'POST':
        TenPhuGia = request.form['TenPhuGia']

        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO QuanLyPhuGia (TenPhuGia)
            VALUES (?)
        """, (TenPhuGia,))
        conn.commit()
        cursor.close()
        return redirect(url_for('quanlynguyenlieuphugia.quanly_phugia'))
    return render_template('addphugia.html')

@quanlynguyenlieuphugia_bp.route('/nguyenlieu/delete/<int:id>')
def delete_nguyenlieu(id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM QuanLyNguyenLieu WHERE ID = ?", (id,))
    conn.commit()
    cursor.close()
    return redirect(url_for('quanlynguyenlieuphugia.quanly_nguyenlieu'))

@quanlynguyenlieuphugia_bp.route('/phugia/delete/<int:id>')
def delete_phugia(id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM QuanLyPhuGia WHERE ID = ?", (id,))
    conn.commit()
    cursor.close()
    return redirect(url_for('quanlynguyenlieuphugia.quanly_phugia'))
