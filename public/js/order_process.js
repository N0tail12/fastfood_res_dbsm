var menu = document.getElementById("menu-section");
var show = menu.getElementsByClassName("btn");
var cart = document.getElementById("insert-order");
let test;
var orderArray = [];
const order_id = async () => {
  const res = await fetch("/getOrderId");
  const data = await res.json();
  let test_id = data[0].order_id;
  test = parseInt(test_id);
  return test_id;
};
order_id();
function createList(index) {
  var tr = document.createElement("tr");
  tr.className = "show";
  var name = document.createElement("th");
  var price = document.createElement("th");
  var id = document.createElement("th");
  id.className = "Id";
  name.textContent = menu.getElementsByTagName("h4")[index].innerHTML;
  price.textContent = menu.getElementsByTagName("h6")[index].innerHTML;
  id.textContent = test + 1;
  test += 1;
  orderArray.push(test);
  var quantity = document.createElement("input");
  quantity.type = "number";
  quantity.id = "quantity";
  var button = document.createElement("button");
  button.type = "button";
  button.className = "btn-close";
  tr.appendChild(id);
  tr.appendChild(name);
  tr.appendChild(price);
  tr.appendChild(quantity);
  tr.appendChild(button);
  cart.appendChild(tr);
}
function updateList(index, orderList){
  test -= 1;
  console.log(index)
  for(let i = index; i < orderList.length; ++i){
    let tmp = parseInt(orderList.item(i).getElementsByClassName("Id").item(0).innerHTML)
    console.log('tmp :',tmp);
    orderList.item(i).getElementsByClassName("Id").item(0).innerHTML = tmp - 1;
  }
}
for (let index = 0; index < show.length; index++) {
  show.item(index).addEventListener("click", function () {
    let oke = document.getElementById("oke-alert");
    createList(index);
    oke.style.display = "block";
    let closeButton = document.getElementById("close-button");
    closeButton.onclick = () => {
      oke.style.display = "none";
    };
    var btns = cart.getElementsByClassName("btn-close");
    console.log(btns);
    var orderList = cart.getElementsByClassName("show");
    for (let index = 0; index < btns.length; index++) {
      btns[index].onclick = () =>{
        console.log(orderList.item(index).getElementsByClassName("Id").item(0).innerHTML)
        orderList.item(index).classList += " hidden";
        updateList(index, orderList);
      }
    }
  });
}