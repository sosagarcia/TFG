# Rutas de LOG

hPath = "/var/log/iot/hum/"
tPath = "/var/log/iot/tem/"
irPath = "/var/log/iot/ir/"
disPath = "/var/log/iot/dis/"
aPath = "/var/log/iot/a/"
cpuTPath = "/var/log/iot/cpuT/"
cpuPath = "/var/log/iot/cpu/"

dName = "_Distancia.log"
hName = "_Humedad.log"
tName = "_Temperatura.log"
irName = "_Movimientos.log"
aName = "_Alarmas.log"
cpuTName = "_TemperaturaCPU.log"
cpuName = "_UsoCPU.log"


# Texto de Recuperación de contraseña
cambio_pass = """El siguiente correo se ha generado automáticamente para ayudarle a cambiar su contraseña del aplicativo de Sistema de gestión de control de aguas .
Si usted no ha solicitado la recuperación de la contraseña, ignore este correo.

Para realizar el cambio de contraseña, introduzca el siguiente código de recuperación:

Su código de recuperación es : """

# Texto de verificación de cuenta
cambio_pass = """El siguiente correo se ha generado automáticamente para verificar su cuenta del  aplicativo de Sistema de gestión de control de aguas .


Para poder verificar su cuenta, introduzca el siguiente código.

Su código de verificación es : """

confText = """###INICIO###
name = {}
mail = {}
altu = {}
disB = {}
disA = {}
temA = {}
humA = {}
htTm = {}
disT = {}
cpuS = {}
###FIN###"""



# Diccionario de mensajes

calendario = [
    {
        'title': "All Day Event",
        'start': "2019-06-01"
    },
    {
        'groupId': 999,
        'title': "Repeating Event",
        'start': "2019-06-09T16:00:00"
    }
]


inicio = [
    {
        'author': 'Bienvenido',
        'titulo': 'INICIO DE SESIÓN',
        'mensaje': 'Por favor, inicie sesión para entrar al portal con su usuario y contraseña',
        'tipo': 'primary'
    }
]


fgt = [
    {
        'author': 'Obtener código de recuperación',
        'titulo': 'CAMBIO DE CONTRASEÑA',
        'mensaje': 'Por favor, introduzca su email para cambiar su contraseña',
        'tipo': 'warning'
    }
]


code = [
    {
        'author': 'Código de recuperación',
        'titulo': 'CAMBIO DE CONTRASEÑA',
        'mensaje': 'Por favor, introduzca el código que le habrá llegado a su correo para cambiar su contraseña. Compruebe su carpeta de SPAM o correo no deseado',
        'tipo': 'warning'
    }
]

codeI = [
    {
        'author': 'Código Erroneo',
        'titulo': 'CAMBIO DE CONTRASEÑA',
        'mensaje': 'Por favor, introduzca el código que le habrá llegado a su correo para cambiar su contraseña. Compruebe su carpeta de SPAM o correo no deseado',
        'tipo': 'danger'
    }
]

cambio = [
    {
        'author': 'Introduzca la nueva contraseña',
        'titulo': 'CAMBIO DE CONTRASEÑA',
        'mensaje': 'Por favor, introduzca la nueva contraseña que desea tener',
        'tipo': 'warning'
    }
]

cambioS = [
    {
        'author': 'Contraseña cambiada correctamente',
        'titulo': 'INICIO DE SESIÓN',
        'mensaje': 'Por favor, inicie sesión para entrar al portal con su usuario y contraseña',
        'tipo': 'success'
    }
]


reg = [
    {
        'author': 'Nuevo Registro',
        'titulo': 'INICIO DE SESIÓN',
        'mensaje': 'Por favor, rellene los siguientes campos',
        'tipo': 'primary'
    }
]

adios = [
    {
        'author': 'Bienvenido',
        'titulo': 'Cierre de sesión correcto',
        'mensaje': 'Por favor, inicie sesión para entrar al portal con su usuario y contraseña',
        'tipo': 'dark'
    }
]

contra = [
    {
        'author': 'Error al iniciar sesión',
        'titulo': 'ERROR',
        'mensaje': 'La contraseña que ha introducido es incorrecta.',
        'tipo': 'danger'
    }
]
usu = [
    {
        'author': 'Error al iniciar sesión',
        'titulo': 'ERROR',
        'mensaje': 'El email introducido es incorrecto.',
        'tipo': 'danger'
    }
]

usuF = [
    {
        'author': 'Error al mandar email',
        'titulo': 'ERROR',
        'mensaje': 'El email introducido es incorrecto.',
        'tipo': 'danger'
    }
]

coincide = [
    {
        'author': 'Las contraseñas no coinciden',
        'titulo': 'ERROR AL CREAR CUENTA',
        'mensaje': '',
        'tipo': 'danger'
    }
]

coincideC = [
    {
        'author': 'Las contraseñas no coinciden',
        'titulo': 'ERROR AL CAMBIAR DE CONTRASEÑA',
        'mensaje': '',
        'tipo': 'danger'
    }
]

usua = [
    {
        'author': 'Usuario ya existente',
        'titulo': 'Error al crear la cuenta',
        'mensaje': 'Ya existe un usuario registrado con ese email',
        'tipo': 'danger'
    }
]

vacio = [
    {
        'author': 'Todos los campos son obligatorios',
        'titulo': 'Error al crear la cuenta',
        'mensaje': 'Se deben de rellenar todos los campos para poder registrar una cuenta',
        'tipo': 'danger'
    }
]

vacioE = [
    {
        'author': 'Todos los campos son obligatorios',
        'titulo': 'EVENTOS',
        'mensaje': 'Se deben de rellenar todos los campos para poder registrar un evento',
        'tipo': 'danger'
    }
]

vacioC = [
    {
        'author': 'Todos los campos son obligatorios',
        'titulo': 'CAMBIO DE CONTRASEÑ',
        'mensaje': 'Los campos de contraseñas no pueden estar vacíos',
        'tipo': 'danger'
    }
]

menor = [
    {
        'author': 'Fechas incorrectas',
        'titulo': 'EVENTOS',
        'mensaje': 'La fecha de fin debe de ser posterior a la fecha de inicio',
        'tipo': 'danger'
    }
]

cal = [
    {
        'author': 'Nuevo registro',
        'titulo': 'EVENTOS',
        'mensaje': 'Rellene todos los campos para añadir un evento',
        'tipo': 'primary'
    }
]
event = [
    {
        'author': 'Evento registrado correctamente',
        'titulo': 'EVENTOS',
        'mensaje': 'Rellene todos los campos para añadir un nuevo evento',
        'tipo': 'success'
    }
]

evente = [
    {
        'author': 'Error al registrar evento',
        'titulo': 'EVENTOS',
        'mensaje': 'Rellene todos los campos para añadir un evento',
        'tipo': 'danger'
    }
]
fechae = [
    {
        'author': 'Error al registrar evento',
        'titulo': 'EVENTOS',
        'mensaje': 'Ya existe un evento que coincide con ese rango de fechas',
        'tipo': 'danger'
    }
]

dosmin = [
    {
        'author': 'Error al registrar evento',
        'titulo': 'EVENTOS',
        'mensaje': 'La diferencia entre el inicio y el final del evento tiene que ser mayor a 2 minutos',
        'tipo': 'danger'
    }
]
unmes = [
    {
        'author': 'Error al registrar evento',
        'titulo': 'EVENTOS',
        'mensaje': 'La diferencia entre el inicio y el final del evento tiene que ser menor a un mes (31 días)',
        'tipo': 'danger'
    }
]

delEv = [
    {
        'author': 'Evento borrado correctamente',
        'titulo': 'EVENTOS',
        'mensaje': 'Se ha borrado el evento correctamente',
        'tipo': 'success'
    }
]
esta = [
    {
        'author': 'Selección de estadísticas',
        'titulo': 'ESTADÍSTICAS',
        'mensaje': 'Seleccione el tipo de datos que desea visualizar',
        'tipo': 'primary'
    }
]
