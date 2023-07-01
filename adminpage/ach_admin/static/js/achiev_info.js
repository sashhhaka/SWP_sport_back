
  $('#exampleModalToggle').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget) // Button that triggered the modal
    var id = button.data('id')
    var url = button.data('imgurl')
    var name = button.data('name')
    var sub_students = button.data('sub_students').split('Student: ')
    var fin_students = button.data('fin_students').split('Student: ')
    var ass_coaches = button.data('ass_coaches').split('Teacher: ')


    var modal = $(this)
    modal.find('.achiev-img').attr('src', url)
    modal.find('.achievement-name').text(name)

    var v = ''
    for (var i = 1; i < sub_students.length; i++) {
      v += '<p class="students_list" style="color: black; font-size: 15px; font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";">' + sub_students[i].split('>')[0] + '</p>'
    }
    if (v == '') {
      v = '<p class="students_list" style="color: black; font-size: 15px; font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";">No subscribed students</p>'
    }
    document.getElementById('sub_students_list').innerHTML = v

    var v = ''
    for (var i = 1; i < fin_students.length; i++) {
      v += '<p class="students_list" style="color: black; font-size: 15px; font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";">' + fin_students[i].split('>')[0] + '</p>'
    }
    if (v == '') {
      v = '<p class="students_list" style="color: black; font-size: 15px; font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";">No finished students</p>'
    }
    document.getElementById('fin_students_list').innerHTML = v

    var v = ''
    for (var i = 1; i < ass_coaches.length; i++) {
      v += '<p class="students_list" style="color: black; font-size: 15px; font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";">' + ass_coaches[i].split('>')[0] + '</p>'
    }
    if (v == '') {
      v = '<p class="students_list" style="color: black; font-size: 15px; font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";">No assigned coaches</p>'
    }
    document.getElementById('ass_coaches_list').innerHTML = v

    return(true)
  })

