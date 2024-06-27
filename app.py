from flask import Flask, render_template, redirect, url_for, session,request,send_file
import pyodbc
import matplotlib.pyplot as plt
import seaborn as sns

import io
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Cấu hình kết nối với SQL Server
connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=Hiep\\SQLEXPRESS;DATABASE=quanlykhopho;Trusted_Connection=yes;"
conn = pyodbc.connect(connection_string)
from thucdon import thucdon_bp
app.register_blueprint(thucdon_bp, url_prefix='/thucdon')
from nguyenlieu import nguyenlieu_bp
app.register_blueprint(nguyenlieu_bp, url_prefix='/nguyenlieu')

from phugiagiavi import phugiagiavi_bp
app.register_blueprint(phugiagiavi_bp, url_prefix='/phugiagiavi')

from nuocdung import nuocdung_bp
app.register_blueprint(nuocdung_bp, url_prefix='/nuocdung')

from loginregister import loginregister_bp
app.register_blueprint(loginregister_bp, url_prefix='/auth')

from baocao import baocao_bp
app.register_blueprint(baocao_bp, url_prefix='/baocao')

from tonkho import tonkho_bp
app.register_blueprint(tonkho_bp, url_prefix='/tonkho')

from nhacungcap import nhacungcap_bp
app.register_blueprint(nhacungcap_bp, url_prefix='/nhacungcap')

from quanlynguyenlieuphugia import quanlynguyenlieuphugia_bp
app.register_blueprint(quanlynguyenlieuphugia_bp, url_prefix='/quanlynguyenlieuphugia')

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('loginregister.login'))
    
    cursor = conn.cursor()

    # Tổng hợp số lượng nguyên liệu
    cursor.execute("SELECT COUNT(*) FROM NguyenLieuPhoBo")
    total_ingredients = cursor.fetchone()[0]

    # Tổng hợp số lượng món ăn
    cursor.execute("SELECT COUNT(*) FROM MonAn")
    total_dishes = cursor.fetchone()[0]

    # Tổng hợp số lượng nhà cung cấp
    cursor.execute("SELECT COUNT(*) FROM NhaCungCap")
    total_suppliers = cursor.fetchone()[0]

    # Lấy thông tin nguyên liệu và phụ gia
    cursor.execute("""
        SELECT TenNguyenLieu, SUM(SoLuongTonKho) AS SoLuongTonKho, DonViTinh
        FROM (
            SELECT TenNguyenLieu, SoLuongTonKho, DonViTinh FROM NguyenLieuPhoBo
            UNION ALL
            SELECT TenPhuGia AS TenNguyenLieu, SoLuongTonKho, DonViTinh FROM PhuGiaGiaVi
        ) AS Combined
        GROUP BY TenNguyenLieu, DonViTinh
    """)
    combined_ingredients = cursor.fetchall()

    # Tên nguyên liệu và mức tồn kho
    ingredient_names = [row.TenNguyenLieu for row in combined_ingredients]
    ingredient_stock_levels = [row.SoLuongTonKho for row in combined_ingredients]

    # Lấy thông tin nhà cung cấp
    cursor.execute("SELECT TenNhaCungCap, COUNT(*) FROM NhaCungCap_NguyenLieu JOIN NhaCungCap ON NhaCungCap.ID = NhaCungCap_NguyenLieu.NhaCungCapID GROUP BY TenNhaCungCap")
    suppliers = cursor.fetchall()
    supplier_names = [row[0] for row in suppliers]
    ingredients_by_supplier = [row[1] for row in suppliers]

    cursor.close()

    return render_template('index.html', total_ingredients=total_ingredients, total_dishes=total_dishes, total_suppliers=total_suppliers, ingredient_names=ingredient_names, ingredient_stock_levels=ingredient_stock_levels, supplier_names=supplier_names, ingredients_by_supplier=ingredients_by_supplier)

@app.route('/thongke', methods=['GET', 'POST'])
def thong_ke():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    data_nguyenlieu = []
    data_phugia = []

    if start_date and end_date:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        query_nguyenlieu = """
        SELECT 
            n.TenNguyenLieu,
            ISNULL(SUM(i.SoLuongTonKho), 0) as TotalNhap,
            ISNULL(SUM(o.SoLuongXuat), 0) as TotalXuat
        FROM NguyenLieuPhoBo n
        LEFT JOIN NguyenLieuPhoBo i ON n.ID = i.ID AND i.NgayNhap BETWEEN ? AND ?
        LEFT JOIN XuatKhoNguyenLieu o ON n.ID = o.NguyenLieuID AND o.NgayXuat BETWEEN ? AND ?
        GROUP BY n.TenNguyenLieu
        """
        cursor.execute(query_nguyenlieu, (start_date, end_date, start_date, end_date))
        data_nguyenlieu = cursor.fetchall()

        query_phugia = """
        SELECT 
            p.TenPhuGia,
            ISNULL(SUM(k.SoLuongTonKho), 0) as TotalNhap,
            ISNULL(SUM(x.SoLuongXuat), 0) as TotalXuat
        FROM PhuGiaGiaVi p
        LEFT JOIN PhuGiaGiaVi k ON p.ID = k.ID AND k.NgayNhap BETWEEN ? AND ?
        LEFT JOIN XuatKhoPhuGia x ON p.ID = x.PhuGiaID AND x.NgayXuat BETWEEN ? AND ?
        GROUP BY p.TenPhuGia
        """
        cursor.execute(query_phugia, (start_date, end_date, start_date, end_date))
        data_phugia = cursor.fetchall()

        conn.close()

    return render_template('./baocao/quanly_baocao.html', data_nguyenlieu=data_nguyenlieu, data_phugia=data_phugia, start_date=start_date, end_date=end_date)

@app.route('/plot_nguyenlieu.png')
def plot_nguyenlieu_png():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    query_nguyenlieu = """
    SELECT 
        n.TenNguyenLieu,
        ISNULL(SUM(i.SoLuongTonKho), 0) as TotalNhap,
        ISNULL(SUM(o.SoLuongXuat), 0) as TotalXuat
    FROM NguyenLieuPhoBo n
    LEFT JOIN NguyenLieuPhoBo i ON n.ID = i.ID AND i.NgayNhap BETWEEN ? AND ?
    LEFT JOIN XuatKhoNguyenLieu o ON n.ID = o.NguyenLieuID AND o.NgayXuat BETWEEN ? AND ?
    GROUP BY n.TenNguyenLieu
    """
    cursor.execute(query_nguyenlieu, (start_date, end_date, start_date, end_date))
    data_nguyenlieu = cursor.fetchall()
    conn.close()

    ten_nguyen_lieu = [row.TenNguyenLieu for row in data_nguyenlieu]
    total_nhap = [row.TotalNhap for row in data_nguyenlieu]
    total_xuat = [row.TotalXuat for row in data_nguyenlieu]

    sns.set(style="whitegrid")
    plt.figure(figsize=(14, 8))
    ax = sns.barplot(x=ten_nguyen_lieu, y=total_nhap, color='blue', label='Nhập Kho')
    sns.barplot(x=ten_nguyen_lieu, y=total_xuat, color='red', label='Xuất Kho')

    ax.set_title('Biểu đồ nhập xuất nguyên liệu')
    ax.set_xlabel('Nguyên liệu')
    ax.set_ylabel('Số lượng')
    ax.legend()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return send_file(img, mimetype='image/png')

@app.route('/plot_phugia.png')
def plot_phugia_png():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    query_phugia = """
    SELECT 
        p.TenPhuGia,
        ISNULL(SUM(k.SoLuongTonKho), 0) as TotalNhap,
        ISNULL(SUM(x.SoLuongXuat), 0) as TotalXuat
    FROM PhuGiaGiaVi p
    LEFT JOIN PhuGiaGiaVi k ON p.ID = k.ID AND k.NgayNhap BETWEEN ? AND ?
    LEFT JOIN XuatKhoPhuGia x ON p.ID = x.PhuGiaID AND x.NgayXuat BETWEEN ? AND ?
    GROUP BY p.TenPhuGia
    """
    cursor.execute(query_phugia, (start_date, end_date, start_date, end_date))
    data_phugia = cursor.fetchall()
    conn.close()

    ten_phu_gia = [row.TenPhuGia for row in data_phugia]
    total_nhap = [row.TotalNhap for row in data_phugia]
    total_xuat = [row.TotalXuat for row in data_phugia]

    sns.set(style="whitegrid")
    plt.figure(figsize=(14, 8))
    ax = sns.barplot(x=ten_phu_gia, y=total_nhap, color='blue', label='Nhập Kho')
    sns.barplot(x=ten_phu_gia, y=total_xuat, color='red', label='Xuất Kho')

    ax.set_title('Biểu đồ nhập xuất phụ gia')
    ax.set_xlabel('Phụ gia')
    ax.set_ylabel('Số lượng')
    ax.legend()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)