function crearNovedad() {
    var idPensionado = getUrlParameter('idP');
    var fechaInicioDate = new Date($('#fechaInicio').val());
    var fechaFinDate = new Date($('#fechaFin').val());

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
    var fechaInicioDate = new Date($('#fechaInicio').val());
    var fechaFinDate = new Date($('#fechaFin').val());

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