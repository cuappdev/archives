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

		// Scrollex for advertised features 
	  $('.features').scrollex({ top: '-20%', bottom: '-20%',
	    enter: function() {
    		$("li.one").animate({ "opacity" : 1 }, function () {
    			$("li.two").animate({ "opacity" : 1 }, function () {
    				$("li.three").animate({ "opacity" : 1 });
    			}); 
    		});  
	    }
	  });



	});


	





}); 
