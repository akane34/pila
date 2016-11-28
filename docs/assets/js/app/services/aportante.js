$(window).load(function () {
    loadCredentials();
    $('#labelUsername').html(USER.fields.username);

    var id = getUrlParameter('id');

    GET('/aportantes/' + id + '/', function (response) {
        $('#nombre').val(response.nombre);
        $('#usuario').val(response.usuario);
        $('#tipoPagador > option[value="' + response.tipo_pagador_pensiones + '"]').attr('selected', 'selected');
    });
});

function crearAportante() {
    var data = {
        nombre: $('#nombre').val(),
        usuario: $('#usuario').val(),
        password: $('#password').val(),
        tipoPagador: parseInt($('#tipoPagador option:selected').val())
    }
    
    POST('/aportantes/', JSON.stringify(data), function (response) {
        if (response.mensaje){
            $('#message').html(response.mensaje);
        }
        else if (response.length > 0){
            $('#message').html('¡Aportante creado exitosamente!');
        }
    });
}

function actualizarAportante() {
    var id = getUrlParameter('id');
    var data = {
        nombre: $('#nombre').val(),
        tipoPagador: parseInt($('#tipoPagador option:selected').val()),
        password: ""
    }

    var password = $('#password').val();
    if(password && password !== ""){
        data.password = password;
    }

    PUT('/aportantes/' + id + '/', JSON.stringify(data), function (response) {
        if (response.mensaje){
            $('#message').html(response.mensaje);
        }
        else if (response.length > 0){
            $('#message').html('¡Aportante actualizado exitosamente!');
        }
    });
}

function eliminarAportante(id) {
    DELETE('/aportantes/' + id + '/', function (response) {
        if (response.mensaje){
            $('#message').html(response.mensaje);
        }
        else if (response.length > 0){
            $('#message').html('¡Aportante eliminado exitosamente!');
        }
        location.reload();
    });
}