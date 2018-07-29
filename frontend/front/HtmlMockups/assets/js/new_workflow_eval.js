
function popUp6(idIndex6){
  operatorId = "operator-" + idIndex6;
  var id = 'popup6-box-' + idIndex6;
  //window.alert(operatorId);
  $('#' + operatorId).click(function(e) {
  
    /* Prevent default actions */
    e.preventDefault();
    e.stopPropagation();
    
    /* Get the id (the number appended to the end of the classes) */
    var name = $(this).attr('id');
    // var id = name[name.length - 1];
    var scrollPos = $(window).scrollTop();
    /* Show the correct popUp6 box, show the blackout and disable scrolling */
    $('#'+id).show();
    $('#blackout').show();
    $('html,body').css('overflow', 'hidden');
    
    /* Fixes a bug in Firefox */
    $('html').scrollTop(scrollPos);
    centerBox(id);
  });
  $('[class*=popup6-box]').click(function(e) { 
    /* Stop the likn working normally on click if it's linked to a popUp6 */
    e.stopPropagation(); 
  });
  $('html').click(function() { 
    var scrollPos = $(window).scrollTop();
    /* Hide the popUp6 and blackout when clicking outside the popUp6 */
    $('#'+id).hide(); 
    $('#blackout').hide(); 
    $("html,body").css("overflow","auto");
    $('html').scrollTop(scrollPos);
  });
  $('.close').click(function() { 
    var scrollPos = $(window).scrollTop();
    /* Similarly, hide the popUp6 and blackout when the user clicks close */
    $('#'+id).hide(); 
    $('#blackout').hide(); 
    $("html,body").css("overflow","auto");
    $('html').scrollTop(scrollPos);
  });
  }

function addChoice(){

        event.preventDefault();
        var newRow = jQuery(`<tr>
                             	<td>
                             	
                             	<input type="text" name="key" style="width: 200px; border-radius: 12px; height: 47px;">
                             	</td>
                             	<td>
                             	
                             	<input type="text" name="value" style="width: 200px; border-radius: 12px; height: 47px;">
                             	</td>
                             	<td>
                             	
                             	<select style="border-radius: 12px; height:50px; width:200px; text-align:center" >
                                                                <option value="0" selected>--choose from here--</option>
                                                                <option value="30" >operator1</option><br></br>
                                                                <option value="31">operator2</option><br></br>
                                                                <option value="32">operator3</option>
                                                            </select>
                             	</td>
                             </tr>`);
        jQuery('table.choice-list').append(newRow);

};
  function addBodyEval(Index6) {

  var id = 'popup6-box-' + Index6;
  $('body').append(`<div class="popup6-box" id="${id}">
        <span class="close btn btn-info"><em class="glyphicon glyphicon-ok"></em></span>
    <div class="top">
        <h2>Evaluation</h2>
    </div>
    <div class="bottom">
        <form class="bootstrap-form-with-validation id="` + id + `-form"">
                                        
                             <table class="choice-list">
                             <tr>
                             	<td>
                             	<label>key</label><br>
                             	<input type="text" name="key" style="width: 200px; border-radius: 12px; height: 47px;">
                             	</td>
                             	<td>
                             	<label>value</label><br>
                             	<input type="text" name="value" style="width: 200px; border-radius: 12px; height: 47px;">
                             	</td>
                             	<td>
                             	<label>operator</label><br>
                             	<select style="border-radius: 12px; height:50px; width:200px; text-align:center" >
                                                                <option value="0" selected>--choose from here--</option>
                                                                <option value="30" >operator1</option><br></br>
                                                                <option value="31">operator2</option><br></br>
                                                                <option value="32">operator3</option>
                                                            </select>
                             	</td>
                             </tr>
                             </table>
                                                                  <a href="#" title="" onClick="addChoice()" class="add-choice"><button type="button" class="btn btn-sm btn-primary btn-create" href="#">Add choice</button></a>

                                        
                                    </form>
    </div>

</div>`);
  $('body').append('<div id="blackout"></div>');

  $(window).resize(centerBox);
  $(window).scroll(centerBox);
  centerBox(id);   
  popUp6(Index6);
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

    $flowchart.siblings('.Evaluation').click(function() {
      var operatorId = 'operator-' + operator;
      var operatorData = {
        top: 200,
        left: 900,
        properties: {
          title: '<a href=""  class="popup6-link-1 text-center" id="' + operatorId + '">Evaluation</a>' ,
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
      addBodyEval(operator);
      // popUp6(configurationParser);  
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
  
