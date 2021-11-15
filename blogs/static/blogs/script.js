$(document).ready(function () {
    window.setTimeout(function () {
        $(".alert").fadeTo(500, 0).slideUp(500, function () {
            $(this).hide();
        });
    }, 5000);


    /* Function to 'Follow' a User. */
    $('.follow-btn').on('click', function () {
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
                    //alert('Follow Success');
                    /*current_obj.removeClass('follow-btn');
                    var following_code = '<i class="fas fa-check-circle"></i>&nbsp;Following';
                    current_obj.addClass('following-btn');
                    current_obj.html(following_code);*/
                    location.reload();
                }
            }
        });
    });

    /* Function to 'Unfollow' a user. */
    $('.following-btn').on('click', function () {
        username = $('.username_field').text();
        //alert(username);
        $.ajax({
            type: 'POST',
            url: '/unfollow/',
            data: {
                username: username,
            },
            success: function (data) {
                if (data.status == 'success') {
                    //alert('Unfollow Success');
                    /*current_obj.removeClass('following-btn');
                    current_obj.addClass('follow-btn');
                    var follow_code = '<i class="fas fa-plus"></i>&nbsp;Follow';
                    current_obj.html(follow_code);*/
                    location.reload();
                }
            }
        });
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
                        alert('You cannot vote on your own post.');
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


    $(document).on("click", ".notification-list", function () {
        n_id = $(this).attr('id');
        //alert(n_id);
        $.ajax({
            type: 'POST',
            url: '/mark_notification_as_read/',
            cache: false,
            data: {
                n_post_id: n_id,
            },
            success: function () {
                //alert('Marked as Read.');
            }
        });
    });

    $('#noti_Button').click(function () {
        // TOGGLE (SHOW OR HIDE) NOTIFICATION WINDOW.
        $('#notifications').fadeToggle('fast', 'linear', function () {
            if ($('#notifications').is(':hidden')) {
            }
        });

        $('#noti_counter').fadeOut('slow');     // HIDE THE COUNTER.

        return false;
    });

    // HIDE NOTIFICATIONS WHEN CLICKED ANYWHERE ON THE PAGE.
    $(document).click(function () {
        $('#notifications').hide();
    });

    /*
    $('#notifications').click(function () {
        return false;       // DO NOTHING WHEN CONTAINER IS CLICKED.
    });*/

    $('.index_blog_full_description img').click(function () {
        $("#full-image").attr("src", $(this).attr("src"));
        $('#image-viewer').show();
    });


    $(".blog_image").click(function () {
        $("#full-image").attr("src", $(this).attr("src"));
        $('#image-viewer').show();
    });


    $("#image-viewer").on('click', function () {
        $('#image-viewer').hide();
    });

    $("#image-viewer .close").click(function () {
        $('#image-viewer').hide();
    });


    
    /* Search function */

    $("#txtSearch").keyup(function () {
        var val = $(this).val();
        //console.log(val);
        $.ajax({
            type: "GET",
            data: { 'uname': val },
            url: '/searchUser/',
            success: function (data) {
                //console.log(data);

                if (data.results.length > 0) {
                    $('#searchResults').empty();
                    for (var key in data) {
                        for (var val in data[key]) {
                            //console.log(val);
                            var htm = '<img class="rounded-circle round_profile_pics mr-2" src="' + data[key][val].profile_pic + '"></img>'
                            $('#searchResults').append(htm + "<a href='/profile/" + data[key][val].user + "'><h6>" + data[key][val].user + "</h6></a></li>");
                        }
                    }
                }
            },

        });
    });

});