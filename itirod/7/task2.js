function decorator1(){
    var a=parseInt(prompt("Please, a"));
    var decoratedTestFunc1=dec1(testFunc1);
    
    console.log(decoratedTestFunc1(a));
    
}

function decorator2(){
    var args=prompt("Please, enter arguments separated by space").split(" ");
    var decoratedTestFunc2=dec2(testFunc2);
    for(i=0;i<args.length;i++) {
        args[i]=parseInt(args[i]);
    }
    console.log(decoratedTestFunc2(args));
}

function testFunc1(a){
    return a==1;
}
function testFunc2(){
    var result=true;
    for (var i = 0; i < arguments[0].length; i++) {
        result=result && arguments[0][i]==1;
    }
    return result;
}

function dec2(f){
    return function(){
        function compare(){
            var result=true;
            for (var i = 0; i < arguments.length; i++) {
                result=result && typeof arguments[i]=="number";
            }
            return result;
        }
        return f.apply(this,arguments) && compare(arguments);
    }
}

function dec1(f){
    return function(){
        return f.apply(this,arguments) && typeof arguments[0]=="number";
    }
}
        
