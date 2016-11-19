<?php

function readFromFile($fileName){
  $str = file_get_contents($fileName);
  $str =  json_decode($str, true);
  return $str;
}

  function square($carry, $item){
      $carry += $item*$item;
      return $carry;
  }

  function lengthNormalize($tfidf, $size){
      $array = $tfidf;
      $normalizingVarArray = array();
      $contador = 0;

      while ($contador++ <= $size) {
          $col = array_column($array, $contador);
          $normalizingVarArray[$contador] = array_reduce($col, "square");
      }
      //divide each tf-idf with each normalized vector result
      foreach ($array as $subArray){
          foreach ($subArray as $key => $value) {
                  $subArray[$key] =$subArray[$key]/$normalizingVarArray[$key];
          }
      }
      return $array;
  }

  //Recieves an array of already stemmed words (query), returns all the documents
  //where the query is mentioned.
  function getDocArray($postings, $termArray){
      $docArray = array();
      foreach ($termArray as $term) {
          $docArray = array_merge($docArray, array_keys($postings[$term])) ;
      }
      return  array_unique($docArray);
  }
  
function createVectorSpace($postings, $termArray){
    

    $vectorSpace = array();

    foreach ($termArray as $term ) {
        $row = array();// array_fill(1, $collectionSize, 0);
        foreach ( $postings[ $term ] as $v => $i ) {
            //
            $row[$v] = $i[weight]*$i[idf];
            //echo $v;
            
        }

        $vectorSpace[$term] = $row;
    }
    return $vectorSpace;
}
           

  function processQuery($termArray){
      $postings = readFromFile('postingsWgts.json'); //complete posting list, read from the file.
      $urls = readFromFile('urls.json');
      $docArray = getDocArray($postings, $termArray); //list of documents regarding the query
      $resultMatrix = createVectorSpace($postings, $termArray);
      $resultMatrix = lengthNormalize($resultMatrix, sizeof($urls));

      $query = array_count_values($termArray);
      $normalizeValue = 0;
      foreach ($query as $key => $value) {
          $idf = log10(sizeof($urls)/sizeof($postings[$key]));
          $query[$key] = (1+log10($value))*$idf;
          $normalizeValue = $normalizeValue + pow($query[$key], 2);
      }
      $normalizeValue = sqrt($normalizeValue);
      foreach ($query as $key => $value) {
          $query[$key] = $query[$key]/$normalizeValue;
      }
      $resultArray = array_fill_keys(array_values($docArray), 0);

       foreach ($resultMatrix as $k1 => $subArray) {
           if (in_array($k1,$termArray)) {
               foreach ($subArray as $k2 => $value) {
                   $resultArray[$k2] +=  $query[$k1]*$value;
               }

           }
      }
       arsort($resultArray);
       $finalResults = array();
      $counter = 1;
       foreach ($resultArray as $key => $value) {
                if ($value == 0){
                    if ( $counter == 1) {
                        $finalResults[$counter] = "<li class=' '  style='display: list-item;'><h3>No results to show :(</h3><p  class='flow-text'> <a href='https://wiki.archlinux.org/' target='_blank'>Take a look!</a></p></li>";
                        $counter++;
                    }
                    break;
                }
            $finalResults[$counter] = "<li class=' '  style='display: list-item;'><h3>"."Result ".$counter."</h3><p  class='flow-text'> <a href='".$urls[$key]."' target='_blank'>".$urls[$key]."</a></p></li>";
            $counter++;
       }
      return $finalResults;
  }
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
    $return = array();

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
    $suggested =" ";
    if ( $suggestions == true )  {
        foreach ( $word as $w ) {
            $suggested .= $w." ";
        }
    }
    $return[0] = $suggested;
    echo json_encode(array_merge($return, processQuery(explode(" ", $message))),JSON_FORCE_OBJECT);
    // echo json_encode($return);
    exit; // to make sure you arn't getting nothing else

} else {
    // so you can access the error message in jQuery
    echo json_encode(array('errror' => TRUE, 'message' => 'a problem occured'));
    exit;
}


?>
