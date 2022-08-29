function dropdown1() {
var orders = document.getElementById('dropdown1');
var order_caret = document.getElementById('order-caret');
var product_caret = document.getElementById('product-caret');
if (orders.style.display == 'flex') {
    orders.style.display = 'none';
    order_caret.classList.remove('fa-caret-down');
    order_caret.classList.add('fa-caret-right');
}
else {
    orders.style.display = 'flex';
    order_caret.classList.remove('fa-caret-right');
    order_caret.classList.add('fa-caret-down');
    var products = document.getElementById('dropdown2');
    products.style.display = 'none';
    product_caret.classList.remove('fa-caret-down');
    product_caret.classList.add('fa-caret-right');
}
}

function dropdown2() {
    var products = document.getElementById('dropdown2');
    var order_caret = document.getElementById('order-caret');
    var product_caret = document.getElementById('product-caret');
    if (products.style.display == 'flex') {
        products.style.display = 'none';
        product_caret.classList.remove('fa-caret-down');
        product_caret.classList.add('fa-caret-right');
    }
    else {
        products.style.display = 'flex';
        product_caret.classList.remove('fa-caret-right');
        product_caret.classList.add('fa-caret-down');
        var orders = document.getElementById('dropdown1');
        orders.style.display = 'none';
        order_caret.classList.remove('fa-caret-down');
        order_caret.classList.add('fa-caret-right');
    }
}

function updateProduct(product_id) {
    var name = document.getElementById(`name${product_id}`).value;
    var price = document.getElementById(`price${product_id}`).value;
    window.location.replace(`/update-product/${product_id}/${name}/${price}`)
}

const elements1 = [document.getElementById("left")];
const elements2 = document.getElementsByClassName("dropdown");
var elements = elements1.concat([...elements2]);
document.addEventListener("click", (event) => {
    var isClickInside = false;
    elements.forEach(checkClick);
    function checkClick(element) {
        if (element.contains(event.target)) {
            isClickInside = true;
        }
    }
    
    if (!isClickInside) {
        document.getElementById('dropdown1').style.display = 'none';
        document.getElementById('dropdown2').style.display = 'none';
        var caret = document.getElementsByClassName('fa-caret-down');
        if (caret.length == 1) {
            caret[0].classList.add('fa-caret-right');
            caret[0].classList.remove('fa-caret-down');
        }
    }
});