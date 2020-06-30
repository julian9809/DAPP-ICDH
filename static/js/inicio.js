$(document).ready(function() {
  $('#cargar_imagen_inicio').click(function() {
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

  $('#clasificar_imagen_inicio').click(function() {
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

  $('#visualizar_imagen_inicio').click(function() {
    $.ajax({
      type: 'POST',
      url: '/visualizar',
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

  $('a[href^="#"]').click(function() {
    var destino = $(this.hash); //this.hash lee el atributo href de este
    $('html, body').animate({ scrollTop: destino.offset().top }, 700); //Llega a su destino con el tiempo deseado
    return false;
  });

});
