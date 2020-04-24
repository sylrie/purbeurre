
const off = document.getElementById("off");
const page = document.getElementById("page");

// searching gif
off.onclick = function(){
    let elt = document.getElementById("off");
    elt.innerHTML = "";

    var newA = elt.appendChild(document.createElement("a"));
    newA.id ="searching";

    var newImg = newA.appendChild(document.createElement("img"));
    newImg.src = "{% static 'product/img/gif/loader2.gif";
};
