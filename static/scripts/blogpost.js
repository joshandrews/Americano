function scrollBanner() {
    //Get the scoll position of the page
    var scrollPos = jQuery(this).scrollTop();
    var height = jQuery(window).height();
    //Scroll and fade out the banner text
    if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || $(window).width() < 1024) {
        jQuery('#title').css({
          '-webkit-transform' : 'translate3d(0px, '+ 0 +'px, 0px)',
          '-ms-transform': 'translate3d(0px, '+ 0 +'px, 0px)',
          'transform':  'translate3d(0px, '+ 0 +'px, 0px)',
          'opacity' : 1
        });
        jQuery('.arrow').css({
          'opacity' : 1
        });
        //Scroll the background of the banner
        jQuery('#hero').css({
          'opacity' : 0.8
        });
    }
    else {
        if (height-scrollPos > 0  && scrollPos >= 0) {
            jQuery('#title').css({
              '-webkit-transform' : 'translate3d(0px, '+ scrollPos/1.2 +'px, 0px)',
              '-ms-transform': 'translate3d(0px, '+ scrollPos/1.2 +'px, 0px)',
              'transform':  'translate3d(0px, '+ scrollPos/1.2 +'px, 0px)',
              'opacity' : 1-(Math.pow(scrollPos, 0.9)/500)
            });
            jQuery('.arrow').css({
              'opacity' : 1-(scrollPos/30)
            });
            //Scroll the background of the banner
            jQuery('#hero').css({
              'opacity' : 0.8-(Math.pow(scrollPos*2, 0.8)/500)
            });
        }
    }
  }

$(document).ready(function(){
    jQuery(window).scroll(function() {
	       scrollBanner();
	});
});