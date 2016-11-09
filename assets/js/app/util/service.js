function GET(uri, callbackResponse, callbackError) {
    $.ajax({
        type: 'GET',
        url: URL_HOME + uri,
        dataType: 'json',
        success: function (response) {
            if (callbackResponse){
                callbackResponse(response);
            }
        },
        fail: function (error) {
            if (callbackError){
                callbackError(error);
            }
        }
    });
}

function POST(uri, data, callbackResponse, callbackError) {
    $.ajax({
        type: 'POST',
        url: URL_HOME + uri,
        dataType: 'json',
        data: data,
        success: function (response) {
            if (callbackResponse){
                callbackResponse(response);
            }
        },
        fail: function (error) {
            if (callbackError){
                callbackError(error);
            }
        }
    });
};

function PUT(uri, data, callbackResponse, callbackError){
    $.ajax({
        type: 'PUT',
        url: URL_HOME + uri,
        dataType: 'json',
        data: data,
        success: function (response) {
            if (callbackResponse){
                callbackResponse(response);
            }
        },
        fail: function (error) {
            if (callbackError){
                callbackError(error);
            }
        }
    });
};

function DELETE(uri, callbackResponse, callbackError) {
    $.ajax({
        type: 'DELETE',
        url: URL_HOME + uri,
        dataType: 'json',
        success: function (response) {
            if (callbackResponse){
                callbackResponse(response);
            }
        },
        fail: function (error) {
            if (callbackError){
                callbackError(error);
            }
        }
    });
}

function getToken() {
    var token = {"Content-Type" : "application/json"};
    return token;
}
