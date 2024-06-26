from flask import Blueprint, render_template, request, redirect, url_for
import pyodbc
from datetime import datetime

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
            'NgayNhap': row.NgayNhap,
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
        SoLuongTonKho = int(request.form['SoLuongTonKho'])
        NgayNhap = request.form['NgayNhap']
        NgayHetHan = request.form['NgayHetHan']

        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO PhuGiaGiaVi (TenPhuGia, MoTa, DonViTinh, SoLuongTonKho, NgayNhap, NgayHetHan)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (TenPhuGia, MoTa, DonViTinh, SoLuongTonKho, NgayNhap, NgayHetHan))
        conn.commit()

        # Cập nhật kho
        cursor.execute("SELECT ID FROM PhuGiaGiaVi WHERE TenPhuGia = ?", (TenPhuGia,))
        phugia_id = cursor.fetchone()[0]

        cursor.execute("SELECT * FROM KhoPhuGia WHERE PhuGiaID = ?", (phugia_id,))
        kho_phugia = cursor.fetchone()

        if kho_phugia:
            cursor.execute("UPDATE KhoPhuGia SET SoLuongTon = SoLuongTon + ?, DonViTinh = ? WHERE PhuGiaID = ?", (SoLuongTonKho, DonViTinh, phugia_id))
        else:
            cursor.execute("INSERT INTO KhoPhuGia (PhuGiaID, SoLuongTon, DonViTinh) VALUES (?, ?, ?)", (phugia_id, SoLuongTonKho, DonViTinh))

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
        'NgayNhap': row.NgayNhap,
        'NgayHetHan': row.NgayHetHan
    }

    if request.method == 'POST':
        TenPhuGia = request.form['TenPhuGia']
        MoTa = request.form['MoTa']
        DonViTinh = request.form['DonViTinh']
        SoLuongTonKho = int(request.form['SoLuongTonKho'])
        NgayNhap = request.form['NgayNhap']
        NgayHetHan = request.form['NgayHetHan']

        cursor.execute("""
            UPDATE PhuGiaGiaVi
            SET TenPhuGia = ?, MoTa = ?, DonViTinh = ?, SoLuongTonKho = ?, NgayNhap = ?, NgayHetHan = ?
            WHERE ID = ?
        """, (TenPhuGia, MoTa, DonViTinh, SoLuongTonKho, NgayNhap, NgayHetHan, id))
        conn.commit()

        # Cập nhật kho
        cursor.execute("SELECT * FROM KhoPhuGia WHERE PhuGiaID = ?", (id,))
        kho_phugia = cursor.fetchone()

        if kho_phugia:
            cursor.execute("UPDATE KhoPhuGia SET SoLuongTon = ?, DonViTinh = ? WHERE PhuGiaID = ?", (SoLuongTonKho, DonViTinh, id))
        else:
            cursor.execute("INSERT INTO KhoPhuGia (PhuGiaID, SoLuongTon, DonViTinh) VALUES (?, ?, ?)", (id, SoLuongTonKho, DonViTinh))

        conn.commit()
        cursor.close()
        return redirect(url_for('phugiagiavi.quanlyphugiagiavi'))

    cursor.close()
    return render_template('edit_phugiagiavi.html', phugiagiavi=phugiagiavi)

@phugiagiavi_bp.route('/delete/<int:id>')
def delete_phugiagiavi(id):
    cursor = conn.cursor()

    # Lấy thông tin phụ gia cần xóa
    cursor.execute("SELECT TenPhuGia, SoLuongTonKho FROM PhuGiaGiaVi WHERE ID = ?", (id,))
    row = cursor.fetchone()
    ten_phu_gia = row.TenPhuGia
    so_luong_ton_kho = row.SoLuongTonKho

    # Lấy thông tin kho
    cursor.execute("SELECT ID, SoLuongTon FROM KhoPhuGia WHERE PhuGiaID = ?", (id,))
    kho_row = cursor.fetchone()

    if kho_row:
        kho_id = kho_row.ID
        so_luong_ton_kho_hien_tai = kho_row.SoLuongTon
        so_luong_ton_kho_moi = so_luong_ton_kho_hien_tai - so_luong_ton_kho

        if so_luong_ton_kho_moi > 0:
            # Cập nhật số lượng tồn trong kho
            cursor.execute("UPDATE KhoPhuGia SET SoLuongTon = ? WHERE ID = ?", (so_luong_ton_kho_moi, kho_id))
        else:
            # Xóa bản ghi khỏi kho nếu số lượng tồn bằng 0
            cursor.execute("DELETE FROM KhoPhuGia WHERE ID = ?", (kho_id,))

        conn.commit()

    # Xóa phụ gia khỏi bảng PhuGiaGiaVi
    cursor.execute("DELETE FROM PhuGiaGiaVi WHERE ID = ?", (id,))
    conn.commit()
    cursor.close()

    return redirect(url_for('phugiagiavi.quanlyphugiagiavi'))
@phugiagiavi_bp.route('/xuat_kho', methods=['GET', 'POST'])


@phugiagiavi_bp.route('/xuat_kho_phugia', methods=['GET', 'POST'])
def xuat_kho_phugia():
    if request.method == 'POST':
        PhuGiaID = int(request.form['PhuGiaID'])
        SoLuongXuat = int(request.form['SoLuongXuat'])
        cursor = conn.cursor()
        cursor.execute("SELECT SoLuongTon, DonViTinh FROM KhoPhuGia WHERE PhuGiaID = ?", (PhuGiaID,))
        row = cursor.fetchone()
        current_stock = row[0]
        don_vi_tinh = row[1]

        if current_stock < SoLuongXuat:
            return render_template('xuat_kho_phugia.html', phugiagiavi=get_phugiagiavi_with_stock(), error="Không đủ số lượng tồn kho", xuat_kho=get_xuat_kho_phugia())

        cursor.execute("UPDATE KhoPhuGia SET SoLuongTon = SoLuongTon - ? WHERE PhuGiaID = ?", (SoLuongXuat, PhuGiaID))
        cursor.execute("INSERT INTO XuatKhoPhuGia (PhuGiaID, SoLuongXuat, NgayXuat, DonViTinh) VALUES (?, ?, ?, ?)", (PhuGiaID, SoLuongXuat, datetime.now(), don_vi_tinh))
        conn.commit()
        cursor.close()
        return redirect(url_for('phugiagiavi.xuat_kho_phugia'))

    return render_template('xuat_kho_phugia.html', phugiagiavi=get_phugiagiavi_with_stock(), xuat_kho=get_xuat_kho_phugia())

def get_phugiagiavi_with_stock():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT PGGV.ID, PGGV.TenPhuGia, KPG.SoLuongTon, KPG.DonViTinh
        FROM PhuGiaGiaVi PGGV
        JOIN KhoPhuGia KPG ON PGGV.ID = KPG.PhuGiaID
    """)
    rows = cursor.fetchall()
    cursor.close()
    return rows

def get_xuat_kho_phugia():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT XK.ID, PGGV.TenPhuGia, XK.SoLuongXuat, XK.NgayXuat, XK.DonViTinh
        FROM XuatKhoPhuGia XK
        JOIN PhuGiaGiaVi PGGV ON XK.PhuGiaID = PGGV.ID
    """)
    rows = cursor.fetchall()
    cursor.close()
    return rows