
	
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
    
    $('#device_table').DataTable({
        "columnDefs": [
            {
                "targets": [ 5 ],
                "searchable": false,
                
            }, 
        ]
    });
		function showHideBoolean() {this.addEventListener("click", function(){
        	var test = this.value;
            if (test == 'true') {
              $("#" + this.id + '-div').show();
              }
            else {
              $("#" + this.id + '-div').hide();
            }
	})
		}
$("input[name='use_enable_password']").each(showHideBoolean);
}

$(document).ready(function() {
	
$('#notification_table').DataTable({
    "columnDefs": [
        {
            "targets": [ 4 ],
            "searchable": false
        }, 
    ]
})


} );



function new_device(Url)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "POST", "?"+ Url +"=new", false ); // false for synchronous request
    xmlHttp.send( null );
    // var y = JSON.parse(xmlhttp.responseText);
    // var m = "{{ deviceingroup_list.devices }}";

    return (document).on('click',"#demo").innerHTML = xmlHttp.responseText;

    
}

function edit_group(Url)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "POST", "?"+ Url +"=new", false ); // false for synchronous request
    xmlHttp.send( null );
    // var y = JSON.parse(xmlhttp.responseText);
    // var m = "{{ deviceingroup_list.devices }}";

    return (document).on('click',"#demo").innerHTML = xmlHttp.responseText;

    
}
         function update(Url)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "?"+ Url +"=new", false ); // false for synchronous request
    xmlHttp.send( null );
    // var y = JSON.parse(xmlhttp.responseText);
    // var m = "{{ deviceingroup_list.devices }}";

    return document.getElementById("demo").innerHTML = xmlHttp.responseText;

     
    
}
         $(function () {
        	    // 6 create an instance when the DOM is ready
        	    $('#jstree').jstree({
        	    	"types" : {
        	    	      "default" : {
        	    	        "icon" : "glyphicon glyphicon-share-alt"
        	    	      },
        	    	      "group" : {
        	    	        "icon" : "glyphicon glyphicon-th"
        	    	      },
        	    	      "location" : {
          	    	        "icon" : "glyphicon glyphicon-map-marker"
          	    	      },
          	    	    "deviceClass" : {
        	    	        "icon" : "glyphicon glyphicon-tasks"
        	    	      },
        	    	    },
        	    	    "core" : {
      	    	          "check_callback" : true
      	    	        },
      	    	      "themes":{
      	                "icons":false
      	            },
        	        "theme" : { "icons": false },
        	        
        	        "plugins": ["ui", "themes", "theme", "wholerow", "types", "search", "dnd"]
        	    });
        	    var to = false;
        	    $('#search_tree').keyup(function () {
        	        if(to) { clearTimeout(to); }
        	        to = setTimeout(function () {
        	          var v = $('#search_tree').val();
        	          $('#jstree').jstree(true).search(v);
        	        }, 250);
        	      });
        	   
        	    // 7 bind to events triggered on the tree
        	    $('#jstree').on("changed.jstree", function (e, data) {
        	      console.log(data.selected);
        	    });
        	    // 8 interact with the tree - either way is OK
        	    
        	  });
         
         function changeClass() {
        	    $('#dashboard').addClass('active');
        	}
         
         
         $.fn.dataTable.pipeline = function ( opts ) {
        	    // Configuration options
        	    var conf = $.extend( {
        	        pages: 5,     // number of pages to cache
        	        url: '',      // script url
        	        data: null,   // function or object with parameters to send to the server
        	                      // matching how `ajax.data` works in DataTables
        	        method: 'GET' // Ajax HTTP method
        	    }, opts );
        	 
        	    // Private variables for storing the cache
        	    var cacheLower = -1;
        	    var cacheUpper = null;
        	    var cacheLastRequest = null;
        	    var cacheLastJson = null;
        	 
        	    return function ( request, drawCallback, settings ) {
        	        var ajax          = false;
        	        var requestStart  = request.start;
        	        var drawStart     = request.start;
        	        var requestLength = request.length;
        	        var requestEnd    = requestStart + requestLength;
        	         
        	        if ( settings.clearCache ) {
        	            // API requested that the cache be cleared
        	            ajax = true;
        	            settings.clearCache = false;
        	        }
        	        else if ( cacheLower < 0 || requestStart < cacheLower || requestEnd > cacheUpper ) {
        	            // outside cached data - need to make a request
        	            ajax = true;
        	        }
        	        else if ( JSON.stringify( request.order )   !== JSON.stringify( cacheLastRequest.order ) ||
        	                  JSON.stringify( request.columns ) !== JSON.stringify( cacheLastRequest.columns ) ||
        	                  JSON.stringify( request.search )  !== JSON.stringify( cacheLastRequest.search )
        	        ) {
        	            // properties changed (ordering, columns, searching)
        	            ajax = true;
        	        }
        	         
        	        // Store the request for checking next time around
        	        cacheLastRequest = $.extend( true, {}, request );
        	 
        	        if ( ajax ) {
        	            // Need data from the server
        	            if ( requestStart < cacheLower ) {
        	                requestStart = requestStart - (requestLength*(conf.pages-1));
        	 
        	                if ( requestStart < 0 ) {
        	                    requestStart = 0;
        	                }
        	            }
        	             
        	            cacheLower = requestStart;
        	            cacheUpper = requestStart + (requestLength * conf.pages);
        	 
        	            request.start = requestStart;
        	            request.length = requestLength*conf.pages;
        	 
        	            // Provide the same `data` options as DataTables.
        	            if ( $.isFunction ( conf.data ) ) {
        	                // As a function it is executed with the data object as an arg
        	                // for manipulation. If an object is returned, it is used as the
        	                // data object to submit
        	                var d = conf.data( request );
        	                if ( d ) {
        	                    $.extend( request, d );
        	                }
        	            }
        	            else if ( $.isPlainObject( conf.data ) ) {
        	                // As an object, the data given extends the default
        	                $.extend( request, conf.data );
        	            }
        	 
        	            settings.jqXHR = $.ajax( {
        	                "type":     conf.method,
        	                "url":      conf.url,
        	                "data":     request,
        	                "dataType": "json",
        	                "cache":    false,
        	                "success":  function ( json ) {
        	                    cacheLastJson = $.extend(true, {}, json);
        	 
        	                    if ( cacheLower != drawStart ) {
        	                        json.data.splice( 0, drawStart-cacheLower );
        	                    }
        	                    if ( requestLength >= -1 ) {
        	                        json.data.splice( requestLength, json.data.length );
        	                    }
        	                     
        	                    drawCallback( json );
        	                }
        	            } );
        	        }
        	        else {
        	            json = $.extend( true, {}, cacheLastJson );
        	            json.draw = request.draw; // Update the echo for each response
        	            json.data.splice( 0, requestStart-cacheLower );
        	            json.data.splice( requestLength, json.data.length );
        	 
        	            drawCallback(json);
        	        }
        	    }
        	};
        	 
        	// Register an API method that will empty the pipelined data, forcing an Ajax
        	// fetch on the next draw (i.e. `table.clearPipeline().draw()`)
        	$.fn.dataTable.Api.register( 'clearPipeline()', function () {
        	    return this.iterator( 'table', function ( settings ) {
        	        settings.clearCache = true;
        	    } );
        	} );
        	 
         $(document).ready(function() {
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
           response = document.getElementById('request_response_device')
           
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
        	      if(obj.includes('created') || obj.includes('edited') || obj.includes('deleted')){
        	        toastr.success(obj);
        	      }
        	      else if(obj == 'Unknown Error'){
        	    	  toastr.error(obj);
        	      }
        	    }
        	 }
        	 $('#device_table_all').DataTable({
        	    } );
        	});
         
         