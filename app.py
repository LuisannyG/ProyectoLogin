
#Nuestro servidor
from flask import Flask, flash, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#Configuracion
app= Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'
app.config['SQLALCHEMY_DATABASE_URI']=  'postgresql://postgres:1234@localhost:5432/proyecto_login'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#Conexión para consultas
engine = create_engine('postgresql://postgres:1234@localhost:5432/proyecto_login')
Session = sessionmaker(engine)
session = Session()

#modelos
class Usuario(db.Model):
    __tablename__= 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(), nullable=False)
    apellido = db.Column(db.String(), nullable=False)
    correo = db.Column(db.String(), nullable=False)
    contrasena = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'Todo: {self.id}, nombre={self.nombre}, apellido={self.apelldio}, correo={self.correo}, contrasena={self.contrasena}'


db.create_all()


#Controlador
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/usuario_login', methods= ['POST'])
def login_todo():
    usu= request.form.get('usuario', )
    contra= request.form.get('contrasena', )
    
    con = session.query(Usuario).filter(
        Usuario.correo == usu
    ).filter(
        Usuario.contrasena == contra
    )
    
    if con.count() > 0:
        return render_template('exito.html')
    else:
        return render_template('error.html')
    
@app.route('/usuario_crear_registro', methods= ['POST'])
def crear_usuario_todo():
    corr= request.form.get('correo', )
    nomb= request.form.get('nombre', )
    apell= request.form.get('apellido', )
    contra= request.form.get('contrasena', )
    
    session.add(Usuario(correo=corr,nombre=nomb,apellido=apell,contrasena=contra))
    session.commit()
    
    flash('Usuario Creado')
    
    return render_template('crear.html')
    
@app.route('/usuario_recuperar')
def recuperar_todo():
    return render_template('recuperar.html')

@app.route('/usuario_recuperar_contra', methods= ['POST'])
def recuperar_contra_todo():
    usu= request.form.get('usuario', )
    
    con = session.query(Usuario.contrasena).filter(
        Usuario.correo == usu
    )
    
    if con.count() > 0:
        flash('Su contraseña es: ' + con[0].contrasena)
    else: flash('El usuario no existe')
    
    return render_template('recuperar.html')
        

@app.route('/usuario_create')
def create_todo():
    return render_template('crear.html')
    
#Running
if __name__ == '__main__':
    app.run(debug=True)