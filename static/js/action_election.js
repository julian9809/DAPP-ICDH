$(document).ready(function() {

  $('#next_image_election').click(function() {
    $.ajax({
      type: 'POST',
      url: '/visualizar_eleccion',
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