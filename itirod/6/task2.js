function calcBuildingParams(){
    var floors=parseInt(prompt("Please, enter floor count"));
    var entrances=parseInt(prompt("Please, enter entrance count"));
    var appartmentsPerFloor=parseInt(prompt("Please, enter count of appartments per floor"));
    var appNumber=parseInt(prompt("Please, enter desired appartment number"));
    var entranceNum=-1;
    var appsPerEntrance=appartmentsPerFloor*floors;
    var tempAppsCount=appsPerEntrance;
    
    try{
        if(String(floors)=="NaN" || String(entrances)=="NaN" ||
           String(appartmentsPerFloor)=="NaN" ||
           floors<=0 || entrances<=0 || appartmentsPerFloor<=0)
           throw "Incorrect input";
    }
    catch(err){
        console.log(err);
        return;
    }
    
    
    for(i=1;i<=entrances;i++){
        if(appNumber<=tempAppsCount && appNumber>(tempAppsCount-appsPerEntrance))
           entranceNum=i;
        tempAppsCount+=appsPerEntrance;
       }
    
    try{
        if(entranceNum==-1)
           throw "There is no such appartment";
    }
    catch(err){
        console.log(err);
        return;
    }   
    
    console.log("Entrance number for that appartment is "+entranceNum);
}
