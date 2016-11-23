
var resClosed = true;
$(document).ready(function () {

    $('.search').keyup(function(event){
        if(event.keyCode == 13){
            if ( ! srchTxt.value) return;

            $('.form').animate({ top: '-170px' });
            $('#asdf').animate({ top: '-170px' });
            $('.res li').fadeIn(1000);
            $('.overlay').addClass('dim2');
            
            $('#serp').html("Searching...")

            if ( resClosed ) {
                Materialize.toast('Press ESC to close results', 2000, 'gray') // 4000 is the duration of the toast
                resClosed = false;
            }

            var t0 = performance.now();
            $.ajax({
                type: "POST",
                url: "spell.php",
                data: {msg:srchTxt.value},
                success: function(result){
                    //from AJAX string to JSON object.
                    var res = JSON.parse(result);
                    if (res) {//if there's a result, then:
                        var html ="";
                        if (res[0] !== " ") { //if there's a spell suggestion, then tell me.
                            $('#aspell').html("Maybe you meant "+"<a href='asdf'>"+res[0]+"</a>");
                        }
                        //shows first 15 results, adaptable to the user needs.
                        for (var i = 1; i < Object.keys(res).length; i++) {
                            html += res[i]; //retrieve each result
                        }
                        $('#serp').html(html);//finally, show the complete list of retrieved results.
                    }//Done this way to overwrite html from previous querys.
                    else {
                        $('#aspell').html("");
                        $('#serp').html("");
                    }
                }
            });
            var t1 = performance.now();

        }
    })
    ;

    // JS blur is the opposite of focus
    $('.search').blur(function(){
        // $('.overlay').removeClass('dim');
        // $('.overlay').removeClass('dim2');
    })

});

function clear() {
    alert('clear');
    srchTxt.clear();
}

$(document).keyup(function(e) {
//   if (e.keyCode === 13) $('.save').click();     // enter
    // ESC
    if (e.keyCode === 27) {
        $('.form').animate({ top: '0px' });
        $('#asdf').animate({ top: '0px' });
        $('.res li').hide();
        $('.overlay').removeClass('dim');
        $('.overlay').removeClass('dim2');
        $('#aspell').html("");
        $('#serp').html("");

        resClosed = true;
  }
});
// ssdsdjhgf
function btnSearch() {

    if ( ! srchTxt.value) return;

    $('.form').animate({ top: '-170px' });
    $('#asdf').animate({ top: '-170px' });
    $('.res li').fadeIn(1000);
    $('.overlay').addClass('dim2');

    $.ajax({
        type: "POST",
        url: "spell.php",
        data: {msg:srchTxt.value},
        success: function(result){
            // alert(result);
            if (result) {
                $('#aspell').html("Maybe you meant "+"<a href='asdf'>"+result+"</a>");
            }
            else {$('#aspell').html("");}
        }
    });
}
