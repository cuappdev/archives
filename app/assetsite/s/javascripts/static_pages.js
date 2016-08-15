$(document).ready(function () {

	// Conditionally add a bolding to links of page we're currently on 
	var pageURL = window.location.href; 
	$('a').each(function () { if (this.href == pageURL) { $(this).addClass('bold'); }	}); 


	// To animate in appropriate parts of the page 
	$(function() {
		// Scrollex for all "fadein" divs 
	  $(".fadein").scrollex({ top: '-10%', bottom: '-10%',
	  	enter: function () {
	  		$(this).removeClass("fadein", 1000, "easeInOutQuad"); 
	  	}
		}); 
	});

	$('.mailing-form').submit(false);

	// AJAX request for adding email 
	$(".submit-email").on("click", function () {
		var data = { "email" : $(".email-field").val().trim() } 
		$.ajax({
			type: "POST", 
			url: "/home",
			data: data, 
			dataType: "JSON",
		}).success(function (json) {
			// If error 
			if (!json.success) {
				$(".email-result").html(json.data.error); 
			} else {
				$(".email-field").val(''); 
				$(".email-result").html("Thanks for signing up for our mailing list!  We'll keep you in the loop.");
			}
			
		}); 
		return false; 

	}); 


	





}); 
