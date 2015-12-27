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
	
$statement = $db->prepare('SELECT scrape_datetime,ppu FROM listing WHERE item_name=:item_name');
$statement->bindValue(':item_name', $item_name);
$results = $statement->execute();

while($row = $results->fetchArray(SQLITE3_ASSOC))
{
	ChromePHP::log($row);
}
?>