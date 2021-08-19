var addMenu = document.getElementById("add-menu");
var checkId = async (id) =>{
    return await fetch('/checkID', {
        method: "POST",
        headers:{
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(id),
    }).then(res => res.json());
}
addMenu.addEventListener('submit', event =>{
    event.preventDefault();
    var item_id = document.getElementById("menuid");
    checkId({item_id: item_id.value}).then(res => {
        if (res.result) {
            addMenu.submit();
        }else{
            var warning = document.getElementsByClassName("warning-message");
            warning.item(0).style.display = "block";
            item_id.onchange = () => {
                warning.item(0).style.display = "none";
            }
        }
    })
});