from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

#---------------------------
#drop database flaskmysql
#create database flaskmysql
#---------------------------

#----------------------------
#----------usuario----------
#--------------------------
class User(db.Model):
    __tablename__='pfsusers'

    pfsusersid = db.Column(db.Integer, primary_key=True)
    pfsuserscedula = db.Column(db.String(80), nullable=False)
    pfsusersnombres = db.Column(db.String(80), nullable=False)
    pfsusersapellidos = db.Column(db.String(80), nullable=False)
    pfsusersusername = db.Column(db.String(30), unique=True, nullable=False)
    pfsusersemail = db.Column(db.String(120), nullable=False)
    pfsuserspassword = db.Column(db.String(250), nullable=True)
    pfsusersdireccion = db.Column(db.String(100), nullable=True)
    pfsuserscellphone = db.Column(db.String(25), nullable=False)
    pfsusersphone = db.Column(db.String(20), nullable=False)
    pfsusersisadmin = db.Column(db.Boolean, default=False)
    pfsusersavatar = db.Column(db.String(250), nullable=True)
    pfsusersestado = db.Column(db.String(1), nullable=True)
    pfsuserscreatedat = db.Column(db.Date, nullable=True) 

    def onGetSetPassword(self, pfsuserspassword):
        self.pfsuserspassword = generate_password_hash(pfsuserspassword)

    def onGetCheckPassword(self, pfsuserspassword):
        return check_password_hash(self.pfsuserspassword, pfsuserspassword)

    def __init__(self, pfsuserscedula, pfsusersnombres, pfsusersapellidos, pfsusersusername, pfsusersemail, pfsuserspassword, pfsusersdireccion,  pfsuserscellphone, pfsusersphone, pfsusersisadmin, pfsusersavatar, pfsusersestado, pfsuserscreatedat):
        self.pfsuserscedula = pfsuserscedula
        self.pfsusersnombres = pfsusersnombres
        self.pfsusersapellidos = pfsusersapellidos
        self.pfsusersusername = pfsusersusername
        self.pfsusersemail = pfsusersemail
        self.pfsuserspassword = pfsuserspassword 
        self.pfsusersdireccion = pfsusersdireccion 
        self.pfsuserscellphone = pfsuserscellphone
        self.pfsusersphone = pfsusersphone
        self.pfsusersisadmin = pfsusersisadmin
        self.pfsusersavatar = pfsusersavatar
        self.pfsusersestado = pfsusersestado
        self.pfsuserscreatedat = pfsuserscreatedat

class UserSchema(ma.Schema):
    class Meta:
        fields = ('pfsusersid', 'pfsuserscedula', 'pfsusersnombres', 'pfsusersapellidos', 'pfsusersusername', 'pfsusersemail', 'pfsuserspassword', 'pfsusersdireccion',  'pfsuserscellphone', 'pfsusersphone', 'pfsusersisadmin', 'pfsusersavatar', 'pfsusersestado', 'pfsuserscreatedat')

userSchema = UserSchema()
usersSchema = UserSchema(many=True)

#----------------------------
#----------Canasta----------
#--------------------------

class Canasta(db.Model):
    __tablename__='pfscanasta'

    pfscntid = db.Column(db.Integer, primary_key=True)
    pfscntnumpf = db.Column(db.Integer, nullable=False)
    pfscntsubtotal = db.Column(db.Integer, nullable=False)
    pfscntdto = db.Column(db.Integer, nullable=False)
    pfscntiva = db.Column(db.Integer, nullable=False)
    pfscnttotal = db.Column(db.Integer, nullable=False)
    pfscntestado = db.Column(db.String(1), nullable=True)
    pfscntcreatedat = db.Column(db.Date, nullable=True) 

    pfsusersid = db.Column(db.Integer, db.ForeignKey('pfsusers.pfsusersid',ondelete='CASCADE'), nullable=False)
    pfsusers = db.relationship('User',backref=db.backref('pfscanasta',lazy=True))



    def __init__(self, pfscntnumpf, pfscntsubtotal, pfscntdto, pfscntiva, pfscnttotal, pfscntestado, pfscntcreatedat, pfsusersid):
        self.pfscntnumpf = pfscntnumpf
        self.pfscntsubtotal = pfscntsubtotal
        self.pfscntdto = pfscntdto
        self.pfscntiva = pfscntiva
        self.pfscnttotal = pfscnttotal
        self.pfscntestado = pfscntestado
        self.pfscntcreatedat = pfscntcreatedat 
        self.pfsusersid = pfsusersid 

class ProformaSchema(ma.Schema):
    class Meta:
        fields = ('pfscntid','pfscntnumpf', 'pfscntsubtotal', 'pfscntdto', 'pfscntiva', 'pfscnttotal', 'pfscntestado', 'pfscntcreatedat', 'pfsusersid')

proformaSchema = ProformaSchema()
proformaSchema = ProformaSchema(many=True)


#----------------------------
#----------DETALLE CANASTA----------
#--------------------------

class Detallecanasta(db.Model):
    __tablename__='pfsdetallecanasta'

    pfsdcid = db.Column(db.Integer, primary_key=True)
    pfsdcnumpf = db.Column(db.Integer, nullable=False)
    pfsdcantidad = db.Column(db.Integer, nullable=False)
    pfsdcprecio = db.Column(db.Integer, nullable=False)
    pfsdcptotal = db.Column(db.Integer, nullable=False)
    pfsdcestado = db.Column(db.String(1), nullable=True)
    pfsdccreatedat = db.Column(db.String(11), nullable=True) 

    pfsdcproductoid = db.Column(db.Integer, db.ForeignKey('pfsproductos.pfsprodid',ondelete='CASCADE'), nullable=False)
    pfsdcproducto = db.relationship('Producto',backref=db.backref('pfsdetallecanasta',lazy=True))

    pfsdcanastaid = db.Column(db.Integer, db.ForeignKey('pfscanasta.pfscntid',ondelete='CASCADE'), nullable=False)
    pfsdcanasta = db.relationship('Canasta',backref=db.backref('pfsdetallecanasta',lazy=True))



    def __init__(self, pfsdcnumpf, pfsdcantidad, pfsdcprecio, pfsdcptotal, pfsdcestado, pfsdccreatedat, pfsdcproductoid, pfsdcanastaid ):
        self.pfsdcnumpf = pfsdcnumpf
        self.pfsdcantidad = pfsdcantidad
        self.pfsdcprecio = pfsdcprecio
        self.pfsdcptotal = pfsdcptotal
        self.pfsdcestado = pfsdcestado
        self.pfsdccreatedat = pfsdccreatedat
        self.pfsdcproductoid = pfsdcproductoid
        self.pfsdcanastaid = pfsdcanastaid

class DetalleproformaSchema(ma.Schema):
    class Meta:
        fields = ('pfsdcid', 'pfsdcnumpf', 'pfsdcantidad', 'pfsdcprecio', 'pfsdcptotal', 'pfsdcestado', 'pfsdccreatedat', 'pfsdcproductoid', 'pfsdcanastaid')

detalleproformaSchema = DetalleproformaSchema()
detalleproformaSchema = DetalleproformaSchema(many=True)

#----------------------------
#----------CATEGORIA----------
#--------------------------
class Categoria(db.Model):
    __tablename__='pfscategorias'

    pfscateid = db.Column(db.Integer, primary_key=True)
    pfscatenombre = db.Column(db.String(80), nullable=False)
    pfscateimage = db.Column(db.String(300), nullable=False)
    pfscatedetalle = db.Column(db.String(300), nullable=False)
    pfscateestado = db.Column(db.String(1), nullable=True)
    pfscatecreatedat = db.Column(db.String(11), nullable=True) 


    def __init__(self, pfscatenombre, pfscateimage, pfscatedetalle , pfscateestado, pfscatecreatedat):
        self.pfscatenombre = pfscatenombre
        self.pfscateimage = pfscateimage
        self.pfscatedetalle = pfscatedetalle
        self.pfscateestado = pfscateestado
        self.pfscatecreatedat = pfscatecreatedat

class CategoriaSchema(ma.Schema):
    class Meta:
        fields = ('pfscateid','pfscatenombre', 'pfscateimage', 'pfscatedetalle', 'pfscateestado', 'pfscatecreatedat')

categoriaSchema = CategoriaSchema()
categoriaSchema = CategoriaSchema(many=True)

#----------------------------
#----------PRODUCTO----------
#--------------------------
class Producto(db.Model):
    __tablename__='pfsproductos'

    pfsprodid = db.Column(db.Integer, primary_key=True)
    pfsprodmarca = db.Column(db.String(30), nullable=False)
    pfsprodnombre = db.Column(db.String(80), nullable=False)
    pfsprodimage = db.Column(db.String(300), nullable=False)
    pfsproddetalle = db.Column(db.String(300), nullable=False)
    pfsprodprecio = db.Column(db.String(6), nullable=False) #double
    pfsprodstock = db.Column(db.String(10), nullable=False) #int
    pfsprodestado = db.Column(db.String(1), nullable=True)
    pfsprodcreatedat = db.Column(db.String(11), nullable=True) 

    pfscategoriaid = db.Column(db.Integer, db.ForeignKey('pfscategorias.pfscateid',ondelete='CASCADE'), nullable=False)
    pfscategoria = db.relationship('Categoria',backref=db.backref('pfsproductos',lazy=True))


    def __init__(self, pfsprodmarca, pfsprodnombre, pfsprodimage, pfsproddetalle, pfsprodprecio, pfsprodstock, pfsprodestado, pfsprodcreatedat, pfscategoriaid):
        self.pfsprodmarca = pfsprodmarca
        self.pfsprodnombre = pfsprodnombre
        self.pfsprodimage = pfsprodimage
        self.pfsproddetalle = pfsproddetalle
        self.pfsprodprecio = pfsprodprecio
        self.pfsprodstock = pfsprodstock
        self.pfsprodestado = pfsprodestado
        self.pfsprodcreatedat = pfsprodcreatedat
        self.pfscategoriaid = pfscategoriaid
class ProductoSchema(ma.Schema):
    class Meta:
        fields = ('pfsprodid', 'pfsprodmarca', 'pfsprodnombre', 'pfsprodimage', 'pfsproddetalle', 'pfsprodprecio', 'pfsprodstock', 'pfsprodestado', 'pfsprodcreatedat', 'pfscategoriaid')

productoSchema = ProductoSchema()
productoSchema = ProductoSchema(many=True)


#----------------------------
#----------Promociones----------
#--------------------------
class Promociones(db.Model):
    __tablename__='pfspromociones'

    pfspromid = db.Column(db.Integer, primary_key=True)
    pfspromdto = db.Column(db.String(80), nullable=False)
    pfspromfechainicio = db.Column(db.String(10), nullable=False)
    pfspromfechafin = db.Column(db.String(10), nullable=False)
    pfspromdescripcion = db.Column(db.String(300), nullable=False) #double
    pfspromestado = db.Column(db.String(1), nullable=True)
    pfspromcreatedat = db.Column(db.String(11), nullable=True) 

    pfsproductoid = db.Column(db.Integer, db.ForeignKey('pfsproductos.pfsprodid',ondelete='CASCADE'), nullable=False)
    pfsproducto = db.relationship('Producto',backref=db.backref('pfspromociones',lazy=True))


    def __init__(self, pfspromdto, pfspromfechainicio, pfspromfechafin, pfspromdescripcion, pfspromestado, pfspromcreatedat, pfsproductoid):
        self.pfspromdto = pfspromdto
        self.pfspromfechainicio = pfspromfechainicio
        self.pfspromfechafin = pfspromfechafin
        self.pfspromdescripcion = pfspromdescripcion
        self.pfspromestado = pfspromestado
        self.pfspromcreatedat = pfspromcreatedat 
        self.pfsproductoid = pfsproductoid 

class PromocionSchema(ma.Schema):
    class Meta:
        fields = ('pfspromid', 'pfspromdto', 'pfspromfechainicio', 'pfspromfechafin', 'pfspromdescripcion', 'pfspromestado', 'pfspromcreatedat', 'pfsproductoid')

promocionSchema = PromocionSchema()
promocionSchema = PromocionSchema(many=True)


#---------------------------------
#----------Forma de Pago----------
#---------------------------------

class Formapago(db.Model):
    __tablename__='pfsformapago'

    pfsfpid = db.Column(db.Integer, primary_key=True)
    pfsfpestado = db.Column(db.String(1), nullable=True)
    pfsfpcreatedat = db.Column(db.String(11), nullable=True) 

    pfscanastaid = db.Column(db.Integer, db.ForeignKey('pfscanasta.pfscntid',ondelete='CASCADE'), nullable=False)
    pfscanasta = db.relationship('Canasta',backref=db.backref('pfsformapago',lazy=True))

    pfstipopagoid = db.Column(db.Integer, db.ForeignKey('pfstipopago.pfstpid',ondelete='CASCADE'), nullable=False)
    pfstipopago = db.relationship('Tipopago',backref=db.backref('pfsformapago',lazy=True))

    def __init__(self, pfsfpestado, pfsfpcreatedat, pfscanastaid, pfstipopagoid):
        self.pfsfpestado = pfsfpestado
        self.pfsfpcreatedat = pfsfpcreatedat
        self.pfscanastaid = pfscanastaid
        self.pfstipopagoid = pfstipopagoid

class FormapagoSchema(ma.Schema):
    class Meta:
        fields = ('pfsfpid', 'pfsfpestado', 'pfsfpcreatedat', 'pfscanastaid', 'pfstipopagoid')

formapagoSchema = FormapagoSchema()
formapagoSchema = FormapagoSchema(many=True)

#---------------------------------
#----------Tipo de Pago----------
#---------------------------------

class Tipopago(db.Model):
    __tablename__='pfstipopago'

    pfstpid = db.Column(db.Integer, primary_key=True)
    pfstpnombre = db.Column(db.String(30), nullable=True)
    pfstpestado = db.Column(db.String(1), nullable=True)
    pfstpcreatedat = db.Column(db.String(11), nullable=True) 

    def __init__(self, pfstpnombre, pfstpestado, pfstpcreatedat):
        self.pfstpnombre = pfstpnombre
        self.pfstpestado = pfstpestado
        self.pfstpcreatedat = pfstpcreatedat
 

class TipopagoSchema(ma.Schema):
    class Meta:
        fields = ('pfstpid', 'pfstpnombre', 'pfstpestado', 'pfstpcreatedat')

tipopagoSchema = TipopagoSchema()
tipopagoSchema = TipopagoSchema(many=True)


#---------------------------------
#----------Paypal----------
#---------------------------------

class Paypal(db.Model):
    __tablename__='pfspaypal'

    pfspypid = db.Column(db.Integer, primary_key=True)
    pfspypnumcanasta = db.Column(db.Integer, nullable=True)
    pfspyprecanasta = db.Column(db.Integer, nullable=True) #precio canasta
    pfspypestado = db.Column(db.String(1), nullable=True)
    pfspypcreatedat = db.Column(db.String(11), nullable=True) 


    pfsformapagoid = db.Column(db.Integer, db.ForeignKey('pfsformapago.pfsfpid',ondelete='CASCADE'), nullable=False)
    pfsformapago = db.relationship('Formapago',backref=db.backref('pfspaypal',lazy=True))

    def __init__(self, pfspypnumcanasta, pfspyprecanasta, pfspypestado, pfspypcreatedat, pfsformapagoid):
        self.pfspypnumcanasta = pfspypnumcanasta
        self.pfspyprecanasta = pfspyprecanasta
        self.pfspypestado = pfspypestado
        self.pfspypcreatedat = pfspypcreatedat
        self.pfsformapagoid = pfsformapagoid
 

class PaypalSchema(ma.Schema):
    class Meta:
        fields = ('pfspypid', 'pfspypnumproforma', 'pfspypreproforma', 'pfspypestado', 'pfspypcreatedat', 'pfsformapagoid')

paypalSchema = PaypalSchema()
paypalSchema = PaypalSchema(many=True)

#------------------------------------------
#----------Transferencia Bancaria----------
#------------------------------------------

class Transferenciabancaria(db.Model):
    __tablename__='pfstransferenciabancaria'

    pfstbpid = db.Column(db.Integer, primary_key=True)
    pfstbnumcanasta = db.Column(db.Integer, nullable=True)
    pfstbprecanasta = db.Column(db.Integer, nullable=True)
    pfstbboucher = db.Column(db.String(300), nullable=True)
    pfstbestado = db.Column(db.String(1), nullable=True)
    pfstbcreatedat = db.Column(db.String(11), nullable=True) 


    pfsformapagoid = db.Column(db.Integer, db.ForeignKey('pfsformapago.pfsfpid',ondelete='CASCADE'), nullable=False)
    pfsformapago = db.relationship('Formapago',backref=db.backref('pfstransferenciabancaria',lazy=True))

    def __init__(self, pfstbnumcanasta, pfstbprecanasta, pfstbboucher,  pfstbestado, pfstbcreatedat, pfsformapagoid):
        self.pfstbnumcanasta = pfstbnumcanasta
        self.pfstbprecanasta = pfstbprecanasta
        self.pfstbboucher = pfstbboucher
        self.pfstbestado = pfstbestado
        self.pfstbcreatedat = pfstbcreatedat
        self.pfsformapagoid = pfsformapagoid
 

class TransferenciabancariaSchema(ma.Schema):
    class Meta:
        fields = ('pfstbpid', 'pfstbnumcanasta', 'pfstbprecanasta', 'pfstbboucher',  'pfstbestado', 'pfstbcreatedat', 'pfsformapagoid')

transferenciabancariaSchema = TransferenciabancariaSchema()
transferenciabancariaSchema = TransferenciabancariaSchema(many=True)

#------------------------------------------
#-----------------Efectivo-----------------
#------------------------------------------

class Efectivo(db.Model):
    __tablename__='pfsefectivo'

    pfsefid = db.Column(db.Integer, primary_key=True)
    pfseftnumcanasta = db.Column(db.Integer, nullable=True)
    pfseftprecanasta = db.Column(db.Integer, nullable=True)
    pfseftestado = db.Column(db.String(1), nullable=True)
    pfseftcreatedat = db.Column(db.String(11), nullable=True) 


    pfsformapagoid = db.Column(db.Integer, db.ForeignKey('pfsformapago.pfsfpid',ondelete='CASCADE'), nullable=False)
    pfsformapago = db.relationship('Formapago',backref=db.backref('pfsefectivo',lazy=True))

    def __init__(self, pfseftnumcanasta, pfseftprecanasta, pfseftestado,  pfseftcreatedat, pfsformapagoid):
        self.pfseftnumcanasta = pfseftnumcanasta
        self.pfseftprecanasta = pfseftprecanasta
        self.pfseftestado = pfseftestado
        self.pfseftcreatedat = pfseftcreatedat
        self.pfsformapagoid = pfsformapagoid
 

class EfectivoSchema(ma.Schema):
    class Meta:
        fields = ('pfsefid', 'pfseftnumcanasta', 'pfseftprecanasta', 'pfseftestado',  'pfseftcreatedat', 'pfsformapagoid')

efectivoSchema = EfectivoSchema()
efectivoSchema = EfectivoSchema(many=True)
