var user_id = document.getElementById("management_id").value;
console.log(user_id);
var changeInfo = document.getElementById("change-info");
changeInfo.onclick = () => {
    document.getElementById("management_name").disabled = false;
    document.getElementById("change-button").disabled = false;
};
var checkPass = async (info) => {
    return await fetch('/checkManagementPassword', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(info),
    }).then(res => res.json());
}
var changePass = async (info) => {
    return await fetch('/changManagementPassword', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(info),
    }).then(res => res.json());
}
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
      var info = {user_id: user_id, password: oldPass.value};
      checkPass(info).then(res => {
        if(res.result){
          info.password = newPass.value;
          changePass(info).then(res => {
            if(res){
              location.href = '../'
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
