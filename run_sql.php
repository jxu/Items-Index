<?php
$item_name = $_POST['item_name'];
echo $item_name, "\n";

class MyDB extends SQLite3
{
	function __construct()
	{
		$this->open('data/ah.db');
	}
}
$db = new MyDB();
if (!$db)
	echo $db->lastErrorMsg();
else
	echo "Database loaded\n";
	
$statement = $db->prepare('SELECT * FROM listing WHERE item_name=:item_name');
$statement->bindValue(':item_name', $item_name);
$results = $statement->execute();

while($row = $results->fetchArray())
{
	var_dump($row);
}
		
?>