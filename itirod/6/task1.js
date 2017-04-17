function compare(){
var num1=parseInt(prompt("Please, enter the first number"));
var num2=parseInt(prompt("Please, enter the second number"));
if(typeof num1!="number" || String(num1)=="NaN"){
    alert("The first input is not a number");
    return;
}
else if (typeof num2!="number"|| String(num2)=="NaN"){
    alert("The second input is not a number");
    return;
}
else if(num1==num2){
    alert("Numbers are equal");
    return;
}
else if(num1>num2){
    alert("The first number is greater than the second");
    return;
}
else if(num1<num2){
    alert("The second number is greater than the first");
    return;
}
else {
    alert("Something is wrong");
    return;
}
}
