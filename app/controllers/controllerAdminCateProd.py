from datetime import datetime
from flask import request, render_template as render, flash, redirect, url_for
from app.database.database import *
from sqlalchemy.exc import SQLAlchemyError


class ControllerAdminCateProd:

    def controllerAdminCateProdList(page):
        page = page
        pages = 5
        try:
            cateProd = Producto.query.order_by(Producto.pfsprodid.asc()).paginate(page=page, per_page=pages ,error_out=False)
            categorias = Categoria.query.all()
            if cateProd != [] or categorias != []:
                if request.method == 'POST' and 'tag' in request.form:
                    tag = request.form["tag"]
                    search = "%{}%".format(tag)
                    cateProd = Producto.query.filter(Producto.pfsprodnombre.like(search)).paginate(per_page=pages,error_out=False)
                    return render("admin/adminCateProd.html", cateProd=cateProd, categorias=categorias, tag = tag)
                else:    
                    flash('Producto Listadas', category='success')
                    return render("admin/adminCateProd.html", cateProd=cateProd, categorias=categorias)
            else:
                flash('No existe categorias', category='success')
                return render("admin/adminCateProd.html", cateProd=cateProd, categorias=categorias)
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)
            return render('errors/error500.html')

    def onGetControllerAdminCateProdSave():
        try:
            pfsprodmarca = request.form['txtMarca']
            pfsabprodnombre = request.form['txtNombre']
            pfsabprodimage = request.form['txtImage']
            pfsabproddetalle = request.form['txtDetalle']
            pfsabprodprecio = request.form['txtPrecio']
            pfsabprodstock = request.form['txtStock']
            pfsabprodestado = request.form['selectEstado']
            pfsabprodcreatedat = datetime.now()
            categoriaid = request.form['selectCategoria']

            if pfsprodmarca!=''and pfsabprodnombre != '' and pfsabprodimage != '' and pfsabproddetalle != ''and pfsabprodprecio != ''and pfsabprodstock != '' and pfsabprodestado != 'Elija...' and categoriaid != 'Elija...':
                newcateprod = Producto(pfsprodmarca, pfsabprodnombre, pfsabprodimage, pfsabproddetalle,pfsabprodprecio, pfsabprodstock, pfsabprodestado, pfsabprodcreatedat, categoriaid)
                db.session.add(newcateprod)
                db.session.commit()
                flash('Guardado Correctamente', category='success')
                return redirect(url_for('adcapr.controllerAdminCateProdList'))
            else:
                flash('LLene los campos completos porfabor', category='success')
                return redirect(url_for('adcapr.controllerAdminCateProdList'))
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)
            return render('errors/error500.html')
        
    def onGetControllerAdminCateProdUpdate(id):
        try:
            productos = Producto.query.get(id)
            categorias = Categoria.query.all()
            if request.method == 'POST':
                productos.pfsprodmarca = request.form['txtMarca']
                productos.pfsprodnombre = request.form['txtNombre']
                productos.pfsprodimage = request.form['txtImage']
                productos.pfsproddetalle = request.form['txtDetalle']
                productos.pfsprodprecio = request.form['txtPrecio']
                productos.pfsprodstock = request.form['txtStock']
                productos.pfsprodestado = request.form['selectEstado']
                productos.pfsabprodcreatedat = datetime.now()
                productos.pfscategoriaid = request.form['selectCategoria']
                if productos.pfsprodmarca != '' and productos.pfsprodnombre != '' and productos.pfsprodimage != '' and productos.pfsproddetalle != '' and productos.pfsprodprecio != '' and productos.pfsprodstock != '' and productos.pfsprodestado != 'Elija...' and productos.pfsabprodcreatedat != '' and productos.pfscategoriaid != 'Elija...':
                    db.session.commit()
                    flash('Datos Actualizados', category='success')
                    return redirect(url_for('adcapr.controllerAdminCateProdList'))
                else:
                    flash('Campos vacios llene porfabor', category='success')
                    return redirect(url_for('adcapr.controllerAdminCateProdList'))
            return render("modal/modalAdminCateProdUpdate.html", productos=productos, categorias=categorias)
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)
            return render('errors/error500.html')

    def onGetControllerAdminCateProdDelete(id):
        try:
            caso = Producto.query.get(id)
            if caso.pfsprodid >= 0:
                db.session.delete(caso)
                db.session.commit()
                flash('Categoria eliminada', category='danger')
                return redirect(url_for('adcapr.controllerAdminCateProdList'))
            else:
                flash('Error en el servidor', category='danger')
                return redirect(url_for('adcapr.controllerAdminCateProdList'))
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)
            return render('errors/error500.html')