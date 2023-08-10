from flask_login import UserMixin
from app.auth.auth import Auth
class UserModel(UserMixin):
    def __init__(self, userData):
        self.id = userData.pfsusersusername
        self.iduser = userData.pfsusersid
        self.password = userData.pfsuserspassword
        self.email = userData.pfsusersemail
        self.avatar = userData.pfsusersavatar
        self.isadmin = userData.pfsusersisadmin
        self.estado = userData.pfsusersestado
        
    @staticmethod
    def get(username):
        userData = Auth.getUserByUsername(username)
        return UserModel(userData)