function fetchAndGraph() {
	var item_name = $("#selectItem option:selected").text();
	
	$.ajax({
		type: "POST",
		url: "run_sql.php",
		data: {item_name: item_name},
	})
	.done(function(response){
		//console.log("response");
		//console.log(response);
		num_array = JSON.parse(response);

		// Convert array of objects to array of arrays
		for (var i=0; i < num_array.length; i++){
			num_array[i] = $.map(num_array[i], function(el) {return el;});
			num_array[i][0] = new Date(num_array[i][0]*1000);
		}
		//console.log(num_array);

		g = new Dygraph(document.getElementById("graphdiv"),
						num_array,
						{
							labels: ["Datetime", item_name],
							labelsSeperateLines: true,
							title: "Items Price Over Time",
							xlabel: "Time and date",
							ylabel: "Price per unit",
							maxNumberWidth: 9
						});		
	});
}

