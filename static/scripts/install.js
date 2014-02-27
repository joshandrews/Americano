
$( document ).ready(function() {
	var step = parseInt(document.getElementById('step').innerHTML);
    $('#step-'+step).show();
    $('.install-form').bind('submit',function(e){
        e.preventDefault();
        $.ajax({
            type     : "POST",
            cache    : false,
            url      : $(this).attr('action'),
            data     : $(this).serialize(),
            success  : function(data) {
                $('.install-form').hide();
                step = step + 1;
                $('#step-'+step).show();
            },
            error    : function(data) {
                if (step == 1) {
                    $(".mysql").css({"-webkit-box-shadow":"0px 0px 2px 0px #893027",
                                     "-moz-box-shadow":"0px 0px 2px 0px #893027",
                                     "box-shadow":"0px 0px 2px 0px #893027",
                                     "border":"1px solid #893027"})
                }
            }
        });
    });
});