from flask import Flask, render_template, redirect, url_for, session,request,send_file
import pyodbc
import matplotlib.pyplot as plt
import seaborn as sns
import json
import pandas as pd
import io
from io import BytesIO

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
@app.route('/generate_report')
def generate_report():
    # Connect to your database
    conn = pyodbc.connect(connection_string)
    
    # Query for NguyenLieuPhoBo
    query_1 = """
SELECT TenNguyenLieu,mota,donvitinh,SoLuongTonKho
FROM NguyenLieuPhoBo
WHERE ID IN (
    SELECT MIN(ID)
    FROM NguyenLieuPhoBo
    GROUP BY TenNguyenLieu
);
    """
    df_1 = pd.read_sql(query_1, conn)
    
    # Query for PhuGiaGiaVi
    query_2 = """
SELECT Tenphugia,mota,donvitinh,SoLuongTonKho
FROM PhuGiaGiaVi
WHERE ID IN (
    SELECT MIN(ID)
    FROM PhuGiaGiaVi
    GROUP BY tenphugia
);

    """
    df_2 = pd.read_sql(query_2, conn)
    
    conn.close()
    
    # Create a BytesIO buffer to hold the Excel data
    output = BytesIO()
    
    # Write the data to an Excel file in memory
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_1.to_excel(writer, sheet_name='NguyenLieuPhoBo', index=False)
        df_2.to_excel(writer, sheet_name='PhuGiaGiaVi', index=False)
    
    output.seek(0)
    
    # Send the Excel file to the client
    return send_file(output, download_name="report.xlsx", as_attachment=True)

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('loginregister.login'))
    
    cursor = conn.cursor()

    # Tổng hợp số lượng nguyên liệu
    cursor.execute("SELECT COUNT(DISTINCT TenNguyenLieu)  FROM NguyenLieuPhoBo")
    total_ingredients = cursor.fetchone()[0]

    # Tổng hợp số lượng món ăn
    cursor.execute("SELECT COUNT(DISTINCT TenPhuGia)  FROM phugiagiavi")
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
def fetch_data_nguyenlieu(start_date, end_date, tennguyenlieu=None):
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    query = """
    SELECT 
        n.TenNguyenLieu,
        ISNULL(SUM(i.SoLuongTonKho), 0) as TotalNhap,
        ISNULL(SUM(o.SoLuongXuat), 0) as TotalXuat
    FROM NguyenLieuPhoBo n
    LEFT JOIN NguyenLieuPhoBo i ON n.ID = i.ID AND i.NgayNhap BETWEEN ? AND ?
    LEFT JOIN XuatKhoNguyenLieu o ON n.ID = o.NguyenLieuID AND o.NgayXuat BETWEEN ? AND ?
    WHERE (? IS NULL OR ? = '' OR n.TenNguyenLieu = ?)
    GROUP BY n.TenNguyenLieu
    """
    cursor.execute(query, (start_date, end_date, start_date, end_date, tennguyenlieu, tennguyenlieu, tennguyenlieu))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    
    result = [{"TenNguyenLieu": row.TenNguyenLieu, "TotalNhap": row.TotalNhap, "TotalXuat": row.TotalXuat} for row in data]
    return result
def fetch_data_phugia(start_date, end_date, tenphugia=None):
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    query = """
    SELECT 
        p.TenPhuGia,
        ISNULL(SUM(k.SoLuongTonKho), 0) as TotalNhap,
        ISNULL(SUM(x.SoLuongXuat), 0) as TotalXuat
    FROM PhuGiaGiaVi p
    LEFT JOIN PhuGiaGiaVi k ON p.ID = k.ID AND k.NgayNhap BETWEEN ? AND ?
    LEFT JOIN XuatKhoPhuGia x ON p.ID = x.PhuGiaID AND x.NgayXuat BETWEEN ? AND ?
    WHERE (? IS NULL OR ? = '' OR p.TenPhuGia = ?)
    GROUP BY p.TenPhuGia
    """
    cursor.execute(query, (start_date, end_date, start_date, end_date, tenphugia, tenphugia, tenphugia))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    result = [{"TenPhuGia": row.TenPhuGia, "TotalNhap": row.TotalNhap, "TotalXuat": row.TotalXuat} for row in data]
    return result

@app.route('/thong_ke', methods=['GET'])
def thong_ke():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    tennguyenlieu = request.args.get('tennguyenlieu')
    tenphugia = request.args.get('tenphugia')

    data_nguyenlieu = fetch_data_nguyenlieu(start_date, end_date, tennguyenlieu)
    data_phugia = fetch_data_phugia(start_date, end_date, tenphugia)

    nguyenlieu_labels = [item['TenNguyenLieu'] for item in data_nguyenlieu] if data_nguyenlieu else []
    nguyenlieu_data_nhap = [item['TotalNhap'] for item in data_nguyenlieu] if data_nguyenlieu else []
    nguyenlieu_data_xuat = [item['TotalXuat'] for item in data_nguyenlieu] if data_nguyenlieu else []
    
    phugia_labels = [item['TenPhuGia'] for item in data_phugia] if data_phugia else []
    phugia_data_nhap = [item['TotalNhap'] for item in data_phugia] if data_phugia else []
    phugia_data_xuat = [item['TotalXuat'] for item in data_phugia] if data_phugia else []

    return render_template('./baocao/quanly_baocao.html', 
                           data_nguyenlieu=data_nguyenlieu, 
                           data_phugia=data_phugia, 
                           start_date=start_date, 
                           end_date=end_date,
                           nguyenlieu_labels=json.dumps(nguyenlieu_labels),
                           nguyenlieu_data_nhap=json.dumps(nguyenlieu_data_nhap),
                           nguyenlieu_data_xuat=json.dumps(nguyenlieu_data_xuat),
                           phugia_labels=json.dumps(phugia_labels),
                           phugia_data_nhap=json.dumps(phugia_data_nhap),
                           phugia_data_xuat=json.dumps(phugia_data_xuat))

@app.route('/plot_nguyenlieu.png')
def plot_nguyenlieu_png():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    tennguyenlieu = request.args.get('tennguyenlieu')
    data_nguyenlieu = fetch_data_nguyenlieu(start_date, end_date, tennguyenlieu)

    ten_nguyen_lieu = [row['TenNguyenLieu'] for row in data_nguyenlieu]
    total_nhap = [row['TotalNhap'] for row in data_nguyenlieu]
    total_xuat = [row['TotalXuat'] for row in data_nguyenlieu]

    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 10))
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
    tenphugia = request.args.get('tenphugia')
    data_phugia = fetch_data_phugia(start_date, end_date, tenphugia)

    ten_phu_gia = [row['TenPhuGia'] for row in data_phugia]
    total_nhap = [row['TotalNhap'] for row in data_phugia]
    total_xuat = [row['TotalXuat'] for row in data_phugia]

    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 10))
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
