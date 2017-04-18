function fibonacci(){
    var n=parseInt(prompt("Please, enter a number of desired element of Fibonacci sequence"));
    var a=1;
    var b=a;
    var prev=a;
    
    try{
        if(n<=0)
           throw "Incorrect input";
    }
    catch(err){
        console.log(err);
        return;
    }
    
    for(i=2;i<n;i++){
        prev=b;
        b=b+a;
        a=prev;
    }
    
    console.log(b);
}
