<?php
include 'ChromePhp.php';

$item_name = $_POST['item_name'];
ChromePhp::log($item_name);

class MyDB extends SQLite3
{
	function __construct()
	{
		$this->open('data/ah.db');
	}
}
$db = new MyDB();
if (!$db)
	ChromePHP::log($db->lastErrorMsg());
else
	ChromePHP::log("Database loaded\n");
	
$statement = $db->prepare('SELECT scrape_datetime,min(ppu) 
						   FROM listing 
						   WHERE item_name=:item_name 
						   GROUP BY scrape_datetime');
$statement->bindValue(':item_name', $item_name);
$results = $statement->execute();

$php_array = array();
while($row = $results->fetchArray(SQLITE3_ASSOC)) // How it's indexed actually doesn't matter
{
	//ChromePHP::log($row);
	array_push($php_array, $row);
}

echo json_encode($php_array);
?>