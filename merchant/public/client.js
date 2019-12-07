console.log('Client-side code running');

const button = document.getElementById('myButton');
button.onclick = function (req,res) {
    document.getElementById("myButton").submit();
}