var dayStart = document.getElementById("date-start");
var dayEnd = document.getElementById("date-end");
var showData = document.getElementById("show-data");
var emptyField = document.getElementsByClassName("fill-this-field");
var content = document.getElementById("print");
var page = parseInt(
    document.location.href.split("?")[1].split("&")[0].split("=")[1]
  );
var user = document.location.href.split("?")[1].split("&")[1].split("=")[1]
var goPageGo = document.getElementById("go-page");
var getSale = async (data) => {
    return await fetch('/manager/sale',{
        method: 'POST',
        headers:{
            'Content-Type' : 'application/json',
        },
        body: JSON.stringify(data),
    }).then(res => res.json());
}
showData.onclick = () => {
    goPageGo.innerHTML = '';
    if(dayStart.value == '' || dayEnd.value == ''){
        if(dayStart.value == '' ){
            emptyField.item(0).style.display = "block";
            dayStart.onchange = () => {
              emptyField.item(0).style.display = "none";
            }
        }
        if(dayEnd.value == ''){
            emptyField.item(1).style.display = "block";
            dayEnd.onchange = () => {
              emptyField.item(1).style.display = "none";
            }
        }
    }else{
        var start = new Date(dayStart.value);
        var end = new Date(dayEnd.value);
        if(start.getTime() > end.getTime()){
            emptyField.item(2).style.display = "block";
            dayEnd.onchange = () => {
                emptyField.item(2).style.display = "none";
            }
            dayStart.onchange = () => {
                emptyField.item(2).style.display = "none";
            }
        }else{
            var data = {page: page, dateStart: dayStart.value, dateEnd: dayEnd.value};
            getSale(data).then(res => {
                for(let index = 0; index < res.sale.length; ++ index){
                    var tr = document.createElement("tr");
                    var day = document.createElement("td");
                    day.textContent = res.sale[index].todel.slice(0,10);
                    var money = document.createElement("td");
                    money.textContent = res.sale[index].total;
                    tr.appendChild(day);
                    tr.appendChild(money);
                    content.appendChild(tr);
                }
                if (page > 1) {
                    var previous = document.createElement("li");
                    previous.className = "page-item";
                    var number = document.createElement("a");
                    number.className = "page-link";
                    number.href = "/manager/sale?page=" + (page - 1) + "&user=" + user ;
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
                      number.href = "/manager/sale?page=" + index + "&user=" + user ;
                      number.textContent = index;
                      previous.appendChild(number);
                      goPageGo.appendChild(previous);
                    } else {
                      var previous = document.createElement("li");
                      previous.className = "page-item";
                      var number = document.createElement("a");
                      number.className = "page-link";
                      number.href = "/manager/sale?page=" + index + "&user=" + user ;
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
                    number.href = "/manager/sale?page=" + (page + 1) + "&user=" + user ;
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
            })
        }
    }
}