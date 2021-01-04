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
                //alert(data.status);
                if (data.status == 'success') {
                    likes++;
                    $("#" + post_id).find("#votes_count").text(likes);
                    if (likes > 0) {
                        $('#upvote_' + post_id).css('color', 'green');
                    }
                    if (likes == 0) {
                        $("#upvote_" + post_id).css('color', '');
                        $("#downvote_" + post_id).css('color', '');
                    }
                }
                else {
                    if (data.status == 'Invalid') {
                        alert('You cannot vote on your own post!');
                    }
                }
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
            if (data.status == 'success') {
                likes--;
                $("#" + post_id).find("#votes_count").text(likes);
                if (likes < 0) {
                    $('#downvote_' + post_id).css('color', 'red');
                }
                if (likes == 0) {
                    $("#upvote_" + post_id).css('color', '');
                    $("#downvote_" + post_id).css('color', '');
                }
                //console.log('Downvote Success ' + likes);
            }
            else {
                if (data.status == 'Invalid') {
                    alert('You cannot vote on your own post!');
                }
            }
        }
    });
});

/* Script to delete a comment  */
$(document).on("click", ".delete_comment", function () {
    comment_id = $(this).closest("li").attr("id");
    //alert('Comment: '+ comment_id);
    $.ajax({
        type: 'POST',
        url: '/delete_comment/',
        cache: false,
        data: {
            comment_id: comment_id,
        },
        success: function () {
            //alert('Success');
            $("#" + comment_id).hide();
        }
    });
});

/* Script to edit a comment */
$(document).on("click", ".edit_comment", function () {
    comment_id = $(this).closest("li").attr("id");
    comment = $("#" + comment_id).find("p").text().trim();
    alert(comment);
    $("#" + comment_id).find('.comment_p').html("<textarea rows='2'>"+ comment +"</textarea>");
    //alert('Comment: '+ comment_id);
    /*$.ajax({
        type: 'POST',
        url: '/delete_comment/',
        cache: false,
        data: {
            comment_id: comment_id,
        },
        success: function () {
            alert('Success');
            $("#" + comment_id).hide();
        }
    });*/
});



