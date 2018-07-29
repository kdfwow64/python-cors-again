
$(document).ready(function() {
    	

    	   $('#workflowReports_table').DataTable({
    	        "pagingType": "full_numbers",
    	        "order":[3, 'desc'],
    	        "columnDefs": [
    	            {
    	                "searchable": false
    	            }, 
    	        ]
    	    });

    } );