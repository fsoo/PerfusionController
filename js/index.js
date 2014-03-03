
var REFRESHINTERVAL = 500;
var state = 1;
var paused = true;
var STATEPATH = "/PerfusionController/PythonServer/state.json"


function refresh()
{
    
    sendUpdatedState(state);
    state = getUpdatedState();
    

}

function sendUpdatedState(state)
{
    
    
}

function parsestate(rawjsondata)
{
    var jsondata = JSON.parse(rawjsondata);

    $('#ServerTime').text(jsondata.ServerTime);
    $('#ElapsedTime').val(jsondata.ElapsedTime);
    $('#FixTime').val(jsondata.FixTime);
    $('#EtOHTime').val(jsondata.EtOHTime);
    $('#AcetoneTime').val(jsondata.AcetoneTime);
    $('#TotalTime').val(jsondata.TotalTime);
    
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
           if(!paused)
            refresh();
           
           },REFRESHINTERVAL);
       
       
       $('#ElapsedTime').mask('99:z9:z9',{translation: {'z':{pattern:/[0-5]/}}})
       $('#FixTime').mask('99:z9:z9',{translation: {'z':{pattern:/[0-5]/}}})
       $('#EtOHTime').mask('99:z9:z9',{translation: {'z':{pattern:/[0-5]/}}})
       $('#AcetoneTime').mask('99:z9:z9',{translation: {'z':{pattern:/[0-5]/}}})
       $('#TotalTime').mask('99:z9:z9',{translation: {'z':{pattern:/[0-5]/}}})
       
       
       
       
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
                              
          if($(this).html()==="<span class=\"glyphicon glyphicon-play\"></span>")
          {
          paused = false;
          $(this).html("<span class=\"glyphicon glyphicon-pause\"></span>" );
          }
          else
          {
          paused = true;
          $(this).html("<span class=\"glyphicon glyphicon-play\">");
          }
          });

       
       
       
       });
