function popUp2(idIndex3){
  operatorId = "operator-" + idIndex3;
  var id = 'popup2-box-' + idIndex3;
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
  $('[class*=popup2-box]').click(function(e) { 
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

  function addBodyParser(index3) {
  var id = 'popup2-box-' + index3;
  $('body').append(`<div class="popup2-box" id="${id}">
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
                                            <td class="row-padding row-left-color"><label class="control-label">Strict matching</label>
                                            </td>
                                            <td class="row-padding">
                                            <div class="material-switch" >
                            <input id="` + id + `someSwitchOptionPrimary2" value="true" name="strict_matching" type="checkbox" checked/>
                            <label for="` + id + `someSwitchOptionPrimary2" class="label-primary"></label>
                            </div>
                                            </td>
                                            </tr>
                                            <tr>
                                            <td class="row-padding row-left-color"><label class="control-label">Keys</label>
                                            <td class="row-padding"><input class="form-style" type="text" name="text-input" id="text-input">
                                            </td>
                                            </tr>
                                            <tr>
                                            <td class="row-padding row-left-color"><label class="control-label">Remote command</label></td>
                                            <td class="row-padding"><input class="form-style" type="text" name="text-input" id="text-input"></td>
                                            </tr>
                                    </table>
                                            <button type="button" class="close-bottom btn btn-primary btn-close" >Done</button>


                                    </form>
    </div>

 <div class="panel-body" hidden="true">
                <table class="table table-striped table-bordered table-list">
                  <thead>
                    <tr>

                        <th>job_name</th>
                        <th>description</th>
                        <th>strict_matching</th>
                        <th>keys</th>
                        <th>command</th>
                    </tr>
                  </thead>
                  <tbody>

                          {% for obj in jsondata.jobs %}
                          <tr>

                            <td>{{ obj.job_name }}</td>
                            <td>{{ obj.description }}</td>
                            <td>{{ obj.strict_matching }}</td>
                            <td>{{ obj.keys }}</td>
                            <td>{{ obj.command }}</td>
                            <td align="center">


                              <form method="GET">
                              <input type="hidden" value="{{ obj.operatorId }}" name="name" />
                              <input type="submit" name="delete_jobs" value="delete" />
                              </form>




                              <div><a class="btn btn-primary " role="button" href="#{{ obj.operatorId }}" data-toggle="modal">Edit</a>
        <div class="modal fade" role="dialog" tabindex="-1" id="{{ obj.operatorId }}">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true"></span></button>
                        <h4 class="modal-title col col-xs-6 text-left">Edit</h4></div>
                    <div class="modal-body">
                    <form method="GET">
                    <label>job_name</label>
                    <input type="text" name="job_name">
                    <label>description</label>
                    <input type="text" name="description">
                    <select name="strict_matching">
                                    <option value= "True">true</option>
                                    <option value= "False">false</option>
                    </select>
                    <label>keys</label>
                    <input type="text" name="keys">
                    <label>command</label>
                    <input type="text" name="command">
                    
                    
                    </form>
                    

                </div>
            </div>
        </div>
                              </form>




                            </td>
                          </tr>
                        </tbody>
                          {% endfor %}

                </table>

              </div>
</div>`);
  $('body').append('<div id="blackout"></div>');

  $(window).resize(centerBox);
  $(window).scroll(centerBox);
  centerBox(id);   
  popUp2(index3);
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


    $flowchart.siblings('.configurationParser').click(function() {
      var operatorId = 'operator-' + operator;
      var operatorData = {
        top: 60,
        left: 700,
        properties: {
          title: '<a href=""  class="popup2-link-1 text-center" id="' + operatorId + '">Parser</a>' ,
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
      addBodyParser(operator);
      // popUp2(operator);  
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
