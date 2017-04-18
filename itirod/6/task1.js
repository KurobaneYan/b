function compare(){
var num1=parseInt(prompt("Please, enter the first number"));
var num2=parseInt(prompt("Please, enter the second number"));
if(typeof num1!="number" || String(num1)=="NaN"){
    console.log("The first input is not a number");
    return;
}
else if (typeof num2!="number"|| String(num2)=="NaN"){
    console.log("The second input is not a number");
    return;
}
else if(num1==num2){
    console.log("Numbers are equal");
    return;
}
else if(num1>num2){
    console.log("The first number is greater than the second");
    return;
}
else if(num1<num2){
    console.log("The second number is greater than the first");
    return;
}
else {
    console.log("Something is wrong");
    return;
}
}
