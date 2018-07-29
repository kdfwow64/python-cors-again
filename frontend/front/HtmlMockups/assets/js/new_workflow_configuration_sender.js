
function popUp1(idIndex4){
  operatorId = "operator-" + idIndex4;
  var id = 'popup1-box-' + idIndex4;
  //window.alert(operatorId);
  $('#' + operatorId).click(function(e) {
  
    /* Prevent default actions */
    e.preventDefault();
    e.stopPropagation();
    
    /* Get the id (the number appended to the end of the classes) */
    var name = $(this).attr('id');
    // var id = name[name.length - 1];
    var scrollPos = $(window).scrollTop();
    /* Show the correct popup box, show the blackout and disable scrolling */
    $('#'+id).show();
    $('#blackout').show();
    $('html,body').css('overflow', 'hidden');
    
    /* Fixes a bug in Firefox */
    $('html').scrollTop(scrollPos);
    centerBox(id);
  });
  $('[class*=popup1-box]').click(function(e) { 
    /* Stop the likn working normally on click if it's linked to a popup */
    e.stopPropagation(); 
  });
  $('html').click(function() { 
    var scrollPos = $(window).scrollTop();
    /* Hide the popup and blackout when clicking outside the popup */
    $('#'+id).hide(); 
    $('#blackout').hide(); 
    $("html,body").css("overflow","auto");
    $('html').scrollTop(scrollPos);
  });
  $('.close').click(function() { 
    var scrollPos = $(window).scrollTop();
    /* Similarly, hide the popup and blackout when the user clicks close */
    $('#'+id).hide(); 
    $('#blackout').hide(); 
    $("html,body").css("overflow","auto");
    $('html').scrollTop(scrollPos);
  });
  $('.close-bottom').click(function() { 
	    var scrollPos = $(window).scrollTop();
	    /* Similarly, hide the popup and blackout when the user clicks close */
	    $('#'+id).hide(); 
	    $('#blackout').hide(); 
	    $("html,body").css("overflow","auto");
	    $('html').scrollTop(scrollPos);
	  });
	
  }

function showHideBooleanCommandType() {
  this.addEventListener("click", function(){
  alert('walou');
  var test = this.value;
  if (test == 'true') {
    $("#" + this.id + '-1-div').show();
    $("#" + this.id + '-2-div').hide();
    alert(chihaja);
   }
   else {
     $("#" + this.id + '-2-div').show();
     $("#" + this.id + '-1-div').hide();
   }
});
}

$("input[name='hostType']").each(showHideBooleanCommandType);

  function addBodysender(index4) {
  var id = 'popup1-box-' + index4;
  $('body').append(`<div class="popup1-box" id="${id}">
        <span class="close btn btn-close"><em class="glyphicon glyphicon-remove"></em></span>
    <div class="bottom">
        <form class="bootstrap-form-with-validation id="` + id + `-form"">
                                        
                                        <table align="center" class="workflow-table"> 
                                        
                                        <tr>
                                  
                                            <td class="row-padding row-left-color"><label class="control-label" for="text-input">Job name</label></td>
                                            <td class="row-padding" align="center"><input  class="form-style" type="text" name="name" required=""></td>
                                      
                                        </tr>
                                        <tr>
                                            <td class="row-padding row-left-color"><label class="control-label" for="text-input">Description</label></td>
                                            <td class="row-padding" align="center"><input  class="form-style" type="text" name="description" ></td>
                                        </tr>
                                        <tr>
                                            <td class="row-padding row-left-color"><label class="control-label">Command</label>
                                            </td>
                                            <td class="row-padding">
                                                                 
  
      <div class="btn-group btn-group-vertical" data-toggle="buttons">
        <label class="btn">
        <input type="radio" id="differ_precheck_hostChoice" name='hostType' value="true"><i class="fa fa-circle-o fa-1.5x"></i><i class="fa fa-dot-circle-o fa-1.5x"></i> <span>Choose a host and commands file</span>
        </label>
        <label class="btn">
          <input type="radio" id="differ_precheck_hostChoice" name='hostType' value="false"><i class="fa fa-circle-o fa-1.5x"></i><i class="fa fa-dot-circle-o fa-1.5x"></i><span> write your commands</span>
        </label>
  </div>
                                            </td>
                                            </tr>
                                            
                                 <tr>
                                 <td>
                                    <div id="differ_precheck_hostChoice-1-div" class="form-group">
                                                <label class="control-label" for="file-input">Host File :</label>
                                     
                          
                                                <input type="file" name="hostFile">
                                         
                                    </div>
                                    </td>
                                    <td>
                                    <div id="differ_precheck_hostChoice-2-div" class="form-group">
                                       <input type="text">
                                       </div>
                                     </td>
                                     </tr>
                                            </tr>
                                    </table>
                                            <button type="button" class="close-bottom btn btn-primary btn-close" >Done</button>
                                    </form>
    </div>
    
</div>`);
  $('body').append('<div id="blackout"></div>');

  $(window).resize(centerBox);
  $(window).scroll(centerBox);
  centerBox(id);   
  popUp1(index4);
}
  $(document).ready();


  


  $(document).ready(function() {
    // Apply the plugin on a standard, empty div...
    var $flowchart = $('#start');
    $flowchart.flowchart({
      data: start
    });
    $flowchart.siblings('.get_data').click(function() {
      var data = $flowchart.flowchart('getData');
      $('#flowchart_data').val(JSON.stringify(data, null, 2));
    });

    $flowchart.siblings('.configurationSender').click(function() {
      var operatorId = 'operator-' + operator;
      var operatorData = {
        top: 60,
        left: 100,
        properties: {
          title: '<a href=""  class="popup1-link-1 text-center" id="' + operatorId + '">Sender</a>' ,
          inputs: {
            input_1: {
              label: ' ',}
          },
          outputs: {
            success: {
              label: ' success ',},
            failure: {
              label: 'failure',
            }

          }
        }
      };


      $('#start').flowchart('createOperator', operatorId, operatorData);
      addBodysender(operator);
      
      operator++;
    });
    
    $flowchart.siblings('.delete_selected_button').click(function() {
      $flowchart.flowchart('deleteSelected');
    });
    
    $flowchart.siblings('.get_data').click(function() {
      var data = $flowchart.flowchart('getData');
      $('#flowchart_data').val(JSON.stringify(data, null, 2));
    });

  });
