
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

    $flowchart.siblings('.fail').click(function() {
      var operatorId = 'operator-' + operator;
      var operatorData = {
        top: 260,
        left: 1000,
        properties: {
          title: '<div  class="text-center" id="' + operatorId + '">fail</div>' ,
          inputs: {
                input_1: {
                label: ' ',}
            },
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
  
