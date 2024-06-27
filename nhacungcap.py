from flask import Blueprint, render_template, request, redirect, url_for
import pyodbc

nhacungcap_bp = Blueprint('nhacungcap', __name__, template_folder='templates')

connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=Hiep\\SQLEXPRESS;DATABASE=quanlykhopho;Trusted_Connection=yes;"


@nhacungcap_bp.route('/list')
def list_nhacungcap():
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute("SELECT ID, TenNhaCungCap, DiaChi, SoDienThoai, Email, LoaiNguyenLieu FROM NhaCungCap")
    nhacungcaps = cursor.fetchall()
    conn.close()
    return render_template('nhacungcap/danhsach_nhacungcap.html', nhacungcaps=nhacungcaps)

@nhacungcap_bp.route('/nhacungcap/view/<int:id>')
def view_nhacungcap(id):
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute('SELECT ID, TenNhaCungCap, DiaChi, SoDienThoai, Email, LoaiNguyenLieu FROM NhaCungCap WHERE ID = ?', (id,))
    nhacungcap = cursor.fetchone()

    cursor.execute('SELECT TenNguyenLieu, GiaThanh FROM NguyenLieuPhoBo WHERE NhaCungCapID = ?', (id,))
    nguyenlieus = cursor.fetchall()
    conn.close()

    return render_template('nhacungcap/chitiet_nhacungcap.html', nhacungcap=nhacungcap, nguyenlieus=nguyenlieus)

@nhacungcap_bp.route('/nhacungcap/add', methods=['GET', 'POST'])
def add_nhacungcap():
    if request.method == 'POST':
        ten_nhacungcap = request.form['TenNhaCungCap']
        dia_chi = request.form['DiaChi']
        so_dien_thoai = request.form['SoDienThoai']
        email = request.form['Email']
        loai_nguyen_lieu = request.form['LoaiNguyenLieu']

        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO NhaCungCap (TenNhaCungCap, DiaChi, SoDienThoai, Email, LoaiNguyenLieu) VALUES (?, ?, ?, ?, ?)",
                       (ten_nhacungcap, dia_chi, so_dien_thoai, email, loai_nguyen_lieu))
        conn.commit()
        conn.close()
        return redirect(url_for('nhacungcap.list_nhacungcap'))

    return render_template('nhacungcap/them_nhacungcap.html')

@nhacungcap_bp.route('/nhacungcap/edit/<int:id>', methods=['GET', 'POST'])
def edit_nhacungcap(id):
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    if request.method == 'POST':
        ten_nhacungcap = request.form['TenNhaCungCap']
        dia_chi = request.form['DiaChi']
        so_dien_thoai = request.form['SoDienThoai']
        email = request.form['Email']
        loai_nguyen_lieu = request.form['LoaiNguyenLieu']

        cursor.execute("""
            UPDATE NhaCungCap 
            SET TenNhaCungCap = ?, DiaChi = ?, SoDienThoai = ?, Email = ?, LoaiNguyenLieu = ?
            WHERE ID = ?
        """, (ten_nhacungcap, dia_chi, so_dien_thoai, email, loai_nguyen_lieu, id))

        conn.commit()
        conn.close()
        return redirect(url_for('nhacungcap.list_nhacungcap'))

    cursor.execute('SELECT ID, TenNhaCungCap, DiaChi, SoDienThoai, Email, LoaiNguyenLieu FROM NhaCungCap WHERE ID = ?', (id,))
    nhacungcap = cursor.fetchone()
    conn.close()
    return render_template('nhacungcap/chinhsua_nhacungcap.html', nhacungcap=nhacungcap)

@nhacungcap_bp.route('/nhacungcap/delete/<int:id>', methods=['POST'])
def delete_nhacungcap(id):
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM NhaCungCap WHERE ID = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('nhacungcap.list_nhacungcap'))

@nhacungcap_bp.route('/details/<int:id>')
@nhacungcap_bp.route('/details/<int:id>', methods=['GET', 'POST'])
@nhacungcap_bp.route('/details/<int:id>', methods=['GET', 'POST'])
@nhacungcap_bp.route('/details/<int:id>', methods=['GET', 'POST'])
def details_nhacungcap(id):
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    cursor.execute("SELECT ID, TenNhaCungCap, DiaChi, SoDienThoai, Email, LoaiNguyenLieu FROM NhaCungCap WHERE ID = ?", (id,))
    nhacungcap = cursor.fetchone()

    cursor.execute("""
        SELECT nl.ID, nl.TenNguyenLieu, ncnl.Price 
        FROM NhaCungCap_NguyenLieu ncnl
        JOIN NguyenLieuPhoBo nl ON ncnl.NguyenLieuID = nl.ID
        WHERE ncnl.NhaCungCapID = ?
    """, (id,))
    products = cursor.fetchall()

    cursor.execute("SELECT MIN(ID) AS ID, TenNguyenLieu FROM NguyenLieuPhoBo GROUP BY TenNguyenLieu;")
    all_nguyenlieu = cursor.fetchall()

    conn.close()
    return render_template('nhacungcap/chitiet_nhacungcap.html', nhacungcap=nhacungcap, products=products, all_nguyenlieu=all_nguyenlieu)

@nhacungcap_bp.route('/add_product/<int:id>', methods=['POST'])
def add_product(id):
    nguyenlieu_id = request.form.get('nguyenlieu_id')
    price = request.form.get('price')

    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO NhaCungCap_NguyenLieu (NhaCungCapID, NguyenLieuID, Price) VALUES (?, ?, ?)", (id, nguyenlieu_id, price))
    conn.commit()
    conn.close()
    return redirect(url_for('nhacungcap.details_nhacungcap', id=id))

@nhacungcap_bp.route('/edit_product_form/<int:id>/<int:nguyenlieu_id>', methods=['GET'])
def edit_product_form(id, nguyenlieu_id):
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    cursor.execute("SELECT Price FROM NhaCungCap_NguyenLieu WHERE NhaCungCapID = ? AND NguyenLieuID = ?", (id, nguyenlieu_id))
    product = cursor.fetchone()

    cursor.execute("SELECT TenNguyenLieu FROM NguyenLieuPhoBo WHERE ID = ?", (nguyenlieu_id,))
    nguyenlieu = cursor.fetchone()

    conn.close()
    return render_template('nhacungcap/edit_product.html', nhacungcap_id=id, nguyenlieu_id=nguyenlieu_id, product=product, nguyenlieu=nguyenlieu)

@nhacungcap_bp.route('/edit_product/<int:id>/<int:nguyenlieu_id>', methods=['POST'])
def edit_product(id, nguyenlieu_id):
    price = request.form.get('price')
    tennguyenlieu = request.form.get('tennguyenlieu')

    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute("UPDATE NhaCungCap_NguyenLieu SET Price = ? WHERE NhaCungCapID = ? AND NguyenLieuID = ?", (price, id, nguyenlieu_id))
    cursor.execute("UPDATE NguyenLieuPhoBo SET TenNguyenLieu = ? WHERE ID = ?", (tennguyenlieu, nguyenlieu_id))
    conn.commit()
    conn.close()
    return redirect(url_for('nhacungcap.details_nhacungcap', id=id))

@nhacungcap_bp.route('/delete_product/<int:id>/<int:nguyenlieu_id>', methods=['POST'])
def delete_product(id, nguyenlieu_id):
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM NhaCungCap_NguyenLieu WHERE NhaCungCapID = ? AND NguyenLieuID = ?", (id, nguyenlieu_id))
    conn.commit()
    conn.close()
    return redirect(url_for('nhacungcap.details_nhacungcap', id=id))