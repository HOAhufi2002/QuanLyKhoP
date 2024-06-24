from flask import Blueprint, render_template, request, redirect, url_for
import pyodbc

nuocdung_bp = Blueprint('nuocdung', __name__, template_folder='templates')

connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=minhhoa;DATABASE=quanlykhopho;UID=sa;PWD=123"

@nuocdung_bp.route('/nuocdung', methods=['GET'])
def quanly_nuocdung():
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT TOP (1000) [ID]
      ,[TenCongThuc]
      ,[NguyenLieuID]
      ,[PhuGiaGiaViID]
      ,[PhuongPhap]
  FROM [quanlykhopho].[dbo].[CongThucNauNuocDung]

    """)
    congthuc_list = cursor.fetchall()
    conn.close()

    return render_template('nuocdung/quanly_nuocdung.html', congthuc_list=congthuc_list)

@nuocdung_bp.route('/nuocdung/add', methods=['GET', 'POST'])
def add_congthuc():
    if request.method == 'POST':
        TenCongThuc = request.form['TenCongThuc']
        NguyenLieuIDs = list(set(request.form.getlist('NguyenLieuID')))  # Loại bỏ phần tử trùng lặp
        PhuGiaGiaViIDs = list(set(request.form.getlist('PhuGiaGiaViID')))  # Loại bỏ phần tử trùng lặp
        PhuongPhap = request.form['PhuongPhap']
        
        nguyenlieu_str = ','.join(NguyenLieuIDs)
        phugiagiavi_str = ','.join(PhuGiaGiaViIDs)
        
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
            INSERT INTO CongThucNauNuocDung (TenCongThuc, NguyenLieuID, PhuGiaGiaViID, PhuongPhap)
            VALUES (?, ?, ?, ?)
            """, (TenCongThuc, nguyenlieu_str, phugiagiavi_str, PhuongPhap))
            conn.commit()
        except Exception as e:
            conn.rollback()
            return str(e)
        finally:
            conn.close()
        
        return redirect(url_for('nuocdung.quanly_nuocdung'))

    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute("SELECT ID, TenNguyenLieu FROM NguyenLieuPhoBo")
    nguyenlieu_list = cursor.fetchall()
    cursor.execute("SELECT ID, TenPhuGia FROM PhuGiaGiaVi")
    phugiagiavi_list = cursor.fetchall()
    conn.close()

    return render_template('nuocdung/add_congthuc.html', nguyenlieu_list=nguyenlieu_list, phugiagiavi_list=phugiagiavi_list)

@nuocdung_bp.route('/edit_congthuc/<int:id>', methods=['GET', 'POST'])
def edit_congthuc(id):
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    
    if request.method == 'POST':
        TenCongThuc = request.form['TenCongThuc']
        NguyenLieuID = ', '.join(request.form.getlist('NguyenLieuID'))
        PhuGiaGiaViID = ', '.join(request.form.getlist('PhuGiaGiaViID'))
        PhuongPhap = request.form['PhuongPhap']
        
        cursor.execute("""
            UPDATE CongThucNauNuocDung
            SET TenCongThuc = ?, NguyenLieuID = ?, PhuGiaGiaViID = ?, PhuongPhap = ?
            WHERE ID = ?
        """, (TenCongThuc, NguyenLieuID, PhuGiaGiaViID, PhuongPhap, id))
        conn.commit()
        conn.close()
        
        return redirect(url_for('nuocdung.quanly_nuocdung'))
    
    cursor.execute("SELECT * FROM CongThucNauNuocDung WHERE ID = ?", (id,))
    congthuc = cursor.fetchone()
    
    cursor.execute("SELECT * FROM NguyenLieuPhoBo")
    nguyenlieu_list = cursor.fetchall()
    
    cursor.execute("SELECT * FROM PhuGiaGiaVi")
    phugiagiavi_list = cursor.fetchall()
    
    conn.close()
    
    return render_template('nuocdung/edit_congthuc.html', congthuc=congthuc, nguyenlieu_list=nguyenlieu_list, phugiagiavi_list=phugiagiavi_list)


    cursor.execute("SELECT * FROM CongThucNauNuocDung WHERE ID = ?", (id,))
    congthuc = cursor.fetchone()
    
    cursor.execute("SELECT ID, TenNguyenLieu FROM NguyenLieuPhoBo")
    nguyenlieu_list = cursor.fetchall()
    cursor.execute("SELECT ID, TenPhuGia FROM PhuGiaGiaVi")
    phugiagiavi_list = cursor.fetchall()
    conn.close()

    return render_template('nuocdung/edit_congthuc.html', congthuc=congthuc, nguyenlieu_list=nguyenlieu_list, phugiagiavi_list=phugiagiavi_list)

@nuocdung_bp.route('/nuocdung/delete/<int:id>', methods=['POST'])
def delete_congthuc(id):
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM CongThucNauNuocDung WHERE ID = ?", (id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return str(e)
    finally:
        conn.close()
    
    return redirect(url_for('nuocdung.quanly_nuocdung'))
