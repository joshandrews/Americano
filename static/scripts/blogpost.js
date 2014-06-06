function scrollBanner() {
    //Get the scoll position of the page
    var scrollPos = jQuery(this).scrollTop();
    var height = jQuery(window).height();
    //Scroll and fade out the banner text
    if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || $(window).width() < 640) {
    }
    else {
        if (height-scrollPos > 0  && scrollPos >= 0) {
            jQuery('#title').css({
              '-webkit-transform' : 'translate3d(0px, '+ scrollPos/3 +'px, 0px)',
              '-ms-transform': 'translate3d(0px, '+ scrollPos/3 +'px, 0px)',
              'transform':  'translate3d(0px, '+ scrollPos/3 +'px, 0px)',
              'opacity' : 1-(scrollPos/500)
            });
            jQuery('.arrow').css({
              'opacity' : 1-(scrollPos/500)
            });
            //Scroll the background of the banner
            jQuery('#hero').css({
              'background-position' : 'center ' + (-scrollPos/2)+"px"
            });
        }
    }
  }

$(document).ready(function(){
    jQuery(window).scroll(function() {
	       scrollBanner();
	});
});