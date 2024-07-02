from flask import Flask, render_template, redirect, url_for, session,request,send_file
import pyodbc
import matplotlib.pyplot as plt
import seaborn as sns
import json
import pandas as pd
import io
from io import BytesIO
import base64
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Cấu hình kết nối với SQL Server
connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=minhhoa;DATABASE=quanlykhopho;UID=sa;PWD=123"
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
    cursor.execute("SELECT COUNT(DISTINCT TenNguyenLieu) FROM NguyenLieuPhoBo")
    total_ingredients = cursor.fetchone()[0]

    # Tổng hợp số lượng món ăn
    cursor.execute("SELECT COUNT(DISTINCT TenPhuGia) FROM PhuGiaGiaVi")
    total_dishes = cursor.fetchone()[0]

    # Tổng hợp số lượng nhà cung cấp
    cursor.execute("SELECT COUNT(*) FROM NhaCungCap")
    total_suppliers = cursor.fetchone()[0]

    # Lấy thông tin nguyên liệu
    cursor.execute("""
        SELECT TenNguyenLieu, SUM(SoLuongTonKho) AS SoLuongTonKho, DonViTinh
        FROM NguyenLieuPhoBo
        GROUP BY TenNguyenLieu, DonViTinh
    """)
    nguyenlieu_phobo = cursor.fetchall()

    # Lấy thông tin phụ gia
    cursor.execute("""
        SELECT TenPhuGia, SUM(SoLuongTonKho) AS SoLuongTonKho, DonViTinh
        FROM PhuGiaGiaVi
        GROUP BY TenPhuGia, DonViTinh
    """)
    phugiagiavi = cursor.fetchall()

    # Chuyển đổi kết quả truy vấn thành danh sách các tên nguyên liệu và mức tồn kho
    pho_ingredient_names = [row[0] for row in nguyenlieu_phobo]
    pho_ingredient_stock_levels = [row[1] for row in nguyenlieu_phobo]

    # Chuyển đổi kết quả truy vấn thành danh sách các tên phụ gia và mức tồn kho
    gia_vi_names = [row[0] for row in phugiagiavi]
    gia_vi_stock_levels = [row[1] for row in phugiagiavi]

    # Lấy thông tin nhà cung cấp
    cursor.execute("""
        SELECT TenNhaCungCap, COUNT(*) 
        FROM NhaCungCap_NguyenLieu 
        JOIN NhaCungCap ON NhaCungCap.ID = NhaCungCap_NguyenLieu.NhaCungCapID 
        GROUP BY TenNhaCungCap
    """)
    suppliers = cursor.fetchall()
    supplier_names = [row[0] for row in suppliers]
    ingredients_by_supplier = [row[1] for row in suppliers]

    cursor.close()

    return render_template('index.html', 
                           total_ingredients=total_ingredients, 
                           total_dishes=total_dishes, 
                           total_suppliers=total_suppliers, 
                           pho_ingredient_names=pho_ingredient_names, 
                           pho_ingredient_stock_levels=pho_ingredient_stock_levels,
                           gia_vi_names=gia_vi_names,
                           gia_vi_stock_levels=gia_vi_stock_levels,
                           supplier_names=supplier_names, 
                           ingredients_by_supplier=ingredients_by_supplier)

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
    
    result = [{"TenNguyenLieu": row[0], "TotalNhap": row[1], "TotalXuat": row[2]} for row in data]
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
    result = [{"TenPhuGia": row[0], "TotalNhap": row[1], "TotalXuat": row[2]} for row in data]
    return result

def create_chart(data, title, xlabel, ylabel):
    if "TenNguyenLieu" in data[0]:
        labels = [row['TenNguyenLieu'] for row in data]
    else:
        labels = [row['TenPhuGia'] for row in data]
    
    total_nhap = [row['TotalNhap'] for row in data]
    total_xuat = [row['TotalXuat'] for row in data]

    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 5))
    ax = sns.barplot(x=labels, y=total_nhap, color='blue', label='Nhập Kho')
    sns.barplot(x=labels, y=total_xuat, color='red', label='Xuất Kho')

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    return img_base64

@app.route('/thong_ke', methods=['GET'])
def thong_ke():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    tennguyenlieu = request.args.get('tennguyenlieu')
    tenphugia = request.args.get('tenphugia')

    data_nguyenlieu = fetch_data_nguyenlieu(start_date, end_date, tennguyenlieu)
    data_phugia = fetch_data_phugia(start_date, end_date, tenphugia)

    nguyenlieu_chart = create_chart(data_nguyenlieu, 'Biểu đồ nhập xuất nguyên liệu', 'Nguyên liệu', 'Số lượng')
    phugia_chart = create_chart(data_phugia, 'Biểu đồ nhập xuất phụ gia', 'Phụ gia', 'Số lượng')

    return render_template('baocao/quanly_baocao.html', 
                           data_nguyenlieu=data_nguyenlieu, 
                           data_phugia=data_phugia, 
                           start_date=start_date, 
                           end_date=end_date,
                           nguyenlieu_chart=nguyenlieu_chart,
                           phugia_chart=phugia_chart)

if __name__ == '__main__':
    app.run(debug=True)