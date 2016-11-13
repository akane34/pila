$(window).load(function () {
    var idPensionado = getUrlParameter('idP');

    GET('/pensionados/' + idPensionado + '/', function (response) {
        $('#nombre').val(response.nombre);
        $('#codigoCIU').val(response.codigo_CIU);
        $('#salario').val(response.salario);
        $('#tipoPensionado').val(response.tipo_pensionado_nombre);
        $('#tipoPension').val(response.tipo_pension_nombre);
        $('#edad').val(response.edad);
    });
});
