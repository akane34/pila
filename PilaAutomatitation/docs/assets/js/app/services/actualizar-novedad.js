$(window).load(function () {
    var idPensionado = getUrlParameter('idP');
    var idNovedad = getUrlParameter('id');

    GET('/pensionados/' + idPensionado + '/', function (response) {
        if (!response.message){
            for(var i = 0; i < response.novedades.length; i++) {
                if (response.novedades[i].pk == idNovedad) {
                    $('#fechaInicio').val(response.novedades[i].fecha_inicio);
                    $('#fechaFin').val(response.novedades[i].fecha_fin);
                    $('#duracion').val(response.novedades[i].duracion);
                    $('#tipo > option[value="' + response.novedades[i].tipo_novedad + '"]').attr('selected', 'selected');

                    break;
                }
            }
        }
    });
});
