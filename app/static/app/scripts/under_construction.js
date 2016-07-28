$(document).ready(function(){
    $('#developer-images').hide();
    $('#under-construction').mouseenter(function(){
      $('#under-construction').hide();
      $('#developer-images').show();
    });

    $('#under-construction').mouseleave(function(){
      $('#under-construction').show();
      $('#developer-images').hide();
    });
});