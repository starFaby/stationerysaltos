from flask import request, render_template as render, flash
from app.database.database import *
from flask import g
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

class ControllerAdminCanastaPdf:

    def onGetControllerAdminCanastaPdf(user , cnst):
        try:
            numCanasta = 0
            valorCanastaTotal = 0
            fecha =  datetime.now()
            userSelect = User.query.get(user)
            detalleFact = Canasta.query.join(Detallecanasta, Canasta.pfscntnumpf == Detallecanasta.pfsdcnumpf).join(Producto,Detallecanasta.pfsdcproductoid == Producto.pfsprodid ).add_columns(Producto.pfsprodnombre, Producto.pfsproddetalle, Detallecanasta.pfsdcantidad, Detallecanasta.pfsdcprecio, Detallecanasta.pfsdcptotal, Canasta.pfscntnumpf ,Canasta.pfscnttotal).filter(Detallecanasta.pfsdcnumpf == cnst)
            for item in detalleFact:
                valorCanastaTotal = item.pfsabpftotal

            for item in detalleFact:
                numCanasta = item.pfsabpfnumpf
            return render("admin/adminCanastaPdf.html", userSelect=userSelect, detalleFact=detalleFact, valorCanastaTotal=valorCanastaTotal, numCanasta=numCanasta, fecha=fecha)
       
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)
            return render('errors/error500.html')