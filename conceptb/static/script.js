function hideFunction() {
    var x = document.getElementById("myLinks");
    if (x.style.display === "block") {
      x.style.display = "none";
      menu = document.getElementsByClassName('icon')[0];
      menu.style.color = '#ddd';
      menu.style.backgroundColor = '#333';
    } else {
      x.style.display = "block";
      menu = document.getElementsByClassName('icon')[0];
      menu.style.color = 'black';
      menu.style.backgroundColor = '#ddd';
    }
}

function dark() {
  var x = document.getElementById("cart");
  var y = x.getElementsByClassName("items-number");
  x.style.color = "rgb(85, 84, 79)";
  y[0].style.color = "rgb(85, 84, 79)";
}

function light() {
  var x = document.getElementById("cart");
  var y = x.getElementsByClassName("items-number");
  x.style.color = "rgb(235, 234, 221)";
  y[0].style.color = "rgb(235, 234, 221)";
}

function upQuantities(index) {
  var span = document.getElementById(`span${index}`);
  span.textContent = parseInt(span.textContent) + 1;
  var link = document.getElementById(`link${index}`);
  var new_href = `/add-product/${index}/${span.textContent}`;
  link.setAttribute('href', new_href);
}

function downQuantities(index) {
  var span = document.getElementById(`span${index}`);
  if (parseInt(span.textContent) > 1) {
    span.textContent = parseInt(span.textContent) - 1;
    var link = document.getElementById(`link${index}`);
    var new_href = `/add-product/${index}/${span.textContent}`;
    link.setAttribute('href', new_href);
  }
}

function addPopup() {
  document.getElementsByClassName('popup-container')[0].style.display = 'flex';
}

function removePopup() {
  document.getElementsByClassName('popup-container')[0].style.display = 'none';
}