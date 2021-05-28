$(document).ready( function() {
    $("#about-btn").click( function(event) {
        //alert("You clicked the button using JQuery!");
		$("#subcategory_title").hide();
    });
	
	
	$("#id_choice_field_0").click( function(event) {
        //alert("You clicked the button using JQuery!");
		$("#id_category_title").hide();
		$('label[for="id_category_title"]').hide();
		$("#id_subcategory_title").hide();
		$('label[for="id_subcategory_title"]').hide();
    });
});