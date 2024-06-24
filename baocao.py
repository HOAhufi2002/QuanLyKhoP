from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_file
import pyodbc
from datetime import datetime
import matplotlib.pyplot as plt
import io
import base64

baocao_bp = Blueprint('baocao', __name__, template_folder='templates')

connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=minhhoa;DATABASE=quanlykhopho;UID=sa;PWD=123"

@baocao_bp.route('/baocao')
def quanly_baocao():
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # Lấy thông tin tồn kho từ bảng NguyenLieuPhoBo
    cursor.execute("SELECT TenNguyenLieu, SoLuongTonKho FROM NguyenLieuPhoBo")
    nguyenlieu = cursor.fetchall()

    # Lấy thông tin tồn kho từ bảng PhuGiaGiaVi
    cursor.execute("SELECT  TenPhuGia, SoLuongTonKho FROM PhuGiaGiaVi")
    phugiagiavi = cursor.fetchall()

    # Tính toán mức tiêu thụ và hiệu suất tồn kho
    tong_nguyenlieu_tonkho = sum([item.SoLuongTonKho for item in nguyenlieu])
    tong_phugiagiavi_tonkho = sum([item.SoLuongTonKho for item in phugiagiavi])
    hieu_suat_tonkho = tong_nguyenlieu_tonkho + tong_phugiagiavi_tonkho

    # Vẽ biểu đồ
    labels = [item.TenNguyenLieu for item in nguyenlieu] + [item.TenPhuGia for item in phugiagiavi]
    values = [item.SoLuongTonKho for item in nguyenlieu] + [item.SoLuongTonKho for item in phugiagiavi]

    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color='skyblue')
    plt.xlabel('Nguyên Liệu / Phụ Gia')
    plt.ylabel('Số Lượng Tồn Kho')
    plt.title('Hiệu Suất Quản Lý Tồn Kho và Mức Độ Tiêu Thụ của Nguyên Liệu')
    plt.xticks(rotation=90)

    # Lưu biểu đồ vào buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    conn.close()

    return render_template('baocao/quanly_baocao.html', nguyenlieu=nguyenlieu, phugiagiavi=phugiagiavi, hieu_suat_tonkho=hieu_suat_tonkho, img_base64=img_base64)
