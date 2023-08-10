import sys
from datetime import datetime
from app.database.database import *
def createDB():
    db.drop_all()
    db.create_all()

def initDB():
    createDB()
    admin = User( 
        pfsuserscedula = "1725302705",
        pfsusersnombres = "edgar fabian",
        pfsusersapellidos = "estrella guambuguete",
        pfsusersusername = "starfaby",
        pfsusersemail = "star._faby@hotmail.com",
        pfsuserspassword = "star123",
        pfsusersdireccion = "Ferroviaria Media Adrian Navarro S11-82 y puna", 
        pfsuserscellphone = "0983856136", 
        pfsusersphone = "022647002", 
        pfsusersisadmin = True,
        pfsusersavatar = "https://res.cloudinary.com/dqmbrjl7jfs/image/upload/v1638923678/starfaby_uqbwru.jpg",
        pfsusersestado = 1,
        pfsuserscreatedat = datetime.now()
           
    )
    admin.onGetSetPassword(admin.pfsuserspassword)
    db.session.add(admin)
    db.session.commit()  
    return 'base de datos creado existosamente'  