var operator = 0;


function popUp3(idIndex2){
  operatorId = "operator-" + idIndex2;
  var id = 'popup3-box-' + idIndex2;
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
  $('[class*=popup3-box]').click(function(e) { 
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

  function addBodyPostcheck(index2) {
  var id = 'popup3-box-' + index2;
  $('body').append(`<div class="popup3-box" id="${id}">
        <span class="close btn btn-close"><em class="glyphicon glyphicon-remove"></em></span>
   
    <div class="bottom">
        <form class="bootstrap-form-with-validation" id="` + id + `-form">
                                       <table align="center" class="workflow-table">
                                        <tr>
                                            <td class="row-padding row-left-color"><label class="control-label" for="text-input">Job name</label></td>
                                            <td class="row-padding" align="center"><input  class="form-style" type="text" name="name" required=""></td>
                                        </tr>
                                        <tr>
                                            <td class="row-padding row-left-color"><label class="control-label" for="text-input">Description</label></td>
                                            <td class="row-padding" align="center"><input  class="form-style" type="text" name="description" ></td>
                                        </tr>
                                       </table>
                <div class="panel-body" style="overflow:scroll; height:150px;">
                <table class="table table-striped table-bordered table-list display" id="postcheckJob" style="border-radius=8px;" >
                  <thead class="scrollable">
                    <tr>
                        
                        <th class="hidden-xs">choose a precheck job</th>
                        <th>Job Name</th>
                        <th>Execution Date and time</th>
                    </tr> 
                  </thead>
                  
                <tbody>
                          <tr>
                    
                             
                            <td id="jobID"><input type="radio" name="optradio"></td>
                            <td>job1</td>
                            <td>03 August 2017 - 08:05 pm</td>
                          </tr>
                      
                          <tr>
                           <td id="jobID"><input type="radio" name="optradio"></td>
                            <td>job2</td>
                            <td>30 August 2017 - 02:05 am</td>
                            
                          </tr>
                       
                          <tr>
                          <td id="jobID"><input type="radio" name="optradio"></td>
                            <td>job3</td>
                            <td>30 August 2017 - 02:05 am</td>
                          </tr>
                        
                          <tr>
                    
                             
                            <td id="jobID"><input type="radio" name="optradio"></td>
                            <td>job4</td>
                            <td>30 april 2018 - 02:47 pm</td>
                          </tr>
                      
                      
                          <tr>
                           <td id="jobID"><input type="radio" name="optradio"></td>
                            <td>job5</td>
                            <td>30 october 2017 - 08:05 am</td>
                            
                          </tr>
                        
                          <tr>
                          <td id="jobID"><input type="radio" name="optradio"></td>
                            <td>job6</td>
                            <td>20 August 2017 - 06:05 pm</td>
                          </tr>
                          <tr>
                          <td id="jobID"><input type="radio" name="optradio"></td>
                            <td>job7</td>
                            <td>20 August 2017 - 06:05 pm</td>
                          </tr>
                          <tr>
                          <td id="jobID"><input type="radio" name="optradio"></td>
                            <td>job8</td>
                            <td>20 August 2017 - 06:05 pm</td>
                          </tr>
                          <tr>
                          <td id="jobID"><input type="radio" name="optradio"></td>
                            <td>job9</td>
                            <td>20 August 2017 - 06:05 pm</td>
                          </tr>
                          <tr>
                          <td id="jobID"><input type="radio" name="optradio"></td>
                            <td>job10</td>
                            <td>20 August 2017 - 06:05 pm</td>
                          </tr>
                          <tr>
                          <td id="jobID"><input type="radio" name="optradio"></td>
                            <td>job11</td>
                            <td>20 August 2017 - 06:05 pm</td>
                          </tr>
                          <tr>
                          <td id="jobID"><input type="radio" name="optradio"></td>
                            <td>job12</td>
                            <td>20 August 2017 - 06:05 pm</td>
                          </tr>
                        </tbody>
                </table>
                  
            
              </div>
              <button type="button" class="close-bottom btn btn-primary btn-close" >Done</button>

                                    </form>
         
    </div>
        </div>`);
  $('body').append('<div id="blackout"></div>');

  $(window).resize(centerBox);
  $(window).scroll(centerBox);
  centerBox(id);   
  popUp3(index2);
      $('#postcheckJob').DataTable();

}

  $(document).ready();

  $(document).ready(function() {
 // Apply the plugin on a standard, empty div...
	
    
	var $flowchart = $('#start');
    $('html').keydown(function(e){
    if(e.keyCode == 46) {
        $flowchart.flowchart('deleteSelected');
    }
});

    $flowchart.flowchart({
      data: {},
      linkWidth: 3,
      onLinkCreate: setLinkColor
    });

    
    function setLinkColor(linkId, linkData) {

      if (linkData.fromConnector == 'failure') {
        linkData.color = 'red';
      }
      if (linkData.fromConnector == 'success') {
          linkData.color = 'green';
        }
      return true;
    }
    

    $flowchart.siblings('.get_data').click(function() {
      var data = $flowchart.flowchart('getData');
      $('#flowchart_data').val(JSON.stringify(data, null, 2));
    });

    $flowchart.siblings('.differPostcheck').click(function() {
      
      var operatorId = 'operator-' + operator;
      var operatorData = {
        top: 60,
        left: 300,
        properties: {
          title: '<a href=""  class="popup3-link-1 text-center" id="' + operatorId + '">Postcheck</a>' ,
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
      addBodyPostcheck(operator);
      // popUp3(operator);  
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
