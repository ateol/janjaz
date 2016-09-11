$(document).ready(function(){
    $("form").submit(function(event){

        var csrftoken=Cookies.get('csrftoken');
        var search=$("input[name=search]").val();
        var category="no";
        var forum="no";
        var post="no";

        if($("input:checkbox[name=category]:checked").val()){
            category='yes';
        }

        if($("input:checked[name=forum]:checked").val()){
            forum="yes";
        }

        if($("input:checked[name=post]:checked").val()){
            post="yes";
        }

        console.log(search);
        console.log(category);
        console.log(forum);
        console.log(post);


        var request=$.ajax({

            url: '/forum/ajax-search/',
            method: 'POST',
            data: {
                search: search,
                post: post,
                forum: forum,
                category: category,
                csrftoken: csrftoken
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
            if(msg==="method_not_allowed"){
                alert("This message is not allowed");
            }

            else if(msg==="must_select"){
                alert("You must select what to search in the forums");
            }

            else if(msg==="must_enter_search_term"){
                alert("You must enter a search term");
            }
            else{
                $("#search-results").html(msg);
            }
        });

        request.fail(function(jqXHR, textStatus){
           alert("Request failed: "+ textStatus);
        });

        $(this).trigger("reset");
        event.preventDefault();
    });

});