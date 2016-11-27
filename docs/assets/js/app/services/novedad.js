$( function() {
    $( "#fechaInicio" ).datepicker({
        dateFormat: "dd/mm/yy"
    });
    $( "#fechaFin" ).datepicker({
        dateFormat: "dd/mm/yy"
    });

    loadCredentials();
    $('#labelUsername').html(USER.fields.username);
});

$(window).load(function () {
    var idPensionado = getUrlParameter('idP');
    var idNovedad = getUrlParameter('id');

    GET('/pensionados/' + idPensionado + '/', function (response) {
        if (!response.message){
            for(var i = 0; i < response.novedades.length; i++) {
                if (response.novedades[i].pk == idNovedad) {
                    var fechaInicioDate = new Date(Date.parse(response.novedades[i].fecha_inicio.replace(/-/g, '/')));
                    var fechaFinDate = new Date(Date.parse(response.novedades[i].fecha_fin.replace(/-/g, '/')));

                    $('#fechaInicio').val(fechaInicioDate.getDate() + '/' + (fechaInicioDate.getMonth() + 1) + '/' +  fechaInicioDate.getFullYear());
                    $('#fechaFin').val(fechaFinDate.getDate() + '/' + (fechaFinDate.getMonth() + 1) + '/' +  fechaFinDate.getFullYear());
                    $('#duracion').val(response.novedades[i].duracion);
                    $('#tipo > option[value="' + response.novedades[i].tipo_novedad + '"]').attr('selected', 'selected');

                    break;
                }
            }
        }
    });
});

function crearNovedad() {
    var idPensionado = getUrlParameter('idP');
    var fechaInicioDate = new Date(Date.parse($('#fechaInicio').val().replace(/-/g, '/')));
    var fechaFinDate = new Date(Date.parse($('#fechaFin').val().replace(/-/g, '/')));

    var data = {
        fechaInicio: fechaInicioDate.getDate() + '/' + (fechaInicioDate.getMonth() + 1) + '/' +  fechaInicioDate.getFullYear(),
        fechaFin: fechaFinDate.getDate() + '/' + (fechaFinDate.getMonth() + 1) + '/' +  fechaFinDate.getFullYear(),
        duracion: parseInt($('#duracion').val()),
        tipo: parseInt($('#tipo option:selected').val())
    };
    
    POST('/aportantes/' + USER.idAportante + '/pensionados/' + idPensionado + '/novedades/', JSON.stringify(data), function (response) {
        if (response.mensaje){
            $('#message').html(response.mensaje);
        }
        else if (response.length > 0){
            $('#message').html('¡Novedad creada exitosamente!');
        }
    });
}

function actualizarNovedad() {
    var idPensionado = getUrlParameter('idP');
    var idNovedad = getUrlParameter('id');
    var fechaInicioDate = new Date(Date.parse($('#fechaInicio').val().replace(/-/g, '/')));
    var fechaFinDate = new Date(Date.parse($('#fechaFin').val().replace(/-/g, '/')));

    var data = {
        fechaInicio: fechaInicioDate.getDate() + '/' + (fechaInicioDate.getMonth() + 1) + '/' +  fechaInicioDate.getFullYear(),
        fechaFin: fechaFinDate.getDate() + '/' + (fechaFinDate.getMonth() + 1) + '/' +  fechaFinDate.getFullYear(),
        duracion: parseInt($('#duracion').val()),
        tipo: parseInt($('#tipo option:selected').val())
    };

    PUT('/aportantes/' + USER.idAportante + '/pensionados/' + idPensionado + '/novedades/' + idNovedad + '/', JSON.stringify(data), function (response) {
        if (response.mensaje){
            $('#message').html(response.mensaje);
        }
        else if (response.length > 0){
            $('#message').html('¡Novedad actualizada exitosamente!');
        }
    });
}

function eliminarNovedad(idPensionado, id) {
    DELETE('/aportantes/' + USER.idAportante + '/pensionados/' + idPensionado + '/novedades/' + id + '/', function (response) {
        if (response.mensaje){
            $('#message').html(response.mensaje);
        }
        else if (response.length > 0){
            $('#message').html('¡Novedad eliminada exitosamente!');
        }
        location.reload();
    });
}