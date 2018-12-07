// Call API to convert markdown to html
function md2html() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var response_text = JSON.parse(this.responseText);
        document.getElementById("html_format").innerHTML = response_text['html_text'];
        MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
        store_local();
    }
    };
    xhttp.open("POST", "md2html/", true);
    var request_content = {};
    request_content['md_text'] = document.getElementById("md_text").value;
    xhttp.send(JSON.stringify(request_content));
}

// Create and download in markdown format
function download_md() {
    text = document.getElementById("md_text").value;
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', 'file.md');
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

// Create and download in html format
function download_html() {
    head = document.getElementsByTagName('head')[0].innerHTML;
    text = document.getElementById("html_format").innerHTML;
    text = `<div style="margin: 10%;">` + text + `</div>`
    console.log(text)
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(head+text));
    element.setAttribute('download', 'file.html');
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

// Local storage
function store_local(){
    if (typeof(Storage) !== "undefined") {
        localStorage.setItem("md_text", document.getElementById("md_text").value);
    }
}

// Get local storage
function get_local_storage() {
    if (typeof(Storage) !== "undefined") {
        document.getElementById("md_text").value = localStorage.getItem("md_text");
        md2html();
    } 
}
