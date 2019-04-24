// Call API to convert markdown to html
function md2html() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var response_text = JSON.parse(this.responseText);
        document.getElementById("html_format").innerHTML = response_text['html_text'];
        document.querySelectorAll('pre code').forEach((block) => {
          hljs.highlightBlock(block);
        });
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
    // the header of the download html
    head = `
    <html>
        <head>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
        <script type="text/x-mathjax-config">
            MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]}});
        </script>
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML"></script>
        <!--code highlight-->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.15.6/styles/default.min.css">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.15.6/highlight.min.js"></script>
    `;

    // the body of the download html
    var text = "";
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var response_text = JSON.parse(this.responseText);
        text = response_text['html_text'];
        text = `<body><script>hljs.initHighlightingOnLoad();</script><div style="margin: 10%;">` + text + `</div>
        </body>       </html> `; // add some style for the body part

        // send it to generate the file to download
        var element = document.createElement('a');
        element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(head+text));
        element.setAttribute('download', 'markdown.html');
        element.style.display = 'none';
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    }
    };
    xhttp.open("POST", "md2html/", true);
    var request_content = {};
    request_content['md_text'] = document.getElementById("md_text").value;
    xhttp.send(JSON.stringify(request_content));


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
