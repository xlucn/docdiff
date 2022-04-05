function cacheInput() {
    let boxes = document.getElementsByClassName("prefs");
    for (let i = 0; i < boxes.length; i++) {
        localStorage.setItem(boxes[i].id, boxes[i].checked);
    }

    let bg = localStorage.getItem('bg') == "true";
    let fg = localStorage.getItem('fg') == "true";
    let ul = localStorage.getItem('ul') == "true";

    let spans = document.getElementsByClassName("text-add");
    for (let i = 0; i < spans.length; i++) {
        spans[i].style.backgroundColor = bg ? "yellow" : "white";
        spans[i].style.color = fg ? "blue" : "black";
        spans[i].style.textDecoration = ul ? "underline blue" : "";
    }

    spans = document.getElementsByClassName("text-del");
    for (let i = 0; i < spans.length; i++) {
        spans[i].style.backgroundColor = bg ? "yellow" : "white";
        spans[i].style.color = fg ? "red" : "black";
        spans[i].style.textDecoration = ul ? "underline red wavy" : "";
    }
}

function resetInput() {
    let boxes = document.getElementsByClassName("prefs");
    for (let i = 0; i < boxes.length; i++) {
        localStorage.removeItem(boxes[i].id);
    }
}

window.onload = function() {
    let boxes = document.getElementsByClassName("prefs");
    for (let i = 0; i < boxes.length; i++) {
        let v = localStorage.getItem(boxes[i].id);
        if (v == "true") {
            boxes[i].checked = true;
        } else if (v == "false") {
            boxes[i].checked = false;
        }
    }
}
