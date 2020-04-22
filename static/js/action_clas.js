$(document).ready(function() {
  $('#clasificar_imagen').click(function() {
    $.ajax({
      type: 'POST',
      url: '/clasificar',
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

  $('#btn_si_carga').click(function() {
    $.ajax({
      type: 'POST',
      url: '/cargar_imagenes',
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

  $('#btn_no_carga').click(function() {
    clas = "no_clasificado"
    var json_text = '{"clasificacion" : '+'"'+clas+'"}';
    var obj_data = JSON.parse(json_text);
    console.log(obj_data)
    $.ajax({
      data: obj_data,
      type: 'POST',
      url: '/clasificacion',
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

  $('#btn_violenta').click(function() {
    clas = "violenta"
    var json_text = '{"clasificacion" : '+'"'+clas+'"}';
    var obj_data = JSON.parse(json_text);
    console.log(obj_data)
    $.ajax({
      data: obj_data,
      type: 'POST',
      url: '/clasificacion',
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

  $('#btn_no_violenta').click(function() {
    clas = "no_violenta"
    var json_text = '{"clasificacion" : '+'"'+clas+'"}';
    var obj_data = JSON.parse(json_text);
    console.log(obj_data)
    $.ajax({
      data: obj_data,
      type: 'POST',
      url: '/clasificacion',
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

  $('#btn_inicio_cl').click(function() {
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

  $('#btn_carga_cls').click(function() {
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

});
