$(document).ready(function () {
    window.setTimeout(function () {
        $(".alert").fadeTo(500, 0).slideUp(500, function () {
            $(this).remove();
        });
    }, 5000);

    /* Function to send upvote data to server */
    $(document).on("click", ".vote_up", function () {
        post_id = $(this).closest('article').attr('id');
        likes = $("#" + post_id).find("#votes_count").text()
        //alert('Post Liked: ' + post_id);
        $.ajax({
            type: 'POST',
            url: '/vote_up/',
            cache: false,
            data: {
                post_id: post_id,
            },
            success: function (data) {
                likes++;
                $("#" + post_id).find("#votes_count").text(likes);
                //console.log('Upvote Success ' + likes);
            }
        });
    });
});

/* Function to send Downvote data to server */
$(document).on("click", ".vote_down", function () {
    post_id = $(this).closest('article').attr('id');
    likes = $("#" + post_id).find("#votes_count").text()
    //alert('Post Liked: ' + post_id);
    $.ajax({
        type: 'POST',
        url: '/vote_down/',
        cache: false,
        data: {
            post_id: post_id,
        },
        success: function (data) {
            likes--;
            $("#" + post_id).find("#votes_count").text(likes);
            //console.log('Downvote Success ' + likes);
        }
    });
});
