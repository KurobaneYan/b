function task3(){
    var rowCount=parseInt(prompt("Enter row count for matrices"));
    var colCount=parseInt(prompt("Enter column count for matrices"));

    
    var matrix=new Array(rowCount);
    var matrix2=new Array(rowCount);
    
    
    for(i=0;i<rowCount;i++){
        matrix[i]=new Array(colCount);
        matrix2[i]=new Array(colCount);
        for(y=0;y<matrix[i].length;y++){
        matrix[i][y]=Math.floor((Math.random() * 100) + 0);
        matrix2[i][y]=Math.floor((Math.random() * 100) + 0);
    }
    }
    
    console.log("matrixAddition: " + matrixAddition(matrix, matrix2));
}

function matrixAddition(a, b) {
  "use strict";
  var res = [];
  a.forEach((t, n) => {
    res.push(t.reduce((sums, val, i) => sums.concat(val + b[n][i]), []));
  });
  return res;
}
