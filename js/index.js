
var REFRESHINTERVAL = 300;
var state = 1;
var paused = true;
var STATEPATH = "/PerfusionController/PythonServer/state.json"
var PLAYPAUSEPATH = "/PerfusionController/PythonServer/playpause"
var RESETPATH = "/PerfusionController/PythonServer/reset"
var UPDATEPATH = "/PerfusionController/PythonServer/updateparameters"
var PRESETPATH = "/PerfusionController/PythonServer/preset"
var PRESETSELECTORPATH="/PerfusionController/PythonServer/presetselector"
// forms
var FORMPATH="/PerfusionController/PythonServer/forms"

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
    $('#StirBar').val(jsondata.StirBar);
    
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
    {
        $('#PlayPauseButton').html("<span class=\"glyphicon glyphicon-pause\"></span>");
        
    }
    else
    {
        $('#PlayPauseButton').html("<span class=\"glyphicon glyphicon-play\"></span>");
    }

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
    
    //open closed buttons
    if(jsondata.H2OValveOpen == 1)
    {
        test = $('#H2OValveOpen').text();
        $('#H2OValveOpen').text("Open");
        $('#H2OValveOpen').val("1");
        
    }
    else
    {
        $('#H2OValveOpen').text("Closed");
        $('#H2OValveOpen').val("0");

    }

    //open closed buttons
    if(jsondata.EtOHValveOpen == 1)
    {
        $('#EtOHValveOpen').text("Open");
        $('#EtOHValveOpen').val("1");
        
    }
    else
    {
        $('#EtOHValveOpen').text("Closed");
        $('#EtOHValveOpen').val("0");
        
    }

    
    //open closed buttons
    if(jsondata.AcetoneValveOpen == 1)
    {
        $('#AcetoneValveOpen').text("Open");
        $('#AcetoneValveOpen').val("1");
        
    }
    else
    {
        $('#AcetoneValveOpen').text("Closed");
        $('#AcetoneValveOpen').val("0");
        
    }
    
    //open closed buttons
    if(jsondata.WasteValveOpen == 1)
    {
        $('#WasteValveOpen').text("Open");
        $('#WasteValveOpen').val("1");
        
    }
    else
    {
        $('#WasteValveOpen').text("Closed");
        $('#WasteValveOpen').val("0");
        
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


function updateParameters(sender)
{
    
    var s;
    $.post(UPDATEPATH, {name: sender.id, value: sender.value},
          function(data,status){
          s= parsestate(data);
          });
    
    return s;
}

function updatePreset(sender)
{
    // if saving preset, prompt
    var s;
    var r;
    switch (sender.id)
    {
        case "PresetSelector":
            r = sender.value;
            break;
        case "AddPresetButton":
            r =  prompt("Please enter the name of the preset:","Preset");
            break;
        case "SavePresetButton":
            r = confirm("Save current preset?");
            break;
        case "RemovePresetButton":
            r = confirm("Delete current preset?");
            break;
    }
    
    if(r != null)
    var s;
    $.post(PRESETPATH, {name: sender.id, value: r},
           function(data,status){
           s= parsestate(data);
           });
    updatePresetSelector();
}

function updatePresetSelector()
{
    var s;
    $.get(PRESETSELECTORPATH,function(rawjsondata,status){
          var jsondata = JSON.parse(rawjsondata);
          $('#PresetSelector').html(jsondata.PresetSelector);
          });
    
    
    
    return s;
    
}

function loadDynamicContent()
{

    $.get(FORMPATH,function(rawjsondata,status){
          var jsondata = JSON.parse(rawjsondata);
          $('#FixTime').html(jsondata.FixTime);
          $('#EtOHTime').html(jsondata.EtOHTime);
          $('#AcetoneTime').html(jsondata.AcetoneTime);
          
          
          });
    
    updatePresetSelector();
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
       
       
       
       
  //     $(".OpenCloseButton").click(function() {
    //                               if($(this).text()=="Closed")
      //                             {
        //                           $(this).text("Open");
          //                         }
            //                       else
              //                     {
                //                   $(this).text("Closed");
                  //                 }
                    //               });
       
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