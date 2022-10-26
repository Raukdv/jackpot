var spam_key = document.getElementById("spam_key").value
// console.log(spam_key);
    
document.getElementById("type_user").addEventListener("change", myChangeFunction);
    
function myChangeFunction() {
        var x = document.getElementById("type_user");
        x.value = spam_key;
    }

myChangeFunction();
