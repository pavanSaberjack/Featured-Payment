console.log('Client-side code running');

const button = document.getElementById('myButton');
button.onclick = function (req,res) {
    document.getElementById("myButton").submit();
}

const button1 = document.getElementById('otpButton');
button1.onclick = function (req,res) {
    document.getElementById("otpButton").submit();
}


const button2 = document.getElementById('ntButton');
button2.onclick = function (req,res) {
    document.getElementById("ntButton").submit();
}



function isNumber(evt) {
    evt = (evt) ? evt : window.event;
    var charCode = (evt.which) ? evt.which : evt.keyCode;
    if (charCode > 31 && (charCode < 48 || charCode > 57)) {
        return false;
    }
    return true;
}


