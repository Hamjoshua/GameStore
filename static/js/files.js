var carousel_inner = document.getElementsByClassName('carousel-inner')[0];
var carousel_indicators = document.getElementsByClassName('carousel-indicators')[0];
console.log(carousel_inner);

initRemoveButtons();
var add_btn = document.getElementById('addBtn');
add_btn.onclick = addNewImage;

add_btn.ondragover = dragEvent;
add_btn.ondragleave = add_btnFromDropZone;
add_btn.ondrop = dropEvent;

function addCarouselItem(child_count)
{
    let carousel_item = document.createElement('div')
    carousel_item.classList.add('carousel-item');
    carousel_item.id = 'carousel-item' + String(child_count);
    let buttons_div = document.createElement('div')
    buttons_div.classList.add('d-flex', 'justify-content-center');
    if(child_count == 0)
    {
        carousel_item.classList.add('active');
    }
    carousel_item.appendChild(buttons_div);

    let image = document.createElement('img');
    image.id = 'image' + String(child_count);
    image.classList.add("d-block", "img-fluid", "w-100");
    image.src = '/static/missing.png';
    carousel_item.appendChild(image);

    remove_btn = document.createElement('button');
    remove_btn.classList.add('btn', 'btn-danger');
    remove_btn.innerHTML = '<img src="/static/remove_icon.png" width="15px" height="15px">';
    remove_btn.onclick = removeThisCarouselItem;

    download_btn = document.createElement('span');
    download_btn.classList.add('btn', 'btn-success');
    download_btn.innerHTML = '<img src="/static/download_icon.png" width="15px" height="15px">';

    buttons_div.appendChild(remove_btn);

    file_input = document.createElement('input');
    file_input.type = 'file';
    file_input.id = 'file' + String(child_count);
    file_input.name = 'file' + String(child_count);
    file_input.classList.add("d-none");
    file_input.onchange = changePic;
    carousel_item.appendChild(file_input);

    label_download = document.createElement('label');
    label_download.setAttribute('for', file_input.id);
    label_download.appendChild(download_btn);
    buttons_div.appendChild(label_download);

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

function addNewImage()
{
    let child_count = carousel_inner.childElementCount;

    addCarouselItem(child_count)
    addIndicator(child_count)
}

function removeThisCarouselItem(event)
{
    if(event.target.localName == 'img')
    {
        carousel_item = event.target.parentNode.parentNode.parentNode;
    }
    else
    {
        carousel_item = event.target.parentNode.parentNode;
    }

    carousel_item_id = carousel_item.id.split('').pop();
    indicator = carousel_indicators.children[carousel_item_id];
    carousel_inner.removeChild(carousel_item);
    carousel_indicators.removeChild(indicator);
    if(carousel_item.classList.contains('active'))
    {
        carousel_inner.children[0].classList.add('active');
        carousel_indicators.children[0].classList.add('active');
    }
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
    for(let i = 0; i < carousel_inner.children.length; i++)
    {
        carousel_item = carousel_inner.children[i];
        carousel_item.id = changeAttr(carousel_item.id, i);
        file_input = carousel_item.children[2];

        file_input.name = changeAttr(file_input.name, i);
        file_input.id = changeAttr(file_input.id, i);

        image = carousel_item.children[1];
        image.id = changeAttr(image.id, i);

        indicator = carousel_indicators.children[i];
        indicator.removeAttribute('data-bs-slide-to');
        indicator.setAttribute('data-bs-slide-to', String(i));
        console.log("success" + String(i));
    }
}

function changeAttr(attr, new_id)
{
    return attr.substring(0, attr.length - 1) + String(new_id);
}

function initRemoveButtons()
{
    for(let i = 0; i < carousel_inner.children.length; i++)
    {
        let carousel_item = carousel_inner.children[i];
        let buttons_div = carousel_item.children[0];
        let remove_btn = buttons_div.children[0];
        let download_btn = buttons_div.children[1];
        remove_btn.onclick = removeThisCarouselItem;
        file_input = carousel_item.children[2];
        file_input.onchange = changePic;
        console.log("success" + String(i));
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

function preloadImages(image_urls)
{
    for(let i=0; i < carousel_inner.childElementCount; i++)
    {
        let image_path = image_urls[i];
        let dataTransfer = new DataTransfer();
        let file = new File([], image_path, {type: 'image/jpg'})
        dataTransfer.items.add(file);
        carousel_inner.children[i].children[2].files = dataTransfer.files;
    }
}

function dragEvent(event)
{
 event.preventDefault();
 add_btnToDropZone();
}

function dropEvent(event)
{
  event.preventDefault();
  if(event.dataTransfer.items)
    {
      for(let i = 0; i < event.dataTransfer.items.length; i++)
        {
          if (event.dataTransfer.items[i].kind === 'file')
          {
          debugger;
            let file = event.dataTransfer.items[i].getAsFile();
            addNewImage();
            let last_carousel_item = carousel_inner.children[carousel_inner.childElementCount - 1];
            let file_input = last_carousel_item.children[2];
            let image = last_carousel_item.children[1];

            let dt = new DataTransfer();
            dt.items.add(file);

            file_input.files = dt.files;
            let fr = new FileReader();
            fr.onload = function(){
                image.src = fr.result;
            }
            fr.readAsDataURL(file_input.files[0]);
          }
        }
    }
    add_btnFromDropZone();
}

function add_btnToDropZone()
{
    add_btn.classList.add("drop-zone");
    add_btn.value = 'Сюда';
}

function add_btnFromDropZone()
{
    add_btn.classList.remove("drop-zone");
    add_btn.value = 'Нажмите для добавления элемента или перетащите файлы';
}
