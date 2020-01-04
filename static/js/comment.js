function do_reply(comment_id, to_user_name, to_user_name, discussion_id){
    $('#comment_id').val(comment_id);
    $('#to_user_id').val(to_user_id);
    $('#reply_content').attr('placeholder', '回复 ' + to_user_name + ' :');

    if (discussion_id == '-1'){
        $('#reply_form').appendTo($('#comment_reply_' + comment_id));
    } else {
        $('#reply_form').appendTo($('#discussion_reply_' + discussion_id));
    }

    $('#reply_form').show();    
}

function cancel_reply(){
    $('#reply_form').hide();
    $('#reply_content').val('');
}

