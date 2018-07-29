
function popUp4(idIndex1){
  operatorId = "operator-" + idIndex1;
  var id = 'popup4-box-' + idIndex1;
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
  $('[class*=popup4-box]').click(function(e) { 
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

  function addBodyPrecheck(index1) {
  var id = 'popup4-box-' + index1;
  $('body').append(`<div class="popup4-box" id="${id}">
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
                                            <td class="row-padding row-left-color"><label class="control-label">command</label></td>
                                            <td class="row-padding"><input class="form-style" type="text" name="text-input" id="text-input">
                                            </td>
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
  popUp4(index1);
}  $(document).ready();


  


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


    $flowchart.siblings('.differPrecheck').click(function() {
      var operatorId = 'operator-' + operator;
      var operatorData = {
        top: 60,
        left: 500,
        properties: {
          title: '<a href=""  class="popup4-link-1 text-center" id="' + operatorId + '">Precheck</a>' ,
          inputs: {
            input_1: {
              label: ' ',}
          },
          outputs: {
            success: {
              label: 'success',},
            failure: {
              label: 'failure',
            }

          }
        }
      };


      $('#start').flowchart('createOperator', operatorId, operatorData);
      addBodyPrecheck(operator);
      // popUp4(operator);  
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
