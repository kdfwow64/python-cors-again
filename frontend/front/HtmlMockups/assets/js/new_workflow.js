	var checkedButton="";
	function validationValueWorkflow(){

		var checkedValueWorkflow=document.getElementById('someSwitchOptionPrimary');
		checkedValueWorkflow.value = ( $("#someSwitchOptionPrimary").is(':checked') ) ? true : false;
		
	}
	  function deleteEvalRule(ev){
		  console.log(ev);
	  
		  var deletedRule= ev.id;
		  console.log(deletedRule);
		  var chihaja=document.getElementsByClassName(deletedRule);
		  console.log(chihaja);
		  $("."+deletedRule).remove();
		  
	  }
	  
function myFunction(jobID) {
    	        document.getElementById("storage").value = jobID;
    	        checkedButton = document.getElementById("storage").value;
    	    }
$(document).ready(function() {
	var operator=0;
    var $flowchart = $('#start');
    var $container = $flowchart.parent();    
    var cx = $flowchart.width() / 2;
    var cy = $flowchart.height() / 2;
    var precheckList = [];
    var dataName = [];
    var dataDescription = [];
    var dataRemoteCommand = [];
    var thisName;
    var thisDescription;
    var thisRemoteCommand;
    var precheckCount=0;
    var name = "";
    $flowchart.panzoom();
    $flowchart.panzoom('pan', -cx + $container.width() / 2, -cy + $container.height() / 2);    
    var possibleZooms = [0.5, 0.75, 1, 2, 3];
    var currentZoom = 2;
    $container.on('mousewheel.focal', function( e ) {
        e.preventDefault();
        var delta = (e.delta || e.originalEvent.wheelDelta) || e.originalEvent.detail;
        var zoomOut = delta ? delta < 0 : e.originalEvent.deltaY > 0;
        currentZoom = Math.max(0, Math.min(possibleZooms.length - 1, (currentZoom + (zoomOut * 2 - 1))));
        $flowchart.flowchart('setPositionRatio', possibleZooms[currentZoom]);
        $flowchart.panzoom('zoom', possibleZooms[currentZoom], {
            animate: false,
            focal: e
        });
    });
    var $draggableOperatorsParser = $('.draggable_operator_parser');
    var $draggableOperatorsSender = $('.draggable_operator_sender');
    var $draggableOperatorsPostcheck = $('.draggable_operator_postcheck');
    var $draggableOperatorsPrecheck = $('.draggable_operator_precheck');
    var $draggableOperatorsLoader = $('.draggable_operator_loader');
    var $draggableOperatorsEval = $('.draggable_operator_eval');
    var $draggableOperatorsSuccess = $('.draggable_operator_success');
    var $draggableOperatorsFail = $('.draggable_operator_fail');
    var $draggableOperatorsStart = $('.draggable_operator_start');
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
    $('.delete_selected_button').click(function() {
        $flowchart.flowchart('deleteSelected');
        
        
      });
    
    function setLinkColor(linkId, linkData) {
      if (linkData.fromConnector == 'failure') {
        linkData.color = 'red';
      }
      else
          linkData.color = 'green';
      return true;
    }
    $flowchart.siblings('.get_data').click(function() {
      var data = $flowchart.flowchart('getData');
      $('#flowchart_data').val(JSON.stringify(data, null, 1));
    });
    	  function addBodyParser(operatorId) {
    	  var id = 'popup2-box-' + operatorId;
    	  $('body').append(`<div class="popup2-box" id="${id}">
    		        <span class="close btn btn-close"><em class="glyphicon glyphicon-remove"></em></span>
    		        <div class="bottom">
    		        <form class="bootstrap-form-with-validation" id="`+ id + `-form"">
    		                                    <input type="hidden" name="agent_type" id="agent_type_`+operatorId+`" value="configuration_parser" >
    		                                   <table align="center" class="workflow-table"> 
    		                                        <tr>
    		                                            <td class="row-padding row-left-color"><label class="control-label" for="text-input">Job name</label></td>
    		                                            <td class="row-padding" align="center"><input  class="form-style" type="text" name="name" id="name_`+operatorId+`" required=""></td>
    		                                        </tr>
    		                                        <tr>
    		                                            <td class="row-padding row-left-color"><label class="control-label" for="text-input">Description</label></td>
    		                                            <td class="row-padding" align="center"><input  class="form-style" type="text" name="description" id="description_`+operatorId+`" ></td>
    		                                        </tr>
    		                                        <tr>
    		                                            <td class="row-padding row-left-color"><label class="control-label">Strict matching</label>
    		                                            </td>
    		                                            <td class="row-padding">
    		                                            <div class="material-switch" >
    		                            <input id="strict_matching_`+operatorId+`" value="true" name="strict_matching" type="checkbox" checked/>
    		                            <label for="strict_matching_`+operatorId+`" class="label-primary"></label>
    		                            </div>
    		                                            </td>
    		                                            </tr>
    		                                            <tr>
    		                                            <td class="row-padding row-left-color"><label class="control-label">Keys</label>
    		                                            <td class="row-padding"><input class="form-style" type="text" name="keyList" id="keyList_`+operatorId+`">
    		                                            </td>
    		                                            </tr>
    		                                            <tr>
    		                                            <td class="row-padding row-left-color"><label class="control-label">Remote command</label></td>
    		                                            <td class="row-padding"><textarea class="textarea-style" name="remoteCommand" id="remoteCommand_`+operatorId+`"></textarea></td>
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
    	  $("#"+id).show();
    	  /* Get the id (the number appended to the end of the classes) */
  	    var scrollPos = $(window).scrollTop();
  	    /* Show the correct popup box, show the blackout and disable scrolling */
  	    $('#blackout').show();
  	    $('html,body').css('overflow', 'hidden');
  	    /* Fixes a bug in Firefox */
  	    $('html').scrollTop(scrollPos);
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
    	  function addBodySender(operatorId) {
    		  var id = 'popup1-box-' + operatorId;
    		  $('body').append(`<div class="popup1-box" id="${id}">
    			        <span class="close btn btn-close"><em class="glyphicon glyphicon-remove"></em></span>
    				    <div class="bottom">
    				        <form class="bootstrap-form-with-validation" id="`+ id + `-form"">
    				        		        		          <input type="hidden" name="agent_type" id="agent_type_`+operatorId+`" value="configuration_sender">
    				                                        <table align="center" class="workflow-table"> 
    				                                        <tr>
    				                                            <td class="row-padding row-left-color"><label class="control-label" for="text-input">Job name</label></td>
    				                                            <td class="row-padding" align="center"><input  class="form-style" type="text" name="name" required="" id="name_`+operatorId+`"></td>
    				                                        </tr>
    				                                        <tr>
    				                                            <td class="row-padding row-left-color"><label class="control-label" for="text-input">Description</label></td>
    				                                            <td class="row-padding" align="center"><input  class="form-style" type="text" name="description" id="description_`+operatorId+`"></td>
    				                                        </tr>
    				                                        <tr>
    				                                            <td class="row-padding row-left-color"><label class="control-label">Command</label>
    				                                            </td>
    				                                            <td class="row-padding" align="center"><textarea class="textarea-style" name="remoteCommands" id="remoteCommands_`+operatorId+`"></textarea></td>
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
        	  $("#"+id).show();
        	  /* Get the id (the number appended to the end of the classes) */
      	    var scrollPos = $(window).scrollTop();
      	    /* Show the correct popup box, show the blackout and disable scrolling */
      	    $('#'+id).show();
      	    $('#blackout').show();
      	    $('html,body').css('overflow', 'hidden');
      	    /* Fixes a bug in Firefox */
      	    $('html').scrollTop(scrollPos);
      	    centerBox(id);
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
    	  function addBodyPostcheck(operatorId) {
    		  var precheck_list = document.getElementById('precheck_list');
    		  var json = precheck_list.value;
    		  console.log()
    		  var value = "[-5, 5, 5]";
    		  var id = 'popup3-box-' + operatorId;
    		  $('body').append(`<div class="popup3-box" id="${id}">
    			        <span class="close btn btn-close"><em class="glyphicon glyphicon-remove"></em></span>
    				    <div class="bottom">
    				        <form class="bootstrap-form-with-validation" id="`+ id + `-form">
    				        		          <input type="hidden" name="agent_type" id="agent_type_`+operatorId+`" value="configuration_differ_postcheck">
    				                                       <table align="center" class="workflow-table">
    				                                        <tr>
    				                                            <td class="row-padding row-left-color"><label class="control-label" for="text-input">Job name</label></td>
    				                                            <td class="row-padding" align="center"><input  class="form-style" type="text" name="name" id="name_`+operatorId+`" required=""></td>
    				                                        </tr>
    				                                        <tr>
    				                                            <td class="row-padding row-left-color"><label class="control-label" for="text-input">Description</label></td>
    				                                            <td class="row-padding" align="center"><input  class="form-style" type="text" name="description" id="description_`+operatorId+`" ></td>
    				                                        </tr>
    				                                        <tr>
    				                                        <input type="text" id="storage" value="" hidden="true">
    				                                        </tr>
    				                                       </table>
    				                <div class="panel-body" style="overflow:scroll; height:150px;">
    				                <table class="table table-striped table-bordered table-list display" id="postcheckJob`+operatorId+`" style="border-radius=8px;" >
    				                  <thead class="scrollable">
    				                       <tr>
    				                       <th>checkbox</th>
                    	<th hidden="true">Id</th>
                    	<th>Name</th>
                        <th>Description</th>
                        <th>Agent Type</th>
                        <th>Insertion Time</th>	
    				                    </tr> 
    				                  </thead>
    				                </table>
    				                <table class="table table-striped table-bordered table-list precheck-list display" id="precheckJob`+operatorId+`" style="border-radius=8px;" >
    				                  <thead class="scrollable">
    				                       <tr>
    				                       <th>checkbox</th>
    				                	   <th>Name</th>
                                           <th>Description</th>
                                           <th>Remote Command</th>
    				                    </tr> 
    				                  </thead>
    				                  <tbody id="precheckBody`+operatorId+`">
    				                  </tbody>
    				                </table>
    				              </div>
    				              <button type="button" class="close-bottom btn btn-primary btn-close" >Done</button>
    				                                    </form>
    				    </div>
    				        </div>`);
    		  $('body').append('<div id="blackout"></div>');
    		  $('#postcheckJob'+operatorId).DataTable({
    			  "aaData": JSON.parse(json),
    			  "aoColumns": [
    				    { "mData": null, "mRender": function (data, type, full, meta){
    				    	return '<input type="radio">';
    				    	}},
    		            { "mData": "id",  "bVisible": false }, // <-- which values to use inside object
    		            { "mData": "name" },
    		            { "mData": "description" },
    		            { "mData": "agent_type" },
    		            { "mData": "insertion_time" }]
    		  });
    		  $(window).resize(centerBox);
    		  $(window).scroll(centerBox);
    		  centerBox(id);  
    		  $("#"+id).show();
        	  /* Get the id (the number appended to the end of the classes) */
      	    var scrollPos = $(window).scrollTop();
      	    /* Show the correct popup box, show the blackout and disable scrolling */
      	    $('#'+id).show();
      	    $('#blackout').show();
      	    $('html,body').css('overflow', 'hidden');
      	    /* Fixes a bug in Firefox */
      	    $('html').scrollTop(scrollPos);
      	    centerBox(id);
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
    	  function addBodyPrecheck(operatorId) {
    		  var id ='popup4-box-' + operatorId;
    		  $('body').append(`<div class="popup4-box" id="${id}">
    				  <span class="close btn btn-close"><em class="glyphicon glyphicon-remove"></em></span>
    				  <div class="bottom">
    				          <form class="bootstrap-form-with-validation" id="`+id+`-form">
    				          <input type="hidden" name="agent_type" id="agent_type_`+operatorId+`" value="configuration_differ_precheck">
    				          								<div name="precheckTable" id="precheckTable_`+precheckTable+`">
    				                                          <table align="center" class="workflow-table" id="precheck`+operatorId+`table">
    				                                          <tr>
    				                                              <td class="row-padding row-left-color"><label class="control-label" for="text-input">Job name</label></td>
    				                                              <td class="row-padding" align="center"><input  class="form-style" type="text" name="name" id="name_`+operatorId+`" value="" required=""></td>
    				                                          </tr>
    				                                          <tr>
    				                                              <td class="row-padding row-left-color"><label class="control-label" for="text-input">Description</label></td>
    				                                              <td class="row-padding" align="center"><input  class="form-style" type="text" name="description" id="description_`+operatorId+`"></td>
    				                                          </tr>
    				                                         <tr>
    				                                              <td class="row-padding row-left-color"><label class="control-label">command</label></td>
    				                                              <td class="row-padding"><textarea class="textarea-style" name="remoteCommand" id="remoteCommand_`+operatorId+`"></textarea>
    				                                              </td>
    				                                         </tr>
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
        	  $("#"+id).show();
        	  /* Get the id (the number appended to the end of the classes) */
      	    var scrollPos = $(window).scrollTop();
      	    /* Show the correct popup box, show the blackout and disable scrolling */
      	    $('#'+id).show();
      	    $('#blackout').show();
      	    $('html,body').css('overflow', 'hidden');
      	    /* Fixes a bug in Firefox */
      	    $('html').scrollTop(scrollPos);
      	    centerBox(id);
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
    	  function addBodyLoader(operatorId) {
    		  var id = 'popup-box-' + operatorId;
    		  $('body').append(`<div class="popup-box" id="${id}">
    				  <span class="close btn btn-close"><em class="glyphicon glyphicon-remove"></em></span>
    				    <div class="bottom">
    				        <form class="bootstrap-form-with-validation" id="`+ id + `-form"">
    				        <input type="hidden" name="agent_type" id="agent_type_`+operatorId+`" value="configuration_image_loader">
    				                                        <table align="center" class="workflow-table">
    				                                        <tr>
    				                                            <td class="row-padding row-left-color"><label class="control-label" for="text-input">Job name</label></td>
    				                                            <td class="row-padding" align="center"><input  class="form-style" type="text" name="name" id="name_`+operatorId+`"></td>
    				                                        </tr>
    				                                        <tr>
    				                                            <td class="row-padding row-left-color"><label class="control-label" for="text-input">Description</label></td>
    				                                            <td class="row-padding" align="center"><input  class="form-style" type="text" name="description" id="description_`+operatorId+`" ></td>
    				                                        </tr>
    				                                        <tr>
    				                                            <td class="row-padding row-left-color"><label class="control-label">Storage device</label></td>
    				                                            <td class="row-padding"><input class="form-style" type="text" name="deviceStorage" id="deviceStorage_`+operatorId+`">
    				                                            </td>
    				                                       </tr>
    				                                       <tr>
    				                                            <td class="row-padding row-left-color"><label class="control-label">FTP server name</label></td>
    				                                            <td class="row-padding"><input class="form-style" type="text" name="ftpServer" id="ftpServer_`+operatorId+`">
    				                                            </td>
    				                                       </tr>
    				                                            <tr>
    				                                            <td class="row-padding row-left-color"><label class="control-label">FTP server name</label></td>
    				                                            <td class="row-padding"><input class="form-style" type="text" name="ftpProtocol" id="ftpProtocol_`+operatorId+`">
    				                                            </td>
    				                                       </tr>
    				                                       <tr>
    				                                            <td class="row-padding row-left-color"><label class="control-label">FTP port</label></td>
    				                                            <td class="row-padding"><input class="form-style" type="text" name="ftpPort" id="ftpPort_`+operatorId+`">
    				                                            </td>
    				                                       </tr>
    				                                       <tr>
    				                                            <td class="row-padding row-left-color"><label class="control-label">FTP user</label></td>
    				                                            <td class="row-padding"><input class="form-style" type="text" name="ftpUser" id="ftpUser_`+operatorId+`">
    				                                            </td>
    				                                       </tr>
    				                                       <tr>
    				                                            <td class="row-padding row-left-color"><label class="control-label">FTP password</label></td>
    				                                            <td class="row-padding"><input class="form-style" type="text" name="ftpPassword" id="ftpPassword_`+operatorId+`">
    				                                            </td>
    				                                       </tr>
    				                                       <tr>
    				                                            <td class="row-padding row-left-color"><label class="control-label">Image file path</label></td>
    				                                            <td class="row-padding"><input class="form-style" type="text" name="ftpImage" id="ftpImage_`+operatorId+`">
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
        	  $("#"+id).show();
        	  /* Get the id (the number appended to the end of the classes) */
      	    var scrollPos = $(window).scrollTop();
      	    /* Show the correct popup box, show the blackout and disable scrolling */
      	    $('#'+id).show();
      	    $('#blackout').show();
      	    $('html,body').css('overflow', 'hidden');
      	    /* Fixes a bug in Firefox */
      	    $('html').scrollTop(scrollPos);
      	    centerBox(id);
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
    	  function addBodyEval(operatorId) {
    	  var id = 'popup6-box-' + operatorId;
    	  $('body').append(`<div class="popup6-box" id="${id}">
    		        <span class="close btn btn-close"><em class="glyphicon glyphicon-remove"></em></span>
    			    <div class="bottom">
    			        <form class="bootstrap-form-with-validation" id="`+ id + `-form"">
    			        <div>
    			                             	<label style="text-align:center;">Evaluation Name</label>
    			                             	<input type="text" name="name" id="name_`+operatorId+`" style="width: 140px; border-radius: 8px; height: 42px;  border-color: rgba(0, 0, 0, 0.37); border-width: 1px; text-align:center;">
    			                      </div>                  
    			                             <table class="evalTable choice-list" id="rulesTable">
    			                             <thead>
        			                             <th class="evaluation">
    			                             	<label style="text-align:center;">key</label>
    			                             </th>
    			                             <th class="evaluation">
    			                             <label>operator</label>
    			                             </th>
    			                             <th class="evaluation">
    			                             <label>value</label>
    			                             </th>
    			                             </thead>
    			                             <tbody>
    			                             <tr name="rule" id="rule0">
    			                             	<td>
    			                             	<input type="text" name="key" id="key_`+operatorId+`_rule0" style="width: 140px; border-radius: 8px; height: 33px;  border-color: rgba(0, 0, 0, 0.37); border-width: 1px;">
    			                             	</td>
    			                             	<td>
    			                             	<select name="operator" id="operator_`+operatorId+`_rule0" style="border-radius: 8px; height:33px; width:130px; text-align:center; background-color: white;  border-color: rgba(0, 0, 0, 0.37); border-width: 1px;" >
    			                                                                <option value="0" selected>choose from here </option>
    			                                                                <option value="contains" >contains</option><br></br>
    			                                                                <option value="not contains">not contains</option><br></br>
    			                                                                <option value="equal">equal</option>
    			                                                                <option value="not equal">not equal</option>
    			                                                            </select>
    			                             	</td>
    			                             	<td>
    			                             	<input type="text" name="value" id="value_`+operatorId+`_rule0" style="width: 140px; border-radius: 8px; height: 33px;  border-color: rgba(0, 0, 0, 0.37); border-width: 1px;">
    			                             	</td>
    			                             	
    			                             	
    			                             	
    			                             </tr>
    			                             </tbody>
    			                             </table>
    			                                                                  <a title="" class="add-choice"><button type="button" class="btn btn-sm btn-primary btn-create">Add choice</button></a>
    					                                      <button type="button" class="close-bottom btn btn-primary btn-close" >Done</button>

    			                                        
    			                                    </form>
    			    </div>
    			    
    			</div>`);
    	  
    	  
    	  
    	  $('body').append('<div id="blackout"></div>');
    	  var Index=1;
    	  
    	  $('.add-choice').click(function() {
    		  
  	        event.preventDefault();
  	        var newRow = jQuery(`<tr name="rule" id="rule`+Index+`" class="deleted_`+operatorId+`_rule`+Index+`">
  			                             	<td>
  			                             	<input type="text" name="key" id="key_`+operatorId+`_rule`+Index+`" style="width: 140px; border-radius: 8px; height: 33px;  border-color: rgba(0, 0, 0, 0.37); border-width: 1px;">
  			                             	</td>
  			                             	<td>
  			                             	
  			                             	<select name="operator" id="operator_`+operatorId+`_rule`+Index+`" style="border-radius: 8px; height:33px; width:130px; text-align:center; background-color: white;  border-color: rgba(0, 0, 0, 0.37); border-width: 1px;" >
  			                                                                <option value="0" selected>choose from here </option>
  			                                                                <option value="contains" >contains</option><br></br>
  			                                                                <option value="not contains">not contains</option><br></br>
  			                                                                <option value="equal">equal</option>
  			                                                                <option value="not equal">not equal</option>
  			                                                            </select>
  			                             	</td>
  			                             	<td>
  			                             	
  			                             	<input type="text" name="value"  id="value_`+operatorId+`_rule`+Index+`" style="width: 140px; border-radius: 8px; height: 33px;  border-color: rgba(0, 0, 0, 0.37); border-width: 1px;">
  			                             	</td>
  			                             	<td>
    			                             	<span class="glyphicon glyphicon-remove" onclick="deleteEvalRule(this);" id="deleted_`+operatorId+`_rule`+Index+`"></span>
  			                             	
  			                             </tr>`);
  	        jQuery('table.choice-list').append(newRow);
  	        Index++;
  	        

  	});
    	  
    	  
    	  
    	  $(window).resize(centerBox);
    	  $(window).scroll(centerBox);
    	  centerBox(id);  
    	  $("#"+id).show();
    	  /* Get the id (the number appended to the end of the classes) */
  	    var scrollPos = $(window).scrollTop();
  	    /* Show the correct popup box, show the blackout and disable scrolling */
  	    $('#'+id).show();
  	    $('#blackout').show();
  	    $('html,body').css('overflow', 'hidden');
  	    
  	    /* Fixes a bug in Firefox */
  	    $('html').scrollTop(scrollPos);
  	    centerBox(id);
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
    	  
    	  

    	  
    	  function getOperatorDataSenderClone($element) {
    	    	var operatorId = 'job-' + operator;
    	        var dataSender = {
    	          properties: {
    	            title:  '<a href=""  class="popup1-link-1 text-center" id="' + operatorId + '">Sender</a>' ,
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
    	        
    	        return dataSender;
    	      }
    	  function getOperatorDataParserClone($element) {
    	    	
    	        var operatorId = 'job-' + operator;
    	        var dataParser = {
    	          properties: {
    	            title: '<a  class="configurationParser popup2-link-1 text-center" id="' + operatorId + '">Parser</a>' ,
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

    	        
    	        return dataParser;
    	      }
    	  function getOperatorDataPostcheckClone($element) {
    	    	var operatorId = 'job-' + operator;
    	        var dataPostcheck = {
    	          properties: {
    	            title: '<a href=""  class="popup3-link-1 text-center" id="' + operatorId + '">Postcheck</a>' ,
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
    	      
    	        return dataPostcheck;
    	      }
    	    function getOperatorDataPrecheckClone($element) {
    	    	var operatorId = 'job-' + operator;
    	        var dataPrecheck = {
    	          properties: {
    	            title:  '<a href=""  class="popup4-link-1 text-center" id="' + operatorId + '">Precheck</a>' ,
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

    	        return dataPrecheck;
    	      }
    	    function getOperatorDataLoaderClone($element) {
    	    	var operatorId = 'job-' + operator;
    	        var dataLoader = {
    	          properties: {
    	            title: '<a href=""  class="popup-link-1 text-center" id="' + operatorId + '">Image Loader</a>' ,
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

    	        return dataLoader;
    	      }
    	    function getOperatorDataEvalClone($element) {
    	    	var operatorId = 'job-' + operator;
    	        var dataEval = {
    	          properties: {
    	            title: '<a href=""  class="popup6-link-1 text-center" id="' + operatorId + '">Evaluation</a>' ,
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

    	        return dataEval;
    	      }
    	    
    	  $draggableOperatorsParser.draggable({
    	        cursor: "move",
    	        opacity: 0.7,
    	        
    	        helper: 'clone', 
    	        appendTo: 'body',
    	        zIndex: 1000,
    	        
    	        
    	        helper: function(e) {
    	        	

    	     
    	          var $this = $(this);
    	          var dataParser = getOperatorDataParserClone($this);
    	          return $flowchart.flowchart('getOperatorElement', dataParser);
    	        },
    	        stop: function(e, ui) {
    	        	var operatorId = 'job-' + operator;
    	            var dataParser = {
    	              properties: {
    	                title: '<a  class="configurationParser popup2-link-1 text-center" id="' + operatorId + '">Parser</a>' ,
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
    	            var $this = $(this);
    	            var elOffset = ui.offset;
    	            var containerOffset = $container.offset();
    	            if (elOffset.left > containerOffset.left &&
    	                elOffset.top > containerOffset.top && 
    	                elOffset.left < containerOffset.left + $container.width() &&
    	                elOffset.top < containerOffset.top + $container.height()) {

    	                var flowchartOffset = $flowchart.offset();

    	                var relativeLeft = elOffset.left - flowchartOffset.left;
    	                var relativeTop = elOffset.top - flowchartOffset.top;

    	                var positionRatio = $flowchart.flowchart('getPositionRatio');
    	                relativeLeft /= positionRatio;
    	                relativeTop /= positionRatio;
    	                
    	                dataParser.left = relativeLeft;
    	                dataParser.top = relativeTop;
    	                
    	                $flowchart.flowchart('createOperator', operatorId, dataParser);
    	            }
    	            
    	            $('.configurationParser').click(function(){
    	    	    	var opid = this.id;
    	    	    	addBodyParser(opid);
    	    	    	});
    	    	    
    	    	operator++;
    	        }
    	    });
    	  
    	  $draggableOperatorsSender.draggable({
    	        cursor: "move",
    	        opacity: 0.7,
    	        
    	        helper: 'clone', 
    	        appendTo: 'body',
    	        zIndex: 1000,
    	        
    	        helper: function(e) {
    	     
    	          var $this = $(this);
    	          var dataSender = getOperatorDataSenderClone($this);
    	          return $flowchart.flowchart('getOperatorElement', dataSender);
    	        },
    	        stop: function(e, ui) {
    	        	var operatorId = 'job-' + operator;
    	            var dataSender = {
    	              properties: {
    	                title:  '<a class="configurationSender popup1-link-1 text-center" id="' + operatorId + '">Sender</a>' ,
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
    	                      
    	            var elOffset = ui.offset;
    	            var containerOffset = $container.offset();
    	            if (elOffset.left > containerOffset.left &&
    	                elOffset.top > containerOffset.top && 
    	                elOffset.left < containerOffset.left + $container.width() &&
    	                elOffset.top < containerOffset.top + $container.height()) {

    	                var flowchartOffset = $flowchart.offset();

    	                var relativeLeft = elOffset.left - flowchartOffset.left;
    	                var relativeTop = elOffset.top - flowchartOffset.top;

    	                var positionRatio = $flowchart.flowchart('getPositionRatio');
    	                relativeLeft /= positionRatio;
    	                relativeTop /= positionRatio;
    	                
    	                dataSender.left = relativeLeft;
    	                dataSender.top = relativeTop;
    	                
    	                $flowchart.flowchart('createOperator', operatorId, dataSender);
    	            }

    	            
    	    	    $('.configurationSender').click(function(){
    	    	    	var opid = this.id;
    	    	    	addBodySender(opid);
    	    	    	});
    	    	    
    	    	operator++;
    	        }
    	    });
		  var precheckTableIndex=0;

    	    $draggableOperatorsPostcheck.draggable({
    	        cursor: "move",
    	        opacity: 0.7,
    	        
    	        helper: 'clone', 
    	        appendTo: 'body',
    	        zIndex: 1000,
    	        
    	        helper: function(e) {
    	     
    	          var $this = $(this);
    	          var dataPostcheck = getOperatorDataPostcheckClone($this);
    	          return $flowchart.flowchart('getOperatorElement', dataPostcheck);
    	        },
    	        stop: function(e, ui) {

    	        	var operatorId = 'job-' + operator;
    	            var dataPostcheck = {
    	              properties: {
    	                title: '<a  class="differPostcheck popup3-link-1 text-center" id="' + operatorId + '">Postcheck</a>' ,
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
    	            
    	          
    	            var elOffset = ui.offset;
    	            var containerOffset = $container.offset();
    	            if (elOffset.left > containerOffset.left &&
    	                elOffset.top > containerOffset.top && 
    	                elOffset.left < containerOffset.left + $container.width() &&
    	                elOffset.top < containerOffset.top + $container.height()) {

    	                var flowchartOffset = $flowchart.offset();

    	                var relativeLeft = elOffset.left - flowchartOffset.left;
    	                var relativeTop = elOffset.top - flowchartOffset.top;

    	                var positionRatio = $flowchart.flowchart('getPositionRatio');
    	                relativeLeft /= positionRatio;
    	                relativeTop /= positionRatio;
    	                
    	                dataPostcheck.left = relativeLeft;
    	                dataPostcheck.top = relativeTop;
    	                
    	                $flowchart.flowchart('createOperator', operatorId, dataPostcheck);
    	            }
    	            
    	            
    	    	    $('.differPostcheck').click(function(){
    	    	    	
    	    	    	var opid = this.id;
    	    	    	addBodyPostcheck(opid);
    	    	    	event.preventDefault();
      	      	      var len=document.getElementById("precheckJob"+operatorId).getElementsByTagName("TR").length;
    	    	    		var removeTable=document.getElementById("precheckBody"+operatorId);
    	    	    		while(removeTable.hasChildNodes())
    	    	    		{
    	    	    			removeTable.removeChild(removeTable.firstChild);
    	    	    		}
    	    	    	var x=0;
    	      	        for(var rows=0;rows<precheckCount;rows++){
    	      	        	thisName=document.getElementById("name_"+precheckList[x]).value;
    	      	        	thisDescription=document.getElementById("description_"+precheckList[x]).value;
    	      	        	thisRemoteCommand=document.getElementById("remoteCommand_"+precheckList[x]).value;
    	      	        	var newTable = jQuery(`<tr name="rule" id="`+precheckTableIndex+`_`+operatorId+`">
          	    	      	        <td><input type="radio" class="'jobID_`+operatorId+`" name="jobID" onclick="myFunction(this.value)" id="id`+x+`_`+rows+`" value="`+precheckList[x]+`"></td>
          	    	      			                             	<td name="name">`+thisName+`</td>
          	    	      			                             	<td name="description">`+thisDescription+`</td>
          	    	      			                             	<td name="remoteCommand">`+thisRemoteCommand+`</td>
          	    	      			                             	
          	    	      			                             </tr>`);
    	      	        jQuery('table.precheck-list').append(newTable);
    	    	     	var checking=document.getElementById("id"+x+"_"+rows).value;

    	    	    	if(checking==checkedButton){
    	    	    	
    	    	    		document.getElementById("id"+x+"_"+rows).setAttribute("checked", true);
    	    	    	}
    	    	    	x++;

    	      	      precheckTableIndex++;
    	      	    
    	      	        	}
    	      	     
    	      	        
    	    	    	});
    	    	    
    	    	operator++;
    	        }
    	    });
    	    
    	    
    	    
    	    $draggableOperatorsPrecheck.draggable({
    	        cursor: "move",
    	        opacity: 0.7,
    	        
    	        helper: 'clone', 
    	        appendTo: 'body',
    	        zIndex: 1000,
    	        
    	        helper: function(e) {
    	     
    	          var $this = $(this);
    	          var dataPrecheck = getOperatorDataPrecheckClone($this);
    	          return $flowchart.flowchart('getOperatorElement', dataPrecheck);
    	        },
    	        stop: function(e, ui) {
    	        	var operatorId = 'precheckjob-' + operator;
    	        	
    	            var dataPrecheck = {
    	              properties: {
    	                name: operatorId,
    	            	title:  '<a class="differPrecheck popup4-link-1 text-center" id="' + operatorId + '">Precheck</a>' ,
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
    	            precheckList.push(operatorId);
        	    	

    	    	   
    	          
    	            var elOffset = ui.offset;
    	            var containerOffset = $container.offset();
    	            if (elOffset.left > containerOffset.left &&
    	                elOffset.top > containerOffset.top && 
    	                elOffset.left < containerOffset.left + $container.width() &&
    	                elOffset.top < containerOffset.top + $container.height()) {

    	                var flowchartOffset = $flowchart.offset();

    	                var relativeLeft = elOffset.left - flowchartOffset.left;
    	                var relativeTop = elOffset.top - flowchartOffset.top;

    	                var positionRatio = $flowchart.flowchart('getPositionRatio');
    	                relativeLeft /= positionRatio;
    	                relativeTop /= positionRatio;
    	                
    	                dataPrecheck.left = relativeLeft;
    	                dataPrecheck.top = relativeTop;
    	                
    	                $flowchart.flowchart('createOperator', operatorId, dataPrecheck);
    	            }
    	            
    	            $('.differPrecheck').click(function(){
    	            	var opid = this.id;
	    	    		addBodyPrecheck(opid);
    	    	    	});
        	    	operator++;
        	    	
        	    	precheckCount++;
    	        }
    	    });
    
     	var precheckTable = 0;
    	$draggableOperatorsFail.draggable({
        cursor: "move",
        opacity: 0.7,
        
        helper: 'clone', 
        appendTo: 'body',
        zIndex: 1000,
        
        helper: function(e) {

        	
            var operatorId = 'fail';
            var dataFail = {
              properties: {
                title: '<label class="text-center" id="' + operatorId + '"><B>Fail</B></label>' ,
                inputs: {
                    input_1: {
                      label: ' ',}
                  },
                  outputs: {
                      
      

                    }
              } 
            };

     
     
          return $flowchart.flowchart('getOperatorElement', dataFail);
        },
        stop: function(e, ui) {

        	
            var operatorId = 'fail';
            var dataFail = {
              properties: {
                title: '<label class="text-center" id="' + operatorId + '"><B>Fail</B></label>' ,
                inputs: {
                    input_1: {
                      label: ' ',}
                  },
                  outputs: {
                      
      

                    }
              } 
            };

            
          
            var elOffset = ui.offset;
            var containerOffset = $container.offset();
            if (elOffset.left > containerOffset.left &&
                elOffset.top > containerOffset.top && 
                elOffset.left < containerOffset.left + $container.width() &&
                elOffset.top < containerOffset.top + $container.height()) {

                var flowchartOffset = $flowchart.offset();

                var relativeLeft = elOffset.left - flowchartOffset.left;
                var relativeTop = elOffset.top - flowchartOffset.top;

                var positionRatio = $flowchart.flowchart('getPositionRatio');
                relativeLeft /= positionRatio;
                relativeTop /= positionRatio;
                
                dataFail.left = relativeLeft;
                dataFail.top = relativeTop;
                
                $flowchart.flowchart('addOperator', dataFail);
            }
        }
    });
    
    
    
    
    $draggableOperatorsSuccess.draggable({
        cursor: "move",
        opacity: 0.7,
        
        helper: 'clone', 
        appendTo: 'body',
        zIndex: 1000,
        
        helper: function(e) {

        	
            var operatorId = 'sucess';
            var dataSuccess = {
              properties: {
                title: '<label class="text-center" id="' + operatorId + '"><B>Success</B></label>' ,
                inputs: {
                    input_1: {
                      label: ' ',}
                  },
                  outputs: {
                    

                  }
              } 
            };

            
          
     
          return $flowchart.flowchart('getOperatorElement', dataSuccess);
        },
        stop: function(e, ui) {

        	
            var operatorId = 'sucess';
            var dataSuccess = {
              properties: {
                title: '<label class="text-center" id="' + operatorId + '"><B>Success</B></label>' ,
                inputs: {
                    input_1: {
                      label: ' ',}
                  },
                  outputs: {
                    

                  }
              } 
            };

            
          
        	var elOffset = ui.offset;
            var containerOffset = $container.offset();
            if (elOffset.left > containerOffset.left &&
                elOffset.top > containerOffset.top && 
                elOffset.left < containerOffset.left + $container.width() &&
                elOffset.top < containerOffset.top + $container.height()) {

                var flowchartOffset = $flowchart.offset();

                var relativeLeft = elOffset.left - flowchartOffset.left;
                var relativeTop = elOffset.top - flowchartOffset.top;

                var positionRatio = $flowchart.flowchart('getPositionRatio');
                relativeLeft /= positionRatio;
                relativeTop /= positionRatio;
                
                dataSuccess.left = relativeLeft;
                dataSuccess.top = relativeTop;
                
                $flowchart.flowchart('addOperator', dataSuccess);
            }
        }
    });
    
    $draggableOperatorsStart.draggable({
        cursor: "move",
        opacity: 0.7,
        
        helper: 'clone', 
        appendTo: 'body',
        zIndex: 1000,
        
        helper: function(e) {
     
          
        	var operatorId = 'start_workflow';
            var dataStart = {
              properties: {
                title: '<label class="text-center" id="' + operatorId + '"><B>Start</B></label>' ,
                inputs: {},
                  outputs: {
                	  success: {
                          label: '',},
                    

                  }
              } 
            };

          return $flowchart.flowchart('getOperatorElement', dataStart);
        },
        stop: function(e, ui) {
        	var operatorId = 'start_workflow';
            var dataStart = {
              properties: {
                title: '<label class="text-center" id="' + operatorId + '"><B>Start</B></label>' ,
                inputs: {},
                  outputs: {
                	  success: {
                          label: '',},
                    

                  }
              } 
            };

            var elOffset = ui.offset;
            var containerOffset = $container.offset();
            if (elOffset.left > containerOffset.left &&
                elOffset.top > containerOffset.top && 
                elOffset.left < containerOffset.left + $container.width() &&
                elOffset.top < containerOffset.top + $container.height()) {

                var flowchartOffset = $flowchart.offset();

                var relativeLeft = elOffset.left - flowchartOffset.left;
                var relativeTop = elOffset.top - flowchartOffset.top;

                var positionRatio = $flowchart.flowchart('getPositionRatio');
                relativeLeft /= positionRatio;
                relativeTop /= positionRatio;
                
                dataStart.left = relativeLeft;
                dataStart.top = relativeTop;
                
                $flowchart.flowchart('createOperator', operatorId, dataStart);
            }
        }
    });
    

    


    
    
    $draggableOperatorsLoader.draggable({
        cursor: "move",
        opacity: 0.7,
        
        helper: 'clone', 
        appendTo: 'body',
        zIndex: 1000,
        
        helper: function(e) {
     
          var $this = $(this);
          var dataLoader = getOperatorDataLoaderClone($this);
          return $flowchart.flowchart('getOperatorElement', dataLoader);
        },
        stop: function(e, ui) {

        	var operatorId = 'job-' + operator;
            var dataLoader = {
              properties: {
                title: '<a class="imageLoader popup-link-1 text-center" id="' + operatorId + '">Image Loader</a>' ,
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
            
            var elOffset = ui.offset;
            var containerOffset = $container.offset();
            if (elOffset.left > containerOffset.left &&
                elOffset.top > containerOffset.top && 
                elOffset.left < containerOffset.left + $container.width() &&
                elOffset.top < containerOffset.top + $container.height()) {

                var flowchartOffset = $flowchart.offset();

                var relativeLeft = elOffset.left - flowchartOffset.left;
                var relativeTop = elOffset.top - flowchartOffset.top;

                var positionRatio = $flowchart.flowchart('getPositionRatio');
                relativeLeft /= positionRatio;
                relativeTop /= positionRatio;
                
                dataLoader.left = relativeLeft;
                dataLoader.top = relativeTop;
                
                $flowchart.flowchart('createOperator', operatorId, dataLoader);
            }
            $('.imageLoader').click(function(){
            	var opid = this.id;
    	    	addBodyLoader(opid);
    	    	});
    	    
    	operator++;
        }
    });
 
    $draggableOperatorsEval.draggable({
        cursor: "move",
        opacity: 0.7,
        
        helper: 'clone', 
        appendTo: 'body',
        zIndex: 1000,
        
        helper: function(e) {
     
          var $this = $(this);
          var dataEval = getOperatorDataEvalClone($this);
          return $flowchart.flowchart('getOperatorElement', dataEval);
        },
        stop: function(e, ui) {

        	var operatorId = 'eval-' + operator;
            var dataEval = {
              properties: {
                title: '<a class="evaluation popup6-link-1 text-center" id="' + operatorId + '">Evaluation</a>' ,
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
            
          
        	var elOffset = ui.offset;
            var containerOffset = $container.offset();
            if (elOffset.left > containerOffset.left &&
                elOffset.top > containerOffset.top && 
                elOffset.left < containerOffset.left + $container.width() &&
                elOffset.top < containerOffset.top + $container.height()) {

                var flowchartOffset = $flowchart.offset();

                var relativeLeft = elOffset.left - flowchartOffset.left;
                var relativeTop = elOffset.top - flowchartOffset.top;

                var positionRatio = $flowchart.flowchart('getPositionRatio');
                relativeLeft /= positionRatio;
                relativeTop /= positionRatio;
                
                dataEval.left = relativeLeft;
                dataEval.top = relativeTop;
                
                $flowchart.flowchart('createOperator', operatorId, dataEval);
            }
            $('.evaluation').click(function(){
            	var opid=this.id;
            	addBodyEval(opid);
    	    	});
    	    
    	operator++;
        }
    });
    
  });
$(function() {
    $('#devices_configurationParser').change(function(){
        $('.devices_configurationParser').hide();
        $('#' + $(this).val()).show();
    });
});
$(function() {
    $('#devices_workflow').change(function(){
        $('.devices_workflow').hide();
        $('#' + $(this).val()).show();
    });
});
$(document).ready(function() {
	function showHideBoolean() {
    	this.addEventListener("click", function(){
    		var test = this.id;
    		if (test == 'workflow_is_scheduled_true') {
              $("#workflow_is_scheduled_true-div").show();
              document.getElementById('workflow_is_scheduled_true').value = 'false';
              document.getElementById('workflow_is_scheduled_false').value = 'true';

              }
    		if (test == 'workflow_is_scheduled_false') {
              $("#workflow_is_scheduled_true-div").hide();
              document.getElementById('workflow_is_scheduled_false').value = 'false';
              document.getElementById('workflow_is_scheduled_true').value = 'true';

            }
	})}
	function showHideBooleanPass() {
    	this.addEventListener("click", function(){
    		var test = this.id;
    		if (test == 'workflow_use_enable_password_1') {
              $("#workflow_use_enable_password_1-div").show();
              document.getElementById('workflow_use_enable_password_1').value = 'true';
              document.getElementById('workflow_use_enable_password_2').value = 'false';

              }
    		if (test == 'workflow_use_enable_password_2') {
              $("#workflow_use_enable_password_1-div").hide();
              document.getElementById('workflow_use_enable_password_2').value = 'false';
              document.getElementById('workflow_use_enable_password_1').value = 'true';

            }
	})}
	function showHideBooleanInverted() {
    	this.addEventListener("click", function(){
        	var test = this.id;
            if (test == 'workflow_use_device_credentials_1') {
              $('#workflow_use_device_credentials_1-div').show();
              document.getElementById('workflow_use_device_credentials_1').value = 'true';
              $('#workflow_use_device_credentials_2-div').hide();
              document.getElementById('workflow_use_device_credentials_2').value = 'false';
              }
            if (test == 'workflow_use_device_credentials_2') {
            	$('#workflow_use_device_credentials_2-div').show();
                document.getElementById('workflow_use_device_credentials_2').value = 'true';
                $('#workflow_use_device_credentials_1-div').hide();
                document.getElementById('workflow_use_device_credentials_1').value = 'false';
                }
	})
	}
	
	function showHideBooleanHostType() {
		if (this.id.indexOf('achoice') !== -1) {
			return;
		}		
		this.addEventListener("click", function(){
			var test = this.value;
        	if (test == 'hostList') {
            $("#workflow_hostChoice-1-div").show();
            $("#workflow_hostChoice-2-div").hide();
            }
          else {
            $("#workflow_hostChoice-2-div").show();
            $("#workflow_hostChoice-1-div").hide();
          }
	})}
	function showHideBooleanHostTypeMultiple() {
		if (this.id.indexOf('-div') !== -1) {
			return;
		}
    	this.addEventListener("click", function(){
        	var test = this.value;
        	if (test == 'load_host_command_file') {
            $("#" + "achoice1-div").show();
            $("#" + 'achoice2-div').hide();
            $("#" + 'achoice3-div').hide();     
            }
          else if (test == 'choose_host_write_command'){
        	  $("#" + 'achoice1-div').hide();
        	  $("#" + 'achoice2-div').show();
        	  $("#" + 'achoice3-div').hide();
          }
          else {
        	  $("#" + 'achoice1-div').hide();
        	  $("#" + 'achoice2-div').hide();
        	  $("#" + 'achoice3-div').show();
          }
	})}
	function showHideBooleanHostList() {
		
    	this.addEventListener("click", function(){
        	var test = this.value;
        	if (test == 'localisation') {
            $("#" + 'localisation-div').show();
            $("#" + 'deviceClass-div').hide();
            $("#" + 'group-div').hide();
            }
          else if (test == 'deviceClass'){
        	  $("#" + 'localisation-div').hide();
        	  $("#" + 'deviceClass-div').show();
        	  $("#" + 'group-div').hide();
          }
          else {
        	  $("#" + 'localisation-div').hide();
        	  $("#" + 'deviceClass-div').hide();
        	  $("#" + 'group-div').show();
          }
	})}

	$("input[name='useDeviceCredentials']").each(showHideBooleanInverted);
	$("input[name='editUseDeviceCredentials']").each(showHideBooleanInverted);
    $("input[name='useEnablePassword']").each(showHideBooleanPass);
    $("input[name='hostsType']").each(showHideBooleanHostType);
    $("input[name='is_scheduled']").each(showHideBoolean);
    $("input[id^='achoice']").each(showHideBooleanHostTypeMultiple);
 });
function centerBox(identifier) {
    if (typeof identifier != 'string') {
        return false;
    }
    var boxWidth = 500;
    /* Preliminary information */
    var winWidth = $(window).width();
    var winHeight = $(document).height();
    var scrollPos = $(window).scrollTop();
    /* auto scroll bug */
    /* Calculate positions */
    var disWidth = (winWidth - boxWidth) / 2
    var disHeight = 180;
    /* Move stuff about */
    $('#' + identifier).css({'width' : boxWidth+'px', 'left' : disWidth+'px', 'top' : disHeight+'px', });
    $('#blackout').css({'width' : winWidth+'px', 'height' : winHeight+'px'});
    return false;
  }
  $(document).ready();
  var dateNow = new Date();
  $('.form_datetime').datetimepicker({
      //language:  'fr',
      weekStart: 1,
      todayBtn:  1,
      autoclose: 1,
      todayHighlight: 1,
      startView: 2,
      forceParse: 0,
      showMeridian: 1,
      defaultDate:dateNow
  });
    jQuery(function(){
    jQuery('a.add-choice1').click(function(event){
        event.preventDefault();
        var newRow1 = jQuery('<tr><td><select  class="form-control" id="choosen_category1" style="height:50px; width:200px; text-align:center;" name="choosen_category1" ><option value="0" selected>--choose from here--</option><option value="30" >localisation</option><option value="31">device class</option><option value="32">group</option></select></td><td><select class="form-control" id="choices1" name="choices1" style="height:50px; width:200px; text-align:center;" ><option>--choose a device class--</option><option>choice1</option><option>choice2</option><option>choice3</option></select></td><td><input type="text" name="filter1" style="height:50px; width:200px; text-align:center;" /></td></tr>');
        jQuery('table.choice-list1').append(newRow1);
    });
});
    jQuery(function(){
    jQuery('a.add-choice2').click(function(event){
        event.preventDefault();
        var newRow2 = jQuery('<tr><td><select  class="form-control" id="choosen_category" style="height:50px; width:200px; text-align:center;" name="choosen_category" ><option value="0" selected>--choose from here--</option><option value="30" >localisation</option><br></br><option value="31">device class</option><br></br><option value="32">group</option></select></td><td><select class="form-control" id="choices" name="choices" style="height:50px; width:200px; text-align:center;" ><option>--choose a device class--</option><option>choice1</option><option>choice2</option><option>choice3</option></select></td><td><input type="text" name="filter" style="height:50px; width:200px; text-align:center;" /></td></tr>');
        jQuery('table.choice-list2').append(newRow2 );
    });
});
    jQuery(function(){
    jQuery('a.add-choice3').click(function(event){
        event.preventDefault();
        var newRow3 = jQuery('<tr><td><select  class="form-control" id="choosen_category" style="height:50px; width:200px; text-align:center;" name="choosen_category" ><option value="0" selected>--choose from here--</option><option value="40" >localisation</option><br></br><option value="41">device class</option><br></br><option value="42">group</option></select></td><td><select class="form-control" id="choices" name="choices" style="height:50px; width:200px; text-align:center;" ><option>--choose a device class--</option><option>choice1</option><option>choice2</option><option>choice3</option></select></td><td><input type="text" name="filter" style="height:50px; width:200px; text-align:center;" /></td></tr>');
        jQuery('table.choice-list3').append(newRow3 );
    });
});