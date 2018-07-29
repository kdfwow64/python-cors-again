var itemIndex = 1;
var elementIndex = 0;
var element_count = 0;
$(document).ready(function() {
    var max_fields      = 10; //maximum input boxes allowed
    var wrapper         = $("#element_list"); //Fields wrapper
    var add_button      = $("#add_element"); //Add button ID
    
    var x = 1; //initlal text box count
    $(add_button).on("click",function(e){
    	elementIndex++;//on add input button click
        e.preventDefault();
        if(x < max_fields){ //max input box allowed
            x++; //text box increment
            $(wrapper).append(`<table class="element_child" id="div_`+elementIndex+`"> 
            <tr>
            <div class="form-group">
                <td><label class="control-label" for="text-input">Name :</label></td>
                <td align="center"><input id="name_`+elementIndex+`" class="form-control" type="text" name="name"></td>
            </div>
            </tr>
            
            <tr>
            <div>
            
                <td><label class="control-label" for="text-input">Description :</label></td>
                <td align="center"><input id="description_`+elementIndex+`" class="form-control" type="text" name="description" ></td>
            </div>
            </tr>
            <tr>
                <td><label class="control-label" for="text-input">Remote Command :</label></td>
                <td align="center"><textarea id="remoteCommand_`+elementIndex+`" class="form-control" name="remoteCommand" style="margin-left: 23px;"></textarea></td>
            </tr>
            <tr>
                <td><label class="control-label" for="text-input">Checks :</label></td>
                
                <td>
                <br>
                <div class="text-right">
                
            <a id="add_check_` + elementIndex +`" class="add-ruleTask btn btn-primary btn-xs" role="button" data-toggle="modal" onclick="add_check(this)"> <em class="fa fa-plus"></em>Add More Checks</a>
            </div>
            
                 
                <div id="check_list_` + elementIndex +`">
            </div>
            <br>
            <a class="btn btn-primary send_dynamic_form " onclick="get_element_values(`+elementIndex+`)">Validate</a>
            <input type="hidden" value="" id="element_data_` + elementIndex +`">
            <a class="btn btn-danger remove_element" onclick="remove_element(`+elementIndex+`)">Remove</a>
                    
                    </table>`); //add input box
        }
        
    });
    
    $(wrapper).on("click",".remove_field", function(e){ //user click on remove text
        e.preventDefault(); $(this).parent('div').remove(); x--;
    })
    
    $(wrapper).on("click",".remove_element", function(e){
    	document.getElementById("div"+elementIndex)
    	//user click on remove text
        e.preventDefault(); document.getElementById("div_"+elementIndex).remove(); x--;
    })
});

function remove_element(element_id){
	document.getElementById("div_"+element_id).remove();
}

function add_check(element){
	
	var elementId = element.id.split("_")[2]
	var check_id = document.getElementById("check_list_" +elementId).childNodes.length
	var check_index =  check_id + "_" + elementId;
	$("#check_list_" +elementId).append(`<div class="check_child_div`+ elementId +`">
	<a type="text" class="btn btn-default" value="0" id="unit_`+ check_index +`"  href="#check_modal` + check_index + `" data-toggle="modal">Check `+ check_id +`<a href="#" class="remove_field">  X</a></a>
	
	<div class="modal fade container" role="dialog" tabindex="-1" id="check_modal`+ check_index +`">
    <div class="modal-dialog" role="document">
    <div class="modal-content continer" style="width:150%;">
    <div class="modal-header">
    <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">×</span></button>
    <h4 class="modal-title col col-xs-6">Rules</h4></div>
    <br>
    <input id="check_name_`+elementId+`_`+check_id+`" type="text" placeholder="Check Name" style="width:30%;">
    <a id="add_rule_`+elementId+`_`+check_id+`" class="add-ruleTask btn btn-primary btn-xs" role="button" data-toggle="modal" onclick="add_rule(this)"> <em class="fa fa-plus" onclick="add_rule(this)"></em>Add More Rules</a>
    <form>
    <div id="rule_list_`+elementId+`_`+check_id+`" class="text-center container dynamic_form">
    <div id="rule_`+elementId+`_`+check_id+`_0">
    <table>
    <tr>
    <td>
 	<select id="type_`+elementId+`_`+check_id+`_0" class="form-control">
                                    
                                    <option value="not_depend">Not Depend</option><br></br>
                                </select>
 	</td>
 	<td>
 	<select id="operator_`+elementId+`_`+check_id+`_0" class="form-control">
                                    <option value="" selected>Operator</option>
                                    <option value="GetAllRegExLine">GetAllRegExLine</option><br></br>
                                    <option value="GetAllRegEx">GetAllRegEx</option><br></br>
                                    <option value="GetMatchedRegExLine">GetMatchedRegExLine</option><br></br>
                                    <option value="GetMatchedRegEx">GetMatchedRegEx</option><br></br>
                                    <option value="not_contains">not_contains</option><br></br>
                                    <option value="equal">equal</option><br></br>
                                    <option value="not_equal">not_equal</option><br></br>
                                    <option value="contains">contains</option><br></br>
                                </select>
                                </td>
    <input type="hidden" id ="depend_on_`+elementId+`_`+check_id+`_0" value="0">
 	<td>
 	<input type="text" data-name="value" id="value_`+elementId+`_`+check_id+`_0" placeholder="Value">
 	</td>
    </tr>
    </table>
    
    </div>                             
    
</div>
<a class="btn btn-primary send_dynamic_form" onclick="get_check_values(`+elementId+`,`+check_id+`)" data-dismiss="modal">Validate</a>
<br>
<br>
</form>
</div>

</div>

</div>
<input type="hidden" id="check_data_`+elementId+`_`+check_id+`" value="">
</div>`); //add input box

}


function add_rule(element){
	
	var elementId = element.id.split("_")[2]
	var checkId = element.id.split("_")[3]
	var rule_index =  checkId + "_" + elementId;
	var rule_list = document.getElementById("rule_list_"+elementId+"_"+checkId)
	var rule_list_divs = rule_list.getElementsByTagName('div');
	var rule_id = rule_list.getElementsByTagName('div').length;
	var rule_id_1 = rule_id - 1; 
	var divArray = [];
	
	$("#rule_list_"+elementId+"_"+checkId).append(`<div>
	
	<table>
	<a href="#" class="btn btn-danger remove_field">X</a>
	<tr>
	<td>
	<select class="form-control" data-name="type" id="type_`+elementId+`_`+checkId+`_`+rule_id+`"> 
	<option value="not_depend" selected>Type</option> 
	<option value="depend" >Depend</option>
	<br></br> 
	<option value="not_depend">Not Depend</option>
	<br></br>
	</select>
	</td><td> 
	<select data-name="operator" id="operator_`+elementId+`_`+checkId+`_`+rule_id+`" class="form-control"> 
	<option value="" selected>Operator</option> 
	<option value="GetAllRegExLine">GetAllRegExLine</option>
	<br></br> 
	<option value="GetAllRegEx">GetAllRegEx</option>
	<br></br> 
	<option value="GetMatchedRegExLine">GetMatchedRegExLine</option>
	<br></br> 
	<option value="GetMatchedRegEx">GetMatchedRegEx</option>
	<br></br> 
	<option value="not_contains">not_contains</option>
	<br></br> 
	<option value="equal">equal</option>
	<br></br> 
	<option value="not_equal">not_equal</option>
	<br></br> 
	<option value="contains">contains</option>
	<br></br> </select> </td>
	<td> 
	<select id="depend_on_`+elementId+`_`+checkId+`_`+rule_id+`" data-name="depend_on" class="form-control" style="display: none;"> 
	<option value="0" selected>Depends on</option> 
	</select> 
	</td><td> 
	<input class="form-control" id="value_`+elementId+`_`+checkId+`_`+rule_id+`" type="text" data-name="value" placeholder="Value"> 
	</td>
	</tr></table></div>`);
	for (var i = 0; i < rule_id; i += 1) {
		  divArray.push(rule_list_divs[i].id);
		  $('#depend_on_'+elementId+'_'+checkId+'_'+rule_id).append(`<option value="rule`+i+`">rule`+i+`</option>`);
		}
	$('#type_'+elementId+'_'+checkId+'_'+rule_id).change(function(){
		if ($(this).val() == "depend" ){
			$('#depend_on_'+elementId+'_'+checkId+'_'+rule_id).show();
			
		}
		else if ($(this).val() == "not_depend" ){
			$('#depend_on_'+elementId+'_'+checkId+'_'+rule_id).hide();
			$('#depend_on_'+elementId+'_'+checkId+'_'+rule_id).value = "0";
		}
		
    });
    }

$(document).ready(function() {
$("input[name='is_validated']").click(function() {
    if ($("#is_validated_compliance_report").is(":checked")) {
      document.getElementById("is_validated_compliance_report").value = true;
    } else {
	   document.getElementById("is_validated_compliance_report").value = false;
    }
  });
});

function get_check_values(element_id, check_id){
	var rule_list = document.getElementById("rule_list_"+element_id+"_"+check_id);
	var rule_id = rule_list.getElementsByTagName('div').length;
	var check_name = document.getElementById("check_name_"+element_id+"_"+check_id).value;
	var check_data = {};
	check_data["name"] = check_name;
	check_data["rules"] = {};
	 for (var i = 0; i < rule_id; i++) {
		 var type = document.getElementById("type_"+element_id+"_"+check_id+"_"+i).value;
		 var operator = document.getElementById("operator_"+element_id+"_"+check_id+"_"+i).value;
		 var depend_on = document.getElementById("depend_on_"+element_id+"_"+check_id+"_"+i).value;
		 var value = document.getElementById("value_"+element_id+"_"+check_id+"_"+i).value;
		 check_data["rules"]["rule"+i] = {"type": type,"operator": operator, "depend_on": depend_on, "value": value};
		 if (type == "not_depend"){
			 delete check_data["rules"]["rule"+i]["depend_on"];
		 }
	    }
	 
	 var check_data_element = document.getElementById("check_data_"+element_id+"_"+check_id);	 
	 check_data_element.value = JSON.stringify(check_data);
}

function get_element_values(element_id){
	var check_list = document.getElementById("check_list"+element_id);
	var check_lenght = element_list.getElementsByClassName('check_child_div'+element_id).length;
	var element_name = document.getElementById("name_"+element_id).value;
	var element_remoteCommand = document.getElementById("remoteCommand_"+element_id).value;
	var element_description = document.getElementById("description_"+element_id).value;
	var element_data = {};
    element_data["job"] = {};
	element_data["checks"] = {};
	element_data["job"]["name"] = element_name;
	element_data["job"]["description"] = element_description;
	element_data["job"]["parameters"] = {"remoteCommand": element_remoteCommand};
	element_data["job"]["agent_type"] = "configuration_sender";
	for (var i = 1; i <= check_lenght; i++) {
		var check_data = document.getElementById("check_data_"+element_id+"_"+i).value;
		element_data["checks"]["check"+i]= JSON.parse(check_data)
	}
	var element_data_element = document.getElementById("element_data_"+element_id);
	element_data_element.value = JSON.stringify(element_data);
	alert("Element Data Loaded")
}

function get_all_data_values(){
	var element_list = document.getElementById("element_list");
	var element_lenght = element_list.getElementsByClassName('element_child').length;
	var element_list = [];
	for (var i = 0; i < element_lenght; i++) {
		var element_data = document.getElementById("element_data_"+i).value;
		element_list.push(element_data);
	}
	var element_list_data = document.getElementById("element_list_data");
	element_list_data.value = element_list;
}

$(document).ready(function() {
	$("input[name='use_device_credentials']").click(function() {
	     if ($("#compliance_report_provide_credentials").is(":checked")) {
	       $("#compliance_report_use_device_credentials-div").show();
	     } else {
	       $("#compliance_report_use_device_credentials-div").hide();
	     }
	   });
	
	$("input[name='use_enable_password']").click(function() {
	     if ($("#compliance_report_use_enable_password_true").is(":checked")) {
	       $("#compliance_report_use_enable_password_true-div").show();
	     } else {
	       $("#compliance_report_use_enable_password_true-div").hide();
	     }
	   });
	
	$("input[name='hostsType']").click(function() {
	     if ($("#compliance_report_hostList").is(":checked")) {
	       $("#compliance_report_hostList-div").show();
	     } else {
	       $("#compliance_report_hostList-div").hide();
	     }
	   });
	
	$("input[name='hostsType']").click(function() {
	     if ($("#compliance_report_hostFilter").is(":checked")) {
	       $("#compliance_report_hostFilter-div").show();
	     } else {
	       $("#compliance_report_hostFilter-div").hide();
	     }
	   });
	
	$("input[name='is_validated']").click(function() {
	     if ($("#is_validated_compliance_report").is(":checked")) {
	       document.getElementById("is_validated_compliance_report").value = true;
	     } else {
		   document.getElementById("is_validated_compliance_report").value = false;
	     }
	   });
});

$(function() {
    $('#devices_compliance_report').change(function(){
        $('.devices_compliance_report').hide();
        $('#' + $(this).val()).show();
    });
});