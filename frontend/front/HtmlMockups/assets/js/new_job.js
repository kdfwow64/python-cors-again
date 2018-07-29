

function validationValueParser(){

	var checkedValueParser=document.getElementById('is_validated_parser');
	checkedValueParser.value = ( $("#is_validated_parser").is(':checked') ) ? true : false;
	console.log(checkedValueParser); 
}
function validationValueSender(){

	var checkedValueSender=document.getElementById('is_validated_sender');
	checkedValueSender.value = ( $("#is_validated_sender").is(':checked') ) ? true : false;
	
}
function validationValuePrecheck(){

	var checkedValuePrecheck=document.getElementById('is_validated_precheck');
	checkedValuePrecheck.value = ( $("#is_validated_precheck").is(':checked') ) ? true : false;
	
}
function validationValuePostcheck(){

	var checkedValuePostcheck=document.getElementById('is_validated_postcheck');
	checkedValuePostcheck.value = ( $("#is_validated_postcheck").is(':checked') ) ? true : false;
	
}
function validationValueLoader(){

	var checkedValueLoader=document.getElementById('is_validated_loader');
	checkedValueLoader.value = ( $("#is_validated_loader").is(':checked') ) ? true : false;
	
}

$(function() {
    $('#devices_configurationParser').change(function(){
        $('.devices_configurationParser').hide();
        $('#' + $(this).val()).show();
    });
});



$(function() {
    $('#devices_imageLoader').change(function(){
        $('.devices_imageLoader').hide();
        $('#' + $(this).val()).show();
    });
});

$(function() {
    $('#devices_differPrecheck').change(function(){
        $('.devices_differPrecheck').hide();
        $('#' + $(this).val()).show();
    });
});
$(function() {
    $('#devices_configurationSender').change(function(){
        $('.devices_configurationSender').hide();
        $('#' + $(this).val()).show();
    });
});
$(function() {
    $('#devices_configurationParser').change(function(){
        $('.devices_configurationParser').hide();
        $('#' + $(this).val()).show();
    });
});



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

$(document).ready(function() {
	function showHideBoolean() {
    	this.addEventListener("click", function(){
        	var test = this.value;
            if (test == 'true') {
              $("#" + this.id + '-div').show();
              }
            else {
              $("#" + this.id + '-div').hide();
            }
	})}

	function showHideBooleanInverted() {
    	this.addEventListener("click", function(){
        	var test = this.value;
            if (test == 'true') {
              $("#" + this.id + '-div').hide();
              }
            else {
              $("#" + this.id + '-div').show();
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
            $("#" + this.id + '-1-div').show();
            $("#" + this.id + '-2-div').hide();
            
            }
          else {
            $("#" + this.id + '-2-div').show();
            $("#" + this.id + '-1-div').hide();
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
          else if (test == 'hostFilter'){
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
	
	
	    $("input[name='use_device_credentials']").each(showHideBooleanInverted);

	    $("input[name='editUseDeviceCredentials']").each(showHideBooleanInverted);
    $("input[name='use_enable_password']").each(showHideBoolean);
    $("input[name='hostsType']").each(showHideBooleanHostType);
    $("input[name='is_scheduled']").each(showHideBoolean);
    $("input[id^='achoice']").each(showHideBooleanHostTypeMultiple);
    $("option[class='hostFiltering']").each(showHideBooleanHostList);
 });



/*
 $(document).ready(function() {
     $("input[name$='senderCredentials']").click(function() {
        var test = $(this).val();
        if (test == 'true') {
            $("#" + this.name + '-div').show();
        }
        else {
            $("#" + this.name + '-div').hide();

        }
    });

     $("input[name$='senderPassword']").click(function() {
        var test = $(this).val();
        if (test == 'true') {
            $("#" + this.name + '-div').show();
        }
        else {
            $("#" + this.name + '-div').hide();

        }
    });
  $("input[name$='senderHost']").click(function() {
        var test = $(this).val();
        if (test == '1' ) {
            $("#"  + 'choice1-div').show();
            $("#"  + 'choice2-div').hide();
            $("#"  + 'choice3-div').hide();
        }
        else if (test == '2'){
            $("#"  + 'choice1-div').hide();
            $("#"  + 'choice2-div').show();
            $("#"  + 'choice3-div').hide();

        }
        else if (test == '3'){
            $("#"  + 'choice1-div').hide();
            $("#"  + 'choice2-div').hide();
            $("#"  + 'choice3-div').show();

        }
    });
  $("input[name$='senderSchedule']").click(function() {
        var test = $(this).val();
        if (test == 'true') {
            $("#" + this.name + '-div').show();
        }
        else {
            $("#" + this.name + '-div').hide();

        }
    });

});

    $(document).ready(function() {
     $("input[name$='loaderCredentials']").click(function() {
        var test = $(this).val();
        if (test == 'true') {
            $("#" + this.name + '-div').show();
        }
        else {
            $("#" + this.name + '-div').hide();

        }
    });

     $("input[name$='loaderPassword']").click(function() {
        var test = $(this).val();
        if (test == 'true') {
            $("#" + this.name + '-div').show();
        }
        else {
            $("#" + this.name + '-div').hide();

        }
    });
  $("input[name$='loaderHost']").click(function() {
        var test = $(this).val();
        if (test == 'true' ) {
            $("#"  + 'hostFile1-div').show();
            $("#"  + 'hostList1-div').hide();
        }
        else if (test == 'false'){
            $("#"  + 'hostFile1-div').hide();
            $("#"  + 'hostList1-div').show();

        }
    });
  $("input[name$='loaderSchedulechedule']").click(function() {
        var test = $(this).val();
        if (test == 'true') {
            $("#" + this.name + '-div').show();
        }
        else {
            $("#" + this.name + '-div').hide();

        }
    });

});

$(document).ready(function() {
     $("input[name$='parserCredentials']").click(function() {
        var test = $(this).val();
        if (test == 'true') {
            $("#" + this.name + '-div').show();
        }
        else {
            $("#" + this.name + '-div').hide();

        }
    });

     $("input[name$='parserPassword']").click(function() {
        var test = $(this).val();
        if (test == 'true') {
            $("#" + this.name + '-div').show();
        }
        else {
            $("#" + this.name + '-div').hide();

        }
    });
  $("input[name$='parserHost']").click(function() {
        var test = $(this).val();
        if (test == 'true' ) {
            $("#"  + 'hostFile2-div').show();
            $("#"  + 'hostList2-div').hide();
        }
        else if (test == 'false'){
            $("#"  + 'hostFile2-div').hide();
            $("#"  + 'hostList2-div').show();

        }
    });
  $("input[name$='parserSchedule']").click(function() {
        var test = $(this).val();
        if (test == 'true') {
            $("#" + this.name + '-div').show();
        }
        else {
            $("#" + this.name + '-div').hide();

        }
    });

});
*/


