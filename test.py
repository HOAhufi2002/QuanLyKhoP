from flask import Blueprint, render_template, request, redirect, url_for
import pyodbc
from datetime import datetime, timedelta

tonkho_bp = Blueprint('tonkho', __name__, template_folder='templates/tonkho')

connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=minhhoa;DATABASE=quanlykhopho;UID=sa;PWD=123"

@tonkho_bp.route('/')
def quanly_tonkho():
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    
    # Lấy danh sách nguyên liệu từ kho
    cursor.execute("""
        SELECT KNL.NguyenLieuID, NLB.TenNguyenLieu, KNL.SoLuongTon, NLB.DonViTinh
        FROM KhoNguyenLieu KNL
        JOIN NguyenLieuPhoBo NLB ON KNL.NguyenLieuID = NLB.ID
    """)
    nguyenlieu = cursor.fetchall()
    
    # Lấy danh sách phụ gia từ kho
    cursor.execute("""
        SELECT KPG.PhuGiaID, PG.TenPhuGia, KPG.SoLuongTon, PG.DonViTinh
        FROM KhoPhuGia KPG
        JOIN PhuGiaGiaVi PG ON KPG.PhuGiaID = PG.ID
    """)
    phugiagiavi = cursor.fetchall()
    conn.close()
    
    # Checking for low inventory and setting reorder level
    reorder_level = 50  # Example value, you can set it according to your requirement
    low_inventory_nguyenlieu = [item for item in nguyenlieu if item.SoLuongTon < reorder_level]
    low_inventory_phugiagiavi = [item for item in phugiagiavi if item.SoLuongTon < reorder_level]

    return render_template('quanly_tonkho.html', nguyenlieu=nguyenlieu, low_inventory_nguyenlieu=low_inventory_nguyenlieu, phugiagiavi=phugiagiavi, low_inventory_phugiagiavi=low_inventory_phugiagiavi)

@tonkho_bp.route('/han_su_dung')
def quanly_hansudung():
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    
    # Lấy danh sách nguyên liệu
    cursor.execute("""
        SELECT ID, TenNguyenLieu, SoLuongTonKho, DonViTinh, NgayHetHan
        FROM NguyenLieuPhoBo
    """)
    nguyenlieu = cursor.fetchall()
    
    # Lấy danh sách phụ gia
    cursor.execute("""
        SELECT ID, TenPhuGia, SoLuongTonKho, DonViTinh, NgayHetHan
        FROM PhuGiaGiaVi
    """)
    phugiagiavi = cursor.fetchall()
    conn.close()
    
    # Checking for near expiry items
    near_expiry_threshold = (datetime.now() + timedelta(days=7)).date()  # Convert to date object
    near_expiry_nguyenlieu = [item for item in nguyenlieu if item.NgayHetHan and item.NgayHetHan < near_expiry_threshold]
    near_expiry_phugiagiavi = [item for item in phugiagiavi if item.NgayHetHan and item.NgayHetHan < near_expiry_threshold]

    return render_template('quanly_hansudung.html', nguyenlieu=nguyenlieu, near_expiry_nguyenlieu=near_expiry_nguyenlieu, phugiagiavi=phugiagiavi, near_expiry_phugiagiavi=near_expiry_phugiagiavi)
