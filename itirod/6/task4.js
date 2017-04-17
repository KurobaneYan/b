function getDayOfWeek(){
    var month=parseInt(prompt("Please, enter month number"));
    var dayNumber=parseInt(prompt("Please, enter day number"));
    var year=2017;
    
    var dat=new Date(year,month,dayNumber);
    
    var weekday = new Array(7);
    weekday[0] = "Sunday";
    weekday[1] = "Monday";
    weekday[2] = "Tuesday";
    weekday[3] = "Wednesday";
    weekday[4] = "Thursday";
    weekday[5] = "Friday";
    weekday[6] = "Saturday";

    alert(weekday[dat.getDay()]);
}
