from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$', views.pila_login),
    url(r'^aportantes/$', views.crear_consultar_aportante),
    url(r'^aportantes/(?P<id>\d+)/$', views.actualizar_eliminar_aportante),
    url(r'^aportantes/(?P<id>\d+)/pensionados/$', views.consultar_pensionados),
    url(r'^pensionados/$', views.crear_pensionado),
    url(r'^pensionados/(?P<id>\d+)/$', views.actualizar_eliminar_pensionado),
    url(r'^aportantes/(?P<id_aportante>\d+)/pensionados/(?P<id_pensionado>\d+)/novedades/$', views.crear_novedad),
    url(r'^aportantes/(?P<id_aportante>\d+)/pensionados/(?P<id_pensionado>\d+)/novedades/(?P<id>\d+)/$',
        views.actualizar_eliminar_novedad),
    url(r'^usuarios/(?P<id>\d+)/$', views.consultar_tipo_usuario),
    url(r'^aportantes/(?P<id_aportante>\d+)/pensionados/(?P<id_pensionado>\d+)/servicios/(?P<id_servicio>\d+)/$',
        views.calcular_pago_servicio),
    url(r'^aportantes/(?P<id_aportante>\d+)/pensionados/(?P<id_pensionado>\d+)/pagos/$',
        views.registrar_consultar_pago),
]
