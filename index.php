<?php
	
	$ll = isset($_GET['ll']) ? stripslashes($_GET['ll']) : '';
	$name = isset($_GET['n']) ? stripslashes($_GET['n']) : '';
	$desc = isset($_GET['d']) ? stripslashes($_GET['d']) : '';
	$icon = isset($_GET['i']) ? stripslashes($_GET['i']) : 'https://goo.gl/59ScNx';

	if(!$ll) {
		header('HTTP\1.1 400 Bad Request');	
		header('Content-Type: text/plain');
		die('Latitude and longitude empty');
	}

	
	$ll = explode(',',$ll);
	$ll = $ll[1].','.$ll[0];
	
	$desc = preg_replace('/\r\n/',"\n",$desc);
	$desc = preg_replace('/\r/',"\n",$desc);
	$desc = preg_replace('/\n/',"<br />",$desc);
	$desc = preg_replace('/(\s|^|>)(([a-z,A-Z,0-9]+\.)+[a-z,A-Z,0-9]+)(\s|<|$)/',"$1<a href=\"http://$2\">$2</a>$4",$desc);
	$desc = preg_replace('/(\s|^|>)(http\:\/\/[^\s<]+)(\s|<|$)/',"$1<a href=\"$2\">$2</a>$3",$desc);
	$desc = preg_replace('/(\s|^|>)(https\:\/\/[^\s<]+)(\s|<|$)/',"$1<a href=\"$2\">$2</a>$3",$desc);
	$desc = preg_replace('/(\s|^|>)([^\/>\@\s]+\@([^\.\s\<]+\.)+\w+)(\s|<|$)/',"$1<a href=\"mailto:$2\">$2</a>$4",$desc);
	
	//header('Content-Type: application/vnd.google-earth.kml+xml');
	header('Content-Type: text/plain');
	print '<?xml version="1.0" encoding="UTF-8"?>'."\n";
	
?><kml xmlns="http://www.google.com/earth/kml/2">
	<Document>
	<name>dinamickml.kml</name>
	<Style id="iconStyle">
      <IconStyle>
        <Icon>
          <href><?php print $icon; ?></href>
        </Icon>
        <hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction" />
      </IconStyle>
    </Style>
  <Placemark>
    <?php if($name) print "<name>".htmlentities($name)."</name>\n"; ?>
    <?php if($desc) print "<description><![CDATA[
    	<br />$desc
    ]]></description>\n"; ?>
    <styleUrl>#iconStyle</styleUrl>
    <Point>
      <coordinates><?php print $ll; ?></coordinates>
    </Point>
  </Placemark>
  </Document>
</kml>
