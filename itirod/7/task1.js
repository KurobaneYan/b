function isSquare(){
    var coords=prompt("Please, enter eight coordinates separated by space");
    var res=coords.split(" ");
    var x1=parseInt(res[0]);
    var y1=parseInt(res[1]);
    var x2=parseInt(res[2]);
    var y2=parseInt(res[3]);
    var x3=parseInt(res[4]);
    var y3=parseInt(res[5]);
    var x4=parseInt(res[6]);
    var y4=parseInt(res[7]);
    
    var cx=(x1+x2+x3+x4)/4;
    var cy=(y1+y2+y3+y4)/4;

    var dd1=Math.pow(cx-x1,2)+Math.pow(cy-y1,2);
    var dd2=Math.pow(cx-x2,2)+Math.pow(cy-y2,2);
    var dd3=Math.pow(cx-x3,2)+Math.pow(cy-y3,2);
    var dd4=Math.pow(cx-x4,2)+Math.pow(cy-y4,2);
    alert(dd1==dd2 && dd1==dd3 && dd1==dd4 ? "Yes" : "No");
}
function pointIsInSquare(){
    var coords=prompt("Please, enter four coordinates separated by space");
    var coord=prompt("Please, enter the coordinate");
    var res=coords.split(" ");
    var crd=coord.split(" ");
    var x1 = Math.min(parseInt(res[0]), parseInt(res[2]));
    var x2 = Math.max(parseInt(res[0]), parseInt(res[2]));
    var y1 = Math.min(parseInt(res[1]), parseInt(res[3]));
    var y2 = Math.max(parseInt(res[1]), parseInt(res[3]));
    var x = parseInt(crd[0]);
    var y = parseInt(crd[1]);
    
    if ((x1 <= x ) && ( x <= x2) && (y1 <= y) && (y <= y2)) {
        alert("Yes");
    } else {
        alert("No");
    }
}
