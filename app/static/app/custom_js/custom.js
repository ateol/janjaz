
$(document).ready(function(){

/* Here is the javascript for the search button to display the search results */
    $('#s-btn').click(
        function() {
            $('.s_result').removeClass().addClass('.sr-column');
            $('.see').removeClass().addClass('.visible');
        }),

/* javascript ends here */

    $('.page-scroll').hover(

        function() {
        $(this).children('.dropdown-menu').slideDown(400, stop());
    },
        function(){
            $(this).children('.dropdown-menu').slideUp(400, stop());
        }
    );

    function stop() {
        $('.dropdown-menu').stop(true, true);
    }

    /* University page javascript */

    $('#s2-btn').click(

        function() {
            $('.unsee').removeClass().addClass('.visible');
        }
    );

    /* end of university page javascript */
});