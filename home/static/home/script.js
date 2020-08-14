// Function called while clicking add button 
function add_item() { 

    var items = [];

    let item = document.getElementById("box");
    
    let list_item = document.getElementById("list-item");
    if(item.value !==""){
        let make_item = document.createElement("li");
        make_item.appendChild(document.createTextNode(item.value));

        list_item.appendChild(make_item);

        item.value = ""

        make_item.onclick = function(){
            this.parentNode.removeChild(this);
        }
    }
    else{
        alert("Input a Task");
    }
    
    } 
    
