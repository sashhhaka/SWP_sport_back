function search_students() {
    let input = document.getElementById('search_block').value
   input=input.toLowerCase();
   let x = document.getElementsByClassName('students_list');
   for (i = 0; i < x.length; i++) {
       if (!x[i].innerHTML.toLowerCase().includes(input)) {
         x[i].style.display="none";
       }
      else {
          x[i].style.display="block";
      }
   }
}

