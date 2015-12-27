
function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });
    return vars;
}

function getTeacherData(){
    var data, jsres, res;
    var user_id = getUrlVars()['user_id'];
    data = user_id;
    $.ajax({
        type: 'POST',
        async: false,
        timeout: 30000,
        url: "teacher_data",
        dataType: 'json',
        data: {"data": data},
        error: function (request, error) {
            console.log(arguments);
            alert(" Can't do because: " + error + request);
        },
        success:function(data){
            // alert(data);
            // alert("JSRES = " + data);
            // alert("JSRES = " + data['teacher_classes']);
            // alert("JSRES = " + data['teacher_table']['columns']);
            res = data;
        }
    });
    return res;
}


