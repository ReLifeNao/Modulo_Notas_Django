from django.shortcuts import render
from Sistema.models import Notas,Estudiante,Administrador,Bimestre,Docente,TipoUsuario,Materia
from Sistema.forms import EstudianteNotasForm,NotasForm,BimestreForm
from django.shortcuts import render,redirect
from Sistema.forms import CreateUserForm
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages
import logging
from django.http import HttpResponseRedirect,Http404
from django.urls import reverse
from datetime import date


logger = logging.getLogger("mylogger //// ")


#MODULO DOCENTE:
def adminhtml(request):

    context = {}

    return render(request,"Sistema/admin.html",context)



def NotasView(request):
    
    
    NotasAlumnos = Notas.objects.all()
    context = {
        'Notas':NotasAlumnos,
    }
    
    return render(request,"Sistema/NotasEstudiantes.html",context)



def AdministradorView(request):
    
    AdministradorV = Administrador.objects.all()
    context = {
        'Administrador':AdministradorV,
    }
    
    
    return render(request,"Sistema/administrador.html",context)

def EstudiantesNotas(request):
    
    
    EstudianteNotes = Estudiante.objects.all()
    context = {
        'Estudiante':EstudianteNotes,
    }
    
    return render(request,"Sistema/NotasEstudiantes.html",context)



def Delete(request, id):
    EstudiantesD= Estudiante.objects.get(id=id)
    
    EstudiantesD.delete()
    return redirect("/EstudianteNotas")

    
def Edit(request, id,idM,idS):
    
    EstudiantesE = Bimestre.objects.get(Id_Bimestre=id)
    logger.error(idM)
    
    logger.error(idS)
    
    if request.method == "POST":
        
    
        
        Form = BimestreForm(request.POST, instance=EstudiantesE)
        
        
        if Form.is_valid():
            
            
            EstudiantesE.save()
            url='/SalonMateria'+'/'+str(idM)
            return redirect(url)
        else:
            EstudiantesE.save()
            url='/SalonMateria'+'/'+str(idM)
            return redirect(url)
        
    # Si llegamos al final renderizamos el formulario
    #return render(request, 'Notas.html', {'Notas':EstudiantesE})
    #ids=id
    #connect = cx_Oracle.connect('c##jhonny/ilonandraon@localhost') 
    #cursor = connect.cursor()
    #cursor.execute(""" DELETE FROM Base_Productos WHERE Id=:arg_1 """,{"arg_1":ids})
    
def DocenteCursos(request):
    #914
    #if request.user.is_authenticated():
    username = request.user.get_username()
    #logger.error('Something went wrong!')
    
    #logger.error(username)
    instancia=Docente.objects.get(User=username)
    
    #Materias = Materia.objects.get(Id_Docente=username)
    DocenteCursos = Materia.objects.filter(Id_Docente=instancia.Id_Docente  )
    
    return render(request,"Sistema/Docente.html",{'Docente':DocenteCursos})

def Login(request):
    
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(request,username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('/DocenteCursos')
        else:
            messages.info(request, 'Username Or paSsword is incorrect ')
    context = {}
    return render(request,"Sistema/login.html",context)

def Register(request):
    Form = CreateUserForm()
    context = { 'form':Form}
    if request.method == 'POST':
        Form = CreateUserForm(request.POST)
        if Form.is_valid():
            Form.save()

            
            Nombres = Form.cleaned_data['first_name']
            Apellidos = Form.cleaned_data['last_name']
            Username = Form.cleaned_data['username']
            Correo = Form.cleaned_data['email']
            instancia=TipoUsuario.objects.get(Id_TipoUsuario=2)
            
            #Usuario=
            #Password=form.cleaned_data['Nombre']
            sql=Docente(Nombres=Nombres,Apellidos=Apellidos,Correo=Correo,User=Username,Tipo_Usuario=instancia)
            sql.save()
            return redirect('/Login')
    context = { 'form':Form}



    
    return render(request,"Sistema/register.html", context )

def logoutUser(request):
    logout(request)
    return redirect('/Login')

def SalonMateria(request,id):
    instanciaSalon = Materia.objects.get(Id_Materia=id)
    classAlumnos =instanciaSalon.Id_Salon.Id_Salon
    NotasAlumnos = Notas.objects.filter(Id_SalonC=classAlumnos,Id_Materia=id)
    
    return render(request,"Sistema/NotasEstudiantes.html",{'Notas':NotasAlumnos})



#MODULO ESTUDIANTE:


def EstudianteView(request):
    
    username = request.user.get_username()
    
    Estudent = Estudiante.objects.get(User=username)
    
    Salon= Estudent.Salon
    
    
    Materias = Materia.objects.filter(Id_Salon=Salon)
    
    return render(request,"Sistema/estudiante.html",{'Estudiante':Materias})

def NotaCurso(request,curso):

    username = request.user.get_username()
    Estudent = Estudiante.objects.get(User=username)
    
    NotaCurso = Notas.objects.filter(Id_Estudiante=Estudent.Id_Estudiante,Id_Materia=curso)
    
    return render(request,"Sistema/NotaCurso.html",{'Estudiante':NotaCurso})



def RegisterUsuario(request):
    Form = CreateUserForm()
    context = { 'form':Form}
    if request.method == 'POST':
        Form = CreateUserForm(request.POST)
        if Form.is_valid():
            Form.save()

            #Idk = Form.cleaned_data['id']
            #logger.error(Idk)
            Nombres = Form.cleaned_data['first_name']
            Apellidos = Form.cleaned_data['last_name']
            Username = Form.cleaned_data['username']
            Correo = Form.cleaned_data['email']
            instancia=TipoUsuario.objects.get(Id_TipoUsuario=1)
            
            #Usuario=
            #Password=form.cleaned_data['Nombre']
            sql=Estudiante(Nombres=Nombres,Apellidos=Apellidos,Correo=Correo,User=Username,Tipo_Usuario=instancia)
            sql.save()
            return redirect('/LoginUsuario')
    context = { 'form':Form}
    return render(request,"Sistema/RegisterUsuario.html", context )
    
def logoutUsuario(request):
    logout(request)
    return redirect('/LoginUsuario')
    

def LoginUsuario(request):
    
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(request,username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('/Estudiante')
        else:
            messages.info(request, 'Username Or paSsword is incorrect ')
    context = {}
    return render(request,"Sistema/LoginUsuario.html",context)

def AsignarSalon(request, Alumno):
    
    AlumnoX = Estudiante.objects.get(Id_Estudiante=Alumno)
    logger.error(AlumnoX)
    

    if request.method == "POST" :
    
        Form = EstudianteNotasForm(request.POST,instance=AlumnoX)
        if Form.is_valid():
    
            Salon=Form.cleaned_data['Salon']
           
            t = Estudiante.objects.get(Id_Estudiante=Alumno)
            t.Salon = Salon
            t.save() #

        
        else:
            Salon=Form.cleaned_data['Salon']
         #logger.error(Salon)    
            t = Estudiante.objects.get(Id_Estudiante=Alumno)
            t.Salon = Salon
            t.save() #
            
    count=Bimestre.objects.all().count()
    logger.error("CONTADOR:")
    logger.error(count)
    i=2
    #logger.error(i)

    MateriasSalon = Materia.objects.filter(Id_Salon=Salon)
    #logger.error(MateriasSalon)
    for subject in MateriasSalon:
        logger.error(subject)
        sql=Bimestre(Id_Bimestre=count+i,Bimestre1=0,Bimestre2=0,Bimestre3=0,Bimestre4=0)
        #logger.error(sql)
        sql.save()
        Bimester=Bimestre.objects.get(Id_Bimestre=count+i)
        sqlNotas=Notas(Id_Notas=count+i,Id_Estudiante=AlumnoX,Id_Materia=subject,Id_Bimestre=Bimester,Fecha=date.today(),Id_SalonC=Salon)
        #logger.error(sqlNotas)
        sqlNotas.save()
        i=i+1
    context = {}
    return render(request,"Sistema/MostrarAlumnos.html",context)

def MostrarAlumnosSinSalon(request):
    Mostrar=Estudiante.objects.filter(Salon__isnull=True)
    #Mostrar=Estudiante.objects.all()
    return render(request,"Sistema/MostrarAlumnos.html",{'Alumnos':Mostrar})


def MostrarTablaDocentes(request):
    Datos=Docente.objects.all()
    context = { 
        'Docente': Datos
    }
    return render(request,"Sistema/TablaDocente.html",context)

def MostrarTablaEstudiantes(request):
    Datos=Estudiante.objects.all()
    context = { 
        'Estudiante': Datos
    }
    return render(request,"Sistema/TablaEstudiante.html",context)

    