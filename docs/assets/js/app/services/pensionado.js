$(window).load(function () {
    var id = getUrlParameter('id');

    GET('/pensionados/' + id + '/', function (response) {
        $('#nombre').val(response.nombre);
        $('#usuario').val(response.usuario);
        $('#tipoPagador > option[value="' + response.tipo_pagador_pensiones + '"]').attr('selected', 'selected');

        $('#nombre').val(response.nombre);
        $('#edad').val(response.edad);
        $('#salario').val(response.salario);
        //$('input:radio[name="esAltoRiesgo"][value="' + response.es_alto_riesgo + '"]').attr('checked', true);
        $('input:radio[name="esAltoRiesgo"][value="' + response.es_alto_riesgo + '"]').attr('checked', true);
        $('#esCongresistaSI').prop('checked', true);
        $('#esTrabajadorCTISI').prop('checked', 'checked');
        $('input:radio[name="esAviador"]').filter('[value="' + response.es_aviador + '"]').attr('checked', true);
        $('input:radio[name="residenciaExterior"]').filter('[value="' + response.residencia_exterior + '"]').attr('checked', true);
        $('input:radio[name="tieneGrupoFamiliarColombia"]').filter('[value="' + response.tiene_grupo_familiar_colombia + '"]').attr('checked', true);
        $('#codigoCIU > option[value="' + response.codigo_CIU + '"]').attr('selected', 'selected');
        $('#tipoPensionado > option[value="' + response.tipo_pensionado + '"]').attr('selected', 'selected');
        $('#tipoPension > option[value="' + response.tipo_pension + '"]').attr('selected', 'selected');
    });
});

function crearPensionado() {
    var data = {
        aportante: USER.idAportante,
        nombre: $('#nombre').val(),
        edad: $('#edad').val(),
        salario: $('#salario').val(),
        esAltoRiesgo: ($("input[name='esAltoRiesgo']").groupVal() == 'true'),
        esCongresista: ($("input[name='esCongresista']").groupVal() == 'true'),
        esTrabajadorCTI: ($("input[name='esTrabajadorCTI']").groupVal() == 'true'),
        esAviador: ($("input[name='esAviador']").groupVal() == 'true'),
        residenciaExterior: ($("input[name='residenciaExterior']").groupVal() == 'true'),
        tieneGrupoFamiliarColombia: ($("input[name='tieneGrupoFamiliarColombia']").groupVal() == 'true'),
        codigoCIU: $('#codigoCIU option:selected').val(),
        tipoPensionado: $('#tipoPensionado option:selected').val(),
        tipoPension: $('#tipoPension option:selected').val()
    };
    
    POST('/pensionados/', JSON.stringify(data), function (response) {
        if (response.mensaje){
            $('#message').html(response.mensaje);
        }
        else if (response.length > 0){
            $('#message').html('¡Pensionado creado exitosamente!');
        }
    });
}

function actualizarPensionado() {
    var id = getUrlParameter('id');
    var data = {
        nombre: $('#nombre').val(),
        edad: parseInt($('#edad').val()),
        salario: parseFloat($('#salario').val()),
        esAltoRiesgo: ($("input[name='esAltoRiesgo']").groupVal() == 'true'),
        esCongresista: ($("input[name='esCongresista']").groupVal() == 'true'),
        esTrabajadorCTI: ($("input[name='esTrabajadorCTI']").groupVal() == 'true'),
        esAviador: ($("input[name='esAviador']").groupVal() == 'true'),
        residenciaExterior: ($("input[name='residenciaExterior']").groupVal() == 'true'),
        tieneGrupoFamiliarColombia: ($("input[name='tieneGrupoFamiliarColombia']").groupVal() == 'true'),
        codigoCIU: parseInt($('#codigoCIU option:selected').val()),
        tipoPensionado: parseInt($('#tipoPensionado option:selected').val()),
        tipoPension: $('#tipoPension option:selected').val()
    };

    PUT('/pensionados/' + id + '/', JSON.stringify(data), function (response) {
        if (response.mensaje){
            $('#message').html(response.mensaje);
        }
        else if (response.length > 0){
            $('#message').html('¡Pensionado actualizado exitosamente!');
        }
    });
}

function eliminarPensionado(id) {
    DELETE('/pensionados/' + id + '/', function (response) {
        if (response.mensaje){
            $('#message').html(response.mensaje);
        }
        else if (response.length > 0){
            $('#message').html('¡Pensionado eliminado exitosamente!');
        }
        location.reload();
    });
}
