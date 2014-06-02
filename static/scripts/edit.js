// New.js

$( document ).ready(function() {
	//https://github.com/daviferreira/medium-editor
    var title = new MediumEditor('.editable');
    var epicbody = $('#epiceditor').html();
    $('#epiceditor').empty();
    var opts = {
      container: 'epiceditor',
      basePath: window.location.origin,
      clientSideStorage: true,
      localStorageName: 'epiceditor',
      useNativeFullscreen: false,
      parser: marked,
      file: {
        name: 'epiceditor',
        defaultContent: '',
        autoSave: 100
      },
      theme: {
        base: '/static/epicEditor/epiceditor/themes/base/epiceditor.css',
        preview: '/static/epicEditor/epiceditor/themes/preview/preview-dark.css',
        editor: '/static/epicEditor/epiceditor/themes/editor/epic-dark.css'
      },
      button: {
        preview: true,
        fullscreen: true,
        bar: "auto"
      },
      focusOnLoad: true,
      shortcut: {
        modifier: 18,
        fullscreen: 70,
        preview: 80
      },
      string: {
        togglePreview: 'Toggle Preview Mode',
        toggleEdit: 'Toggle Edit Mode',
        toggleFullscreen: 'Enter Fullscreen'
      },
      autogrow: true
    }
    var editor = new EpicEditor(opts).load();
    editor.importFile('epiceditor', epicbody);
    var prog;
    $('#publish').click(function () {
        var title = $('#title').html();
        title = title.replace(/<\/?[^>]+(>|$)/g, "");
        $('#title-input').val(title);
        var body = $('#body').html();
        $('#body-input').val(JSON.parse(localStorage['epiceditor'])['epiceditor']['content'].replace(/\+/g, "%2b"));
        $('#published-input').val("1");
    });
    $('#draft').click(function () {
        var title = $('#title').html();
        title = title.replace(/<\/?[^>]+(>|$)/g, "");
        $('#title-input').val(title);
        var body = $('#body').html();
        $('#body-input').val(JSON.parse(localStorage['epiceditor'])['epiceditor']['content'].replace(/\+/g, "%2b"));
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

    editor.on('autosave',function () {
        var itemValue = JSON.parse(localStorage['epiceditor'])['epiceditor']['content'];
        itemValue = itemValue.replace(/\+/g, "%2b");
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