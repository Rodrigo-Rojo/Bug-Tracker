function myFunction() {
    let input, filter, div, span, a, ab, i;
    input = document.getElementById("mySearch");
    filter = input.value.toUpperCase();
    div = document.getElementById("myMenu");
    span = div.getElementsByTagName("span");

    for (i = 0; i < span.length; i++) {
        a = span[i].getElementsByTagName("p")[0];
        ab = span[i].getElementsByTagName("p")[1];

        if (a.innerHTML.toUpperCase().indexOf(filter) > -1 || ab.innerHTML.toUpperCase().indexOf(filter) > -1) {
            span[i].style.display = "";
        } else {
            span[i].style.display = "none";
        }
    }
}

function myTickets() {
    let input, filter, div, span, a, i;
    input = document.getElementById("mySearch");
    filter = input.value.toUpperCase();
    div = document.getElementById("myTickets");
    devDiv = document.getElementById("devDiv");
    span = div.getElementsByTagName("span");
    span2 = devDiv.getElementsByTagName("span");

    for (i = 0; i < span.length; i++) {
        a = span[i].getElementsByTagName("p")[0];
        ab = span[i].getElementsByTagName("p")[1];
        ac = span[i].getElementsByTagName("p")[2];
        ad = span[i].getElementsByTagName("p")[3];

        if (a.innerHTML.toUpperCase().indexOf(filter) > -1 || 
            ab.innerHTML.toUpperCase().indexOf(filter) > -1 || 
            ac.innerHTML.toUpperCase().indexOf(filter) > -1 || 
            ad.innerHTML.toUpperCase().indexOf(filter) > -1) {
            span[i].style.display = "";
        } else {
            span[i].style.display = "none";
        }
    }
    for (i = 0; i < span2.length; i++) {
        a = span2[i].getElementsByTagName("p")[0];
        ab = span2[i].getElementsByTagName("p")[1];
        ac = span2[i].getElementsByTagName("p")[2];

        if (a.innerHTML.toUpperCase().indexOf(filter) > -1 || 
            ab.innerHTML.toUpperCase().indexOf(filter) > -1 || 
            ac.innerHTML.toUpperCase().indexOf(filter) > -1) {
            span2[i].style.display = "";
        } else {
            span2[i].style.display = "none";
        }
    }
}
