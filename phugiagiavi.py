from flask import Blueprint, render_template, request, redirect, url_for
import pyodbc

connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=Hiep\\SQLEXPRESS;DATABASE=quanlykhopho;Trusted_Connection=yes;"
conn = pyodbc.connect(connection_string)

phugiagiavi_bp = Blueprint('phugiagiavi', __name__, template_folder='templates/phugiagiavi')

@phugiagiavi_bp.route('/')
def quanlyphugiagiavi():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PhuGiaGiaVi")
    rows = cursor.fetchall()
    phugiagiavi = []
    for row in rows:
        phugiagiavi.append({
            'id': row.ID,
            'TenPhuGia': row.TenPhuGia,
            'MoTa': row.MoTa,
            'DonViTinh': row.DonViTinh,
            'SoLuongTonKho': row.SoLuongTonKho,
            'NgayHetHan': row.NgayHetHan
        })
    cursor.close()
    return render_template('quanlyphugiagiavi.html', phugiagiavi=phugiagiavi)

@phugiagiavi_bp.route('/add', methods=['GET', 'POST'])
def add_phugiagiavi():
    if request.method == 'POST':
        TenPhuGia = request.form['TenPhuGia']
        MoTa = request.form['MoTa']
        DonViTinh = request.form['DonViTinh']
        SoLuongTonKho = request.form['SoLuongTonKho']
        NgayHetHan = request.form['NgayHetHan']

        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO PhuGiaGiaVi (TenPhuGia, MoTa, DonViTinh, SoLuongTonKho, NgayHetHan)
            VALUES (?, ?, ?, ?, ?)
        """, (TenPhuGia, MoTa, DonViTinh, SoLuongTonKho, NgayHetHan))
        conn.commit()
        cursor.close()
        return redirect(url_for('phugiagiavi.quanlyphugiagiavi'))
    return render_template('add_phugiagiavi.html')

@phugiagiavi_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_phugiagiavi(id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PhuGiaGiaVi WHERE ID = ?", (id,))
    row = cursor.fetchone()

    phugiagiavi = {
        'id': row.ID,
        'TenPhuGia': row.TenPhuGia,
        'MoTa': row.MoTa,
        'DonViTinh': row.DonViTinh,
        'SoLuongTonKho': row.SoLuongTonKho,
        'NgayHetHan': row.NgayHetHan
    }

    if request.method == 'POST':
        TenPhuGia = request.form['TenPhuGia']
        MoTa = request.form['MoTa']
        DonViTinh = request.form['DonViTinh']
        SoLuongTonKho = request.form['SoLuongTonKho']
        NgayHetHan = request.form['NgayHetHan']

        cursor.execute("""
            UPDATE PhuGiaGiaVi
            SET TenPhuGia = ?, MoTa = ?, DonViTinh = ?, SoLuongTonKho = ?, NgayHetHan = ?
            WHERE ID = ?
        """, (TenPhuGia, MoTa, DonViTinh, SoLuongTonKho, NgayHetHan, id))
        conn.commit()
        cursor.close()
        return redirect(url_for('phugiagiavi.quanlyphugiagiavi'))

    cursor.close()
    return render_template('edit_phugiagiavi.html', phugiagiavi=phugiagiavi)

@phugiagiavi_bp.route('/delete/<int:id>')
def delete_phugiagiavi(id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM PhuGiaGiaVi WHERE ID = ?", (id,))
    conn.commit()
    cursor.close()
    return redirect(url_for('phugiagiavi.quanlyphugiagiavi'))
