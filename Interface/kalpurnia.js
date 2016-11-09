        $(document).ready(function () {
            
            $('.search').keyup(function(event){
                if(event.keyCode == 13){
                    
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
            })
            ;
            
            $('.search').focus(function(){
                $('.overlay').addClass('dim');
            })
            
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
          }
        });