// New.js

$( document ).ready(function() {
	//https://github.com/daviferreira/medium-editor
	var editor = new MediumEditor('.editable');
    var prog;
    $('#publish').click(function () {
        var title = $('#title').html();
        title = title.replace(/<\/?[^>]+(>|$)/g, "");
        $('#title-input').val(title);
        var body = $('#body').html();
        $('#body-input').val(body);
        $('#published-input').val("1");
    });
    $('#draft').click(function () {
        var title = $('#title').html();
        title = title.replace(/<\/?[^>]+(>|$)/g, "");
        $('#title-input').val(title);
        var body = $('#body').html();
        $('#body-input').val(body);
        $('#published-input').val("0");
    });

    [].slice.call( document.querySelectorAll( 'button.progress-button' ) ).forEach( function( bttn ) {
        new ProgressButton( bttn, {
            callback : function( instance ) {
                var progress = 0,
                    interval = setInterval( function() {
                        instance._setProgress( prog/100 );

                        if( prog/100 === 1 ) {
                            instance._stop(1);
                            clearInterval( interval );
                        }
                    }, 200 );
            }
        } );
    } );

    $('#upload-submit').click( function(){
        var xhr = new XMLHttpRequest();

        if ( xhr.upload ) {
            xhr.upload.onprogress = function(e) {
                var done = e.position || e.loaded, total = e.totalSize || e.total;
                prog = Math.round(parseInt((done/total * 100)));
            };
        }

        xhr.open( 'POST', $('#image-upload').attr('action'), true );

        var form = $('#image-upload')[0];
        var fd = new FormData( form );
        xhr.send( fd );

    });

    $('#body').live('keyup',function () {
        var itemValue = document.getElementById('body').innerHTML;
        var postID = document.getElementById('post-id').innerHTML;
        var postPublished = document.getElementById('post-published').innerHTML;
        if (postPublished == 0) {
            $.ajax({
                     type: "POST",
                     url: "/blog/edit/live-save-body/"+postID+"/"+postPublished,
                     data: "textarea="+itemValue,
                     success: function(msg) {
                         $('#autosavenotify').text(msg);
                     }
             })
        }
     });
    $('#body').live('mousedown',function () {
        var itemValue = document.getElementById('body').innerHTML;
        var postID = document.getElementById('post-id').innerHTML;
        var postPublished = document.getElementById('post-published').innerHTML;
        if (postPublished == 0) {
            $.ajax({
                     type: "POST",
                     url: "/blog/edit/live-save-body/"+postID+"/"+postPublished,
                     data: "textarea="+itemValue,
                     success: function(msg) {
                         $('#autosavenotify').text(msg);
                     }
             })
        }
     });

    $('#title').live('keyup',function () {
        var itemValue = document.getElementById('title').innerHTML;
        var postID = document.getElementById('post-id').innerHTML;
        var postPublished = document.getElementById('post-published').innerHTML;
        if (postPublished == 0) {
            $.ajax({
                     type: "POST",
                     url: "/blog/edit/live-save-title/"+postID+"/"+postPublished,
                     data: "title="+itemValue,
                     success: function(msg) {
                         $('#autosavenotify').text(msg);
                     }
             })
        }
     });

	//https://github.com/orthes/medium-editor-images-plugin
	$('.editable').mediumImages();


});