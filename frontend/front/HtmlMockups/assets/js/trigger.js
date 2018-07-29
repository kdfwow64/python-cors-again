$(document).ready(function() {	
toastr.options = {
    		  "closeButton": true,
    		  "debug": false,
    		  "newestOnTop": true,
    		  "progressBar": false,
    		  "positionClass": "toast-bottom-right",
    		  "preventDuplicates": false,
    		  "onclick": null,
    		  "showDuration": "300",
    		  "hideDuration": "1000",
    		  "timeOut": "5000",
    		  "extendedTimeOut": "1000",
    		  "showEasing": "swing",
    		  "hideEasing": "linear",
    		  "showMethod": "fadeIn",
    		  "hideMethod": "fadeOut"
    		}
    response = document.getElementById('request_response')
    try {
      var obj = JSON.parse(response.value)
      if(Object.keys(obj) == 'success'){
      	toastr.success(obj['success']);
      }
      if(Object.keys(obj) == 'error'){
      	toastr.error(obj['error']);
      }
      if(Object.keys(obj) == 'info'){
      	toastr.info(obj['info']);
      }
    }
    catch(err) {
      if (response != null){
      var obj = response.value;
      if(obj == 'Trigger Created'){
        toastr.success(obj);
      }
      else if(obj == 'Unknown Error'){
    	  toastr.error(obj);
      }
    }
    }
});


var ruleId = 1;
	
	var groupList=document.getElementById('groupList').value; 
	var myGroupJSON=JSON.parse(groupList);
	
	var deviceClassList=document.getElementById('deviceClassList').value;
	var mydeviceClassJSON=JSON.parse(deviceClassList);	
	
	var locationList=document.getElementById('locationList').value;
	var myLocationJSON=JSON.parse(locationList);
	
	var devicesList=document.getElementById('devicesList').value;
	var myDevicesJSON=JSON.parse(devicesList);
	  function deleteTriggerRule(tr){
		  console.log(tr);
	  
		  var deletedRule= tr.id;
		  console.log(deletedRule);
		  var chihaja=document.getElementsByClassName(deletedRule);
		  console.log(chihaja);
		  $("."+deletedRule).remove();
		  
	  }
	$(document).ready(function() {
		
        for (locations in myLocationJSON){
        	document.getElementById("locationJson").innerHTML+="<option value='"+myLocationJSON[locations]["id"]+"'>"+myLocationJSON[locations]["name"]+"</option>";
        }
		
        for (groups in myGroupJSON){
        
        	document.getElementById("groupJson").innerHTML+="<option value='"+myGroupJSON[groups]["id"]+"'>"+myGroupJSON[groups]["name"]+"</option>";


        }
        for (deviceClasses in mydeviceClassJSON){
        	document.getElementById("deviceClassJson").innerHTML+="<option value='"+mydeviceClassJSON[deviceClasses]["id"]+"'>"+mydeviceClassJSON[deviceClasses]["name"]+"</option>";


        }
        for (device in myDevicesJSON){ 
        	
        	document.getElementById("deviceJson").innerHTML+="<option value='"+myDevicesJSON[device]["id"]+"'>"+myDevicesJSON[device]["name"]+"</option>";

        }
        
        
		function showHideElement() {
			if (this.id.indexOf('-div') !== -1) {
				return;
			}		
			this.addEventListener("click", function(){
				var test = this.value;
	        	if (test == 'task') {
	            $("#task-div").show();
	            $("#job-div").hide();
	            
	            
	            }
	          else {
	            $("#job-div").show();
	            $("#task-div").hide();
	          }
		})}
/*		function showHideColumn() {
			if (this.id.indexOf('-div') !== -1) {
				return;
			}		
			this.addEventListener("click", function(){
				var test = this.value;
	        	if (test == 'name') {
	            $("#name-div").show();
	            $("#is_validate-div").hide();
	            $("#status-div").hide();
	            $("#agent_type-div").hide();
	            $("#chooseHere-div").hide();
	            }
	          else if(test == 'status') {
	        	  $("#name-div").hide();
		          $("#is_validate-div").hide();
		          $("#status-div").show();
		          $("#agent_type-div").hide();
		          $("#chooseHere-div").hide();
	          }
	          else if(test == 'is_validate') {
	        	  $("#name-div").hide();
		          $("#is_validate-div").show();
		          $("#status-div").hide();
		          $("#agent_type-div").hide();
		          $("#chooseHere-div").hide();
	          }
	          else if(test == 'agent_type') {
	        	  $("#name-div").hide();
		          $("#is_validate-div").hide();
		          $("#status-div").hide();
		          $("#agent_type-div").show();
		          $("#chooseHere-div").hide();
	          }
		})}*/
		
	    $("select[id='element1']").each(showHideElement);
/*	    $("select[id='column']").each(showHideColumn);
*/	 });
	
	
	$(function() {
	    $('#devices_trigger').change(function(){
	        $('.devices_trigger').hide();
	        $('#' + $(this).val()).show();
	        $('#groupSection').show();
	    });
	    
	});
	$(function() {
	    $('#column').change(function(){
	        $('.column').hide();
	        $('#' + $(this).val()).show();
	    });
	    
	});
	
function showHideClasses(tagId){
	//$('#devices_trigger'+tagId).change(function(){
        $('.devices_trigger'+tagId).hide();
        $('#' +event.target.value).show();
        $('#groupSection'+tagId).show();

}
function showHideJobClasses(tagJobId){
	//$('#devices_trigger'+tagId).change(function(){
        $('.column'+tagJobId).hide();
        $('#' +event.target.value).show();

}

/*	$(function() {
	    $('#group').click(function(){
	        
	        var getVal=$(this).val();
	        alert(getVal);
	        var setId=document.getElementsByClassName('groupSection');
	        setId.id=getVal;
	        $('.group').hide();
	        $('#' + $(this).val()).show();

	    });
	});*/
	jQuery(function(){
		
		$('#trigger_table').DataTable({
		
		 "columnDefs": [
		        {
		         "targets": [ 2 ] ,
		         "searchable": false
		        }, 
		    ]
		})
	
		
		
		//================================add rule==============================
/*		  
		$('#element1').change(function(){
			
			$('.column option').show();
			var table = document.getElementById("ruleTable");
			for(id=2;id<=table.rows.length;id++){
			$("#element"+id).hide();
			}
			 if ($(this).data('options') === undefined) {
     		    
     		    $(this).data('options', $('.column option').clone());
     		    
     		    //$(this).data('options', $('.element option').clone())
     		  }
			 var id=$(this).val()
			 var options = $(this).data('options').filter('[class=' + id + ']');
			 $('.column').html(options); 
			  
		});*/
		/*$('#element1').change(function(){
			
			$('.column option').show();
			var table = document.getElementById("ruleTable");
			for(id=2;id<=table.rows.length;id++){
			$("#element"+id).hide();
			}
			 if ($(this).data('options') === undefined) {
     		    
     		    $(this).data('options', $('.column option').clone());
     		    
     		    //$(this).data('options', $('.element option').clone())
     		  }
			 var id=$(this).val()
			 var options = $(this).data('options').filter('[class=' + id + ']');
			 $('.column').html(options); 
			  
		});*/
		
    jQuery('a.add-ruleJob').click(function(event){
    	
        event.preventDefault();
        ruleId++;
        var newRowJob = jQuery(` <tr id="rul` + ruleId + `" class="rul` + ruleId + `">
		                    <input type="hidden" id="rule` + ruleId + `">
		                    
		                  	 <td class="tight-color td-border" name="column">
                                 <Select class="form-control " onclick="showHideJobClasses(` + ruleId + `)" id="column` + ruleId + `" name="column" style="width:135px;">
                                 	<option value="None" selected>--choose from here--</option>
		                            <option class="job" value="name` + ruleId + `"  >name</option>                            
		                            <option class="job" value="is_validated` + ruleId + `" >is_validated</option>
		                            <option class="job" value="status` + ruleId + `" >status</option>
		                            <option class="job" value="agent_type` + ruleId + `" >agent_type</option>
                                 </Select>
                            </td> 
                            
                          
									  
									
		                    <td class="right-color td-border">
									<Select id="operation` + ruleId + `" name="operationJob" class="form-control">
										<option value="None" selected>--choose from here--</option>                               
			                            <option value="equals">equals</option>
			                            <option value="not_equals">not equals</option>
			                       	</Select>
		                   	</td>
		                       
		                    <td class="right-color td-border">
		                    
		                    <div id="chooseHere-div" class="column` + ruleId + `">
		                    <Select id="chooseHere` + ruleId + `" name="valueJobChoose" class="form-control">
										<option value="None" selected>--choose from here--</option>                               
			                       	</Select>
			                 </div>
			                 
		                    <div id="status` + ruleId + `" class="column` + ruleId + `" style="display:none;">
		                    <Select name="status" id="stat` + ruleId + `" class="form-control">
										<option value="None" selected>--choose from here--</option>                               
			                            <option value="SUCCESSFUL">SUCCESSFUL</option>
			                            <option value="FAILED">FAILED</option>
			                       	</Select>
			                 </div>
			                 <div id="is_validated` + ruleId + `" class="column` + ruleId + `" style="display:none;">
		                    <Select name="is_validated" id="valid` + ruleId + `" class="form-control">
										<option value="None" selected>--choose from here--</option>                               
			                            <option value="true">True</option>
			                            <option value="false">False</option>
			                       	</Select>
			                 </div>
			                 <div id="agent_type` + ruleId + `" class="column` + ruleId + `" style="display:none;">
		                    <Select name="agent_type" id="agent` + ruleId + `" class="form-control">
										<option value="None" selected>--choose from here--</option>                               
			                            <option value="configuration_differ_precheck">configuration differ precheck</option>
			                            <option value="configuration_differ_postcheck">configuration differ postcheck</option>
			                            <option value="configuration_parser">configuration parser</option>
			                            <option value="configuration_sender">configuration sender</option>
			                            <option value="configuration_image_loader">configuration image loader</option>
			                       	</Select>
			                 </div>
			                 <div id="name` + ruleId + `" class="column` + ruleId + `" style="display:none;">
			                 <input type="text" id="nam` + ruleId + `" name="valueJobName" value="">
			                 </div>
		                   	</td>
		                   <td>
		                   	<span class="glyphicon glyphicon-remove btn btn-danger btn-s" onclick="deleteTriggerRule(this);" id="rul` + ruleId + `"></span>
		                   	</td>
                    </tr>`);
       
       
        jQuery('table.rule-list').append(newRowJob);
        
        
        
       
    });


    
   jQuery('a.add-ruleTask').click(function(event){
    	
        event.preventDefault();
        ruleId++;
        var newRow = jQuery(`
		                    <tr id="rul` + ruleId + `" class="rul` + ruleId + `">
		                    <input type="hidden" id="rule` + ruleId + `"/>
		                    
		                    
		                    <td class="right-color td-border" >
                                 <Select class="form-control " onclick="showHideClasses(` + ruleId + `)" id="devices_trigger` + ruleId + `" style="width:180px;">
                                 	<option selected>--choose from here--</option>
                                 	<option class="task" value="all` + ruleId + `">all</option>
		                            <option class="task" value="group` + ruleId + `">group</option>
		                            <option class="task" value="location` + ruleId + `">location</option>
		                            <option class="task" value="deviceClass` + ruleId + `">deviceCLass</option>

                                 </Select>
                            </td> 
                            
                          
									 
									 <td class="right-color td-border" >
									 
									 
									 
									 <div id="location` + ruleId + `" class="devices_trigger` + ruleId + `" hidden="true"> 
									 <Select name="location" id="locationJson` + ruleId + `" class="select form-control" style="width:100px;">
                                     <option value="None" selected>--choose frome here--</option>
							 
                                     </Select>
                                     </div>
                                      
                                       
									 <div id="deviceClass` + ruleId + `" class="devices_trigger` + ruleId + `" hidden="true">
									 <Select name="deviceClass" id="deviceClassJson` + ruleId + `" class="select form-control" style="width:100px;">
									 <option value="None" selected>--choose frome here--</option>
                           
                                       </Select>
                                       </div>
									 
									 
									 <div id="group` + ruleId + `" class="devices_trigger` + ruleId + `" hidden="true" style="width:100px;">
									
									 <Select name="group" id="groupJson` + ruleId + `" class="select form-control">
                                     <option value="None" selected>--choose frome here--</option>
					
                                     </Select>
                                   </div>
    
									 </td>
								<td id="groupSection` + ruleId + `" style="width:100px; border:0px" hidden="true">
								  <Select name="device" id="deviceJson` + ruleId + `" class="select form-control">
                                     <option value="all" selected>all</option>

                                     </Select>
                                    
								</td>
                            
		                    <td class="right-color td-border" style="width:180px;">
									<Select id="operation` + ruleId + `" name="operation" class="form-control">
										<option value="None" selected>--choose from here--</option>                               
			                            <option value="equals">equals</option>
			                            <option value="not_equals">not equals</option>
			                       	</Select>
		                   	</td>
		                       
		                    <td class="right-color td-border" style="width: 180px;">
		                    <Select id="value` + ruleId + `" name="value" class="form-control">
										<option value="None" selected>--choose from here--</option>                               
			                            <option value="SUCCESSFUL">SUCCESSFUL</option>
			                            <option value="FAILED">FAILED</option>
			                       	</Select>
		                   	</td>
		                   	<td>
		                   	<span class="glyphicon glyphicon-remove btn btn-danger btn-s" onclick="deleteTriggerRule(this);" id="rul` + ruleId + `"></span>
		                   	</td>
                    </tr>`);
      
        jQuery('table.rule-list').append(newRow);
        
        
        
        for (groups in myGroupJSON){
            
        	document.getElementById("groupJson"+ ruleId).innerHTML+="<option value='"+myGroupJSON[groups]["id"]+"'>"+myGroupJSON[groups]["name"]+"</option>";


        }
        for (locations in myLocationJSON){
        	document.getElementById("locationJson"+ ruleId).innerHTML+="<option value='"+myLocationJSON[locations]["id"]+"'>"+myLocationJSON[locations]["name"]+"</option>";
        }
		
        
        for (deviceClasses in mydeviceClassJSON){
        	document.getElementById("deviceClassJson"+ ruleId).innerHTML+="<option value='"+mydeviceClassJSON[deviceClasses]["id"]+"'>"+mydeviceClassJSON[deviceClasses]["name"]+"</option>";


        }
        for (device in myDevicesJSON){
        	document.getElementById("deviceJson"+ ruleId).innerHTML+="<option value='"+myDevicesJSON[device]["id"]+"'>"+myDevicesJSON[device]["name"]+"</option>";


        }
    });

    
    
    
    $('#formRule').submit(function(event) {
    	
		var table = document.getElementById("ruleTable");
		var rule=new Array();
		
		for(ruleId=1;ruleId<=table.rows.length-1;ruleId++){
			if (ruleId == 1){
     			element_val = $('#element1').val();
		     	location_val = $('#locationJson').val();
				deviceClass_val = $('#deviceClassJson').val();
				group_val = $('#groupJson').val();
				device_val = $('#deviceJson').val();
				if(element_val=="task"){
					operation_val=  $('#operation1').val();
					value_val =  $('#value1').val();
				}
				else{
					column_val = $('#column').val().replace(/[0-9]/g, '');
					operation_val=  $('#operation').val();
					value_name= $('#nam').val();
					value_agent_type= $('#agent').val();
					value_status= $('#stat').val();
					value_is_validated= $('#valid').val();
				}
				

			}else{
				
				element_val = $('#element1').val();
				if(element_val=="task"){
					location_val = $('#locationJson'+ruleId).val();
					deviceClass_val = $('#deviceClassJson'+ruleId).val();
					group_val = $('#groupJson'+ruleId).val();
					device_val = $('#deviceJson'+ruleId).val();
					operation_val=  $('#operation'+ruleId).val();
					value_val =  $('#value'+ruleId).val();
				}else{
					column_val = $('#column'+ruleId).val().replace(/[0-9]/g, '');
					operation_val=  $('#operation'+ruleId).val();
					value_name= $('#nam'+ruleId).val();
					value_agent_type= $('#agent'+ruleId).val();
					value_status= $('#stat'+ruleId).val();
					value_is_validated= $('#valid'+ruleId).val();
				}
				
				
				
			}
			if(element_val=="task"){
			rule.push({
				
				/*					  
			       
			  	element: element_val,
		    	column:$('#column'+ruleId).val(),
		    	operation: $('#operation'+ruleId).val(),
		    	value: $('#value'+ruleId).val()
		 
    		*/
				element: element_val,
				location: location_val,
				deviceClass: deviceClass_val,
				group: group_val,
				device: device_val,
				operation: operation_val,
				value: value_val,
				
					});
			}else{
				
				if(column_val == 'name'){
				rule.push({
				element: "job",
				column: column_val,
				operation: operation_val,
				value: value_name,
				});
				}
			if(column_val == 'agent_type'){
				rule.push({
				element: "job",
				column: column_val,
				operation: operation_val,
				value: value_agent_type,
			});
			}
			if(column_val == 'status'){
				rule.push({
				element: "job",
				column: column_val,
				operation: operation_val,
				value: value_status,
			});
			}
			if(column_val =='is_validated'){
				rule.push({
				element: "job",
				column: column_val,
				operation: operation_val,
				value: value_is_validated,
			});
			}
			
		}  
    }

		data=JSON.stringify(rule);	
	    var rules=document.getElementById("rule1");		    
	    rules.value=data;
    })
    
                  //=============================edit rule===================================
     
    
    
    jQuery('a.edit_rule').click(function(event){
    	
    	var ids=this.id
    	var td_table = document.getElementById("edit_ruleTable_"+ids);
    	
    	for(var i=2;i<=td_table.rows.length;i++){
    	
    	 td_rule=document.getElementById("td_"+ids+"_"+i)
    		
    	}
    });
    
   
    jQuery('a.edit_add_rule').click(function(event){
    	event.preventDefault();
    	   
    	var index=this.id;
    	var edit_table = document.getElementById("edit_ruleTable_"+index);
    	
    	var edit_rule_id = edit_table.rows.length-2;
    	
        var newRow = jQuery(`
		                    <tr id="edit_rul_` + edit_rule_id + `">		                    
		                    <td class="right-color td-border">		                   
				                    <Select class="form-control" onclick="showHideJobClasses(` + edit_rule_id + `)" id="column` + edit_rule_id + `" name="column" style="width:135px;">                      
                                 	<option value="None" selected>--choose from here--</option>
		                            <option value="name` + edit_rule_id + `"  >name</option>                            
		                            <option value="is_validated` + edit_rule_id + `" >is_validated</option>
		                            <option value="status` + edit_rule_id + `" >status</option>
		                            <option value="agent_type` + edit_rule_id + `" >agent_type</option>
                                 </Select>
		                    </td>
		                     <td class="right-color td-border">
								<Select id="edit_operation_` + edit_rule_id + `" class="form-control">
									<option selected>--choose from here--</option>                               
		                            <option value="equals">equals</option>
		                            <option value="not equals">not equals</option>
		                       	</Select>
		                   	</td>
		                    
		                    <td class="right-color td-border">
		                    
		                    <div id="chooseHere-div" class="column` + edit_rule_id + `">
		                    <Select id="chooseHere` + edit_rule_id + `" name="valueJobChoose" class="form-control">
										<option value="None" selected>--choose from here--</option>                               
			                       	</Select>
			                 </div>
			                 
		                    <div id="status` + edit_rule_id + `" class="column` + edit_rule_id + `" hidden="true">
		                    <Select name="status" id="stat` + edit_rule_id + `" class="form-control">
										<option value="None" selected>--choose from here--</option>                               
			                            <option value="SUCCESSFUL">SUCCESSFUL</option>
			                            <option value="FAILED">FAILED</option>
			                       	</Select>
			                 </div>
			                 <div id="is_validated` + edit_rule_id + `" class="column` + edit_rule_id + `" hidden="true">
		                    <Select name="is_validated" id="valid` + edit_rule_id + `" class="form-control">
										<option value="None" selected>--choose from here--</option>                               
			                            <option value="true">True</option>
			                            <option value="false">False</option>
			                       	</Select>
			                 </div>
			                 <div id="agent_type` + edit_rule_id + `" class="column` + edit_rule_id + `" hidden="true">
		                    <Select name="agent_type" id="agent` + edit_rule_id + `" class="form-control">
										<option value="None" selected>--choose from here--</option>                               
			                            <option value="configuration_differ_precheck">configuration differ precheck</option>
			                            <option value="configuration_differ_postcheck">configuration differ postcheck</option>
			                            <option value="configuration_parser">configuration parser</option>
			                            <option value="configuration_sender">configuration sender</option>
			                            <option value="configuration_image_loader">configuration image loader</option>
			                       	</Select>
			                 </div>
			                 <div id="name` + edit_rule_id + `" class="column` + edit_rule_id + `" hidden="true">
			                 <input type="text" id="nam` + edit_rule_id + `" name="valueJobName" value="">
			                 </div>
		                   	</td>
		                   <td>
		                   	<span class="glyphicon glyphicon-remove btn btn-danger btn-s" onclick="deleteTriggerRule(this);" id="rul` + edit_rule_id + `"></span>
		                   	</td>
		                   
		                       	
		                    
                    </tr>`);
       
        jQuery('table#edit_ruleTable_'+index).append(newRow);

       
    });
 
 });         
		  
	 function showId(obj) {
		 
		 var table = document.getElementById("edit_ruleTable_"+obj);
		
			for(index=2;index<=table.rows.length;index++){
			$("#edit_element_"+obj+"_"+index).hide();
			}
			
		 	$('#edit_element_'+obj+'_1').change(function(){
			 
			 for(ruleId=1;ruleId<=table.rows.length;ruleId++){

				 $('.edit_column_'+obj+' option').show();
			 
			    if ($(this).data('options') === undefined) {
			    	 $(this).data('options', $('#edit_column_'+obj+'_'+ruleId+' option').clone());
			    }
			   
			 var id=$(this).val()
			 var options = $(this).data('options').filter('[class=' + id + ']');
			 $('.edit_column_'+obj).html(options);
			 
			 }	 
	});
		 
	        $('.edit_formRule').submit(function(event) {
	        	
	    		var table = document.getElementById("edit_ruleTable_"+obj);
	    		var rule=new Array();
	    		
	    		for(ruleId=1;ruleId<=table.rows.length;ruleId++){
	    			if (ruleId == 1){
	    				edit_element_val = $('#edit_element_'+obj+'_'+ruleId).val()
	    			}else{
	    				edit_element_val = $('#edit_element_'+obj+'_1').val()
	    			}
	    			 rule.push({
	    					
	    					element: edit_element_val,
	    			    	column:$('#edit_column_'+obj+'_'+ruleId).val(),
	    			    	operation: $('#edit_operation_'+obj+'_'+ruleId).val(),
	    			    	value: $('#edit_value_'+obj+'_'+ruleId).val()
	    			})
	    			
	    			data=JSON.stringify(rule);
	    			var rules=document.getElementById("edit_rules_"+obj+"_"+ruleId);
	    		    rules.value=data;
	    	}
	     });  
	  }
	 
	 
	 function enabledValueTrigger(){

			var enabledValue=document.getElementById('enabledTrigger');
			enabledValue.value = ( $("#enabledTrigger").is(':checked') ) ? true : false;
		}

	 function enabledValueTriggerEdit(){

			var enabledValue=document.getElementById('enabledTriggerEdit');
			enabledValue.value = ( $("#enabledTriggerEdit").is(':checked') ) ? true : false;
		}