/*$(function() {
        $('#devices').change(function(){
            $('.devices').hide();
            $('#' + $(this).val()).show();
        });
        alert('chihaja');
    });


    jQuery(function(){
    jQuery('a.add-choice').click(function(event){
        event.preventDefault();
        var newRow = jQuery(`
                                     <Select id="devices">
                                     <option value="0" selected>--choose from here--</option>
  								     <option value="localisation">locations</option>
  									 <option value="group">group</option>
   									 <option value="deviceClass">device class</option>
									 </Select>
									 <div id="localisation" class="devices" style="display:none"> 
									 <Select id="localisation">
									<option value="1" selected>--choose from here--</option>
									 
									   {% for obj in localisation.locations %}                                       
                                       <option id="{{obj.id}}" value="localisationFilter">{{obj.name}}</option>
                                       {% endfor %} 
                                     </Select>
                                     <label>filter</label>
                                     <input type="text" name="localisationFilter">
                                     </div>
                                      
                                       
									 <div id="deviceClass" class="devices" style="display:none"> 
									 <Select id="deviceclass">
                                     <option value="2" selected>--choose from here--</option>
                                       {% for obj in deviceClass.deviceClasses %}
                                       
                                       <option id="{{obj.id}}">{{obj.name}}</option>
                                       {% endfor %} 
                                       </Select>
                                       <label>filter</label>
                                       <input type="text" name="deviceClassFilter">
                                       </div>
									 
									 
									 <div id="group" class="devices" style="display:none">
									 
									 <Select id="group">
									<option value="3" selected>--choose from here--</option>
									 
									   {% for obj in group.groups %}                                       
                                       <option id="{{obj.id}}">{{obj.name}}</option>
                                       {% endfor %} 
                                     </Select>
                                     <label>filter</label>
                                     <input type="text" name="groupFilter">
									 </div>
									 `);
        jQuery('div.choosenDevice').append(newRow);
    });
});

    jQuery(function(){
    jQuery('a.add-choice1').click(function(event){
        event.preventDefault();
        var newRow1 = jQuery('<tr><td><select  class="form-control" id="choosen_category1" style="height:50px; width:200px; text-align:center;" name="choosen_category1" ><option value="0" selected>--choose from here--</option><option value="30" >localisation</option><option value="31">device class</option><option value="32">group</option></select></td><td><select class="form-control" id="choices1" name="choices1" style="height:50px; width:200px; text-align:center;" ><option>--choose a device class--</option><option>choice1</option><option>choice2</option><option>choice3</option></select></td><td><input type="text" name="filter1" style="height:50px; width:200px; text-align:center;" /></td></tr>');
        jQuery('table.choice-list1').append(newRow1);
    });
});




*/




$(function() {
    $('#hostsListing').change(function(){
        $('.hostsListing').hide();
        alert((this).val());
        $('#' + $(this).val()).show();
    });
});


