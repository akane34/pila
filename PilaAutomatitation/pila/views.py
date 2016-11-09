# coding=utf-8
import json
import traceback
from datetime import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.core import serializers
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from . import models


# Create your views here.
@csrf_exempt
def pila_login(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)

            nombre_usuario = data['usuario']
            contrasenia = data['password']

            usuario = authenticate(username=nombre_usuario, password=contrasenia)

            if usuario is not None:
                login(request, usuario)

                return HttpResponse(serializers.serialize("json", [usuario]))
            else:
                return JsonResponse({"mensaje": "Ocurrió un error al intentar hacer login"})
    except:
        traceback.print_exc()
        return JsonResponse({"mensaje": "Ocurrió un error al intentar hacer login"})


@csrf_exempt
def crear_consultar_aportante(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)

            nombre_usuario = data['usuario']
            contrasenia = data['password']
            nombre = data['nombre']
            tipo_pagador_pensiones = data['tipoPagador']

            usuario = User.objects.create_user(username=nombre_usuario, password=contrasenia)
            grupo = Group.objects.get(name__iexact="APORTANTE")
            grupo.user_set.add(usuario)

            operador_servicio = models.OperadorServicio.objects.get(pk=1)

            aportante = models.Aportante()
            aportante.usuario_id = usuario
            aportante.nombre = nombre
            aportante.tipo_pagador_pensiones = tipo_pagador_pensiones
            aportante.operador_servicio = operador_servicio
            aportante.save()

            return HttpResponse(serializers.serialize("json", [aportante]))
        elif request.method == 'GET':
            aportantes = models.Aportante.objects.all().values('pk', 'usuario_id', 'nombre', 'tipo_pagador_pensiones',
                                                               'operador_servicio')

            for aportante in aportantes:
                a = models.Aportante.objects.get(pk=aportante['pk'])
                aportante['tipo_pagador_pensiones_nombre'] = a.get_tipo_pagador_pensiones_display()

            aportantes = json.loads(json.dumps(list(aportantes)))

            return JsonResponse(aportantes, safe=False)
    except:
        traceback.print_exc()
        return JsonResponse({"mensaje": "Ocurrió un error creando el aportante"})


@csrf_exempt
def actualizar_eliminar_aportante(request, id):
    try:
        if request.method == 'PUT':
            data = json.loads(request.body)

            aportante = models.Aportante.objects.get(pk=id)
            usuario = User.objects.get(pk=aportante.usuario_id.id)

            if data['password']:
                usuario.set_password(data['password'])
                usuario.save()

            if data['nombre']:
                aportante.nombre = data['nombre']

            if data['tipoPagador']:
                aportante.tipo_pagador_pensiones = data['tipoPagador']

            aportante.save()

            return HttpResponse(serializers.serialize("json", [aportante]))
        elif request.method == 'DELETE':
            aportante = models.Aportante.objects.get(pk=id)
            usuario = User.objects.get(pk=aportante.usuario_id.id)
            aportante.delete()
            usuario.delete()

            return JsonResponse({"mensaje": "ok"})
        elif request.method == 'GET':
            aportante = models.Aportante.objects.get(pk=id)
            respuesta = {
                'pk': aportante.pk,
                'usuario_id': aportante.usuario_id.id,
                'usuario': aportante.usuario_id.username,
                'nombre': aportante.nombre,
                'tipo_pagador_pensiones': aportante.tipo_pagador_pensiones,
                'operador_servicio': aportante.operador_servicio.id,
                'tipo_pagador_pensiones_nombre': aportante.get_tipo_pagador_pensiones_display()
            }

            return JsonResponse(respuesta, safe=False)
    except:
        traceback.print_exc()
        return JsonResponse({"mensaje": "Ocurrió un error actualizando/eliminando el aportante " + str(id)})


@csrf_exempt
def crear_pensionado(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)

            aportante = models.Aportante.objects.get(pk=data['aportante'])

            pensionado = models.Pensionado()
            pensionado.nombre = data['nombre']
            pensionado.edad = data['edad']
            pensionado.salario = data['salario']
            pensionado.es_alto_riesgo = data['esAltoRiesgo']
            pensionado.es_congresista = data['esCongresista']
            pensionado.es_trabajador_CTI = data['esTrabajadorCTI']
            pensionado.es_aviador = data['esAviador']
            pensionado.residencia_exterior = data['residenciaExterior']
            pensionado.tiene_grupo_familiar_colombia = data['tieneGrupoFamiliarColombia']
            pensionado.codigo_CIU = data['codigoCIU']
            pensionado.tipo_pensionado = data['tipoPensionado']
            pensionado.aportante = aportante
            pensionado.save()

            return HttpResponse(serializers.serialize("json", [pensionado]))
    except:
        traceback.print_exc()
        return JsonResponse({"mensaje": "Ocurrió un error creando el pensionado"})


@csrf_exempt
def consultar_pensionados(request, id):
    try:
        if request.method == 'GET':
            respuesta = []
            pensionados = models.Pensionado.objects.filter(aportante_id=id)

            for pensionado in pensionados:
                novedades = models.Novedad.objects.filter(pensionado_id=pensionado.pk).values('pk', 'fecha_inicio',
                                                                                              'fecha_fin',
                                                                                              'duracion',
                                                                                              'tipo_novedad')

                for novedad in novedades:
                    n = models.Novedad.objects.get(pk=novedad['pk'])
                    novedad['fecha_inicio'] = str(n.fecha_inicio)
                    novedad['fecha_fin'] = str(n.fecha_fin)
                    novedad['tipo_novedad_nombre'] = n.get_tipo_novedad_display()

                novedades = json.loads(json.dumps(list(novedades)))

                respuesta.append({
                    'pk': pensionado.pk,
                    'nombre': pensionado.nombre,
                    'edad': pensionado.edad,
                    'salario': pensionado.salario,
                    'es_alto_riesgo': pensionado.es_alto_riesgo,
                    'es_congresista': pensionado.es_congresista,
                    'es_trabajador_CTI': pensionado.es_trabajador_CTI,
                    'es_aviador': pensionado.es_aviador,
                    'residencia_exterior': pensionado.residencia_exterior,
                    'tiene_grupo_familiar_colombia': pensionado.tiene_grupo_familiar_colombia,
                    'codigo_CIU': pensionado.codigo_CIU,
                    'tipo_pensionado': pensionado.tipo_pensionado,
                    'tipo_pensionado_nombre': pensionado.get_tipo_pensionado_display(),
                    'novedades': novedades
                })

            return JsonResponse(respuesta, safe=False)
    except:
        traceback.print_exc()
        return JsonResponse({"mensaje": "Ocurrió un error consultando los pensionados del aportante " + str(id)})


@csrf_exempt
def actualizar_eliminar_pensionado(request, id):
    try:
        if request.method == 'PUT':
            data = json.loads(request.body)

            pensionado = models.Pensionado.objects.get(pk=id)

            if data['nombre']:
                pensionado.nombre = data['nombre']

            if data['edad']:
                pensionado.edad = data['edad']

            if data['salario']:
                pensionado.salario = data['salario']

            if data['esAltoRiesgo']:
                pensionado.es_alto_riesgo = data['esAltoRiesgo']

            if data['esCongresista']:
                pensionado.es_congresista = data['esCongresista']

            if data['esTrabajadorCTI']:
                pensionado.es_trabajador_CTI = data['esTrabajadorCTI']

            if data['esAviador']:
                pensionado.es_aviador = data['esAviador']

            if data['residenciaExterior']:
                pensionado.residencia_exterior = data['residenciaExterior']

            if data['tieneGrupoFamiliarColombia']:
                pensionado.tiene_grupo_familiar_colombia = data['tieneGrupoFamiliarColombia']

            if data['codigoCIU']:
                pensionado.codigo_CIU = data['codigoCIU']

            if data['tipoPensionado']:
                pensionado.tipo_pensionado = data['tipoPensionado']

            pensionado.save()

            return HttpResponse(serializers.serialize("json", [pensionado]))
        elif request.method == 'DELETE':
            pensionado = models.Pensionado.objects.get(pk=id)

            pensionado.delete()

            return JsonResponse({"mensaje": "ok"})
        elif request.method == 'GET':
            pensionado = models.Pensionado.objects.get(pk=id)
            novedades = models.Novedad.objects.filter(pensionado_id=pensionado.pk).values('pk', 'fecha_inicio',
                                                                                          'fecha_fin',
                                                                                          'duracion', 'tipo_novedad')

            for novedad in novedades:
                n = models.Novedad.objects.get(pk=novedad['pk'])
                novedad['fecha_inicio'] = str(n.fecha_inicio)
                novedad['fecha_fin'] = str(n.fecha_fin)
                novedad['tipo_novedad_nombre'] = n.get_tipo_novedad_display()

            novedades = json.loads(json.dumps(list(novedades)))

            respuesta = {
                'pk': pensionado.pk,
                'nombre': pensionado.nombre,
                'edad': pensionado.edad,
                'salario': pensionado.salario,
                'es_alto_riesgo': pensionado.es_alto_riesgo,
                'es_congresista': pensionado.es_congresista,
                'es_trabajador_CTI': pensionado.es_trabajador_CTI,
                'es_aviador': pensionado.es_aviador,
                'residencia_exterior': pensionado.residencia_exterior,
                'tiene_grupo_familiar_colombia': pensionado.tiene_grupo_familiar_colombia,
                'codigo_CIU': pensionado.codigo_CIU,
                'tipo_pensionado': pensionado.tipo_pensionado,
                'tipo_pensionado_nombre': pensionado.get_tipo_pensionado_display(),
                'novedades': novedades
            }

            return JsonResponse(respuesta, safe=False)
    except:
        traceback.print_exc()
        return JsonResponse({"mensaje": "Ocurrió un error actualizando/eliminando el pensionado " + str(id)})


@csrf_exempt
def crear_novedad(request, id_aportante, id_pensionado):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)

            aportante = models.Aportante.objects.get(pk=id_aportante)
            pensionado = models.Pensionado.objects.get(pk=id_pensionado)

            novedad = models.Novedad()
            novedad.fecha_inicio = datetime.strptime(data['fechaInicio'], "%d/%m/%Y")
            novedad.fecha_fin = datetime.strptime(data['fechaFin'], "%d/%m/%Y")
            novedad.duracion = data['duracion']
            novedad.tipo_novedad = data['tipo']
            novedad.aportante = aportante
            novedad.pensionado = pensionado
            novedad.save()

            return HttpResponse(serializers.serialize("json", [novedad]))
    except:
        traceback.print_exc()
        return JsonResponse({"mensaje": "Ocurrió un error creando la novedad"})


@csrf_exempt
def actualizar_eliminar_novedad(request, id_aportante, id_pensionado, id):
    try:
        if request.method == 'PUT':
            data = json.loads(request.body)

            novedad = models.Novedad.objects.get(pk=id)

            if data['fechaInicio']:
                novedad.fecha_inicio = datetime.strptime(data['fechaInicio'], "%d/%m/%Y")

            if data['fechaFin']:
                novedad.fecha_fin = datetime.strptime(data['fechaFin'], "%d/%m/%Y")

            if data['duracion']:
                novedad.duracion = data['duracion']

            if data['tipo']:
                novedad.tipo_novedad = data['tipo']

            novedad.save()

            return HttpResponse(serializers.serialize("json", [novedad]))
        elif request.method == 'DELETE':
            novedad = models.Novedad.objects.get(pk=id)

            novedad.delete()

            return JsonResponse({"mensaje": "ok"})
    except:
        traceback.print_exc()
        return JsonResponse({"mensaje": "Ocurrió un error actualizando/eliminando la novedad"})


@csrf_exempt
def consultar_tipo_usuario(request, id):
    try:
        if request.method == 'POST':
            respuesta = {
                "id_aportante": "",
                "id_operador_servicio": ""
            }
            usuario = User.objects.get(pk=id)
            grupos = usuario.groups.all()

            if len(grupos) == 1:
                if str(grupos[0]).upper() == "APORTANTE":
                    aportante = models.Aportante.objects.get(usuario_id=usuario.pk)
                    respuesta['id_aportante'] = aportante.pk
                elif str(grupos[0]).upper() == "OPERADOR":
                    operador_servicio = models.OperadorServicio.objects.get(pk=usuario.pk)
                    respuesta['id_operador_servicio'] = operador_servicio.pk

            return JsonResponse(respuesta, safe=False)
    except:
        traceback.print_exc()
        return JsonResponse({"mensaje": "Ocurrió un error consultando el tipo del usuario " + str(id)})


@csrf_exempt
def calcular_pago_servicio(request, id_aportante, id_pensionado, id_servicio):
    valor_a_pagar = 0
    try:
        if request.method == 'POST':
            servicio = models.Servicio.objects.get(pk=id_servicio)
            pensionado = models.Pensionado.objects.get(pk=id_pensionado)

            if servicio.pk == 1:
                valor_a_pagar = servicio.calcular_pago_aporte_pension(pensionado)
            elif servicio.pk == 2:
                valor_a_pagar = servicio.calcular_pago_aporte_salud(pensionado)
            elif servicio.pk == 3:
                valor_a_pagar = servicio.calcular_pago_aporte_riesgos_laborales(pensionado)

        respuesta = {
            'valor_a_pagar': valor_a_pagar
        }

        return JsonResponse(respuesta, safe=False)
    except:
        traceback.print_exc()
        return JsonResponse({"mensaje": "Ocurrio un error calculando el pago del servicio"})
