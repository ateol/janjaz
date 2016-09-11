$(document).ready(function(){
    $("#like-button").click(function(){
        var csrftoken=Cookies.get('csrftoken');
        console.log(csrftoken)
        var event_id=$("#like-button").attr('name');
        var request=$.ajax({
            url: '/likes/',
            method: 'POST',
            data: {event_id: event_id,
                csrftoken:csrftoken
            },
            datatype: 'html',

            beforeSend: function(xhr, settings) {
                 if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                     // Only send the token to relative URLs i.e. locally.
                     xhr.setRequestHeader("X-CSRFToken", csrftoken);
                 }
             }
        });
    
        request.done(function(msg){
            var color=$("#likes").attr('class');
            $("#like-circle").css('color', color);
            $("#like-div").html(msg);
        });
    
        request.fail(function(jqXHR, textStatus){
           alert("Request failed: "+ textStatus);
        });
    });
});