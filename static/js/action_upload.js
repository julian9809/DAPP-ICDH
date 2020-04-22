$(document).ready(function() {
  $('#btn_upload').click(function() {
    var opc = $('input:radio[name=eleccion]:checked').val();
    const fi = document.getElementById('archivos');
    if(fi.files.length == 1){
      $.ajax({
        type : 'POST',
        url : '/uploader'
      });
    }
  });

  $('#cargar_imagen').click(function() {
    $.ajax({
      type: 'POST',
      url: '/carga',
      success: function(response){
        console.log(response);
        var x = window.open("","_self");
        x.document.open();
        x.document.write(response);
        x.document.close();
      },
      error: function(error){
        console.log(error);
      }
    });
  });

  $('#cargar_meta').click(function() {
    var name = $("#name").val();
    var description = $("#description").val();
    var date = $("#start").val();
    if(name == ''){
      swal({
             title: "Oops!",
             text: "Por favor ingresar nombre",
             icon: "error"
           });
    }else if(description == ''){
      swal({
             title: "Oops!",
             text: "Por favor ingresar descripción",
             icon: "error"
           });
    }
    else{
      var json_text = '{"name" : '+'"'+name+'" , "description" : '+'"'+description+'", "date" : '+'"'+date+'"}';
      var obj_data = JSON.parse(json_text);
      console.log(obj_data)
      $.ajax({
        data : obj_data,
        type : 'POST',
        url : '/formulario_carga',
        success: function(response){
          console.log(response);
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
    event.preventDefault();
  });

  $('#btn_carga').click(function() {
    $.ajax({
      type: 'POST',
      url: '/carga',
      success: function(response){
        console.log(response);
        var x = window.open("","_self");
        x.document.open();
        x.document.write(response);
        x.document.close();
      },
      error: function(error){
        console.log(error);
      }
    });
  });

  $('#btn_carga_ipfs').click(function() {
    $.ajax({
      type: 'POST',
      url: '/carga_ipfs',
      success: function(response){
        console.log(response);
        var x = window.open("","_self");
        x.document.open();
        x.document.write(response);
        x.document.close();
      },
      error: function(error){
        console.log(error);
      }
    });
  });

  $('#inicio').click(function() {
    $.ajax({
      type: 'POST',
      url: '/inicio',
      success: function(response){
        console.log(response);
        var x = window.open("","_self");
        x.document.open();
        x.document.write(response);
        x.document.close();
      },
      error: function(error){
        console.log(error);
      }
    });
  });

  $('#btn_inicio').click(function() {
    $.ajax({
      type: 'POST',
      url: '/inicio',
      success: function(response){
        console.log(response);
        var x = window.open("","_self");
        x.document.open();
        x.document.write(response);
        x.document.close();
      },
      error: function(error){
        console.log(error);
      }
    });
  });

  $('#btn_inicio_ipfs').click(function() {
    $.ajax({
      type: 'POST',
      url: '/inicio_ipfs',
      success: function(response){
        console.log(response);
        var x = window.open("","_self");
        x.document.open();
        x.document.write(response);
        x.document.close();
      },
      error: function(error){
        console.log(error);
      }
    });
  });

  $('#btn_formulario').click(function() {
    $.ajax({
      type: 'POST',
      url: '/formulario',
      success: function(response){
        console.log(response);
        var x = window.open("","_self");
        x.document.open();
        x.document.write(response);
        x.document.close();
      },
      error: function(error){
        console.log(error);
      }
    });
  });

  $('#btn_exito').click(function() {
    $.ajax({
      type: 'POST',
      url: '/exito',
      success: function(response){
        console.log(response);
        var x = window.open("","_self");
        x.document.open();
        x.document.write(response);
        x.document.close();
      },
      error: function(error){
        console.log(error);
      }
    });
  });

});
