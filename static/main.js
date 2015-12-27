
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

function newTeacherIdInput() {
    var teacherIdInput = document.createElement('input');
    teacherIdInput.type = 'hidden';
    teacherIdInput.name = 'teacher_id';
    teacherIdInput.value = getUrlVars()['user_id'];

    return teacherIdInput;
}

function createClassSelect(classes) {
    var form = document.createElement('form');
    
    var classSelect = document.createElement('select');
    classSelect.size = "1";
    classSelect.className = "form-control";
    classSelect.name = "class_id";
   
    for (i in classes) {
        var option = document.createElement('option');
        option.value = classes[i][0];
        option.text = classes[i][1];
        classSelect.appendChild(option);   
    }

    form.appendChild(newTeacherIdInput());
    form.appendChild(classSelect);

    document.body.insertBefore(form, document.getElementById('tchTable'));

}

function createTableHeader(columns) {
    var thead = document.createElement('thead');
    var tr = document.createElement('tr'); 
    thead.appendChild(tr);
    var tchTable = document.getElementById('tchTable');
    tchTable.appendChild(thead);
    
    var th = document.createElement('th');
    th.innerHTML = "Студент";
    tr.appendChild(th);
    
    for(i in columns)  {
        var th = document.createElement('th');
        th.innerHTML = columns[i][1];
        tr.appendChild(th);
    }
    
    var thBtn = document.createElement('th');
    var form = document.createElement('form');
    form.appendChild(newTeacherIdInput());
    form.method = "POST";
    form.action = "add";
    form.setAttribute("role", "form"); 
    
    var btn = document.createElement('button');
    btn.type = "submit";
    btn.className = "btn btn-success";
    btn.innerHTML = "new";
    form.appendChild(btn);
    thBtn.appendChild(form);
    tr.appendChild(thBtn);
    
}

function createTableBody(students, table) {
    var tbody = document.createElement('tbody');
    var tchTable = document.getElementById('tchTable');
    tchTable.appendChild(tbody);

    i = 0;
    var j = 1;
    for(i in students) {
        var tr = document.createElement('tr');
       
        var td = document.createElement('td');
        td.innerHTML = students[i][1];
        tr.appendChild(td);
       
        for(var k=1; k < table[j].length; k++){
                td = document.createElement('td');
                td.innerHTML = table[j][k];
                tr.appendChild(td);
        }
        
        var form = document.createElement('form');
        form.method = "POST";
        form.action = "update";
        form.setAttribute("role", "form"); 
        
        form.appendChild(newTeacherIdInput());
       
        var input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'student_id';
        input.value = students[i][0];
        form.appendChild(input);        
        
        var tdBtn = document.createElement('td');
        var btn = document.createElement('button');
        btn.type = "submit";
        btn.className = "btn btn-success";
        btn.innerHTML = "update";
     
        form.appendChild(btn);
        tdBtn.appendChild(form);
        tr.appendChild(tdBtn);
       
        tbody.appendChild(tr);
        
        j++;
    }
}

window.onload = function createTable()
{
    data = getTeacherData();
    var user_id = getUrlVars()['user_id'];
    createClassSelect(data['teacher_classes']);

    var tchTable = document.getElementById('tchTable');
    
    var teacherIdInput = newTeacherIdInput();
   
    createTableHeader(data['teacher_table']['columns']);
    createTableBody(data['teacher_table']['students'], data['teacher_table']['table']);
    
}
