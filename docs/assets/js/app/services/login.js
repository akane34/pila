function loginPila() {
    var data = {
        usuario : $('#username').val(),
        password : $('#password').val()
    };

    POST('/login/', JSON.stringify(data), function (response) {
        if (response && response.mensaje){
            $('#errorMessage').html(response.mensaje);
        }
        else{
            $('#errorMessage').html('');

            setCredentials(response[0]);

            POST('/usuarios/' + USER.pk + '/', undefined, function (response) {
                if (response){
                    loadCredentials();
                    if (response.id_operador_servicio){
                        USER.idOperadorServicio = response.id_operador_servicio;
                    }

                    if (response.id_aportante){
                        USER.idAportante = response.id_aportante;
                    }

                    setCredentials(USER);

                    if ($.inArray(1, USER.fields.groups) == 0){
                        window.location.href = "html/aportante/consultar-pensionado.html";
                    }
                    else if ($.inArray(2, USER.fields.groups) == 0){
                        window.location.href = "html/operadorServicio/consultar-aportante.html";
                    }
                    else if ($.inArray(3, USER.fields.groups) == 0){
                        window.location.href = "html/operadorServicio/consultar-aportante.html";
                    }
                    else{
                        window.location.href = "html/aportante/consultar-pensionado.html";
                    }
                }
            });
        }
    });
}

function logoutPila() {
    sessionStorage.clear();
    localStorage.clear();
    USER = undefined;
    window.location.href = "../../index.html";
}

function verifyUserInIndex(){
    loadCredentials();
    if (USER){
        if (USER.tipo == OPERATOR){
            window.location.href = "html/operadorServicio/consultar-aportante.html";
        }
        else if (USER.tipo == CONTRIBUTOR){
            window.location.href = "html/aportante/consultar-pensionado.html";
        }
    }
}

function loadCredentials() {
    var user = undefined;

    REMEMBER = localStorage.getItem('remember');

    if (REMEMBER && REMEMBER == 'true'){
        user = localStorage.getItem('userPayService');
    }
    else {
        user = sessionStorage.getItem('userPayService');
    }

    if (user) {
        USER = JSON.parse(user);
    }
    else {
        USER = undefined;
    }

    return USER;
}

function setCredentials(user) {
    USER = user;
    REMEMBER = $('input[name="remember"]:checked');
    localStorage.setItem('remember', REMEMBER);

    if (REMEMBER && REMEMBER == 'true'){
        localStorage.setItem('userPayService', JSON.stringify(user));
    }
    else{
        sessionStorage.setItem('userPayService', JSON.stringify(user));
    }
}
