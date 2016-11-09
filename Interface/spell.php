<?php


# if you want to use other languajes, spanish for example:
#    sudo apt-get install aspell-es

$pspell_link = pspell_new("en");
// $pspell_link = pspell_new("es");


// http://stackoverflow.com/questions/1957808/how-can-i-install-pspell-in-php5-ubuntu

//should be using explode instead of implode
//$word = implode(" ", $message);

$nl  = '<br>';

if ($_POST) {
    $message = $_POST['msg'];
    
    // echo "msg: ".$message;
    
    $word = explode(" ", $message);
    // echo $message.$nl.$nl;
    // foreach($word as $k => $v) {
    //   if (pspell_check($pspell_link, $v)) {
    //       echo $v." spelled right".$nl;
    //   } else {
    //       echo $v." spelled wrong".$nl.$nl;
    //       print_r( pspell_suggest($pspell_link, $v) );
    //   };
    // };
    
    $suggestions = false;
    for ( $i=0; $i<count($word); $i++)  {
       if ( !pspell_check($pspell_link, $word[$i])) {
           
            $wsggtd = pspell_suggest($pspell_link, $word[$i])[0];
            if ( $wsggtd ) {
                $suggestions = true;
                $word[$i] = '<b>'.$wsggtd.'</b>';
           }
       }
        
    }
    
    if ( $suggestions == true )  {
        foreach ( $word as $w ) {
            echo $w." ";
        }
    }


    exit; // to make sure you arn't getting nothing else

} else {
    // so you can access the error message in jQuery
    echo json_encode(array('errror' => TRUE, 'message' => 'a problem occured'));
    exit;
}


?>
