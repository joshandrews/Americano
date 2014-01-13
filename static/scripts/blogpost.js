function scrollBanner() {
    //Get the scoll position of the page
    scrollPos = jQuery(this).scrollTop();
    console.log(scrollPos);
    //Scroll and fade out the banner text
    if ($(window).width() >= 640) {
        jQuery('#title').css({
          'margin-top' : -(.8+scrollPos/3)+"em",
          'opacity' : 1-(scrollPos/300)
        });
        jQuery('.arrow').css({
          'opacity' : 1-(scrollPos/500)
        });

        //Scroll the background of the banner
        jQuery('#hero').css({
          'background-position' : 'center ' + (-scrollPos/4)+"px"
        });
    }
  }

$(document).ready(function(){
    jQuery(window).scroll(function() {
	       scrollBanner();
	});
});