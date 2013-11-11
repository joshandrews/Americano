function scrollBanner() {
    //Get the scoll position of the page
    scrollPos = jQuery(this).scrollTop();
    console.log(scrollPos);
    //Scroll and fade out the banner text
    jQuery('#title').css({
      'margin-top' : -(.8+scrollPos/3)+"em",
      'opacity' : 1-(scrollPos/600)
    });

    //Scroll the background of the banner
    jQuery('#hero').css({
      'background-position' : 'center ' + (-scrollPos/4)+"px"
    });
  }

$(document).ready(function(){
    jQuery(window).scroll(function() {
	       scrollBanner();
	});
});