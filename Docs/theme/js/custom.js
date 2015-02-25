/*
$( document ).ready(
    function() {
    $('.slide').click(function(event){
        //$(this).hide();
        //$('.slide').not($(this)).hide();
        html2canvas($(this), {
            onrendered: function(canvas) {
                //$('.imageHolder').html(canvas);
                var dataURL = canvas.toDataURL("image/png");
                location.href = dataURL;
               // $('.imageHolder').append('<img src="'+dataURL+'" />');
               // $('.imageHolder').html('Generating..');
               // $.post('image.php',{image: dataURL},function(data){
               //     $('.imageHolder').html(data);
               }
               });
            });
        });

function pad(n, width, z) {
  z = z || '0';
  n = n + '0';
  return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
}

function download() {
    var content = zip.generate({type:"blob"});
    saveAs(content, "slides.zip");
}

function generate() {

    zip = new JSZip();
    var slidecounter=0;
    $('.slide').each(
        function(){
        html2canvas($(this), {
            onrendered: function(canvas) {
                var dataURL = canvas.toDataURL("image/png");
                dataURL = dataURL.replace('data:image/png;base64,', '');
                paddedcounter = pad(slidecounter, 4)
                slidecounter++;
                zip.file("slide"+paddedcounter+".png", dataURL, {base64: true});
                return
                }
            }).then(
            function () { 
                console.log("Se generaron " + slidecounter + " slides.");
            });
        });
    };
*/
