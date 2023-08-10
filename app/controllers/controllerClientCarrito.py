from flask import request, render_template as render, g, redirect, url_for, flash
from app.database.database import *
from sqlalchemy.exc import SQLAlchemyError
from flask_login import current_user
from datetime import datetime


class ControllerClientCarrito:

    def onGetControllerClientCarritoList(id):
        try:
            producto = Producto.query.get(id)
            if producto != []:
                return render('client/clientCarrito.html', producto=producto)
            else:
                return render('index.html')
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)
            return render('errors/error500.html')
        
    def onGetControllerClientCarritoSaveProforma():
        try:
            
            pfscntnumpf = 0
            pfscntsubtotal = 0
            pfscntdto = 0
            pfscntiva = 0
            pfscnttotal = 0
            pfscntestado = 0
            pfscntcreatedat = datetime.now()
            pfsusersid = current_user.iduser
            #session.query(func.max(table_name.column_name)).all()
            pfscntnumpf = Canasta.query.count()
            
            if pfscntnumpf == None:
                pfscntnumpf = 1
            if pfscntnumpf != None:
                pfscntnumpf = pfscntnumpf + 1

            if pfscntnumpf != '' and pfscntsubtotal != '' and pfscntdto != '' and pfscntiva != '' and pfscnttotal != '' and pfscntestado != '' and pfscntcreatedat!= '' and pfsusersid != '':
                newCanasta = Canasta(pfscntnumpf, pfscntsubtotal, pfscntdto, pfscntiva, pfscnttotal, pfscntestado, pfscntcreatedat, pfsusersid)
                db.session.add(newCanasta)
                db.session.commit()
                flash('Guardado Correctamente', category='success')
                return redirect(url_for('clca.onGetControllerClientCategoriaList'))
            else:
                flash('LLene los campos completos porfabor', category='success')
                return redirect(url_for('clca.onGetControllerClientCategoriaList'))
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)
            return render('errors/error500.html')
    
    
    def onGetControllerClientNumProforma():
        try:
            numberProf = 0
            if current_user.is_authenticated:
                userId = current_user.iduser
                numProf = Canasta.query.filter(Canasta.pfscntsubtotal == 0 and Canasta.pfsusersid == userId)
                for item in numProf:
                    numberProf = item.pfscntnumpf
                    return numberProf
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)
            return render('errors/error500.html')

    def onGetControllerClientAnadirCanasta():
        try:
            userId = current_user.iduser
            pfsdcnumpf = g.fact
            pfsdcantidad = request.form['txtCantidad']
            pfsdcprecio = request.form['txtPrecio']
            pfsdcptotal = request.form['txtPrecioFinal']
            pfsdcestado = 1
            pfsdccreatedat = datetime.now()
            pfsdcproductoid = request.form['txtProductoId']
            canastaid = Canasta.query.filter(Canasta.pfscnttotal == 0 and Canasta.pfsusersid == userId)
            pfsabcanastaid = 0
            for item in canastaid:
                pfsabcanastaid = item.pfscntid
            if pfsdcnumpf != '' and pfsdcantidad != '' and pfsdcprecio != '' and pfsdcptotal != '' and pfsdcestado != '' and pfsdccreatedat != '' and pfsdcproductoid != '' and pfsabcanastaid != '':
                newDetalleProforma = Detallecanasta(pfsdcnumpf, pfsdcantidad, pfsdcprecio, pfsdcptotal, pfsdcestado, pfsdccreatedat, pfsdcproductoid, pfsabcanastaid)
                db.session.add(newDetalleProforma)
                db.session.commit()
                ControllerClientCarrito.onGetUpdateProductoId(pfsdcproductoid,pfsdcantidad)
                flash('Datos Actualizados', category='success')
                return redirect(url_for('rcnt.onGetControllerClientCanastaList'))
            else:
                flash('Campos vacios llene porfabor', category='success')
                return redirect(url_for('rcnt.onGetControllerClientCanastaList'))
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)
            return render('errors/error500.html')

    @staticmethod   
    def onGetUpdateProductoId(pfsabproductoid, pfsabdpcantidad):
        try:
            stok = 0
            updateProduct = Producto.query.get(pfsabproductoid)
            stok = updateProduct.pfsabprodstock
            
            updateProdStok = int(stok) - int(pfsabdpcantidad)
            updateProduct.pfsabprodstock = updateProdStok
            if updateProduct.pfsabprodstock != 0:
                db.session.commit()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)
            return render('errors/error500.html')