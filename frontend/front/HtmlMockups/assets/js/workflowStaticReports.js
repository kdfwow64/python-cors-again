

$(document).ready(function() {
var job_list=document.getElementById('job_list').value;
var eval_list=document.getElementById('eval_list').value;
var link_list=document.getElementById('link_list').value;
var first_job=document.getElementById('first_job').value;
var workflow_id=document.getElementById('workflow_id').value;

var myJobJSON=JSON.parse(job_list);
var myEvalJSON=JSON.parse(eval_list);
var myLinkJSON=JSON.parse(link_list);

var position=100;
data = {operators:{
			start:{
				top: 50,
		    left: 200 + position,
		    properties: {
		      title: 'start',
		      inputs: {
			
		      },
		      outputs: {
			  start:{
				  label:"",
			  }
		      }
		  }
			}
},
	links:{
		start_link:{
		      fromOperator: 'start',
		      fromConnector: 'start',
		      toOperator: "operator_"+first_job,
		      toConnector: "input_"+first_job,
		    }
	}}


agents= {configuration_sender: "Sender",
	configuration_parser: "Praser",
	configuration_differ_precheck: "precheck",
	configuration_differ_postcheck: "postcheck",
	configuration_image_loader: "loader",
}


for(job in myJobJSON){
operator = "operator_"+myJobJSON[job]["id"].toString();
input = "input_" + myJobJSON[job]["id"].toString();
output1 = "output1_" + myJobJSON[job]["id"].toString();
output2 = "output2_" + myJobJSON[job]["id"].toString();
data['operators'][operator] = {
	    top: 180,
	    left: 1100 + position,
	    properties: {
	      title: '<span title="'+ myJobJSON[job]["status"].toString()+'" id="dot_status_'+ myJobJSON[job]["id"].toString() +'" class="glyphicon workflow-dot-status-'+ myJobJSON[job]["status"].toString().toLowerCase()+'"></span><a href="http://'+window.location.host.split(':')[0]+':80/reports/tasks/?job_id='+ myJobJSON[job]["id"].toString() +'"><p title="name: '+ myJobJSON[job]["name"].toString()+'" style="margin: -21px 36px 7.5px">'+agents[myJobJSON[job]["agent_type"]].toString()+'<p></a>',
	              inputs: {
	                
	              },
	              outputs: {
	              }
	          }
	          
	      	  }
	data['operators'][operator]['properties']['inputs'][input] = {
        label: "",
    }
	data['operators'][operator]['properties']['outputs'][output1] = {
            label:'success',
    }
	data['operators'][operator]['properties']['outputs'][output2] = {
            label:'fail',
    }
	position += -180;
}

for(eval in myEvalJSON){
	operator = "operator_"+myEvalJSON[eval]["id"].toString();
	input = "input_" + myEvalJSON[eval]["id"].toString();
	output1 = "output1_" + myEvalJSON[eval]["id"].toString();
	output2 = "output2_" + myEvalJSON[eval]["id"].toString();
	data['operators'][operator] = {
	            top: 400,
	            left: 1800 + position,
	            properties: {
	              title: '<span title="'+ myEvalJSON[eval]["status"].toString()+'" id="dot_status_'+ myEvalJSON[eval]["id"].toString() +'" class="glyphicon workflow-dot-status-'+ myEvalJSON[eval]["status"].toString().toLowerCase()+'"></span><p style="margin: -21px 36px 7.5px">'+myEvalJSON[eval]["name"].toString()+'<p>',
	              inputs: {
	                
	              },
	              outputs: {
	              }
	          }
	          
	}
	data['operators'][operator]['properties']['inputs'][input] = {
        label: "",
    }
	data['operators'][operator]['properties']['outputs'][output1] = {
            label: "success",
    }
	data['operators'][operator]['properties']['outputs'][output2] = {
            label: "fail",
    }
	position += -300;
}

for (link in myLinkJSON){
	_link = "link_"+link;
	if (myLinkJSON[link]['link_type'] == "SUCCESSFUL"){
	data['links'][_link] = {
	      fromOperator: 'operator_'+myLinkJSON[link]['src_node']['uid'],
	      fromConnector: 'output1_'+myLinkJSON[link]['src_node']['uid'],
	      toOperator: 'operator_'+myLinkJSON[link]['dst_node']['uid'],
	      toConnector: 'input_'+myLinkJSON[link]['dst_node']['uid'],
	      color: 'green',
	    }
}
	else{
		data['links'][_link] = {
			      fromOperator: 'operator_'+myLinkJSON[link]['src_node']['uid'],
			      fromConnector: 'output2_'+myLinkJSON[link]['src_node']['uid'],
			      toOperator: 'operator_'+myLinkJSON[link]['dst_node']['uid'],
			      toConnector: 'input_'+myLinkJSON[link]['dst_node']['uid'],
			      color: 'red',
			    }
		}
	}
    


    // Apply the plugin on a standard, empty div...
    $('#example_3').flowchart({
      data: data,
    });
    var $flowchart = $('#example_3');
    var $container = $flowchart.parent();    
    var cx = $flowchart.width() / 2;
    var cy = $flowchart.height() / 2;
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
  /*function setLinkColor(linkId, linkData) {
	  console.log(linkData);
    if (linkData.fromConnector == 'failure') {
      linkData.color = 'red';
    }
    else
        linkData.color = 'green';
    return true;
  }*/
function refresh(){
	  var current_url = window.location.host
	  $.getJSON("http://" +window.location.host.split(':')[0] +":5000/job?workflow_id="+workflow_id,
			   function(data) {
		  var arrayLength = data['jobs'].length;

		
		  var array = data['jobs']

		  for (var i = 0; i < arrayLength; i++)
	      {
			  $("#dot_status_" + data['jobs'][i].id).attr('class', 'glyphicon workflow-dot-status-' + data['jobs'][i].status.toLowerCase());
			  $("#dot_status_" + data['jobs'][i].id).attr('title',  data['jobs'][i].status.toLowerCase());

			  //document.getElementById("duration_" + data['tasks'][i].id).value = duration;
			  //document.getElementById("dot_status_" + data['tasks'][i].id).className = "glyphicon dot-status-" + data['tasks'][i].status.toLowerCase();
			  //document.getElementById("dot_status_" + data['tasks'][i].id).title = data['tasks'][i].status; 

		  }
		
		  
			   });
	  $.getJSON("http://" +window.location.host.split(':')[0] +":5000/eval?workflow_id="+workflow_id,
			   function(data) {
		  var evalArrayLength= data['evals'].length;
		  var evalArray=data['evals']

	  for (var i = 0; i < evalArrayLength; i++)
      {
		  $("#dot_status_" + data['evals'][i].id).attr('class', 'glyphicon workflow-dot-status-' + data['evals'][i].status.toLowerCase());
		  $("#dot_status_" + data['evals'][i].id).attr('title',  data['evals'][i].status.toLowerCase());

		  //document.getElementById("duration_" + data['tasks'][i].id).value = duration;
		  //document.getElementById("dot_status_" + data['tasks'][i].id).className = "glyphicon dot-status-" + data['tasks'][i].status.toLowerCase();
		  //document.getElementById("dot_status_" + data['tasks'][i].id).title = data['tasks'][i].status; 

	  }
		  });
	 
	  }
	  
	      window.setInterval(function(){
	    	  refresh()
	    	  },3000);
	      
  });
