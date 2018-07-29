function httpGet(Url, type)
{
	var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "?"+ Url +"=true", false ); // false for synchronous request
    xmlHttp.send( null );
    // var y = JSON.parse(xmlhttp.responseText);
    // var m = "{{ deviceingroup_list.devices }}";0
    document.getElementById("demo").innerHTML = xmlHttp.responseText;
    document.getElementById("delete_confirmation_text").innerHTML = "Are you sure you want to delete : " + Url; 
    var delete_tree = document.getElementById("delete_tree_element");
    delete_tree.value = Url;
    var edit_tree = document.getElementById("edit_tree_element");
    edit_tree.value = Url;
    var type_of_tree_element_delete = document.getElementById("tree_type_delete");
    type_of_tree_element_delete.value = type;
    var type_of_tree_element_edit = document.getElementById("tree_type_edit");
    type_of_tree_element_edit.value = type;
   
}