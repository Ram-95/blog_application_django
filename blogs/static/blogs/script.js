$(document).ready(function () {
    window.setTimeout(function () {
        $(".alert").fadeTo(500, 0).slideUp(500, function () {
            $(this).remove();
        });
    }, 5000);

    /* Functionality to Like and Unlike a button */ 
    $(document).on("click", ".like_post", function () {
        //alert('Like button clicked');
        // Getting the POST_ID from the like button clicked
        post_id = $(this).closest('article').attr('id');
        alert('Post Liked: ' + post_id);
    });
});