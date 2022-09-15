$(document).ready(function(){
    $('#CustomUserCreationForm').validate({
        rules:{
            first_name:{
                required:true,
                minlenght:6
            },
            email:{
                required:true,
            }
        }

    })


})