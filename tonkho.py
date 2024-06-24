from flask import Blueprint, render_template
import pyodbc
from datetime import datetime, timedelta

tonkho_bp = Blueprint('tonkho', __name__, template_folder='templates/tonkho')

connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=minhhoa;DATABASE=quanlykhopho;UID=sa;PWD=123"

@tonkho_bp.route('/')
def quanly_tonkho():
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM NguyenLieuPhoBo")
    nguyenlieu = cursor.fetchall()
    conn.close()
    
    # Checking for low inventory and setting reorder level
    reorder_level = 50  # Example value, you can set it according to your requirement
    low_inventory_items = [item for item in nguyenlieu if item.SoLuongTonKho < reorder_level]

    return render_template('quanly_tonkho.html', nguyenlieu=nguyenlieu, low_inventory_items=low_inventory_items)

@tonkho_bp.route('/han_su_dung')
def quanly_hansudung():
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM NguyenLieuPhoBo")
    nguyenlieu = cursor.fetchall()
    conn.close()
    
    # Checking for near expiry items
    near_expiry_threshold = (datetime.now() + timedelta(days=7)).date()  # Convert to date object
    near_expiry_items = [item for item in nguyenlieu if item.NgayHetHan and item.NgayHetHan < near_expiry_threshold]

    return render_template('quanly_hansudung.html', nguyenlieu=nguyenlieu, near_expiry_items=near_expiry_items)