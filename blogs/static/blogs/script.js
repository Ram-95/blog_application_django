$(document).ready(function () {
    window.setTimeout(function () {
        $(".alert").fadeTo(500, 0).slideUp(500, function () {
            $(this).remove();
        });
    }, 5000);


    /* Function to change DOM for Follow/Unfollow */
    $('.follow').on('click', function () {
        username = $('.username_field').text();
        var current_obj = $(this)
        //alert(current_obj);
        $.ajax({
            type: 'POST',
            url: '/follow/',
            data: {
                username: username,
            },
            success: function (data) {
                if (data.status == 'success') {
                    alert('Success');
                    current_obj.removeClass('follow-btn');
                    var following_code = '<i class="fas fa-check-circle"></i>&nbsp;Following';
                    current_obj.addClass('following-btn');
                    current_obj.html(following_code);
                }
            }
        });
        /*
        if ($(this).hasClass('follow-btn')) {
            $(this).removeClass('follow-btn');
            var following_code = '<i class="fas fa-check-circle"></i>&nbsp;Following';
            $(this).addClass('following-btn');
            $(this).html(following_code);
        }
        else if ($(this).hasClass('following-btn')) {
            $(this).removeClass('following-btn');
            var follow_code = '<i class="fas fa-plus"></i>&nbsp;Follow';
            $(this).addClass('follow-btn');
            $(this).html(follow_code);
        }*/
    });


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
                    $('#upvote_' + post_id).css('color', '#8bf178');
                    $('#downvote_' + post_id).css('color', '');
                }
                else {
                    if (data.status == 'Invalid') {
                        alert('You cannot vote on your own post!');
                    }
                }
            }
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
                    $('#downvote_' + post_id).css('color', 'red');
                    $('#upvote_' + post_id).css('color', '');
                }
                else {
                    if (data.status == 'Invalid') {
                        alert('You cannot vote on your own post!');
                    }
                }
            }
        });
    });


    function refresh_comments(post_id) {
        $.ajax({
            type: 'GET',
            url: '/refresh_comments/',
            data: {
                post_id: post_id,
            },
            success: function (data) {
                no_of_comments = data.no_of_comments;
                if (no_of_comments == 0) {
                    $('.comments').text('No comments yet.');
                }
                else if (no_of_comments == 1) {
                    $('.comments').text(no_of_comments + ' Comment');
                }
                else {
                    $('.comments').text(no_of_comments + ' Comments');
                }
                //alert('Comments Updated.');
            }
        });
    }

    /* Script to delete a comment  */
    $(document).on("click", ".delete_comment", function () {
        var result = confirm("Are you sure you want to delete your comment?");
        if (result) {
            comment_id = $(this).closest("li").attr("id");
            post_id = $("article").attr("id");
            //alert('Post: '+ post_id);
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
                    refresh_comments(post_id);
                }
            });
        }
    });

    $(function () {

        // variable to store the comment text
        var comment;
        /* Function to get the comment ID and the comment text when 'edit' comment is clicked */
        $(document).on("click", ".edit_comment", function () {
            comment_id = $(this).closest("li").attr("id");
            comment = $("#" + comment_id).find("p").text().trim();
            $('.edit_delete').hide();
            //alert(comment);
            $("#" + comment_id).find('.comment_p').html("<textarea class='form-control mb-2 comment_edit_text'>" + comment + "</textarea><a href='#' class='save_edit_btn mr-3'>Save</a><a href='#' class='cancel_edit_btn'>Cancel</a>");
        });

        /* Function to putback the comment when edit comment operation is cancelled. 'Cancel' button is clicked */
        $(document).on('click', '.cancel_edit_btn', function () {
            comment_id = $(this).closest("li").attr("id");
            $('.edit_delete').show();
            $("#" + comment_id).find('.comment_p').html('<p class="comment_text">' + comment + '</p>');
        });

    });


    /* Script that runs when comment is edited */
    $(document).on("click", ".save_edit_btn", function () {
        comment_id = $(this).closest("li").attr("id");
        edit_comment = $('.comment_edit_text').val();
        //alert('ID: ' + comment_id + ' Text: ' + edit_comment);
        $.ajax({
            type: 'POST',
            url: '/edit_comment/',
            cache: false,
            data: {
                comment_id: comment_id,
                edit_comment: edit_comment,
            },
            success: function () {
                //alert('success');
                $('.edit_delete').show();
                $("#" + comment_id).find('.comment_p').html('<p class="comment_text">' + edit_comment + '</p>');
            }
        });
    });
});