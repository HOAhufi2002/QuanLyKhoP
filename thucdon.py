from flask import Blueprint, render_template, request, redirect, url_for, session
import pyodbc

thucdon_bp = Blueprint('thucdon', __name__, template_folder='templates')

connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=Hiep\\SQLEXPRESS;DATABASE=quanlykhopho;Trusted_Connection=yes;"

@thucdon_bp.route('/thucdon')
def quanly_thucdon():
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM ThucDon")
    thucdon_list = cursor.fetchall()
    
    conn.close()
    return render_template('thucdon/quanly_thucdon.html', thucdon_list=thucdon_list)

@thucdon_bp.route('/thucdon/add', methods=['GET', 'POST'])
def add_thucdon():
    if request.method == 'POST':
        TenThucDon = request.form['TenThucDon']
        MoTa = request.form['MoTa']
        
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO ThucDon (TenThucDon, MoTa) VALUES (?, ?)", (TenThucDon, MoTa))
        conn.commit()
        conn.close()
        
        return redirect(url_for('thucdon.quanly_thucdon'))
    
    return render_template('thucdon/add_thucdon.html')

@thucdon_bp.route('/thucdon/edit/<int:id>', methods=['GET', 'POST'])
def edit_thucdon(id):
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    
    if request.method == 'POST':
        TenThucDon = request.form['TenThucDon']
        MoTa = request.form['MoTa']
        
        cursor.execute("UPDATE ThucDon SET TenThucDon = ?, MoTa = ? WHERE ID = ?", (TenThucDon, MoTa, id))
        conn.commit()
        conn.close()
        
        return redirect(url_for('thucdon.quanly_thucdon'))
    
    cursor.execute("SELECT * FROM ThucDon WHERE ID = ?", (id,))
    thucdon = cursor.fetchone()
    
    conn.close()
    return render_template('thucdon/edit_thucdon.html', thucdon=thucdon)

@thucdon_bp.route('/thucdon/delete/<int:id>', methods=['POST'])
def delete_thucdon(id):
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM ThucDon WHERE ID = ?", (id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('thucdon.quanly_thucdon'))

@thucdon_bp.route('/monan/<int:thucdon_id>')
def quanly_monan(thucdon_id):
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM MonAn WHERE ThucDonID = ?", (thucdon_id,))
    monan_list = cursor.fetchall()
    
    conn.close()
    return render_template('thucdon/quanly_monan.html', monan_list=monan_list, thucdon_id=thucdon_id)

@thucdon_bp.route('/monan/add/<int:thucdon_id>', methods=['GET', 'POST'])
def add_monan(thucdon_id):
    if request.method == 'POST':
        TenMonAn = request.form['TenMonAn']
        MoTa = request.form['MoTa']
        NguyenLieu = ', '.join(request.form.getlist('NguyenLieu'))
        PhuGiaGiaVi = ', '.join(request.form.getlist('PhuGiaGiaVi'))
        PhuongPhap = request.form['PhuongPhap']
        
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO MonAn (TenMonAn, ThucDonID, MoTa, NguyenLieu, PhuGiaGiaVi, PhuongPhap) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (TenMonAn, thucdon_id, MoTa, NguyenLieu, PhuGiaGiaVi, PhuongPhap))
        conn.commit()
        conn.close()
        
        return redirect(url_for('thucdon.quanly_monan', thucdon_id=thucdon_id))
    
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM NguyenLieuPhoBo")
    nguyenlieu_list = cursor.fetchall()
    
    cursor.execute("SELECT * FROM PhuGiaGiaVi")
    phugiagiavi_list = cursor.fetchall()
    
    conn.close()
    
    return render_template('thucdon/add_monan.html', thucdon_id=thucdon_id, nguyenlieu_list=nguyenlieu_list, phugiagiavi_list=phugiagiavi_list)

@thucdon_bp.route('/monan/edit/<int:id>', methods=['GET', 'POST'])
def edit_monan(id):
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    
    if request.method == 'POST':
        TenMonAn = request.form['TenMonAn']
        MoTa = request.form['MoTa']
        NguyenLieu = ', '.join(request.form.getlist('NguyenLieu'))
        PhuGiaGiaVi = ', '.join(request.form.getlist('PhuGiaGiaVi'))
        PhuongPhap = request.form['PhuongPhap']
        
        cursor.execute("""
            UPDATE MonAn
            SET TenMonAn = ?, MoTa = ?, NguyenLieu = ?, PhuGiaGiaVi = ?, PhuongPhap = ?
            WHERE ID = ?
        """, (TenMonAn, MoTa, NguyenLieu, PhuGiaGiaVi, PhuongPhap, id))
        conn.commit()
        conn.close()
        
        return redirect(url_for('thucdon.quanly_monan', thucdon_id=request.form['ThucDonID']))
    
    cursor.execute("SELECT * FROM MonAn WHERE ID = ?", (id,))
    monan = cursor.fetchone()
    
    cursor.execute("SELECT * FROM NguyenLieuPhoBo")
    nguyenlieu_list = cursor.fetchall()
    
    cursor.execute("SELECT * FROM PhuGiaGiaVi")
    phugiagiavi_list = cursor.fetchall()
    
    conn.close()
    
    return render_template('thucdon/edit_monan.html', monan=monan, nguyenlieu_list=nguyenlieu_list, phugiagiavi_list=phugiagiavi_list)

@thucdon_bp.route('/monan/delete/<int:id>', methods=['POST'])
def delete_monan(id):
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    
    cursor.execute("SELECT ThucDonID FROM MonAn WHERE ID = ?", (id,))
    thucdon_id = cursor.fetchone().ThucDonID
    
    cursor.execute("DELETE FROM MonAn WHERE ID = ?", (id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('thucdon.quanly_monan', thucdon_id=thucdon_id))
