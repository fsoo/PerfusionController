
var REFRESHINTERVAL = 500;
var state = 1;
var paused = true;



function refresh()
{
    
    sendUpdatedState(state);
    state = getUpdatedState();
    

}

function sendUpdatedState(state)
{
    
    
}

function getUpdatedState()
{
    
    $.get("/PerfusionController/PythonServer/state.json",function(data,status){
          state++;
    //      alert("Data: " + data + "\nStatus: " + status);
          });
    
    $('#ElapsedTimeInput').val(state);
    return state;
    
}



jQuery(function($){
       refresh();
       
       setInterval(function(){
           if(!paused)
            refresh();
           
           },REFRESHINTERVAL);
       
       
       $('#ElapsedTimeInput').mask('99:z9:z9',{translation: {'z':{pattern:/[0-5]/}}})
       $('#FixTimeInput').mask('99:z9:z9',{translation: {'z':{pattern:/[0-5]/}}})
       $('#EtOHTimeInput').mask('99:z9:z9',{translation: {'z':{pattern:/[0-5]/}}})
       $('#AcetoneTimeInput').mask('99:z9:z9',{translation: {'z':{pattern:/[0-5]/}}})
       $('#TotalTimeInput').mask('99:z9:z9',{translation: {'z':{pattern:/[0-5]/}}})
       
       
       
       
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
