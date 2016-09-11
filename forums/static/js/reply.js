$(document).ready(function(){
    $("form").submit(function(event){

        var csrftoken=Cookies.get('csrftoken');
        var content=$('textarea[name=content]').val();
        var subscribe="no";

        if($('input:checkbox[name=subscribe]:checked').val()){
            subscribe="yes";
        }
        var thread_id=$('#thread-id').attr('data-id');
        
        console.log(content);
        console.log(subscribe);
        console.log(thread_id);

        var request=$.ajax({
            
            url: '/forum/reply/',
            method: 'POST',
            data: {content: content,
                subscribe: subscribe,
                thread_id: thread_id,
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
            if (msg==="no_content"){
                alert("You can not submit an empty reply");
            }
            else if (msg==="no_perm"){
                alert("You do not have permission to post a reply");
            }
            else if (msg==="closed"){
                alert("This thread is already closed");
            }
            else if (msg==="method_not_allowed"){
                alert("This method is not allowed");
            }
            else{
                $('.post-div').last().after(msg);
            }
        });
    
        request.fail(function(jqXHR, textStatus){
           alert("Request failed: "+ textStatus);
        });

        $(this).trigger("reset");
        location.reload(false);
        event.preventDefault();
    });

});