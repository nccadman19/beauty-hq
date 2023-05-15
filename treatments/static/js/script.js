document.addEventListener("DOMContentLoaded", function() {
    // select initialization
    let selects = document.querySelectorAll("select");
    M.FormSelect.init(selects);

    // dropdown initialization
    var elems = document.querySelectorAll('.modal');
    var instances = M.Modal.init(elems);
});
