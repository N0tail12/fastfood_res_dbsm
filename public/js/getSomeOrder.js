var user = document.location.href.split("?")[1].split("&")[0].split("=")[1];
var page = parseInt(
  document.location.href.split("?")[1].split("&")[1].split("=")[1]
);
var designation = document.location.href
  .split("?")[1]
  .split("&")[2]
  .split("=")[1];
var content = document.getElementById("order-content");
var goPageGo = document.getElementById("go-page");
var getOrderEmployee = async (page) => {
  return await fetch("/employeeOrder", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(page),
  }).then((res) => res.json());
};
var getOrderCooker = async (data) => {
    return await fetch('/cookerOrder', {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    }).then(res => res.json());
}
var completeOrder = async (id) =>{
    return await fetch("/complete", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(id),
      }).then((res) => res.json());
}
if (designation === "Employee") {
  getOrderEmployee({ page: page }).then((res) => {
    for (let index = 0; index < res.order.length; index++) {
      var tr = document.createElement("tr");
      var id = document.createElement("td");
      id.textContent = res.order[index].order_id;
      var email = document.createElement("td");
      email.textContent = res.order[index].email;
      var item = document.createElement("td");
      item.textContent = res.order[index].item_id;
      var quantity = document.createElement("td");
      quantity.textContent = res.order[index].quantity;
      var status = document.createElement("td");
      status.textContent = res.order[index].status;
      var cooker = document.createElement("td");
      cooker.textContent = res.order[index].user_id;
      var dayRcv = document.createElement("td");
      dayRcv.textContent = res.order[index].torcv.slice(0, 10);
      var dayDel = document.createElement("td");
      dayDel.textContent = res.order[index].todel.slice(0, 10);
      var option = document.createElement("td");
    //   option.style.backgroundColor = "#198754";
      if (status.innerHTML == "Pending" || status.innerHTML == "Cancel") {
        option.textContent = "Cannot Delivery";
      }else{
        option.textContent = "Can Delivery";
      }
      tr.appendChild(id);
      tr.appendChild(email);
      tr.appendChild(item);
      tr.appendChild(quantity);
      tr.appendChild(dayRcv);
      tr.appendChild(dayDel);
      tr.appendChild(status);
      tr.appendChild(cooker);
      tr.appendChild(option);
      content.appendChild(tr);
    }
    if (page > 1) {
      var previous = document.createElement("li");
      previous.className = "page-item";
      var number = document.createElement("a");
      number.className = "page-link";
      number.href = "/employee/order?user=" + user + "&page=" + (page - 1) + "&designation=" + designation;
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
        number.href = "/employee/order?user=" + user + "&page=" + index + "&designation=" + designation;
        number.textContent = index;
        previous.appendChild(number);
        goPageGo.appendChild(previous);
      } else {
        var previous = document.createElement("li");
        previous.className = "page-item";
        var number = document.createElement("a");
        number.className = "page-link";
        number.href = "/employee/order?user=" + user + "&page=" + index + "&designation=" + designation
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
      number.href = "/employee/order?user=" + user + "&page=" + (page + 1) + "&designation=" + designation
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
}else if(designation === 'Cook'){
    var data = {page: page, user_id: user};
    getOrderCooker(data).then(res => {
        for (let index = 0; index < res.order.length; index++) {
            var tr = document.createElement("tr");
            var id = document.createElement("td");
            id.textContent = res.order[index].order_id;
            var email = document.createElement("td");
            email.textContent = res.order[index].email;
            var item = document.createElement("td");
            item.textContent = res.order[index].item_id;
            var quantity = document.createElement("td");
            quantity.textContent = res.order[index].quantity;
            var status = document.createElement("td");
            status.textContent = res.order[index].status;
            var cooker = document.createElement("td");
            cooker.textContent = res.order[index].user_id;
            var dayRcv = document.createElement("td");
            dayRcv.textContent = res.order[index].torcv.slice(0, 10);
            var dayDel = document.createElement("td");
            dayDel.textContent = res.order[index].todel.slice(0, 10);
            var option = document.createElement("button");
            option.type = "button";
            option.className = "btn btn-success";
            option.textContent = "Complete Order";
            option.style.backgroundColor = "#198754";
            if (status.innerHTML == "Ready" || status.innerHTML == "Cancel") {
              option.disabled = true;
            }
            tr.appendChild(id);
            tr.appendChild(email);
            tr.appendChild(item);
            tr.appendChild(quantity);
            tr.appendChild(dayRcv);
            tr.appendChild(dayDel);
            tr.appendChild(status);
            tr.appendChild(cooker);
            tr.appendChild(option);
            content.appendChild(tr);
          }
          var complete = document.getElementsByClassName("btn btn-success");
          var line = content.getElementsByTagName("tr");
          for (let index = 0; index < complete.length; ++index) {
              if(!complete[index].disabled){
                  complete[index].addEventListener('click', () => {
                    var order_id = line.item(index).getElementsByTagName("td").item(0).innerHTML;
                    completeOrder({order_id: order_id}).then(res => {
                        if(res.result){
                            location.reload();
                        }else{
                            console.log("Some thing wrong?");
                        }
                    })
                  })
              }
          }
          if (page > 1) {
            var previous = document.createElement("li");
            previous.className = "page-item";
            var number = document.createElement("a");
            number.className = "page-link";
            number.href = "/employee/order?user=" + user + "&page=" + (page - 1) + "&designation=" + designation;
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
              number.href = "/employee/order?user=" + user + "&page=" + index + "&designation=" + designation;
              number.textContent = index;
              previous.appendChild(number);
              goPageGo.appendChild(previous);
            } else {
              var previous = document.createElement("li");
              previous.className = "page-item";
              var number = document.createElement("a");
              number.className = "page-link";
              number.href = "/employee/order?user=" + user + "&page=" + index + "&designation=" + designation
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
            number.href = "/employee/order?user=" + user + "&page=" + (page + 1) + "&designation=" + designation
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
}
