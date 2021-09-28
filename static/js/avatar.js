var avatar_url = document.getElementById('avatar_url');
console.log(avatar_url);
avatar_url.onchange = changePic;


function changePic (evt) {
    var input_id = evt.target.id;
    var tgt = evt.target || window.event.srcElement,
        files = tgt.files;

    // FileReader support
    if (FileReader && files && files.length) {
        var fr = new FileReader();
        fr.onload = function () {
            console.log(fr.result);
            console.log(input_id + '_img');
            img = document.getElementById(input_id + '_img');
            img.src = fr.result;
        }
        fr.readAsDataURL(files[0]);
    }
}