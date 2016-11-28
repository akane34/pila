# coding=utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class OperadorServicio(models.Model):
    usuario_id = models.OneToOneField(User)
    nombre = models.CharField(max_length=250)


class TipoPagadorPensiones(models.Model):
    descripcion = models.CharField(max_length=250)


class Aportante(models.Model):
    TIPO_PAGADOR_PENSIONES = []
    usuario_id = models.OneToOneField(User)
    nombre = models.CharField(max_length=250)
    tipo_pagador_pensiones = models.IntegerField(choices=TIPO_PAGADOR_PENSIONES)
    operador_servicio = models.ForeignKey(OperadorServicio)

    def __init__(self, *args, **kwargs):
        super(Aportante, self).__init__(*args, **kwargs)
        opciones = TipoPagadorPensiones.objects.all()
        for opcion in opciones:
            self.TIPO_PAGADOR_PENSIONES.append((opcion.pk, opcion.descripcion))


class TipoPensionado(models.Model):
    descripcion = models.CharField(max_length=250)


class TipoPension(models.Model):
    descripcion = models.CharField(max_length=250)


class TipoPensionadoTipoPagadorPensiones(models.Model):
    tipo_pensionado = models.ForeignKey(TipoPensionado)
    tipo_pagador_pensiones = models.ForeignKey(TipoPagadorPensiones)


class Pensionado(models.Model):
    TIPO_PENSIONADO = []
    TIPO_PENSION = []
    nombre = models.CharField(max_length=250)
    edad = models.IntegerField()
    salario = models.FloatField()
    es_alto_riesgo = models.BooleanField()
    es_congresista = models.BooleanField()
    es_trabajador_CTI = models.BooleanField()
    es_aviador = models.BooleanField()
    residencia_exterior = models.BooleanField()
    tiene_grupo_familiar_colombia = models.BooleanField()
    codigo_CIU = models.IntegerField()
    tipo_pensionado = models.IntegerField(choices=TIPO_PENSIONADO)
    tipo_pension = models.IntegerField(choices=TIPO_PENSION)
    aportante = models.ForeignKey(Aportante)

    def __init__(self, *args, **kwargs):
        super(Pensionado, self).__init__(*args, **kwargs)

        opciones_tipo_pensionado = TipoPensionado.objects.all()
        for opcion_tipo_pensionado in opciones_tipo_pensionado:
            self.TIPO_PENSIONADO.append((opcion_tipo_pensionado.pk, opcion_tipo_pensionado.descripcion))

        opciones_tipo_pension = TipoPension.objects.all()
        for opcion_tipo_pension in opciones_tipo_pension:
            self.TIPO_PENSION.append((opcion_tipo_pension.pk, opcion_tipo_pension.descripcion))


class TipoNovedad(models.Model):
    descripcion = models.CharField(max_length=250)


class Novedad(models.Model):
    TIPO_NOVEDAD = []
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    duracion = models.IntegerField()
    tipo_novedad = models.IntegerField(choices=TIPO_NOVEDAD)
    aportante = models.ForeignKey(Aportante)
    pensionado = models.ForeignKey(Pensionado)

    def __init__(self, *args, **kwargs):
        super(Novedad, self).__init__(*args, **kwargs)
        opciones = TipoNovedad.objects.all()
        for opcion in opciones:
            self.TIPO_NOVEDAD.append((opcion.pk, opcion.descripcion))


class Servicio(models.Model):
    nombre = models.CharField(max_length=250)
    operador_servicio = models.ForeignKey(OperadorServicio)

    @staticmethod
    def calcular_pago_aporte_pension(pensionado):
        novedades = Novedad.objects.filter(pensionado_id=pensionado.pk).order_by('pk')
        ultima_novedad = None

        if len(novedades) > 0:
            ultima_novedad = novedades.reverse()[0]

        if len(novedades) == 0:
            return pensionado.salario * 0.16
        elif ultima_novedad is not None and (
                            ultima_novedad.tipo_novedad == 3 or
                            ultima_novedad.tipo_novedad == 4 or
                        ultima_novedad.tipo_novedad == 5):
            if ultima_novedad.duracion > 7:
                return pensionado.salario * 0.16
            elif 3 < ultima_novedad.duracion <= 7:
                return pensionado.salario * 0.12
            elif 0 < ultima_novedad.duracion <= 3:
                return 0
        elif pensionado.es_alto_riesgo:
            return pensionado.salario * 0.26
        elif pensionado.es_congresista:
            return pensionado.salario * 0.255
        elif pensionado.es_trabajador_CTI:
            return pensionado.salario * 0.35
        elif pensionado.es_aviador:
            return pensionado.salario * 0.21

    @staticmethod
    def calcular_pago_aporte_salud(pensionado):
        novedades = Novedad.objects.filter(pensionado_id=pensionado.pk).order_by('pk')
        ultima_novedad = None

        if len(novedades) > 0:
            ultima_novedad = novedades.reverse()[0]

        if pensionado.residencia_exterior and pensionado.tiene_grupo_familiar_colombia:
            return 0
        elif len(novedades) == 0:
            return pensionado.salario * 0.12
        else:
            if ultima_novedad is not None and (
                                ultima_novedad.tipo_novedad == 3 or
                                ultima_novedad.tipo_novedad == 4 or
                            ultima_novedad.tipo_novedad == 5):
                if 0 <= ultima_novedad.duracion <= 3:
                    return 0
                elif 3 < ultima_novedad.duracion <= 7:
                    return pensionado.salario * 0.12
                elif ultima_novedad.duracion > 7:
                    return pensionado.salario * 0.16

    @staticmethod
    def calcular_pago_aporte_riesgos_laborales(pensionado):
        if 8022 <= pensionado.codigo_CIU <= 8513:
            return pensionado.salario * 0.00522

        if 0117 <= pensionado.codigo_CIU <= 1541:
            return pensionado.salario * 0.01044

        if 1592 <= pensionado.codigo_CIU <= 1743:
            return pensionado.salario * 0.02436

        if 2101 <= pensionado.codigo_CIU <= 2322:
            return pensionado.salario * 0.04350

        if 1431 <= pensionado.codigo_CIU <= 2321:
            return pensionado.salario * 0.06960


class Pago(models.Model):
    valor_salud = models.FloatField()
    valor_pension = models.FloatField()
    valor_riesgos = models.FloatField()
    valor_total = models.FloatField()
    aportante = models.ForeignKey(Aportante)
    beneficiario = models.ForeignKey(Pensionado)
