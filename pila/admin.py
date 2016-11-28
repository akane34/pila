from django.contrib import admin

from .models import OperadorServicio, Aportante, Pensionado, Novedad, Pago, Servicio, TipoPagadorPensiones, \
    TipoPensionado, TipoNovedad, TipoPensionadoTipoPagadorPensiones, TipoPension

# Register your models here.

admin.site.register(OperadorServicio)
admin.site.register(Aportante)
admin.site.register(Pensionado)
admin.site.register(Novedad)
admin.site.register(Pago)
admin.site.register(Servicio)
admin.site.register(TipoPagadorPensiones)
admin.site.register(TipoPensionado)
admin.site.register(TipoPension)
admin.site.register(TipoNovedad)
admin.site.register(TipoPensionadoTipoPagadorPensiones)
