var menu = document.getElementById("menu-section");
var show = menu.getElementsByClassName("btn");
var cart = document.getElementById("insert-order");
var userName = document.location.href.split('?')[1].split('=')[1];
var profile = document.getElementById("my-profile");
profile.href += "?user=" + userName;
let test;
var orderArray = [];
const order_id = async () => {
  const res = await fetch("/getOrderId");
  const data = await res.json();
  let test_id = data.order_id;
  test = parseInt(test_id);
  console.log("oke");
  return test_id;
};
order_id();
function createList(index) {
  var d = new Date();
  var date = d.toJSON().slice(0,10);
  var tr = document.createElement("tr");
  tr.className = "show";
  tr.id = "planned_item";
  var name = document.createElement("th");
  var price = document.createElement("th");
  var item_id = document.createElement("th");
  var id = document.createElement("th");
  id.className = "Id";
  name.textContent = menu.getElementsByTagName("h4")[index].innerHTML;
  item_id.textContent = menu.getElementsByTagName("h5")[index].innerHTML;
  item_id.className = "hidden";
  price.textContent = menu.getElementsByTagName("h6")[index].innerHTML;
  id.textContent = test + 1;
  test += 1;
  orderArray.push(test);
  var quantity = document.createElement("input");
  quantity.type = "number";
  quantity.id = "quantity";
  quantity.value = 1;
  var time = document.createElement("input");
  time.type = "date";
  time.id = "order_time";
  time.value = date;
  var button = document.createElement("button");
  button.type = "button";
  button.className = "btn-close";
  tr.appendChild(id);
  tr.appendChild(name);
  tr.appendChild(price);
  tr.appendChild(quantity);
  tr.appendChild(time);
  tr.appendChild(button);
  tr.appendChild(item_id);
  cart.appendChild(tr);
}
function updateList(index, orderList) {
  test -= 1;
  for (let i = index; i < orderList.length; ++i) {
    let tmp = parseInt(
      orderList.item(i).getElementsByClassName("Id").item(0).innerHTML
    );
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
    var orderList = cart.getElementsByClassName("show");
    for (let index = 0; index < btns.length; index++) {
      btns[index].onclick = () => {
        orderList.item(index).classList += " hidden";
        updateList(index, orderList);
      };
    }
  });
}
var addOrder = async (data) =>{
  return await fetch('/rainbow', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  }).then(res => res.json())
  .then(res => res.result);
}
var orderButton = document.getElementById("order-button");
var ctn = '';
var notification = document.getElementById("notification");
orderButton.onclick = () =>{
  notification.innerHTML = "";
  var orderList = cart.getElementsByClassName("show");
  for (let index = 0; index < orderList.length; index++) {
    if(orderList.item(index).classList.length == 1){
      var idSend = orderList.item(index).getElementsByClassName("Id").item(0).innerHTML;
      var todayDate = new Date().toJSON().slice(0,10);
      var delDay = document.getElementById("order_time").value;
      var itemId = orderList.item(index).getElementsByClassName("hidden").item(0).innerHTML;
      var numberDisk = document.getElementById("quantity").value;
      var data = {
        order_id: idSend,
        torcv: todayDate,
        todel: delDay,
        item_id: itemId,
        quantity: numberDisk,
        user_id: userName
      };
    let rs = async () => {return await addOrder(data)};
    rs().then(res =>{
      if(res){
        console.log("oke?")
        ctn += `<div
        class="alert alert-success alert-dismissible fade show"
        role="alert"
      >
        <strong> Add successfully. </strong>
        <button type="button" 
        class="btn-close"
        data-bs-dismiss="alert"
        aria-label="Close"">
        </button>
      </div>`
      orderList.item(index).classList += " hidden";
      }
      else{
        console.log("no");
        ctn += `<div
        class="alert alert-danger alert-dismissible fade show"
        role="alert"
      >
        <strong>An error occurred while adding order ` + data.order_id + `. </strong>
        <button type="button" 
        class="btn-close"
        data-bs-dismiss="alert"
        aria-label="Close"">
        </button>
      </div>`
      }
      notification.innerHTML = ctn;
    })
  }
  ctn = '';
  }
  
  //location.reload();
}
