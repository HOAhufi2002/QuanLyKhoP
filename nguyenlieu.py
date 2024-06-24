from flask import Blueprint, render_template, request, redirect, url_for
import pyodbc

connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=minhhoa;DATABASE=quanlykhopho;UID=sa;PWD=123"
conn = pyodbc.connect(connection_string)

nguyenlieu_bp = Blueprint('nguyenlieu', __name__, template_folder='templates/nguyenlieu')

@nguyenlieu_bp.route('/')
def quanlynguyenlieupho():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM NguyenLieuPhoBo")
    rows = cursor.fetchall()
    nguyenlieu = []
    for row in rows:
        nguyenlieu.append({
            'id': row.ID,
            'TenNguyenLieu': row.TenNguyenLieu,
            'MoTa': row.MoTa,
            'DonViTinh': row.DonViTinh,
            'SoLuongTonKho': row.SoLuongTonKho,
            'NgayHetHan': row.NgayHetHan
        })
    cursor.close()
    return render_template('quanlynguyenlieupho.html', nguyenlieu=nguyenlieu)

@nguyenlieu_bp.route('/add', methods=['GET', 'POST'])
def add_nguyenlieu():
    if request.method == 'POST':
        TenNguyenLieu = request.form['TenNguyenLieu']
        MoTa = request.form['MoTa']
        DonViTinh = request.form['DonViTinh']
        SoLuongTonKho = request.form['SoLuongTonKho']
        NgayHetHan = request.form['NgayHetHan']

        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO NguyenLieuPhoBo (TenNguyenLieu, MoTa, DonViTinh, SoLuongTonKho, NgayHetHan)
            VALUES (?, ?, ?, ?, ?)
        """, (TenNguyenLieu, MoTa, DonViTinh, SoLuongTonKho, NgayHetHan))
        conn.commit()
        cursor.close()
        return redirect(url_for('nguyenlieu.quanlynguyenlieupho'))
    return render_template('add_nguyenlieu.html')

@nguyenlieu_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_nguyenlieu(id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM NguyenLieuPhoBo WHERE ID = ?", (id,))
    row = cursor.fetchone()

    nguyenlieu = {
        'id': row.ID,
        'TenNguyenLieu': row.TenNguyenLieu,
        'MoTa': row.MoTa,
        'DonViTinh': row.DonViTinh,
        'SoLuongTonKho': row.SoLuongTonKho,
        'NgayHetHan': row.NgayHetHan
    }

    if request.method == 'POST':
        TenNguyenLieu = request.form['TenNguyenLieu']
        MoTa = request.form['MoTa']
        DonViTinh = request.form['DonViTinh']
        SoLuongTonKho = request.form['SoLuongTonKho']
        NgayHetHan = request.form['NgayHetHan']

        cursor.execute("""
            UPDATE NguyenLieuPhoBo
            SET TenNguyenLieu = ?, MoTa = ?, DonViTinh = ?, SoLuongTonKho = ?, NgayHetHan = ?
            WHERE ID = ?
        """, (TenNguyenLieu, MoTa, DonViTinh, SoLuongTonKho, NgayHetHan, id))
        conn.commit()
        cursor.close()
        return redirect(url_for('nguyenlieu.quanlynguyenlieupho'))

    cursor.close()
    return render_template('edit_nguyenlieu.html', nguyenlieu=nguyenlieu)

@nguyenlieu_bp.route('/delete/<int:id>')
def delete_nguyenlieu(id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM NguyenLieuPhoBo WHERE ID = ?", (id,))
    conn.commit()
    cursor.close()
    return redirect(url_for('nguyenlieu.quanlynguyenlieupho'))
