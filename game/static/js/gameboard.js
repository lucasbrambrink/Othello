token = document.getElementsByName('csrfmiddlewaretoken')[0].value
board = []
color = 'W'


$(document).ready(function(){

    $('.alerts').hide();

function buildBoard(board,moves) {
    $('.board').empty();
    for(var i = 0; i < board.length; i++){
        var row = "<div class='row' id='row-"+ i +"'></div>"
        $('.board').append(row)
        for(var j = 0; j < board[0].length; j++){
            var cell = "<div class='cell col-md-1' id='row-" + i + ",col-"+ j +"'>"
            for(var k = 0; k < moves.length; k++){
                if(moves[k]['cell'][0] == i && moves[k]['cell'][1] == j){
                    var marker = "<div class='possible'></div>"
                    cell += marker
                }
            }
            if(board[i][j] == "W" || board[i][j] == "B"){
                var piece = "<div class='piece " + board[i][j] + "'></div>"
                cell += piece
            }
            $('#row-'+i).append(cell+'</div>')        
        }
    }

    var white = 0
    var black = 0
    for(var i = 0; i < board.length; i++){
        for(var j = 0; j < board.length; j++){
            if(board[i][j] == 'W'){ white += 1 }
            else if (board[i][j] == 'B'){ black += 1 }
        }
    }
    if(black > white){
        var styles = ['#FF4D4D','#99E699']
    } else if (white > black) {
        var styles = ['#99E699','#FF4D4D']
    } else {
        var styles = ['#80B2FF','#80B2FF']
    }

    $('#score_white').empty()
        .append("<td style='width:10em;'><h2>Blue</h2></td><td style='width:5em;'><h2><strong>"+white+"</strong></h2></td>")
        .css('background-color',styles[0])
    $('#score_black').empty()
        .append("<td style='width:10em;'><h2>Black</h2></td><td style='width:5em;'><h2><strong>"+black+"</strong></h2></td>")
        .css('background-color',styles[1])
};

    $.ajax({
            url: 'game/board/',
            type: "GET",
            success: function (data) {
                board = data['board']
                buildBoard(board,[])
            },
            error: function (xhr, errmsg, err) {
                alert("error");
            }
        },'json');

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
                        $('.alerts').show().delay(800).fadeOut(400);
                    }
                    if (data['first_board']) {
                        buildBoard(data['first_board'],[])
                        setTimeout(function() { buildBoard(data['board'],[]); board = data['board']; }, 1000 );
                    } else if (data['board']) {
                        board = data['board']
                        buildBoard(data['board'],[])
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

    $('#highlight_moves').on('click', function(){
        var link = "/game/find-moves/";

        $.ajax({
                url: link,
                type: "POST",
                data: {
                    csrfmiddlewaretoken: token,
                    board: JSON.stringify(board)
                },
                success: function (data) {
                    if (data['moves']){
                        buildBoard(data['board'],data['moves'])
                        $('.possible').delay(400).fadeOut(800).empty()
                        }
                },
                error: function (xhr, errmsg, err) {
                    alert("error");
                }
            },'json');
    })
});

