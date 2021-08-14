var content = document.getElementById("order-content");
var email = document.getElementById("customer_email").value;
var page = parseInt(
  document.location.href.split("?")[1].split("&")[1].split("=")[1]
);
var changeInfo = document.getElementById("change-info");
changeInfo.onclick = () => {
  document.getElementById("customer_phone").disabled = false;
  document.getElementById("customer_area").disabled = false;
  document.getElementById("customer_town").disabled = false;
  document.getElementById("change-button").disabled = false;
};
var changeButton = document.getElementById("change-button");
changeButton.onclick = () => {};
var goPageGo = document.getElementById("go-page");
var data = { email: email, page: page };
// Fetch Section
var getAllOrder = async (data) => {
  return await fetch("/getAllOrder", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  }).then((res) => res.json());
};
var cancelOrder = async (id) => {
  return await fetch("/cancelOrder", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(id),
  }).then((res) => res.json());
};
var checkPass = async(info) =>{
  return await fetch('/checkPassword', {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(info),
  }).then(res => res.json());
}
var changePass = async(info) =>{
  return await fetch('/changePassword', {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(info),
  }).then(res => res.json());
}

getAllOrder(data).then((res) => {
  for (let index = 0; index < res.order.length; index++) {
    var tr = document.createElement("tr");
    var id = document.createElement("td");
    id.textContent = res.order[index].order_id;
    var item = document.createElement("td");
    item.textContent = res.order[index].item_name;
    var quantity = document.createElement("td");
    quantity.textContent = res.order[index].quantity;
    var torc = document.createElement("td");
    torc.textContent = res.order[index].order_date.slice(0, 10);
    var todel = document.createElement("td");
    todel.textContent = res.order[index].order_del.slice(0, 10);
    var status = document.createElement("td");
    status.textContent = res.order[index].status;
    var close = document.createElement("button");
    close.type = "button";
    close.style.backgroundColor = "#dc3545";
    close.style.paddingTop = "5px";
    close.className = "btn btn-danger";
    close.textContent = "Cancel Order";
    if (
      res.order[index].status == "Ready" ||
      res.order[index].status == "Cancel"
    ) {
      close.disabled = true;
    }
    tr.appendChild(id);
    tr.appendChild(item);
    tr.appendChild(quantity);
    tr.appendChild(torc);
    tr.appendChild(todel);
    tr.appendChild(status);
    tr.appendChild(close);
    content.appendChild(tr);
  }
  var cancelButton = document.getElementsByClassName("btn btn-danger");
  var orderID = content.getElementsByTagName("tr");
  for (let index = 0; index < cancelButton.length; ++index) {
    if (!cancelButton[index].disabled) {
      cancelButton[index].addEventListener("click", () => {
        let id = {
          order_id: orderID[index].getElementsByTagName("td")[0].innerHTML,
        };
        cancelOrder(id).then((res) => {
          if (res) {
            location.reload();
          }
        });
      });
    }
  }
  if (page > 1) {
    var previous = document.createElement("li");
    previous.className = "page-item";
    var number = document.createElement("a");
    number.className = "page-link";
    number.href = "/customer/profile?user=" + email + "&page=" + (page - 1);
    number.textContent = "Previous";
    previous.appendChild(number);
    goPageGo.appendChild(previous);
  }
  if (page == 1) {
    var previous = document.createElement("li");
    previous.className = "page-item";
    var number = document.createElement("a");
    number.className = "page-link";
    number.textContent = "Previous";
    previous.appendChild(number);
    goPageGo.appendChild(previous);
  }
  for (let index = 1; index <= res.pageNumber; ++index) {
    if (index == page) {
      var previous = document.createElement("li");
      previous.className = "page-item active";
      var number = document.createElement("a");
      number.className = "page-link";
      number.href = "/customer/profile?user=" + email + "&page=" + index;
      number.textContent = index;
      previous.appendChild(number);
      goPageGo.appendChild(previous);
    } else {
      var previous = document.createElement("li");
      previous.className = "page-item";
      var number = document.createElement("a");
      number.className = "page-link";
      number.href = "/customer/profile?user=" + email + "&page=" + index;
      number.textContent = index;
      previous.appendChild(number);
      goPageGo.appendChild(previous);
    }
  }
  if (page < res.pageNumber) {
    var previous = document.createElement("li");
    previous.className = "page-item";
    var number = document.createElement("a");
    number.className = "page-link";
    number.href = "/customer/profile?user=" + email + "&page=" + (page + 1);
    number.textContent = "Next";
    previous.appendChild(number);
    goPageGo.appendChild(previous);
  }
  if (page == res.pageNumber) {
    var previous = document.createElement("li");
    previous.className = "page-item";
    var number = document.createElement("a");
    number.className = "page-link";
    number.textContent = "Next";
    previous.appendChild(number);
    goPageGo.appendChild(previous);
  }
});
var changPassButton = document.getElementById("change-password");
var emptyField = document.getElementsByClassName("fill-this-field");
changPassButton.addEventListener("click", () => {
  var oldPass = document.getElementById("old-password");
  var newPass = document.getElementById("new-password");
  var repeatPass = document.getElementById("repeat");
  if (oldPass.value == "" || newPass.value == "" || repeatPass.value == "") {
    if (oldPass.value == "") {
      emptyField.item(0).style.display = "block";
      oldPass.onchange = () => {
        emptyField.item(0).style.display = "none";
      }
    }
    if (newPass.value == "") {
      emptyField.item(1).style.display = "block";
      newPass.onchange = () => {
        emptyField.item(1).style.display = "none";
      }
    }
    if (repeatPass.value == "") {
      emptyField.item(2).style.display = "block";
      repeatPass.onchange = () => {
        emptyField.item(2).style.display = "none";
      }
    }
  }
  else{
    var warningMess = document.getElementsByClassName("warning-message");
    if(newPass.value !== repeatPass.value){
      warningMess.item(1).style.display = "block";
      warningMess.item(2).style.display = "block";
      newPass.onchange = () => {
        warningMess.item(1).style.display = "none";
        warningMess.item(2).style.display = "none";
      }
      repeatPass.onchange = () => {
        warningMess.item(1).style.display = "none";
        warningMess.item(2).style.display = "none";
      }
    }else{
      var info = {email: email, password: oldPass.value};
      checkPass(info).then(res => {
        if(res.result){
          info.password = newPass.value;
          changePass(info).then(res => {
            if(res){
              window.open('../')
            }else{
              console.log("Failed");
            }       
          })
        }
        else{
          warningMess.item(0).style.display = "block";
          oldPass.onchange = () => {
            warningMess.item(0).style.display = "none";
          }
        }
      })
    }
  }
});
