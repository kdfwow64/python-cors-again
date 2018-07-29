$(document).ready(function() {
		
	 $('#complianceexecutionlist').DataTable({
		 "order":[0, 'desc'],
		 "columnDefs": [
		   	         {
		   	             "targets": [1],
		   	             "searchable": false
		   	         }, 
		   	     ]
	 })
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
   if(obj == 'Report Executed'){
     toastr.success(obj);
   }
   else if(obj == 'Unknown Error'){
 	  toastr.error(obj);
   }
 }
 }

	 } );