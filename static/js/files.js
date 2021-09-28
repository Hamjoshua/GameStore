var file_list = document.getElementById('fileList');
var carousel_inner = document.getElementsByClassName('carousel-inner')[0];
var carousel_indicators = document.getElementsByClassName('carousel-indicators')[0];
var old_img_urls = document.getElementById('old_img_urls');
var old_img_urls_list = eval(old_img_urls.value);
console.log(carousel_inner);

initRemoveButtons();
var add_btn = document.getElementById('addBtn');
add_btn.onclick = addNewImage;

function addCarouselItem(child_count)
{
    let carousel_item = document.createElement('div')
    carousel_item.classList.add('carousel-item');
    carousel_item.id = 'carousel-item' + String(child_count);
    let image_holder_game = document.createElement('div')
    image_holder_game.classList.add('image-holder-game');
    if(child_count == 0)
    {
        carousel_item.classList.add('active');
    }
    carousel_item.appendChild(image_holder_game);

    let image = document.createElement('img');
    image.id = 'image' + String(child_count);
    image.src = '/static/missing.png';
    image_holder_game.appendChild(image);

    carousel_inner.appendChild(carousel_item);
}

function addIndicator(child_count)
{
    let indicator = document.createElement('li');
    indicator.setAttribute('data-bs-target', '#carousel-1');
    indicator.setAttribute('data-bs-slide-to', String(child_count));
    if(child_count == 0)
    {
        indicator.classList.add('active');
    }

    carousel_indicators.appendChild(indicator);
}


function addFileField(child_count)
{
    let file_field = document.createElement('div');
    file_field.id = 'fileField' + String(child_count);

    let file_input = document.createElement('input');
    file_input.type = 'file';
    file_input.name = 'file' + String(child_count);
    file_input.id = 'file' + String(child_count);
    file_input.onchange = changePic;

    let remove_btn = document.createElement('input');
    remove_btn.classList.add('btn', 'btn-danger');
    remove_btn.value = 'Удалить';
    remove_btn.type = 'button';
    remove_btn.onclick = removeThisFileField;

    file_field.appendChild(file_input);
    file_field.appendChild(remove_btn);

    file_list.appendChild(file_field);
}


function addNewImage()
{
    let child_count = file_list.childElementCount;

    addFileField(child_count)
    addCarouselItem(child_count)
    addIndicator(child_count)
}

function removeThisFileField(event)
{
    file_field = event.target.parentNode;
    carousel_item_id = file_field.id[file_field.id.length - 1];
    refreshOldImgUrls(carousel_item_id);
    carousel_item = carousel_inner.getElementsByClassName('carousel-item')[carousel_item_id];
    indicator = carousel_indicators.children[carousel_item_id];
    file_list.removeChild(file_field);
    if(carousel_item.classList.contains('active'))
    {
        carousel_inner.children[0].classList.add('active');
        carousel_indicators.children[0].classList.add('active');
    }
    carousel_inner.removeChild(carousel_item);
    carousel_indicators.removeChild(indicator);
    renameChildren();
}

function refreshOldImgUrls(id)
{
    if(id < old_img_urls_list.length)
    {
        old_img_urls_list.splice(id, 1);
        old_img_urls.value = old_img_urls_list;
    }
    console.log(old_img_urls_list);
}

function renameChildren()
{
    for(let i = 0; i < file_list.children.length; i++)
    {
        file_field = file_list.children[i];
        console.log(file_field.id);
        file_field.id = changeAttr(file_field.id, i);
        let file_input = file_field.children[0];
        file_input.name = changeAttr(file_input.name, i);
        file_input.id = changeAttr(file_input.id, i);

        carousel_item = carousel_inner.children[i];
        carousel_item.id = changeAttr(carousel_item.id, i);
        image = carousel_item.children[0].children[0];
        image.id = changeAttr(image.id, i);

        indicator = carousel_indicators.children[i];
        indicator.removeAttribute('data-bs-slide-to');
        indicator.setAttribute('data-bs-slide-to', String(i));
    }
}

function changeAttr(attr, new_id)
{
    return attr.substring(0, attr.length - 1) + String(new_id);
}

function initRemoveButtons()
{
    for(let i = 0; i < file_list.children.length; i++)
    {
        file_field = file_list.children[i];
        file_field.children[0].onchange = changePic;
        file_field.children[1].onclick = removeThisFileField;
    }
}

function changePic (event) {
    console.log(event);
    var input_id = event.target.id[event.target.id.length - 1];
    var target = event.target || window.event.srcElement,
        files = target.files;
        console.log(files);

    // FileReader support
    if (FileReader && files && files.length) {
        var fr = new FileReader();
        fr.onload = function () {
            image = document.getElementById('image' + String(input_id));
            image.src = fr.result;
        }
        fr.readAsDataURL(files[0]);
    } 
}
