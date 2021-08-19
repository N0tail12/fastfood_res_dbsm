var addEmployee = document.getElementById("add-employee");
var checkId = async (id) =>{
    return await fetch('/checkUser', {
        method: "POST",
        headers:{
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(id),
    }).then(res => res.json());
}
addEmployee.addEventListener('submit', event =>{
    event.preventDefault();
    var user_id = document.getElementById("emusername");
    checkId({user_id: user_id.value}).then(res => {
        if (res.result) {
            addEmployee.submit();
        }else{
            var warning = document.getElementsByClassName("warning-message");
            warning.item(0).style.display = "block";
            user_id.onchange = () => {
                warning.item(0).style.display = "none";
            }
        }
    })
});