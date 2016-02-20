$(document).ready(function() {
	var availableTutorials = [
               "Andy",
               "Andrew",
               "Bob",
               "Bobby",
               "Chuck",
               "Charles",
               "David",
               "Bobby", 
            ];
            $( "#automplete-1" ).autocomplete({
               source: availableTutorials
            });
});