$(document).ready(function(){
   $('#liket').click(function(){
       $.ajax({
           type:"POST",
           url: '/like/',
           data: {
               'post_id':$(this).attr('name')
           },
           success:like_sucess,
           datatype:'html'
       });
   });
});

function lke_sucess(data, textStatus, jqXHR)
{
    ("#like_count").html(data);
}