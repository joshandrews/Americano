// New.js

$( document ).ready(function() {
	//https://github.com/daviferreira/medium-editor
	var editor = new MediumEditor('.editable')

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
	//https://github.com/orthes/medium-editor-images-plugin
	$('.editable').mediumImages();
});