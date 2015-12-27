
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
            //alert(data);
            //alert("JSRES = " + data);
            //alert("JSRES = " + data['teacher_classes'][0][1]);
            //alert("JSRES = " + data['teacher_table']['columns']);
            //alert("JSRES = " + data['teacher_table']['students']);
            //alert("JSRES = " + data['']['students']);
            res = data;
        }
    });
    return res;
}
window.onload = function createTable()
{
   // document.write("<link rel='stylesheet' href='bootstrap.css' type='text/css'>");
    data = getTeacherData();
    
    var tchTable = document.getElementById('tchTable');
    
    var input1 = document.createElement('input');
    input1.type = 'hidden';
    input1.name = 'teacher_id';
    
    var user_id = getUrlVars()['user_id'];
    input1.value = user_id;
    
    var tr1 = document.createElement('tr'); 
    tr1.className = "tr1";
    tr1.appendChild(input1);
    
    var mySelect = document.createElement('select');
    mySelect.size = "1";
    mySelect.className = "form-control";
    mySelect.name = "class_id";
    
    var trOption = document.createElement('option');
    trOption.value = data['teacher_classes'][0][0];
    trOption.text = data['teacher_classes'][0][1];
    mySelect.appendChild(trOption);   
    tr1.appendChild(mySelect);

    var mform = document.createElement('form');
    mform.method = "POST";
    mform.action = "new";
    mform.setAttribute("role", "form"); 
    mform.appendChild(tr1);


    var tr2 = document.createElement('tr'); 

    var td1 = document.createElement('td');
    td1.innerHTML = "Студент";
    tr2.appendChild(td1);
    for(i in data['teacher_table']['columns'])  {
        var input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'column_id';
        input.value = data['teacher_table']['columns'][i][0];
        tr2.appendChild(input);
        var td = document.createElement('td');
        td.innerHTML = data['teacher_table']['columns'][i][1];
        tr2.appendChild(td);
    }
    var tdBtn = document.createElement('td');
    var btn = document.createElement('button');
    btn.type = "submit";
    btn.className = "btn btn-success";
    btn.innerHTML = "new";
    tdBtn.appendChild(btn);
    tr2.appendChild(tdBtn);
    mform.appendChild(tr2);
    tchTable.appendChild(mform);

    i = 0;
    var j = 1;
    for(i in data['teacher_table']['students']){
        var form = document.createElement('form');
        form.method = "POST";
        form.action = "update";
        form.setAttribute("role", "form"); 

        var tr = document.createElement('tr');
       
        var input2 = document.createElement('input');
        input2.type = 'hidden';
        input2.name = 'student_id';
        input2.value = data['teacher_table']['students'][i][0];
        tr.appendChild(input2);
       
        var input3 = document.createElement('input');
        input3.type = 'hidden';
        input3.name = 'teacher_id';
        input3.value = user_id;
        tr.appendChild(input3);
       
        var td1 = document.createElement('td');
        td1.innerHTML = data['teacher_table']['students'][i][1];
        tr.appendChild(td1);
        form.appendChild(tr);
       
        for(var k=1; k < data['teacher_table']['table'][j].length; k++){
                var td2 = document.createElement('td');
                td2.innerHTML = data['teacher_table']['table'][j][k];
                tr.appendChild(td2);
        }
       
        var tdBtn = document.createElement('td');
        
        var btn = document.createElement('button');
        btn.type = "submit";
        btn.className = "btn btn-success";
        btn.innerHTML = "update";
        tdBtn.appendChild(btn);
       
        tr.appendChild(tdBtn);
       
        tchTable.appendChild(form);
        form.appendChild(tr);
        
        j++;
    }
}