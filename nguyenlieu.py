from flask import Blueprint, render_template, request, redirect, url_for
import pyodbc
from datetime import datetime

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
            'NgayNhap': row.NgayNhap,
            'NgayHetHan': row.NgayHetHan,
        })
    cursor.close()
    return render_template('quanlynguyenlieupho.html', nguyenlieu=nguyenlieu)

@nguyenlieu_bp.route('/add', methods=['GET', 'POST'])
def add_nguyenlieu():
    if request.method == 'POST':
        TenNguyenLieu = request.form['TenNguyenLieu']
        MoTa = request.form['MoTa']
        DonViTinh = request.form['DonViTinh']
        SoLuongTonKho = float(request.form['SoLuongTonKho'])
        NgayNhap = request.form['NgayNhap']
        NgayHetHan = request.form['NgayHetHan']

        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO NguyenLieuPhoBo (TenNguyenLieu, MoTa, DonViTinh, SoLuongTonKho, NgayNhap, NgayHetHan)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (TenNguyenLieu, MoTa, DonViTinh, SoLuongTonKho, NgayNhap, NgayHetHan))
        conn.commit()

        # Cập nhật kho
        cursor.execute("SELECT ID FROM NguyenLieuPhoBo WHERE TenNguyenLieu = ?", (TenNguyenLieu,))
        nguyenlieu_id = cursor.fetchone()[0]

        cursor.execute("SELECT * FROM KhoNguyenLieu WHERE NguyenLieuID = ?", (nguyenlieu_id,))
        kho_nguyenlieu = cursor.fetchone()

        if kho_nguyenlieu:
            cursor.execute("UPDATE KhoNguyenLieu SET SoLuongTon = SoLuongTon + ?, DonViTinh = ? WHERE NguyenLieuID = ?", (SoLuongTonKho, DonViTinh, nguyenlieu_id))
        else:
            cursor.execute("INSERT INTO KhoNguyenLieu (NguyenLieuID, SoLuongTon, DonViTinh) VALUES (?, ?, ?)", (nguyenlieu_id, SoLuongTonKho, DonViTinh))

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
        'NgayNhap': row.NgayNhap,
        'NgayHetHan': row.NgayHetHan,
    }

    if request.method == 'POST':
        TenNguyenLieu = request.form['TenNguyenLieu']
        MoTa = request.form['MoTa']
        DonViTinh = request.form['DonViTinh']
        SoLuongTonKho = float(request.form['SoLuongTonKho'])
        NgayNhap = request.form['NgayNhap']
        NgayHetHan = request.form['NgayHetHan']

        cursor.execute("""
            UPDATE NguyenLieuPhoBo
            SET TenNguyenLieu = ?, MoTa = ?, DonViTinh = ?, SoLuongTonKho = ?, NgayNhap = ?, NgayHetHan = ?
            WHERE ID = ?
        """, (TenNguyenLieu, MoTa, DonViTinh, SoLuongTonKho, NgayNhap, NgayHetHan, id))
        conn.commit()

        # Cập nhật kho
        cursor.execute("SELECT * FROM KhoNguyenLieu WHERE NguyenLieuID = ?", (id,))
        kho_nguyenlieu = cursor.fetchone()

        if kho_nguyenlieu:
            cursor.execute("UPDATE KhoNguyenLieu SET SoLuongTon = ?, DonViTinh = ? WHERE NguyenLieuID = ?", (SoLuongTonKho, DonViTinh, id))
        else:
            cursor.execute("INSERT INTO KhoNguyenLieu (NguyenLieuID, SoLuongTon, DonViTinh) VALUES (?, ?, ?)", (id, SoLuongTonKho, DonViTinh))

        conn.commit()
        cursor.close()
        return redirect(url_for('nguyenlieu.quanlynguyenlieupho'))

    cursor.close()
    return render_template('edit_nguyenlieu.html', nguyenlieu=nguyenlieu)

@nguyenlieu_bp.route('/delete/<int:id>')
def delete_nguyenlieu(id):
    cursor = conn.cursor()

    # Lấy thông tin nguyên liệu cần xóa
    cursor.execute("SELECT TenNguyenLieu, SoLuongTonKho FROM NguyenLieuPhoBo WHERE ID = ?", (id,))
    row = cursor.fetchone()
    ten_nguyen_lieu = row.TenNguyenLieu
    so_luong_ton_kho = row.SoLuongTonKho

    # Lấy thông tin kho
    cursor.execute("SELECT ID, SoLuongTon FROM KhoNguyenLieu WHERE NguyenLieuID = ?", (id,))
    kho_row = cursor.fetchone()

    if kho_row:
        kho_id = kho_row.ID
        so_luong_ton_kho_hien_tai = kho_row.SoLuongTon
        so_luong_ton_kho_moi = so_luong_ton_kho_hien_tai - so_luong_ton_kho

        if so_luong_ton_kho_moi > 0:
            # Cập nhật số lượng tồn trong kho
            cursor.execute("UPDATE KhoNguyenLieu SET SoLuongTon = ? WHERE ID = ?", (so_luong_ton_kho_moi, kho_id))
        else:
            # Xóa bản ghi khỏi kho nếu số lượng tồn bằng 0
            cursor.execute("DELETE FROM KhoNguyenLieu WHERE ID = ?", (kho_id,))

        conn.commit()

    # Xóa nguyên liệu khỏi bảng NguyenLieuPhoBo
    cursor.execute("DELETE FROM NguyenLieuPhoBo WHERE ID = ?", (id,))
    conn.commit()
    cursor.close()

    return redirect(url_for('nguyenlieu.quanlynguyenlieupho'))

@nguyenlieu_bp.route('/xuat_kho', methods=['GET', 'POST'])


def get_xuat_kho_nguyenlieu():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT XK.ID, NL.TenNguyenLieu, XK.SoLuongXuat, XK.NgayXuat , Xk.DonViTinh
        FROM XuatKhoNguyenLieu XK
        JOIN NguyenLieuPhoBo NL ON XK.NguyenLieuID = NL.ID
    """)
    rows = cursor.fetchall()
    cursor.close()
    
    # In dữ liệu ra console
    print("Dữ liệu từ get_xuat_kho_nguyenlieu:")
    for row in rows:
        print(row)
    
    return rows

@nguyenlieu_bp.route('/xuat_kho_nguyenlieu', methods=['GET', 'POST'])
def xuat_kho_nguyenlieu():
    if request.method == 'POST':
        NguyenLieuID = int(request.form['NguyenLieuID'])
        SoLuongXuat = int(request.form['SoLuongXuat'])
        cursor = conn.cursor()
        cursor.execute("SELECT SoLuongTon, DonViTinh FROM KhoNguyenLieu WHERE NguyenLieuID = ?", (NguyenLieuID,))
        row = cursor.fetchone()
        current_stock = row[0]
        don_vi_tinh = row[1]

        if current_stock < SoLuongXuat:
            return render_template('xuat_kho_nguyenlieu.html', nguyenlieu=get_nguyenlieu_with_stock(), error="Không đủ số lượng tồn kho", xuat_kho=get_xuat_kho_nguyenlieu())

        cursor.execute("UPDATE KhoNguyenLieu SET SoLuongTon = SoLuongTon - ? WHERE NguyenLieuID = ?", (SoLuongXuat, NguyenLieuID))
        cursor.execute("INSERT INTO XuatKhoNguyenLieu (NguyenLieuID, SoLuongXuat, NgayXuat, DonViTinh) VALUES (?, ?, ?, ?)", (NguyenLieuID, SoLuongXuat, datetime.now(), don_vi_tinh))
        conn.commit()
        cursor.close()
        return redirect(url_for('nguyenlieu.xuat_kho_nguyenlieu'))

    return render_template('xuat_kho_nguyenlieu.html', nguyenlieu=get_nguyenlieu_with_stock(), xuat_kho=get_xuat_kho_nguyenlieu())

def get_nguyenlieu_with_stock():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT NLB.ID, NLB.TenNguyenLieu, KNL.SoLuongTon, KNL.DonViTinh
        FROM NguyenLieuPhoBo NLB
        JOIN KhoNguyenLieu KNL ON NLB.ID = KNL.NguyenLieuID
    """)
    rows = cursor.fetchall()
    cursor.close()
    return rows
