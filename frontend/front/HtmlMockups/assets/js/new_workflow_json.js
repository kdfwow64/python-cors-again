function getFormData(operatorId){ 
		var formData={};
		var parameters = {};
		var rules = {};
			formData["name"] = $('#name_'+operatorId).val();
			formData["description"] = $('#description_'+operatorId).val();
			parameters["remoteCommand"] = $('#remoteCommand_'+operatorId).val();
			parameters["remoteCommands"] = $('#remoteCommands_'+operatorId).val();
			parameters["deviceStorage"] = $('#deviceStorage_'+operatorId).val();
			parameters["ftpServer"] = $('#ftpServer_'+operatorId).val();
			parameters["ftpPort"] = $('#ftpPort_'+operatorId).val();
			parameters["ftpUser"] = $('#ftpUser_'+operatorId).val();
			parameters["ftpPassword"] = $('#ftpPassword_'+operatorId).val();
			parameters["ftpProtocol"] = $('#ftpProtocol_'+operatorId).val();

			parameters["ftpImage"] = $('#ftpImage_'+operatorId).val();
			parameters["keyList"] = $('#keyList_'+operatorId).val();
			if(document.getElementById("storage")){
			parameters["jobID"] = document.getElementById("storage").value;
			}
			formData["agent_type"] = $('#agent_type_'+operatorId).val();
			  if (operatorId.includes("job")){
				formData["parameters"] = parameters;
			  }
			  else if (operatorId.includes("eval")){ 
				  var rulesTable = document.getElementById("rulesTable");
					for (index=0;index<rulesTable.rows.length-1;index++){
						rules["rule"+index]={};
						rules["rule"+index]["key"] = $('#key_'+operatorId+'_rule'+index).val();
						rules["rule"+index]["operator"] = $('#operator_'+operatorId+'_rule'+index).val();
						rules["rule"+index]["value"] = $('#value_'+operatorId+'_rule'+index).val();
					
					}
			    formData["rules"] = rules;
			    formData["status"] = 'NEW';
			  }
			  
			data=JSON.stringify(formData);
			data = JSON.parse(data)
    return formData;
}
var input = document.getElementById("hostFile");
input.addEventListener("change", function(e) {
    var file = e.target.files[0];

    // Only render plain text files
    if (!file.type === "text/plain")
        return;

    var reader = new FileReader();

    reader.onload = function(event) {
        document.getElementById("hostList").value = event.target.result;
    };

    reader.readAsText(file);
});

	
function getGlobalData(){ 
		var globalData={};
		globalData["name"] = $('#name').val();
		globalData["description"] = $('#description').val();
		globalData["credentials"] = $('#workflow_use_device_credentials_1').val();
		if (globalData["credentials"] == "false"){
		  globalData["login"] = $('#login').val();
		  globalData["password"] = $('#password').val();
		  globalData["use_enable_password"] = $('#workflow_use_enable_password_1').val();
			if (globalData["use_enable_password"] == "true"){
			  globalData["enable_password"] = $('#enable_password').val();
			}
		}
		globalData["is_scheduled"] = $('#workflow_is_scheduled_false').val();
		if (globalData["is_scheduled"] == "true"){
		  globalData["schedule_time"] = $('#schedule_time').val();
		}
		var filtering = document.getElementById('Filter');

		  if (filtering.value == "hostFilter"){
			  globalData["element"] = $('#devices_workflow').val();
			  globalData["value"] = $('#value').val();
			  globalData["device"] = $('#device').val();
		  }
		  globalData["is_validated"] = $('#someSwitchOptionPrimary').val();

			global=JSON.stringify(globalData);
			global = JSON.parse(global)
    return globalData;
}

function getFlowchartData(){
var elementList={};
var $flowchart = $('#start');
var flowchartData = $flowchart.flowchart('getData');
var job_list = {};
var eval_list = {};
var link_list = {};
var global_data = getGlobalData("#globalData-form");

elementList = global_data;
for (var operatorId in flowchartData.operators) {
  if (operatorId.includes("job")){
    var job_data = getFormData(operatorId);
    job_list[operatorId] = job_data;
  }
  if (operatorId.includes("eval")){
	var eval_data = getFormData(operatorId);
	eval_list[operatorId] = eval_data;
	
  }  
  elementList["job_list"] = job_list;
  elementList["eval_list"] = eval_list;
}

for (var idx in flowchartData.links){
	var link = {};
	 var link_src_node_succ = {};
	 var link_dst_node_succ = {};
	 var link_src_node_fail = {};
	 var link_dst_node_fail = {};
	 if (flowchartData.links[idx].fromOperator == "start_workflow"){ 
		 elementList["start"] = flowchartData.links[idx].toOperator
   		}
	 else{
	      if (flowchartData.links[idx].fromConnector == 'success') {
	    	link_src_node_succ["uid"] = flowchartData.links[idx].fromOperator;
	    	if (flowchartData.links[idx].fromOperator.includes("job")){ 
	    	  link_src_node_succ["node_type"] = "job";
	    		}
	    	if (flowchartData.links[idx].fromOperator.includes("eval")){ 
		      link_src_node_succ["node_type"] = "eval";
		    	}
	    	
	    	link_dst_node_succ["uid"] = flowchartData.links[idx].toOperator;
	    	if (flowchartData.links[idx].toOperator.includes("job")){ 
	    	  link_dst_node_succ["node_type"] = "job";
		    	}
		    if (flowchartData.links[idx].toOperator.includes("eval")){ 
		      link_dst_node_succ["node_type"] = "eval";
			    }
	    	link["src_node"] = link_src_node_succ;
	    	link["dst_node"] = link_dst_node_succ;
	    	link["link_type"] = "SUCCESSFUL";
	    	
	      } 
	 
	      if (flowchartData.links[idx].fromConnector == 'failure') {
	    	  
	    	  link_src_node_fail["uid"] = flowchartData.links[idx].fromOperator;
		    	if (flowchartData.links[idx].fromOperator.includes("job")){ 
		    	  link_src_node_fail["node_type"] = "job";
		    		}
		    	if (flowchartData.links[idx].fromOperator.includes("eval")){ 
			      link_src_node_fail["node_type"] = "eval";
			    	}
		    	
		    	link_dst_node_fail["uid"] = flowchartData.links[idx].toOperator;
		    	if (flowchartData.links[idx].toOperator.includes("job")){ 
		    	  link_dst_node_fail["node_type"] = "job";
			    	}
			    if (flowchartData.links[idx].toOperator.includes("eval")){ 
			      link_dst_node_fail["node_type"] = "eval";
				    }
		    	link["src_node"] = link_src_node_fail;
		    	link["dst_node"] = link_dst_node_fail;
		    	link["link_type"] = "FAILED";	     
		    	}
	  link_list["link"+idx] = link;
	 }
	  }
elementList["link_list"] = link_list;
var workflowData= document.getElementById('workflow_data');
workflowData.value= JSON.stringify(elementList);
return elementList;
}