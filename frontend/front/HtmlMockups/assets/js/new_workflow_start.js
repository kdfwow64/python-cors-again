
  $(document).ready(function() {
    // Apply the plugin on a standard, empty div...
    var $flowchart = $('#start');
    $flowchart.flowchart({
      data: start
    });
    $flowchart.siblings('.get_data').click(function() {
      var data = $flowchart.flowchart('getData');
      $('#flowchart_data').val(JSON.stringify(data, null, 2));
    });

    $flowchart.siblings('.starting').click(function() {
      var operatorId = 'operator-' + operator;
      var operatorData = {
        top: 200,
        left: 0,
        properties: {
          title: '<div  class="text-center" id="' + operatorId + '">start</div>' ,
          outputs: {
            success: {
              label: ' success ',}
           

          }
        }
      };


      $('#start').flowchart('createOperator', operatorId, operatorData);
       operator++;
    });
    
    $flowchart.siblings('.delete_selected_button').click(function() {
      $flowchart.flowchart('deleteSelected');
    });
    
    $flowchart.siblings('.get_data').click(function() {
      var data = $flowchart.flowchart('getData');
      $('#flowchart_data').val(JSON.stringify(data, null, 2));
    });

  });
  
