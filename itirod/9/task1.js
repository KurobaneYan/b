function task1(){
    var x=parseInt(prompt("Enter x coordinate for the first vector"));
    var y=parseInt(prompt("Enter y coordinate for the first vector"));
    var z=parseInt(prompt("Enter z coordinate for the first vector"));
    var x2=parseInt(prompt("Enter x coordinate for the second vector"));
    var y2=parseInt(prompt("Enter y coordinate for the second vector"));
    var z2=parseInt(prompt("Enter z coordinate for the second vector"));
    
    Vector.prototype.plus = function(vector) {
        return new Vector(this.x+vector.x,this.y+vector.y,this.z+vector.z);
    };
    Vector.prototype.scalar = function(vector) {
        return new Vector((this.x*vector.x)+(this.y*vector.y)+(this.z*vector.z));
    };
    Object.defineProperty(Vector.prototype, "length", {
        get: function() {
            return 3;
        }
    });
    Vector.prototype.toString = Vector.prototype.valueOf = function() {
        return "x:"+this.x+" y:"+this.y+" z:"+this.z;
    }
    
    
    var vec1=new Vector(x,y,z);
    var vec2=new Vector(x2,y2,z2);
    console.log(vec1.plus(vec2));
}

function Vector(x,y,z){
    this.x=x;
    this.y=y;
    this.z=z;
}
