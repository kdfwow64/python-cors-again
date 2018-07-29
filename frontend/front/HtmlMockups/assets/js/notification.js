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
      if(obj == 'Notification Created'){
        toastr.success(obj);
      }
      else if(obj == 'Unknown Error'){
    	  toastr.error(obj);
      }
    }
    }
  
function showHideBooleanHostTypeMultiple() {
		if (this.id.indexOf('-div') !== -1) {
			return;
		}
    	this.addEventListener("click", function(){
        	var test = this.value;
        	if (test == 'email') {
            $("#" + "email-div").show(); 
            $("#" + 'api-div').hide();
            $("#" + 'command-div').hide();
            
            }
          else if (test == 'api'){
        	  $("#" + 'email-div').hide();
        	  $("#" + 'api-div').show();
        	  $("#" + 'command-div').hide();
          }
          else {
        	  $("#" + 'email-div').hide();
        	  $("#" + 'api-div').hide();
        	  $("#" + 'command-div').show();
          }
	})}

$("select[id^='selecting']").each(showHideBooleanHostTypeMultiple);



function enabledValueNotification(){

	var enabledValue=document.getElementById('enabled');
	enabledValue.value = ( $("#enabled").is(':checked') ) ? true : false;
}

$(function () {
    $('#element_type').on('click', function () {
        var text = $('#message-content');
        text.val(text.val() + '{element}');    
    });
    $('#element_id').on('click', function () {
        var text = $('#message-content');
        text.val(text.val() + '{element_id}');    
    });
    $('#element_name').on('click', function () {
        var text = $('#message-content');
        text.val(text.val() + '{element_name}');    
    });
    $('#element_column').on('click', function () {
        var text = $('#message-content');
        text.val(text.val() + '{element_column}');    
    });
    $('#element_value').on('click', function () {
        var text = $('#message-content');
        text.val(text.val() + '{element_value}');    
    });
    $('#notification_name').on('click', function () {
        var text = $('#notification-content');
        text.val(text.val() + '{notificaion_name}');    
    });
    $('#notification_text').on('click', function () {
        var text = $('#notification-content');
        text.val(text.val() + '{notificaion_text}');    
    });
});

    
    jQuery('a.edit_notif').click(function(event){
    	var index=this.id
    	
    	  $(function() { 
    	    		
    	    $('.edit_element_type').on('click', function () {
    	        var text = $('#edit_message-content_'+index);
    	        text.val(text.val() + '{element}');    
    	    });
    	    $('.edit_element_id').on('click', function () {
    	        var text = $('#edit_message-content_'+index);
    	        text.val(text.val() + '{element_id}');    
    	    });
    	    $('.edit_element_name').on('click', function () {
    	        var text = $('#edit_message-content_'+index);
    	        text.val(text.val() + '{element_name}');    
    	    });
    	    $('.edit_element_column').on('click', function () {
    	        var text = $('#edit_message-content_'+index);
    	        text.val(text.val() + '{element_column}');    
    	    });
    	    $('.edit_element_value').on('click', function () {
    	        var text = $('#edit_message-content_'+index);
    	        text.val(text.val() + '{element_value}');    
    	    });    	
    	});    	
    })
    

      
$(function() {

	$('#new_sub').multiselect({
	includeSelectAllOption: true
	});
	
	$('.edit_sub').multiselect({
		includeSelectAllOption: true,
		//enableFiltering: true
	});
	
		
	$("button.add_sub").click(function() { 
		var index=this.id
		id++
	    var user = $("#subscriber_"+index).val()
	    var table=document.getElementById("sub_table_"+index)
	   for(var i=0;i<table.rows.length;i++){
	    var t=document.getElementsByClassName("users")[i].id
	    console.log(t)
	   }
	    var id=table.rows.length
	    var new_row = (`<tr id="row_`+ index +`_`+ t + `">
	    				  <td><input type="checkbox"></td>
          		 	 	  <td>User</td>
          		 	 	  <input type="hidden" id="subscribers_`+ index +`_`+ t + `" name="subscribers">
          		 	 	  <td id="sub_`+ index +`_`+ t +`">`+user+`</td>
          		 	 	</tr>`)
	    $("table#sub_table_"+index).append(new_row);
	    return false;  
	   
	 }); 
	  
  	  $("button.delete_sub").click(function() {
 		index=this.id
 		var table=document.getElementById("sub_table_"+index)
 		var i=table.rows.length
	   // document.getElementById("row_"+index+"_1").remove();
 		for(var j=0; j<i; j++) {
			var row = table.rows[j];
			var chkbox = row.cells[0].childNodes[0];
			if( chkbox != null && chkbox.checked == true) {
				table.deleteRow(j);
				i--; j--;
			}
		}
 		return false;
	  });
  	  
  	 $(".form_notif").submit(function(event){
   		var index=this.id;
 	  	var table=document.getElementById("sub_table_"+index)
   		for (var id=1;id<=table.rows.length;id++){
	   	  var subsr=document.getElementById("sub_"+index).innerHTML
	      var d=document.getElementById("subscribers_"+index)
	   	  d.value=subsr
   		}	 
  });
	});
   
    $('.multiselect').on('click', function() {
    var ide = this.title;
    var newTitle = new Array()
    var i=ide.split(",").join("")
    newTitle.push(i)
    console.log(newTitle)
});  
    $(document).ready(function() {
    $('.multiselectsearch').fSelect();
    });
