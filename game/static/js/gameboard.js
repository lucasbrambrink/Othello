token = document.getElementsByName('csrfmiddlewaretoken')[0].value
board = []
color = 'W'

$(document).ready(function(){


    $.ajax({
            url: 'game/board/',
            type: "GET",
            success: function (data) {
                console.log(data['board'])
                board = data['board']

            },
            error: function (xhr, errmsg, err) {
                alert("error");
            }
        },'json');




    console.log(token)
    $('.cell').on('click', function(){
        var row = $(this).parent().attr('id').split('-')[1];
        var col = $(this).attr('id').split('-')[1];
        var link = "/game/place/";

        $.ajax({
                url: link,
                type: "POST",
                data: {
                    csrfmiddlewaretoken: token,
                    move: JSON.stringify([row,col,color]),
                    board: JSON.stringify(board)
                },
                success: function (data) {
                    if (data['e']) {
                        alert(data['e'])
                    }
                    else {
                        console.log(data['board'])
                        console.log('hello')
                    }

                },
                error: function (xhr, errmsg, err) {
                    alert("error");
                }
            },'json');
    });
});

