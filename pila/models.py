# coding=utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class OperadorServicio(models.Model):
    usuario_id = models.OneToOneField(User)
    nombre = models.CharField(max_length=250)


class Aportante(models.Model):
    TIPO_PAGADOR_PENSIONES = (
        (1, 'Empleador'),
        (2, 'Administrador de pensiones'),
        (3, 'Pagador de pensiones'),
        (4, 'Pensiones de entidades de los regímenes especiales y de excepción')
    )
    usuario_id = models.OneToOneField(User)
    nombre = models.CharField(max_length=250)
    tipo_pagador_pensiones = models.IntegerField(choices=TIPO_PAGADOR_PENSIONES)
    operador_servicio = models.ForeignKey(OperadorServicio)


class Pensionado(models.Model):
    TIPO_PENSIONADO = (
        (1, 'Pensionado de régimen de prima media. Tope máximo de pensión 25 smlmv'),
        (2, 'Pensionado de régimen de prima media. Sin tope máximo de pensión'),
        (3, 'Pensionado de régimen de ahorro individual. No aplica tope máximo de pensión'),
        (4, 'Pensionado de Riesgos Laborales. Tope máximo de 25 smlmv'),
        (5, 'Pensionado por el empleador, con tope máximo de pensión 25 smlmv'),
        (6, 'Pensionado por el empleador sin tope máximo de pensión'),
        (7, 'Pensionado de entidades de los regímenes especial y de excepción, con tope máximo de pensión 25 smlmv'),
        (8, 'Pensionado de entidades de los regímenes especial y de excepción sin tope máximo de pensión'),
        (9, 'Beneficiario UPC adicional')
    )
    nombre = models.CharField(max_length=250)
    edad = models.IntegerField()
    salario = models.FloatField()
    es_alto_riesgo = models.BooleanField()
    es_congresista = models.BooleanField()
    es_trabajador_CTI = models.BooleanField()
    es_aviador = models.BooleanField()
    residencia_exterior = models.CharField(max_length=250)
    tiene_grupo_familiar_colombia = models.BooleanField()
    codigo_CIU = models.IntegerField()
    tipo_pensionado = models.IntegerField(choices=TIPO_PENSIONADO)
    aportante = models.ForeignKey(Aportante)


class Novedad(models.Model):
    TIPO_NOVEDAD = (
        (1, 'Traslado'),
        (2, 'Variación transitoria de salario'),
        (3, 'Supención temporal'),
        (4, 'Licencia no remunerada'),
        (5, 'Comisión por servicios'),
        (6, 'Incapacidad temporal por enfermedad'),
        (7, 'Licencia maternidad/paternidad'),
        (8, 'Vacaciones'),
        (9, 'Licencia remunerada'),
        (10, 'Aporte volunatario a pensiones')
    )
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    duracion = models.IntegerField()
    tipo_novedad = models.IntegerField(choices=TIPO_NOVEDAD)
    aportante = models.ForeignKey(Aportante)
    pensionado = models.ForeignKey(Pensionado)


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

        if pensionado.residencia_exterior == 'S' or pensionado.tiene_grupo_familiar_colombia == 'S':
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
