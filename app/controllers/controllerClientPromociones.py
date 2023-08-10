from flask import request, render_template as render
from app.database.database import *
from sqlalchemy.exc import SQLAlchemyError

class ControllerClientPromociones:

    def onGetControllerClientPromocionesList():
        try:
            promociones = Promociones.query.join(Producto, Promociones.pfsproductoid == Producto.pfsprodid).add_columns(Producto.pfsprodnombre, Producto.pfsprodimage, Producto.pfsproddetalle , Promociones.pfspromfechainicio, Promociones.pfspromfechafin).filter(Promociones.pfspromestado == 1)
            return render('client/clientPromociones.html', promociones=promociones)
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)
            return render('errors/error500.html')
    