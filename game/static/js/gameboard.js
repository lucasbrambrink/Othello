token = document.getElementsByName('csrfmiddlewaretoken')[0].value
board = []
color = 'W'


$(document).ready(function(){

function buildBoard(board) {
    $('.board').empty();
    for(var i = 0; i < board.length; i++){
        var row = "<div class='row' id='row-"+ i +"'></div>"
        $('.board').append(row)
        for(var j = 0; j < board[0].length; j++){
            var cell = "<div class='cell col-md-1' id='row-" + i + ",col-"+ j +"'>"
            if(board[i][j] == "W" || board[i][j] == "B"){
                var piece = "<div class='piece " + board[i][j] + "'></div>"
                cell += piece
            }
            $('#row-'+i).append(cell+'</div>')        
        }
    }
};

    $.ajax({
            url: 'game/board/',
            type: "GET",
            success: function (data) {
                board = data['board']
                buildBoard(board)
            },
            error: function (xhr, errmsg, err) {
                alert("error");
            }
        },'json');




    console.log(token)
    $('.board').on('click','.cell', function(){
        var id = $(this).attr('id').split(',');
        var row = id[0].split('-')[1];
        var col = id[1].split('-')[1];

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
                        $('.alerts').empty();
                        $('.alerts').append("<h1 id='illegal'>"+data['e']+"</h1>")
                        $('#illegal').delay(800).fadeOut(400);
                    }
                    if (data['first_board']) {
                        buildBoard(data['first_board'])
                        setTimeout(function() { buildBoard(data['board']); board = data['board']; }, 1500 );
                    } else if (data['board']) {
                        board = data['board']
                        buildBoard(data['board'])
                    }
                    if (data['g']) {
                        alert(data['g'])
                    }
                },
                error: function (xhr, errmsg, err) {
                    alert("error");
                }
            },'json');
    });
});

