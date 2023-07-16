$('#exampleModalToggle').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget); // Button that triggered the modal
  var id = button.data('id');
  var url = button.data('imgurl');
  var name = button.data('name');
  var sub_students = button.data('sub_students').split('Student: ');
  var fin_students = button.data('fin_students').split('Student: ');
  var ass_coaches = button.data('ass_coaches').split('Teacher: ');
  var fin_num = fin_students.length;
  var sub_num = sub_students.length;
  var short_description = button.data('short_description');
  var description = button.data('description');





  //update modal field lists of students every time its opened
  updateSubStudentsList();
  updateFinStudentsList();

  var modal = $(this);
  modal.find('.achiev-img').attr('src', url);
  modal.find('.achievement-name').text(name);
  modal.find('.short_description').text(short_description)
  modal.find('.description').text(description)

  var v = '';
  for (var i = 1; i < sub_students.length; i++) {
      v += '<div class="students_list">' +
      '<p style="color: black; font-size: 15px; font-family: -apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,\'Helvetica Neue\',Arial,\'Noto Sans\',sans-serif,\'Apple Color Emoji\',\'Segoe UI Emoji\',\'Segoe UI Symbol\',\'Noto Color Emoji\';">' +
      '<span style="display: inline-block; width: 80%; word-wrap: break-word; vertical-align: middle;">' +
      sub_students[i].split('>')[0] +
      '</span>' +
      '<input class="button_for_students" id="lbutton' + name + (i - 1).toString() + '" type="checkbox" style="display: inline-block; width: 20%; vertical-align: middle;">' +
      '</p>' +
      '</div>';
  }
  if (v === '') {
    v = '<p class="students_list" style="color: black; font-size: 15px; font-family: -apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,\'Helvetica Neue\',Arial,\'Noto Sans\',sans-serif,\'Apple Color Emoji\',\'Segoe UI Emoji\',\'Segoe UI Symbol\',\'Noto Color Emoji\';">No subscribed students</p>';
  }
  document.getElementById('sub_students_list').innerHTML = v;

function subListeners(v){
  if (v !== '') {
    for (var i = 1; i < sub_num; i++) {
  (function (index) {
    var checkbox = document.getElementById('lbutton' + name + (index - 1).toString());
    checkbox.addEventListener('change', function () {
      // Get the CSRF token value from the cookies
      var csrftoken = getCookie('csrftoken');
      // Send an AJAX request to the Django backend
      var xhr = new XMLHttpRequest();
      xhr.onload = function () {
        if (xhr.status === 200) {
          updateSubStudentsList();
          updateFinStudentsList();
        }
      };
      if (this.checked) {
      fin_num += 1;
      sub_num -= 1;
      xhr.open('POST', '/ach_admin/move/', true);
      }
      else{
      fin_num -= 1;
      sub_num += 1;
      xhr.open('POST', '/ach_admin/move2/', true);
      }
      xhr.setRequestHeader('Content-Type', 'application/json');
      xhr.setRequestHeader('X-CSRFToken', csrftoken); // Set the CSRF token in the request header
      xhr.send(JSON.stringify({ ids: id + '/%/' + document.getElementById("l" + name + (index - 1).toString()).innerHTML }));
      document.getElementById('l' + name + (index - 1).toString()).setAttribute('id', 'r' + name + (fin_num - 2).toString());

if (index < sub_num){
for (var j = index; j < sub_num;j++){
document.getElementById('l' + name + (j).toString()).setAttribute('id','l' + name + (j-1).toString());

}
}




    });

  })(i);
}

  }
}
subListeners(v);
  var v = '';
  for (var i = 1; i < fin_students.length; i++) {
      v += '<div class="students_list">' +
      '<p style="color: black; font-size: 15px; font-family: -apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,\'Helvetica Neue\',Arial,\'Noto Sans\',sans-serif,\'Apple Color Emoji\',\'Segoe UI Emoji\',\'Segoe UI Symbol\',\'Noto Color Emoji\';">' +
      '<span style="display: inline-block; width: 80%; vertical-align: middle;">' +
      fin_students[i].split('>')[0] +
      '</span>' +
      '<input class="button_for_students" id="rbutton' + name + (i - 1).toString() + '" type=checkbox checked=checked style="display: inline-block; width: 20%; vertical-align: middle;">' +
      '</p>' +
      '</div>';
     }
  if (v === '') {
    v = '<p class="students_list" style="color: black; font-size: 15px; font-family: -apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,\'Helvetica Neue\',Arial,\'Noto Sans\',sans-serif,\'Apple Color Emoji\',\'Segoe UI Emoji\',\'Segoe UI Symbol\',\'Noto Color Emoji\';">No finished students</p>';
  }
  document.getElementById('fin_students_list').innerHTML = v;

function finListeners(v){
if (v !== '') {
    for (var i = 1; i < fin_num; i++) {
  (function (index) {
    var checkbox = document.getElementById('rbutton' + name + (index - 1).toString());
    checkbox.addEventListener('change', function () {
      // Get the CSRF token value from the cookies
      var csrftoken = getCookie('csrftoken');

      // Send an AJAX request to the Django backend
      var xhr = new XMLHttpRequest();
      xhr.onload = function () {
        if (xhr.status === 200) {
          updateSubStudentsList();
          updateFinStudentsList();
        }
      };


      if (this.checked) {
      fin_num += 1;
      sub_num -= 1;
      xhr.open('POST', '/ach_admin/move/', true);
      }
      else{
      fin_num -= 1;
      sub_num += 1;
      xhr.open('POST', '/ach_admin/move2/', true);
      }

      xhr.setRequestHeader('Content-Type', 'application/json');
      xhr.setRequestHeader('X-CSRFToken', csrftoken); // Set the CSRF token in the request header
      xhr.send(JSON.stringify({ ids: id + '/%/' + document.getElementById("r" + name + (index - 1).toString()).innerHTML }));
      document.getElementById('r' + name + (index - 1).toString()).setAttribute('id', 'l' + name + (sub_num - 2).toString());

if (index < fin_num){
for (var j = index; j < fin_num;j++){
document.getElementById('r' + name + (j).toString()).setAttribute('id','r' + name + (j-1).toString());

}
}

    });
  })(i);
}

  }
}
finListeners(v);
  var v = '';
  for (var i = 1; i < ass_coaches.length; i++) {
    v += '<p class="students_list" style="color: black; font-size: 15px; font-family: -apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,\'Helvetica Neue\',Arial,\'Noto Sans\',sans-serif,\'Apple Color Emoji\',\'Segoe UI Emoji\',\'Segoe UI Symbol\',\'Noto Color Emoji\';">' + ass_coaches[i].split('>')[0] + '</p>';
  }
  if (v === '') {
    v = '<p class="students_list" style="color: black; font-size: 15px; font-family: -apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,\'Helvetica Neue\',Arial,\'Noto Sans\',sans-serif,\'Apple Color Emoji\',\'Segoe UI Emoji\',\'Segoe UI Symbol\',\'Noto Color Emoji\';">No assigned coaches</p>';
  }
  document.getElementById('ass_coaches_list').innerHTML = v;



function updateSubStudentsList() {
  var xhr = new XMLHttpRequest();

  xhr.open('POST', '/ach_admin/sub_students_list/', true); // Use POST instead of GET

  // Get the CSRF token value from the cookies
  var csrftoken = getCookie('csrftoken');
  xhr.setRequestHeader('Content-Type', 'application/json'); // Set the content type
  xhr.setRequestHeader('X-CSRFToken', csrftoken); // Set the CSRF token in the request header
  var data = JSON.stringify({ ids: id + "/%/" + name}); // Convert the data to JSON string
  xhr.send(data);
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      document.getElementById('sub_students_list').innerHTML = xhr.responseText;
      subListeners(xhr.responseText);
    }
  };
}


function updateFinStudentsList() {
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/ach_admin/fin_students_list/', true); // Use POST instead of GET

  // Get the CSRF token value from the cookies
  var csrftoken = getCookie('csrftoken');
  xhr.setRequestHeader('Content-Type', 'application/json'); // Set the content type
  xhr.setRequestHeader('X-CSRFToken', csrftoken); // Set the CSRF token in the request header
  var data = JSON.stringify({ ids: id + "/%/" + name}); // Convert the data to JSON string
  xhr.send(data);
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      document.getElementById('fin_students_list').innerHTML = xhr.responseText;
      finListeners(xhr.responseText);
    }
  };
}



  return true;
});

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
