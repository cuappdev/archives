$(document).ready(function () {

  // Conditionally add a bolding to links of page we're currently on
  var pageURL = window.location.href;
  $('a').each(function () { if (this.href == pageURL) { $(this).addClass('active-page'); }  });

  var scroll_start = 0;
  var startchange = $('.navbar-change');
  var offset = startchange.offset();
  var navbar_height = $(".pages-navbar").height();

  $(".nav-element").addClass('white-nav-element');
  $(".icon-bar").css('background-color', 'white');

  if (startchange.length){
    $(document).scroll(function() {
      navbar_height = $(".navbar-default").height();
      scroll_start = $(this).scrollTop() + navbar_height;
      if(scroll_start > offset.top) {
        $(".pages-navbar").css('background-color', 'white');
        $(".pages-navbar").addClass('navbar-shadow');
        $(".nav-element").removeClass('white-nav-element');
        $(".nav-element").css('color', '#B9B9B9');
        $(".icon-bar").css('background-color', 'rgb(66, 66, 66)');
      } else {
        $(".pages-navbar").css('background-color', 'transparent');
        $(".pages-navbar").removeClass('navbar-shadow');
        $(".nav-element").addClass('white-nav-element');
        $(".icon-bar").css('background-color', 'white');
      }
    });
  }

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
