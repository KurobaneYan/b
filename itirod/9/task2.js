function task(){
    this.name="";
    this.description="";
    this.beginningDate="";
    this.endDate="";
    this.innerTasks=[];
    
}

var inherited=Object.create(task);
inherited.percentComplete=20;
inherited.isCompleted=false;
