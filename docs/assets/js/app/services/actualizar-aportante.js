$(window).load(function () {
    var id = getUrlParameter('id');

    GET('/aportantes/' + id + '/', function (response) {
        $('#nombre').val(response.nombre);
        $('#usuario').val(response.usuario);
        $('#tipoPagador > option[value="' + response.tipo_pagador_pensiones + '"]').attr('selected', 'selected');
    });
});
