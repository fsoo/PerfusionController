
var REFRESHINTERVAL = 300;
var state = 1;
var paused = true;
var STATEPATH = "/PerfusionController/PythonServer/state.json"
var PLAYPAUSEPATH = "/PerfusionController/PythonServer/playpause"
var RESETPATH = "/PerfusionController/PythonServer/reset"


function refresh()
{
    
    sendUpdatedState(state);
    state = getUpdatedState();
    

}

function sendUpdatedState(state)
{
    
    
}

function secstohhmmss(secs)
{
    var txt;
    var hours = Math.floor(secs/(60*60));
    var mins = Math.floor((secs - hours*(60*60))/60);
    var secs = (secs - hours*(60*60)-mins*60);
    txt = hours.toString() + ":" + mins.toString() + ":" + secs.toString();
    return txt;
}

function parsestate(rawjsondata)
{
    var jsondata = JSON.parse(rawjsondata);
    
   


    $('#ServerTime').text(jsondata.ServerTimeString);
    $('#ElapsedTime').val(jsondata.ElapsedTime);
    $('#FixTime').val(jsondata.FixTime);
    $('#EtOHTime').val(jsondata.EtOHTime);
    $('#AcetoneTime').val(jsondata.AcetoneTime);
    $('#RemainingTime').val(jsondata.RemainingTime);
  
    // update flow rate progress bars
   
    $('#H2OFlowRate').css("width", String(jsondata.H2OFlowRate / jsondata.FixFlowRate * 100)+"%");
    $('#H2OFlowRateText').html("H<sub>2</sub>O "+String(jsondata.H2OFlowRate)+" mL/min");
   
    
    var etohnormalizedrate =jsondata.EtOHFlowRate / jsondata.FixFlowRate * 100;
    if(etohnormalizedrate > 100)
        etohnormalizedrate = 100;
        
    $('#EtOHFlowRate').css("width", String(etohnormalizedrate)+"%");
    $('#EtOHFlowRateText').html("EtOH "+String(jsondata.EtOHFlowRate)+" mL/min");
    
    
    $('#AcetoneFlowRate').css("width", String(jsondata.AcetoneFlowRate / jsondata.AcetoneRinseFlowRate * 100)+"%");
    $('#AcetoneFlowRateText').html("Acetone "+String(jsondata.AcetoneFlowRate)+" mL/min");
    
   
    if(jsondata.PlayPauseState == "Play")
        $('#PlayPauseButton').html("<span class=\"glyphicon glyphicon-pause\"></span>");
    else
        $('#PlayPauseButton').html("<span class=\"glyphicon glyphicon-play\"></span>");
    

    // clear state indicators and update
    $('#PauseStateIndicator').removeClass('lstbox-xs-active').addClass('lstbox-xs');
    $('#FixStateIndicator').removeClass('lstbox-xs-active').addClass('lstbox-xs');
    $('#EtOHStateIndicator').removeClass('lstbox-xs-active').addClass('lstbox-xs');
    $('#AcetoneStateIndicator').removeClass('lstbox-xs-active').addClass('lstbox-xs');
    $('#EndStateIndicator').removeClass('lstbox-xs-active').addClass('lstbox-xs');
    
    switch (jsondata.ProcessStep)
    {
        case "Fix":
            $('#FixStateIndicator').removeClass('lstbox-xs').addClass('lstbox-xs-active');
            break;
        case "EtOHRinse":
            $('#EtOHStateIndicator').removeClass('lstbox-xs').addClass('lstbox-xs-active');
            break;
        case "AcetoneRinse":
            $('#AcetoneStateIndicator').removeClass('lstbox-xs').addClass('lstbox-xs-active');
            break;
        case "End":
            $('#EndStateIndicator').removeClass('lstbox-xs').addClass('lstbox-xs-active');
            break;
        default:
            
            break;
            
            
            
    }
    
    
    return jsondata;

}


function getUpdatedState()
{
    var s;
    $.get(STATEPATH,function(data,status){
          s= parsestate(data);
          });
    
    return s;
    
}



jQuery(function($){
       refresh();
       
       setInterval(function(){
            refresh();
           
           },REFRESHINTERVAL);
       
       
   //    $('#ElapsedTime').mask('99:z9:z9',{translation: {'z':{pattern:/[0-5]/}}})
     //  $('#FixTime').mask('99:z9:z9',{translation: {'z':{pattern:/[0-5]/}}})
     //  $('#EtOHTime').mask('99:z9:z9',{translation: {'z':{pattern:/[0-5]/}}})
     //  $('#AcetoneTime').mask('99:z9:z9',{translation: {'z':{pattern:/[0-5]/}}})
     //  $('#TotalTime').mask('99:z9:z9',{translation: {'z':{pattern:/[0-5]/}}})
       
       
       
       
       $(".OpenCloseButton").click(function() {
                                   if($(this).text()=="Closed")
                                   {
                                   $(this).text("Open");
                                   }
                                   else
                                   {
                                   $(this).text("Closed");
                                   }
                                   });
       
       $(".PlayButton").click(function() {
                              
                              $.get(PLAYPAUSEPATH,function(data,status){
                                    s= parsestate(data);
                                    });
                              });
                              
                              
       
       $(".ResetButton").click(function() {
                               paused = true;
                               $.get(RESETPATH,function(data,status){
                                     
                                     s= parsestate(data);
                                     });
                               
                               });
       
       });