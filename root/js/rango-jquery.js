$(document).ready( function() {
    $("#id_choice_field_0").prop("checked", true)
	$("#id_category_title").hide();
	$('label[for="id_category_title"]').hide();
	$("#id_subcategory_title").hide();
	$('label[for="id_subcategory_title"]').hide();
	
	$("#id_choice_field_0").click( function(event) {
        //alert("You clicked the button using JQuery!");
		$("#id_category_title").hide();
		$('label[for="id_category_title"]').hide();
		$("#id_subcategory_title").hide();
		$('label[for="id_subcategory_title"]').hide();
    });
	
	$("#id_choice_field_1").click( function(event) {
        //alert("You clicked the button using JQuery!");
		$("#id_category_title").show();
		$('label[for="id_category_title"]').show();
		$("#id_subcategory_title").hide();
		$('label[for="id_subcategory_title"]').hide();
    });
	
	$("#id_choice_field_2").click( function(event) {
        //alert("You clicked the button using JQuery!");
		$("#id_category_title").hide();
		$('label[for="id_category_title"]').hide();
		$("#id_subcategory_title").show();
		$('label[for="id_subcategory_title"]').show();
    });
	
   if (document.AddEventForm.alert.value==1){
		swal("¡Bien hecho!", "El registro fue exitoso.", "success")
	}

});