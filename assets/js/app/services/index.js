var globalParameters = {};


function isServiceOperatorAuthenticated() {
    loadCredentials();
    if (USER) {
        if (USER.tipo == OPERATOR) {
            $('#labelUsername').html(USER.name + '<small>' + USER.tipo + '</small>');
        }
    }
    else{
        window.location.href = "../../index.html";
    }
};

function isContributorAuthenticated() {
    loadCredentials();
    if (USER) {
        if (USER.tipo == CONTRIBUTOR) {
            $('#labelUsername').html(USER.name + '<small>' + USER.tipo + '</small>');
        }
    }
    else{
        window.location.href = "../../index.html";
    }
};

var nf = new Intl.NumberFormat('es-CO', {
  style: 'currency',
  currency: 'COP',
  minimumFractionDigits: 2,
  maximumFractionDigits: 2
});


