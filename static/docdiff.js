function updatePreview() {
    let bg = localStorage.getItem("bg") == "true";
    let fg = localStorage.getItem("fg") == "true";
    let ul = localStorage.getItem("ul") == "true";

    let spans = document.getElementsByClassName("text-add");
    for (let i = 0; i < spans.length; i++) {
        spans[i].style.backgroundColor = bg ? "yellow" : "unset";
        spans[i].style.color = fg ? "blue" : "unset";
        spans[i].style.textDecorationLine = ul ? "underline" : "";
        spans[i].style.textDecorationColor = ul ? "blue" : "";
    }

    spans = document.getElementsByClassName("text-del");
    for (let i = 0; i < spans.length; i++) {
        spans[i].style.backgroundColor = bg ? "yellow" : "unset";
        spans[i].style.color = fg ? "red" : "unset";
        spans[i].style.textDecorationLine = ul ? "underline" : "";
        spans[i].style.textDecorationColor = ul ? "red" : "";
        spans[i].style.textDecorationStyle = ul ? "wavy" : "";
    }
}

function cacheSettings() {
    let boxes = document.getElementsByClassName("prefs");
    for (let i = 0; i < boxes.length; i++) {
        localStorage.setItem(boxes[i].id, boxes[i].checked);
    }
    updatePreview();
}

function resetSettings() {
    let boxes = document.getElementsByClassName("prefs");
    for (let i = 0; i < boxes.length; i++) {
        localStorage.setItem(boxes[i].id, boxes[i].defaultChecked);
    }
    updatePreview();
}

window.onload = function() {
    let boxes = document.getElementsByClassName("prefs");
    for (let i = 0; i < boxes.length; i++) {
        boxes[i].checked = eval(localStorage.getItem(boxes[i].id));
        boxes[i].addEventListener("change", cacheSettings);
    }
    updatePreview();
    document.querySelector("input[type=reset]").addEventListener("click", resetSettings);
}
