$(document).ready(function() {
    $('#dataTableId').DataTable( {
        "pagingType": "full_numbers",
        "order":[4, 'desc'],
        "columnDefs": [
            {
                "targets": [ 8 ],
                "searchable": false
            }, 
        ]
    } );
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
      if(obj == 'Job created'){
        toastr.success(obj);
      }
      else if(obj == 'Unknown Error'){
    	  toastr.error(obj);
      }
    }
    }
      
} );
$(document).ready(function() {
function refresh(){
	  $.getJSON("http://"+window.location.host.split(':')[0]+ ":5000/job",
			   function(data) {
		  var arrayLength = data['jobs'].length;
		  var array = data['jobs'];
		  var status = {'failed': 0, 'new': 0, 'ongoing': 0, 'queued': 0, 'successful': 0};
		  for (var i = 0; i < arrayLength; i++)
	      {
			  var start_time = Date.parse(data['jobs'][i].processing_start_time);
			  var end_time = Date.parse(data['jobs'][i].processing_end_time);
			  if (end_time == null || start_time == null)
			  {
				  var duration = -1;
			  }
			  var duration = (end_time - start_time)/1000;
			  //console.log(duration);
			  $("#dot_status_" + data['jobs'][i].id).attr('class', 'glyphicon dot-status-' + data['jobs'][i].status.toLowerCase());
			  $("#dot_status_" + data['jobs'][i].id).attr('title', data['jobs'][i].status);
			  //console.log("duration_" + data['tasks'][i].id);
			  //document.getElementById("duration_" + data['tasks'][i].id).value = duration;
			  //document.getElementById("dot_status_" + data['tasks'][i].id).className = "glyphicon dot-status-" + data['tasks'][i].status.toLowerCase();
			  //document.getElementById("dot_status_" + data['tasks'][i].id).title = data['tasks'][i].status;


		  }
		  for (var key in status) {
	          $("span[title='" + key + "'] > span").html(status[key]);
	      }
		  
			   });
	  }
	  
	      window.setInterval(function(){
	    	  refresh()
	    	  },3000);
	      
} );
	      
$(document).ready(function() {
    $('#precheckTableId').DataTable( {
        "pagingType": "full_numbers",
        "order":[5, 'desc'],
        
    } );
} );


$(document).ready(function() {
    $('#taskreporttable').DataTable( {
        "pagingType": "full_numbers",
        "order":[3, 'desc'],
        "columnDefs": [
            {
                "targets": [ 6 ],
                "searchable": false
            }, 
        ]
    } );
	function showHideBoolean() {
    	this.addEventListener("click", function(){
        	var test = this.value;
            if (test == 'hidden') {
              $("#" + this.id + '-div').show();
              }
	})}
    $("button[name='hiddentd']").each(showHideBoolean);

    
} );

$(document).ready(function() {
    $('#jobreporttable').DataTable( {
        "pagingType": "full_numbers",
        "order":[3, 'desc'],
        "columnDefs": [
            {
                "targets": [ 9 ],
                "searchable": false
            }, 
        ]
    } );
} );

$(document).ready(function() {
    $('#devicereporttable').DataTable( {
        "pagingType": "full_numbers",
        "order":[3, 'desc'],
    } );
} );
$(function() {
    $('#btnAdd1').click(function() {
        $('.td1').toggle();
    });
});

$(document).ready(function() {
	
	
	function showHideBooleanEdit() {
		
		/*var chihaja = 0;
		for (chihaja=0; chihaja<1000; chihaja++){
	    document.getElementById("edit_configuration_sender_credentials").id = "edit_configuration_sender_credentials"+chihaja+"-div";*/
		
		
		
		if (this.id.indexOf('-div') !== -1) {
			return;
		}
    	this.addEventListener("click", function(){
        	var test = this.value;
        	if (test == 'true') {
            $("#" + "use_device_credentials"+"-div").hide();
            
            }
       
          else {
        	  $("#" + "use_device_credentials"+"-div").show();

          }
	})
    	/*}*/
	}
	
	function showHideBooleanHostTypeMultipleEdit() {
		if (this.id.indexOf('-div') !== -1) {
			return;
		}
		
		
    	this.addEventListener("click", function(){
        	var test = this.value;
        	
        	if (test == 'load_host_command_file') {
            $("#" + "edit_achoice1-div").show();
            $("#" + 'edit_achoice2-div').hide();
            $("#" + 'edit_achoice3-div').hide();
            
            }
          else if (test == 'choose_host_write_command'){
        	  $("#" + 'edit_achoice1-div').hide();
        	  $("#" + 'edit_achoice2-div').show();
        	  $("#" + 'edit_achoice3-div').hide();
          }
          else {
        	  $("#" + 'edit_achoice1-div').hide();
        	  $("#" + 'edit_achoice2-div').hide();
        	  $("#" + 'edit_achoice3-div').show();
          }
        	
	})}

	function showEditSender() {
    	this.addEventListener("click", function(){
    		
    		/*$(function() {
    		    $('#editConfigurationSender').change(function(){
    		        $('.editConfigurationSender').hide();
    		        $('#' + $(this).val()).show();
    		    });
    		});
    		*/
    	
        	var test = this.value;
            if (test == 'configuration_sender') {
              $("#" + "editConfigurationSender").show();
              //$("#" + 'editConfigurationSender').show();            
              //$("#" + 'editImageLoader').hide();
              //$("#" + 'editDifferPostcheck').hide();
              //$("#" + 'editDifferPretcheck').hide();
              }
            /*else if (test == 'configuration_sender') {
            	$("#" + 'editConfigurationSender').show();
                $("#" + 'editConfigurationParser').hide();
                $("#" + 'editImageLoader').hide();
                $("#" + 'editDifferPostcheck').hide();
                $("#" + 'editDifferPretcheck').hide();
            }
            else if (test == 'image_loader') {
            	$("#" + 'editConfigurationSender').show();
                $("#" + 'editConfigurationParser').hide();
                $("#" + 'editImageLoader').hide();
                $("#" + 'editDifferPostcheck').hide();
                $("#" + 'editDifferPretcheck').hide();
            }*/
          
    	})};
    	
	    $("input[name='editUseDeviceCredentials']").each(showHideBooleanEdit);

    	//$("input[name='agent_type']").each(showEditSender);
    	$("input[id^='edit_achoice']").each(showHideBooleanHostTypeMultipleEdit);
	});

