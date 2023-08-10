from flask import request, render_template as render, g, redirect, url_for, flash
from app.database.database import *
from flask_login import current_user
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

class ControllerClientCanasta:

    def onGetControllerClientCanastaList():
        try:
            
            userId = current_user.iduser
            userSelect = User.query.get(userId)
            fecha =  datetime.now()
            numberFact = g.fact
            sumaTotal = 0
            detalleFact = Detallecanasta.query.join(Producto, Detallecanasta.pfsdcproductoid == Producto.pfsprodid).add_columns(Detallecanasta.pfsdcid , Detallecanasta.pfsdcproductoid, Producto.pfsprodnombre, Producto.pfsproddetalle, Detallecanasta.pfsdcantidad, Detallecanasta.pfsdcprecio, Detallecanasta.pfsdcptotal).filter(Detallecanasta.pfsdcestado == 1).filter(Detallecanasta.pfsdcnumpf == numberFact)
            for item in detalleFact:
                sumaTotal += item.pfsabdptotal

            dateGeneral = {
                "userSelect": userSelect,
                "fecha": fecha,
                "numberFact": numberFact,
                "detalleFact": detalleFact,
                "sumaTotal": sumaTotal
            }
            print(dateGeneral)

            return render('client/clientCanasta.html', dateGeneral=dateGeneral)
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)
            return render('errors/error500.html')

    def onGetControllerClientProductUpdate(dpid, dpcant, pid):
        try:
            putDetalleProforma = Detallecanasta.query.get(dpid)
            putDetalleProforma.pfsabdpestado = 0

            putProducto = Producto.query.get(pid)
            pstock = int(putProducto.pfsprodstock )
            ccanasta = int(dpcant)
            retornarProd = pstock + ccanasta
            putProducto.pfsprodstock = retornarProd
            db.session.commit()
            
            return  redirect(url_for('rcnt.onGetControllerClientCanastaList'))
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)
            return render('errors/error500.html')

    def onGetControllerClientSaveCanasta():
        try:
            pfscntnumpf = request.form["txtNumFact"]
            pfscnttotal = request.form["txtSumaTotal"]
            updateCanasta = Canasta.query.get(pfscntnumpf)
            updateCanasta.pfscnttotal = pfscnttotal
            updateCanasta.pfscntestado = 1
            db.session.commit()
            flash('Datos Actualizados', category='success')
            return redirect(url_for('clca.onGetControllerClientCategoriaList'))
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)
            return render('errors/error500.html')
       

    