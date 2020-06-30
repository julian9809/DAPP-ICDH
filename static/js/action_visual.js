$(document).ready(function() {

  $('#next_image').click(function() {
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

  $('#btn_visualizar').click(function() {
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

});
