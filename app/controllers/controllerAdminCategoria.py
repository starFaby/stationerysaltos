from datetime import datetime
from flask import request, render_template as render, flash, redirect, url_for
from app.database.database import *
from sqlalchemy.exc import SQLAlchemyError


class ControllerAdminCategoria:

    def controllerAdminCategoriaList(page):
        try:
            page = page
            pages = 5
            categorias = Categoria.query.order_by(Categoria.pfscateid.asc()).paginate(page=page, per_page=pages ,error_out=False)
            if categorias != []:
                if request.method == 'POST' and 'tag' in request.form:
                    tag = request.form["tag"]
                    search = "%{}%".format(tag)
                    categorias = Categoria.query.filter(Categoria.pfscatenombre.like(search)).paginate(per_page=pages,error_out=False)
                    return render("admin/adminCategoria.html", categorias=categorias, tag = tag)
                else:
                    flash('Categorias Listadas', category='success')
                    return render("admin/adminCategoria.html", categorias=categorias)
            else:
                flash('No existe categorias', category='success')
                return render("admin/adminCategoria.html", categorias=categorias)
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)
            return render('errors/error500.html')

    def onGetControllerAdminCategoriaSave():
        pfscatenombre = request.form['txtNombre']
        pfscateimage = request.form['txtImage']
        pfscatedetalle = request.form['txtDetalle']
        pfscateestado = request.form['selectEstado']
        pfscatecreatedat = datetime.now()
        try:
            if pfscatenombre != '' and pfscateimage != '' and pfscatedetalle != '' and pfscateestado != 'Elija...':
                newcategoria = Categoria(pfscatenombre, pfscateimage, pfscatedetalle, pfscateestado, pfscatecreatedat)
                db.session.add(newcategoria)
                db.session.commit()
                flash('Guardado Correctamente', category='success')
                return redirect(url_for('adcate.controllerAdminCategoriaList'))
            else:
                flash('LLene los campos completos porfabor', category='success')
                return redirect(url_for('adcate.controllerAdminCategoriaList'))
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)
            return render('errors/error500.html')
   
    def onGetControllerAdminCategoriaUpdate(id):
        try:
            categoria = Categoria.query.get(id)
            if request.method == 'POST':
                categoria.pfscatenombre = request.form['txtNombre']
                categoria.pfscateimage = request.form['txtImage']
                categoria.pfscatedetalle = request.form['txtDetalle']
                categoria.pfscateestado = request.form['selectEstado']
                if categoria.pfscatenombre != '' and categoria.pfscateimage != '' and categoria.pfscatedetalle != '' and categoria.pfscateestado != 'Elija...':
                    db.session.commit()
                    flash('Datos Actualizados', category='success')
                    return redirect(url_for('adcate.controllerAdminCategoriaList'))
                else:
                    flash('Campos vacios llene porfabor', category='success')
                    return redirect(url_for('adcate.controllerAdminCategoriaList'))

            return render("modal/modalAdminCateUpdate.html", categoria = categoria)
            
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)
            return render('errors/error500.html')
        
    def onGetControllerAdminCategoriaDelete(id):
        try:
            categoria = Categoria.query.get(id)
            if categoria.pfscateid >= 0:
                db.session.delete(categoria)
                db.session.commit()
                flash('Categoria eliminada', category='danger')
                return redirect(url_for('adcate.controllerAdminCategoriaList'))
            else:
                flash('Error en el servidor', category='danger')
                return redirect(url_for('adcate.controllerAdminCategoriaList'))
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)
            return render('errors/error500.html')
    
