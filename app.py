from flask import Flask, render_template, redirect, url_for, session
import pyodbc

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


@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('loginregister.login'))
    
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM NguyenLieuPhoBo")
    total_ingredients = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM MonAn")
    total_dishes = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM NhaCungCap")
    total_suppliers = cursor.fetchone()[0]



    cursor.execute("SELECT TenNguyenLieu, SoLuongTonKho FROM NguyenLieuPhoBo")
    ingredients = cursor.fetchall()
    ingredient_names = [row[0] for row in ingredients]
    ingredient_stock_levels = [row[1] for row in ingredients]

    cursor.execute("SELECT TenNhaCungCap, COUNT(*) FROM NhaCungCap_NguyenLieu JOIN NhaCungCap ON NhaCungCap.ID = NhaCungCap_NguyenLieu.NhaCungCapID GROUP BY TenNhaCungCap")
    suppliers = cursor.fetchall()
    supplier_names = [row[0] for row in suppliers]
    ingredients_by_supplier = [row[1] for row in suppliers]

    return render_template('index.html', total_ingredients=total_ingredients, total_dishes=total_dishes, total_suppliers=total_suppliers, ingredient_names=ingredient_names, ingredient_stock_levels=ingredient_stock_levels, supplier_names=supplier_names, ingredients_by_supplier=ingredients_by_supplier)

# @app.route('/')
# def index():
#     if 'user_id' not in session:
#         return redirect(url_for('loginregister.login'))
#     return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
