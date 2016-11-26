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

function pagarServicio(idServicio) {
    loadCredentials();
    var idPensionado = getUrlParameter('idP');
    var idAportante = USER.idAportante;

    $('#step2Message').html('');

    POST('/aportantes/' + idAportante + '/pensionados/' + idPensionado + '/servicios/' + idServicio + '/', undefined, function (response) {
        if (!response.mensaje){
            if (idServicio == 1){
                $('#valorPension').val('$ ' + nf.format(response.valor_a_pagar));
                $('#valorPensionR').val('$ ' + nf.format(response.valor_a_pagar));
            }
            else if(idServicio == 2){
                $('#valorSalud').val('$ ' + nf.format(response.valor_a_pagar));
                $('#valorSaludR').val('$ ' + nf.format(response.valor_a_pagar));
            }
            else if(idServicio == 3){
                $('#valorRiesgos').val('$ ' + nf.format(response.valor_a_pagar));
                $('#valorRiesgosR').val('$ ' + nf.format(response.valor_a_pagar));
            }
        }
        else {
            $('#step2Message').html(response.message);
        }
    });
};

function calcularTotal() {
    var valorPension = parseFloat($('#valorPension').val().replace(/[\.\$]/g, ''));
    var valorSalud = parseFloat($('#valorSalud').val().replace(/[\.\$]/g, ''));
    var valorRiesgos = parseFloat($('#valorRiesgos').val().replace(/[\.\$]/g, ''));

    var total = valorSalud + valorPension + valorRiesgos;

    $('#valorTotal').val('$ ' + nf.format(total));
    $('#valorTotalR').val('$ ' + nf.format(total));
};
