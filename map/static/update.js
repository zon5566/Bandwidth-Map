$(function() {
  $('#select_form select').on('change', function(e){
    $("#test").text($('#carrier_select').val());
  });
});