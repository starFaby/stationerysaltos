from flask import Blueprint
from app.migrate.migrate import initDB

psfpsdb= Blueprint('psfpsdb', __name__)

psfpsdb.route('/psfpsdb', methods=['GET'])(initDB)
