function viewDivS(){
    display = document.getElementById("students_sub_and_fin").style.display;

    if(display=='none'){
       document.getElementById("students_sub_and_fin").style.display = "grid";
    }else{
       document.getElementById("students_sub_and_fin").style.display = "none";
    }
};

function viewDivC(){
    display = document.getElementById("ass_coaches_info").style.display;

    if(display=='none'){
       document.getElementById("ass_coaches_info").style.display = "grid";
    }else{
       document.getElementById("ass_coaches_info").style.display = "none";
    }
};

function viewDiv(){
    display1 = document.getElementById("students_sub_and_fin").style.display;
    display2 = document.getElementById("ass_coaches_info").style.display;
    
    if(display1=='grid'){
       document.getElementById("students_sub_and_fin").style.display = "none";
    }

    if(display2=='grid'){
        document.getElementById("ass_coaches_info").style.display = "none";
     }
};

