$(document).ready(function() {
  var account = '';
  $("#register").hide()
  $("#register-phrase").hide()

  $('#register_account_form').click(function() {
    $("#login").hide();
    $("#register").show();
    event.preventDefault();
  });

  $('#login_form').click(function() {
    $("#register").hide();
    $("#login").show();
    event.preventDefault();
  });

  $('#btn_login').click(function() {
    var password_login = $("#password_login").val();
    var frase_login = $("#frase_usuario").val();
    if(password_login == ''){
      swal({
             title: "Oops!",
             text: "Ingresa contraseña",
             icon: "error"
           });
    }else if(frase_login == ''){
      swal({
             title: "Oops!",
             text: "Ingresa frase",
             icon: "error"
           });
    }
    else{
      var json_text = '{"password" : '+'"'+password_login+'" , "frase" : '+'"'+frase_login+'"}';
      var obj_data = JSON.parse(json_text);
      console.log(obj_data)
      $.ajax({
      data : obj_data,
      type : 'POST',
      url : '/login'
    })
    .done(function(data) {
        if(data.response == "Error"){
          swal({
                 title: "Oops!",
                 text: "Credenciales invalidas",
                 icon: "error"
               });
        }
        else{
               console.log(data.address)//swal("It`s Okey", data.success,"success");
               var json_text = '{"account" : '+'"'+data.address+'"}';
               var obj_data = JSON.parse(json_text);
               console.log(obj_data)
               $.ajax({
               data : obj_data,
               type : 'POST',
               url : '/user',
               success: function(response){
      				//console.log(response);
              var x = window.open("","_self");
              x.document.open();
              x.document.write(response);
              x.document.close();

      			},
      			error: function(error){
      				console.log(error);
      			}
             });
        }

    });

    }
    event.preventDefault();
  });



  $('#btn_registrar').click(function() {
    var password = $("#password_registrer").val();
    var password_confirmation = $("#password_registrer_confirmation").val();
    if(password === '' || password_confirmation === ''){
      swal({
             title: "Oops!",
             text: "Las contraseñas no son iguales",
             icon: "error"
           });
    }
    else if(password !== password_confirmation){
      swal({
             title: "Oops!",
             text: "Las contraseñas no son iguales",
             icon: "error"
           });
    }
    else{
      var json_text = '{"password" : '+'"'+password+'"}';
      var obj_data = JSON.parse(json_text);
      console.log(obj_data);
      $.ajax({
      data : obj_data,
      type : 'POST',
      url : '/register'
    }).done(function(data) {
        if(data.response == "Error"){
          swal({
                 title: "Oops!",
                 text: "Credenciales invalidas",
                 icon: "error"
               });
        }
        else{
          swal({
                 title: "Registro Correcto",
                 text: "Bienvenido",
                 icon: "success"
               });
               console.log(data.phrase);
               console.log(data.address);
               account = data.address;
               $("#register").hide()
               $("#register-phrase").show()
               $("#frase_usuario_registro").append(data.phrase)
        }
      });
    }
    event.preventDefault();
  });


$('#btn_guardar').click(function() {
  console.log('entre guardar');
  console.log(account)
  var json_text = '{"account" : '+'"'+account+'"}';
  var obj_data = JSON.parse(json_text);
  console.log(obj_data)
  $.ajax({
  data : obj_data,
  type : 'POST',
  url : '/user',
  success: function(response){
   //console.log(response);
   var x = window.open("","_self");
   x.document.open();
   x.document.write(response);
   x.document.close();

  },
  error: function(error){
   console.log(error);
  }
  });
  event.preventDefault();
});

$('#log_out').click(function() {
  //var json_text = '{"account" : '+'"'+account+'"}';
  //var obj_data = JSON.parse(json_text);
  //console.log(obj_data)
  //$.ajax({
  //data : obj_data,
  //type : 'POST',
  //url : '/',
  //success: function(response){
   //console.log(response);
   //var x = window.open("","_self");
   //x.document.open();
   //x.document.write(response);
   //x.document.close();

  //},
  //error: function(error){
   //console.log(error);
  //}
  //});
  window.location = '/'
  event.preventDefault();
});

});
