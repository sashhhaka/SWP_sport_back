$('#exampleModalToggle').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget); // Button that triggered the modal
  var id = button.data('id');
  var url = button.data('imgurl');
  var name = button.data('name');
  var sub_students = button.data('sub_students').split('Student: ');
  var fin_students = button.data('fin_students').split('Student: ');
  var ass_coaches = button.data('ass_coaches').split('Teacher: ');
  // var short_description = button.data('short_description');
  var description = button.data('description');

  var modal = $(this);
  modal.find('.achiev-img').attr('src', url);
  modal.find('.achievement-name').text(name);
  // modal.find('.short_description').text(short_description)
  modal.find('.description').text(description)


// Function to update the modal field
// Function to update the modal field
// Function to update the modal field



function updateModalField() {
  // Get the modal element
  var modal = $('#exampleModalToggle');

  // Update the subscribed students list
  var subStudentsList = modal.find('#sub_students_list');
  var subStudents = modal.find('.students_list');
  subStudentsList.empty(); // Clear the existing list

  subStudents.each(function (index) {
    var checkbox = $(this).find('.button_for_students');
    var isChecked = checkbox.prop('checked');
    var studentName = $(this).find('span').text().trim(); // Trim whitespace

    if (studentName !== '') { // Filter out empty student names
      if (!isChecked) {
        // Add the student back to the subscribed students list
        var studentHTML = '<div class="students_list">' +
          '<p style="color: black; font-size: 15px; font-family: -apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,\'Helvetica Neue\',Arial,\'Noto Sans\',sans-serif,\'Apple Color Emoji\',\'Segoe UI Emoji\',\'Segoe UI Symbol\',\'Noto Color Emoji\';">' +
          '<span style="display: inline-block; width: 80%; vertical-align: middle;">' +
          studentName +
          '</span>' +
          '<input class="button_for_students" id="button' + id + index.toString() + '" type="checkbox" style="display: inline-block; width: 20%; vertical-align: middle;">' +
          '</p>' +
          '</div>';

        subStudentsList.append(studentHTML);
        checkbox.prop('checked', false);
      } else {
        // Move the student to the finished students list
        var finStudentsList = modal.find('#fin_students_list');
        var studentHTML = '<p class="students_list" style="color: black; font-size: 15px; font-family: -apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,\'Helvetica Neue\',Arial,\'Noto Sans\',sans-serif,\'Apple Color Emoji\',\'Segoe UI Emoji\',\'Segoe UI Symbol\',\'Noto Color Emoji\';">' + studentName + '</p>';
        finStudentsList.append(studentHTML);
        $(this).remove(); // Remove the student from the subscribed students list
      }
    }
  });

  // Update the assigned coaches list
  var assCoachesList = modal.find('#ass_coaches_list');
  var assCoaches = modal.find('.students_list');
  assCoachesList.empty(); // Clear the existing list

  assCoaches.each(function (index) {
    var coachName = $(this).text();
    var coachHTML = '<p class="students_list" style="color: black; font-size: 15px; font-family: -apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,\'Helvetica Neue\',Arial,\'Noto Sans\',sans-serif,\'Apple Color Emoji\',\'Segoe UI Emoji\',\'Segoe UI Symbol\',\'Noto Color Emoji\';">' + coachName + '</p>';
    assCoachesList.append(coachHTML);
  });

  // Reattach event listeners to the newly created checkboxes
  subStudentsList.find('.button_for_students').each(function (index) {
    var checkbox = $(this);

    checkbox.on('change', function () {
      var studentName = checkbox.closest('.students_list').find('span').text().trim();
      var isChecked = checkbox.prop('checked');

      if (isChecked) {
        // Move the student to the finished students list
        var finStudentsList = modal.find('#fin_students_list');
        var studentHTML = '<p class="students_list" style="color: black; font-size: 15px; font-family: -apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,\'Helvetica Neue\',Arial,\'Noto Sans\',sans-serif,\'Apple Color Emoji\',\'Segoe UI Emoji\',\'Segoe UI Symbol\',\'Noto Color Emoji\';">' + studentName + '</p>';
        finStudentsList.append(studentHTML);
        checkbox.prop('checked', false);
        checkbox.closest('.students_list').remove();// Remove the student from the subscribed students list


      var csrftoken = getCookie('csrftoken');

      // Send an AJAX request to the Django backend
      var xhr = new XMLHttpRequest();
      xhr.open('POST', '/ach_admin/move/', true);
      xhr.setRequestHeader('Content-Type', 'application/json');
      xhr.setRequestHeader('X-CSRFToken', csrftoken); // Set the CSRF token in the request header
      if (kaleka <= index){kaleka = index + 1}
      else {kaleka = index}
      studentID = (document.getElementById(name + (kaleka).toString()).innerHTML);
      xhr.send(JSON.stringify({ ids: id + '/%/' +  studentID}));


        // Perform AJAX request to update the database here
        // ...

        // Uncomment the line below if you want to call the updateModalField function after the AJAX request
        // updateModalField();
      }
    });
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
}

var kaleka = 0;

  var v = '';
  for (var i = 1; i < sub_students.length; i++) {
      v += '<div class="students_list">' +
      '<p style="color: black; font-size: 15px; font-family: -apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,\'Helvetica Neue\',Arial,\'Noto Sans\',sans-serif,\'Apple Color Emoji\',\'Segoe UI Emoji\',\'Segoe UI Symbol\',\'Noto Color Emoji\';">' +
      '<span style="display: inline-block; width: 80%; vertical-align: middle;">' +
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

  if (v !== '') {
    for (var i = 1; i < sub_students.length; i++) {
  (function (index) {
    var checkbox = document.getElementById('lbutton' + name + (index - 1).toString());

    checkbox.addEventListener('change', function () {
      // Get the CSRF token value from the cookies
      var csrftoken = getCookie('csrftoken');




      // Send an AJAX request to the Django backend
      var xhr = new XMLHttpRequest();
      xhr.onload = function () {
        if (xhr.status === 200) {
          //updateModalField(); // Call the function to update the modal field
        }
      };
      kaleka = index-1;
      if (this.checked) {
      xhr.open('POST', '/ach_admin/move/', true);
      }
      else{
      xhr.open('POST', '/ach_admin/move2/', true);
      }
      xhr.setRequestHeader('Content-Type', 'application/json');
      xhr.setRequestHeader('X-CSRFToken', csrftoken); // Set the CSRF token in the request header
      xhr.send(JSON.stringify({ ids: id + '/%/' + document.getElementById("l" + name + (index - 1).toString()).innerHTML }));


    });
  })(i);
}

    // Function to get the CSRF cookie value
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
  }

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

if (v !== '') {
    for (var i = 1; i < fin_students.length; i++) {
  (function (index) {
    var checkbox = document.getElementById('rbutton' + name + (index - 1).toString());


    checkbox.addEventListener('change', function () {

      // Get the CSRF token value from the cookies
      var csrftoken = getCookie('csrftoken');

      // Send an AJAX request to the Django backend
      var xhr = new XMLHttpRequest();
      xhr.onload = function () {
        if (xhr.status === 200) {
          //updateModalField(); // Call the function to update the modal field
        }
      };
      kaleka = index-1;

      if (this.checked) {
      xhr.open('POST', '/ach_admin/move/', true);
      }
      else{
      xhr.open('POST', '/ach_admin/move2/', true);
      }

      xhr.setRequestHeader('Content-Type', 'application/json');
      xhr.setRequestHeader('X-CSRFToken', csrftoken); // Set the CSRF token in the request header
      xhr.send(JSON.stringify({ ids: id + '/%/' + document.getElementById("r" + name + (index - 1).toString()).innerHTML }));

    });
  })(i);
}

    // Function to get the CSRF cookie value
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
  }

  var v = '';
  for (var i = 1; i < ass_coaches.length; i++) {
    v += '<p class="students_list" style="color: black; font-size: 15px; font-family: -apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,\'Helvetica Neue\',Arial,\'Noto Sans\',sans-serif,\'Apple Color Emoji\',\'Segoe UI Emoji\',\'Segoe UI Symbol\',\'Noto Color Emoji\';">' + ass_coaches[i].split('>')[0] + '</p>';
  }
  if (v === '') {
    v = '<p class="students_list" style="color: black; font-size: 15px; font-family: -apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,\'Helvetica Neue\',Arial,\'Noto Sans\',sans-serif,\'Apple Color Emoji\',\'Segoe UI Emoji\',\'Segoe UI Symbol\',\'Noto Color Emoji\';">No assigned coaches</p>';
  }
  document.getElementById('ass_coaches_list').innerHTML = v;

  return true;
});
