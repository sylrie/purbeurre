const valid = $("#user_request")[0];
var count = 0;

// manage and display the response
function grandpy(response) {
  
  let elt = $("#chatbox")[0];
  
  let papy_1 = response["papy_1"];
  let address = response["address"];
  let papy_2 = response["papy_2"];
  let story = response["story"];
  let fullurl = response["fullurl"];
  let lat = response["lat"];
  let lng = response["lng"];
  
  searchingGif("stop");

  var newP = elt.appendChild(document.createElement("p"));
  newP.innerHTML += papy_1;
  
  if (address != "") {
    var newP = elt.appendChild(document.createElement("p"));
    var strong = newP.appendChild(document.createElement("STRONG"));
    strong.setAttribute("class", "text-warning")
    strong.innerHTML = address;
    
    count++;
    let map = elt.appendChild(document.createElement("div"));
    map.id = "map" + count;
    map.setAttribute("class", "map col-lg-6 my-1");
    map.style.height = "300px";
  
    if (lat != "") {
      initMap(lat, lng, map);
    };
  };
  
  if (papy_2 != "") {
    var newP = elt.appendChild(document.createElement("p"));
    newP.innerHTML += papy_2;
  };

  if (story != "") {
    var newP = elt.appendChild(document.createElement("p"));
    newP.innerHTML += story;
  };

  if (fullurl != "") {
    var newP = elt.appendChild(document.createElement("p"));
    newP.innerHTML += (
      "Si tu en veux plus, vas voir sur "
    );

    var newA = newP.appendChild(document.createElement("a"));
    var linkText = document.createTextNode("Wikipedia");
    newA.appendChild(linkText);
    newA.href = fullurl;
  };
  
window.scrollTo(0,document.body.scrollHeight);
};

// init google map
function initMap(lat, lng, map) {
  var pos = {lat: lat, lng: lng};
  var map = new google.maps.Map(map , {
    zoom: 12,
    center: pos
  });
  var marker = new google.maps.Marker({
    position: pos,
    map: map
  });
};

//manage searching Gif
function searchingGif(action){
  let elt = $("#chatbox")[0];
  if (action == "start"){
    
    var newA = elt.appendChild(document.createElement("a"));
    newA.id ="searching";

    var newImg = newA.appendChild(document.createElement("img"));
    newImg.src = "../static/img/loader.gif";
    window.scrollTo(0,document.body.scrollHeight);
  } else {
    let gif = $("#searching")[0];
    elt.removeChild(gif);
  }
};

//remove the welcome image
function deleteWelcomeImg(){
  let imgBox = $("#imgBox")[0];
  let welcome = $("#welcome")[0];
  if ($("#welcome")[0]){
    imgBox.removeChild(welcome)
    }else{
    };
};

//send the question to the app
valid.addEventListener("submit", function(evt) {
  
  // user request
  var question = $("#question")[0].value;
  
  if (question.trim() != "") {
    
    //remove welcome image
    deleteWelcomeImg();
    //select element
    let elt = $("#chatbox")[0];
    
    // display the question
    let user = elt.appendChild(document.createElement("p"));
    user.id = "user";
    user.setAttribute("class", "text-success text-right")
    user.innerHTML = question;
    window.scrollTo(0,document.body.scrollHeight);
    // reset form
    $("#question")[0].value = "";

    // display searching img
    searchingGif("start");
    // run search
    $.ajax({url: "/grandpy/" + question, success: grandpy});
  };
  evt.preventDefault();
  
});

