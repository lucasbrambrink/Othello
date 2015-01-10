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
                        board = data['board']
                        for(var i = 0; i < board.length; i++){
                            for(var j = 0; j < board[0].length; j++){
                                if(board[i][j] == "W"){
                                    // DOM change
                                } else if(board[i][j] == "B"){
                                    // DOM
                                } else {
                                    continue
                                }
                            }
                        }
                    }

                },
                error: function (xhr, errmsg, err) {
                    alert("error");
                }
            },'json');
    });
});

