
function popUp(){

  $('[class*=popup-link]').click(function(e) {
  
    /* Prevent default actions */
    e.preventDefault();
    e.stopPropagation();
    
    /* Get the id (the number appended to the end of the classes) */
    var name = $(this).attr('class');
    var id = name[name.length - 1];
    var scrollPos = $(window).scrollTop();
    
    /* Show the correct popup box, show the blackout and disable scrolling */
    $('#popup-box-'+id).show();
    $('#blackout').show();
    $('html,body').css('overflow', 'hidden');
    
    /* Fixes a bug in Firefox */
    $('html').scrollTop(scrollPos);
  });
  $('[class*=popup-box]').click(function(e) { 
    /* Stop the link working normally on click if it's linked to a popup */
    e.stopPropagation(); 
  });
  $('html').click(function() { 
    var scrollPos = $(window).scrollTop();
    /* Hide the popup and blackout when clicking outside the popup */
    $('[id^=popup-box-]').hide(); 
    $('#blackout').hide(); 
    $("html,body").css("overflow","auto");
    $('html').scrollTop(scrollPos);
  });
  $('.close').click(function() { 
    var scrollPos = $(window).scrollTop();
    /* Similarly, hide the popup and blackout when the user clicks close */
    $('[id^=popup-box-]').hide(); 
    $('#blackout').hide(); 
    $("html,body").css("overflow","auto");
    $('html').scrollTop(scrollPos);
  });
  }


  $(document).ready(function() {


  $('body').append('<div class="popup-box" id="popup-box-1"><div class="close">X</div><div class="top"><h2>Hi, it is demo window!</h2></div><div class="bottom">Sample content!</div></div>');
  $('body').append('<div id="blackout"></div>');
  
  var boxWidth = 400;
  

  
    function centerBox() {
    
    /* Preliminary information */
    var winWidth = $(window).width();
    var winHeight = $(document).height();
    var scrollPos = $(window).scrollTop();
    /* auto scroll bug */
    
    /* Calculate positions */
    
    var disWidth = (winWidth - boxWidth) / 2
    var disHeight = scrollPos + 150;
    
    /* Move stuff about */
    $('.popup-box').css({'width' : boxWidth+'px', 'left' : disWidth+'px', 'top' : disHeight+'px'});
    $('#blackout').css({'width' : winWidth+'px', 'height' : winHeight+'px'});
  
    return false;
  }
  
  
  $(window).resize(centerBox);
  $(window).scroll(centerBox);
  centerBox();   

  popUp();
});

function popUp1(){

  $('[class*=popup1-link]').click(function(e) {
  
    /* Prevent default actions */
    e.preventDefault();
    e.stopPropagation();
    
    /* Get the id (the number appended to the end of the classes) */
    var name = $(this).attr('class');
    var id = name[name.length - 1];
    var scrollPos = $(window).scrollTop();
    
    /* Show the correct popup1 box, show the blackout and disable scrolling */
    $('#popup1-box-'+id).show();
    $('#blackout').show();
    $('html,body').css('overflow', 'hidden');
    
    /* Fixes a bug in Firefox */
    $('html').scrollTop(scrollPos);
  });
  $('[class*=popup1-box]').click(function(e) { 
    /* Stop the link working normally on click if it's linked to a popup */
    e.stopPropagation(); 
  });
  $('html').click(function() { 
    var scrollPos = $(window).scrollTop();
    /* Hide the popup and blackout when clicking outside the popup */
    $('[id^=popup1-box-]').hide(); 
    $('#blackout').hide(); 
    $("html,body").css("overflow","auto");
    $('html').scrollTop(scrollPos);
  });
  $('.close').click(function() { 
    var scrollPos = $(window).scrollTop();
    /* Similarly, hide the popup and blackout when the user clicks close */
    $('[id^=popup1-box-]').hide(); 
    $('#blackout').hide(); 
    $("html,body").css("overflow","auto");
    $('html').scrollTop(scrollPos);
  });
  }


  $(document).ready(function() {


  $('body').append('<div class="popup1-box" id="popup1-box-1"><div class="close">X</div><div class="top"><h2>Hi, this is it yahahaha!</h2></div><div class="bottom">chiiii hajaaaaa!</div></div>');
  $('body').append('<div id="blackout"></div>');
  
  var boxWidth = 400;
  

  
    function centerBox() {
    
    /* Preliminary information */
    var winWidth = $(window).width();
    var winHeight = $(document).height();
    var scrollPos = $(window).scrollTop();
    /* auto scroll bug */
    
    /* Calculate positions */
    
    var disWidth = (winWidth - boxWidth) / 2
    var disHeight = scrollPos + 150;
    
    /* Move stuff about */
    $('.popup1-box').css({'width' : boxWidth+'px', 'left' : disWidth+'px', 'top' : disHeight+'px'});
    $('#blackout').css({'width' : winWidth+'px', 'height' : winHeight+'px'});
  
    return false;
  }
  
  
  $(window).resize(centerBox);
  $(window).scroll(centerBox);
  centerBox();   

  popUp1();
});

  function popUp6(){

	  $('[class*=popup6-link]').click(function(e) {
	  
	    /* Prevent default actions */
	    e.preventDefault();
	    e.stopPropagation();
	    
	    /* Get the id (the number appended to the end of the classes) */
	    var name = $(this).attr('class');
	    var id = name[name.length - 1];
	    var scrollPos = $(window).scrollTop();
	    
	    /* Show the correct popup1 box, show the blackout and disable scrolling */
	    $('#popup6-box-'+id).show();
	    $('#blackout').show();
	    $('html,body').css('overflow', 'hidden');
	    
	    /* Fixes a bug in Firefox */
	    $('html').scrollTop(scrollPos);
	  });
	  $('[class*=popup6-box]').click(function(e) { 
	    /* Stop the link working normally on click if it's linked to a popup */
	    e.stopPropagation(); 
	  });
	  $('html').click(function() { 
	    var scrollPos = $(window).scrollTop();
	    /* Hide the popup and blackout when clicking outside the popup */
	    $('[id^=popup1-box-]').hide(); 
	    $('#blackout').hide(); 
	    $("html,body").css("overflow","auto");
	    $('html').scrollTop(scrollPos);
	  });
	  $('.close').click(function() { 
	    var scrollPos = $(window).scrollTop();
	    /* Similarly, hide the popup and blackout when the user clicks close */
	    $('[id^=popup6-box-]').hide(); 
	    $('#blackout').hide(); 
	    $("html,body").css("overflow","auto");
	    $('html').scrollTop(scrollPos);
	  });
	  }


	  $(document).ready(function() {


	  $('body').append('<div class="popup6-box" id="popup6-box-1"><div class="close">X</div><div class="top"><h2>Hi, this is it yahahaha!</h2></div><div class="bottom">chiiii hajaaaaa!</div></div>');
	  $('body').append('<div id="blackout"></div>');
	  
	  var boxWidth = 400;
	  

	  
	    function centerBox() {
	    
	    /* Preliminary information */
	    var winWidth = $(window).width();
	    var winHeight = $(document).height();
	    var scrollPos = $(window).scrollTop();
	    /* auto scroll bug */
	    
	    /* Calculate positions */
	    
	    var disWidth = (winWidth - boxWidth) / 2
	    var disHeight = scrollPos + 150;
	    
	    /* Move stuff about */
	    $('.popup6-box').css({'width' : boxWidth+'px', 'left' : disWidth+'px', 'top' : disHeight+'px'});
	    $('#blackout').css({'width' : winWidth+'px', 'height' : winHeight+'px'});
	  
	    return false;
	  }
	  
	  
	  $(window).resize(centerBox);
	  $(window).scroll(centerBox);
	  centerBox();   

	  popUp6();
	});
  
  
  function popUp2(){

  $('[class*=popup2-link]').click(function(e) {
  
    /* Prevent default actions */
    e.preventDefault();
    e.stopPropagation();
    
    /* Get the id (the number appended to the end of the classes) */
    var name = $(this).attr('class');
    var id = name[name.length - 1];
    var scrollPos = $(window).scrollTop();
    
    /* Show the correct popup2 box, show the blackout and disable scrolling */
    $('#popup2-box-'+id).show();
    $('#blackout').show();
    $('html,body').css('overflow', 'hidden');
    
    /* Fixes a bug in Firefox */
    $('html').scrollTop(scrollPos);
  });
  $('[class*=popup2-box]').click(function(e) { 
    /* Stop the link working normally on click if it's linked to a popup */
    e.stopPropagation(); 
  });
  $('html').click(function() { 
    var scrollPos = $(window).scrollTop();
    /* Hide the popup and blackout when clicking outside the popup */
    $('[id^=popup2-box-]').hide(); 
    $('#blackout').hide(); 
    $("html,body").css("overflow","auto");
    $('html').scrollTop(scrollPos);
  });
  $('.close').click(function() { 
    var scrollPos = $(window).scrollTop();
    /* Similarly, hide the popup and blackout when the user clicks close */
    $('[id^=popup2-box-]').hide(); 
    $('#blackout').hide(); 
    $("html,body").css("overflow","auto");
    $('html').scrollTop(scrollPos);
    
  });
  }


  $(document).ready(function() {


  $('body').append('<div class="popup2-box" id="popup2-box-1"><div class="close">X</div><div class="top"><h2>Hi, this is it yahahaha!</h2></div><div class="bottom">chiiii hajaaaaa!</div></div>');
  $('body').append('<div id="blackout"></div>');
  
  var boxWidth = 400;
  

  
    function centerBox() {
    
    /* Preliminary information */
    var winWidth = $(window).width();
    var winHeight = $(document).height();
    var scrollPos = $(window).scrollTop();
    /* auto scroll bug */
    
    /* Calculate positions */
    
    var disWidth = 435;
    var disHeight = scrollPos + 150;
    
    /* Move stuff about */
    $('.popup2-box').css({'width' : boxWidth+'px', 'left' : disWidth+'px', 'top' : disHeight+'px'});
    $('#blackout').css({'width' : winWidth+'px', 'height' : winHeight+'px'});
  
    return false;
  }
  
  
  $(window).resize(centerBox);
  $(window).scroll(centerBox);
  centerBox();   

  popUp2();
});

function popUp3(){

  $('[class*=popup3-link]').click(function(e) {
  
    /* Prevent default actions */
    e.preventDefault();
    e.stopPropagation();
    
    /* Get the id (the number appended to the end of the classes) */
    var name = $(this).attr('class');
    var id = name[name.length - 1];
    var scrollPos = $(window).scrollTop();
    
    /* Show the correct popup box, show the blackout and disable scrolling */
    $('#popup3-box-'+id).show();
    $('#blackout').show();
    $('html,body').css('overflow', 'hidden');
    
    /* Fixes a bug in Firefox */
    $('html').scrollTop(scrollPos);
  });
  $('[class*=popup3-box]').click(function(e) { 
    /* Stop the link working normally on click if it's linked to a popup */
    e.stopPropagation(); 
  });
  $('html').click(function() { 
    var scrollPos = $(window).scrollTop();
    /* Hide the popup and blackout when clicking outside the popup */
    $('[id^=popup3-box-]').hide(); 
    $('#blackout').hide(); 
    $("html,body").css("overflow","auto");
    $('html').scrollTop(scrollPos);
  });
  $('.close').click(function() { 
    var scrollPos = $(window).scrollTop();
    /* Similarly, hide the popup and blackout when the user clicks close */
    $('[id^=popup3-box-]').hide(); 
    $('#blackout').hide(); 
    $("html,body").css("overflow","auto");
    $('html').scrollTop(scrollPos);
  });
  }



  $(document).ready(function() {


  $('body').append('<div class="popup3-box" id="popup3-box-1"><div class="close">X</div><div class="top"><h2>Hi, it is demo window!</h2></div><div class="bottom">Sample content!</div></div>');
  $('body').append('<div id="blackout"></div>');
  
  var boxWidth = 400;
  

  
    function centerBox() {
    
    /* Preliminary information */
    var winWidth = $(window).width();
    var winHeight = $(document).height();
    var scrollPos = $(window).scrollTop();
    /* auto scroll bug */
    
    /* Calculate positions */
    
    var disWidth = (winWidth - boxWidth) / 2
    var disHeight = scrollPos + 150;
    
    /* Move stuff about */
    $('.popup3-box').css({'width' : boxWidth+'px', 'left' : disWidth+'px', 'top' : disHeight+'px'});
    $('#blackout').css({'width' : winWidth+'px', 'height' : winHeight+'px'});
  
    return false;
  }
  
  
  $(window).resize(centerBox);
  $(window).scroll(centerBox);
  centerBox();   

  popUp3();
});

function popUp4(){

  $('[class*=popup4-link]').click(function(e) {
  
    /* Prevent default actions */
    e.preventDefault();
    e.stopPropagation();
    
    /* Get the id (the number appended to the end of the classes) */
    var name = $(this).attr('class');
    var id = name[name.length - 1];
    var scrollPos = $(window).scrollTop();
    
    /* Show the correct popup box, show the blackout and disable scrolling */
    $('#popup4-box-'+id).show();
    $('#blackout').show();
    $('html,body').css('overflow', 'hidden');
    
    /* Fixes a bug in Firefox */
    $('html').scrollTop(scrollPos);
  });
  $('[class*=popup4-box]').click(function(e) { 
    /* Stop the link working normally on click if it's linked to a popup */
    e.stopPropagation(); 
  });
  $('html').click(function() { 
    var scrollPos = $(window).scrollTop();
    /* Hide the popup and blackout when clicking outside the popup */
    $('[id^=popup4-box-]').hide(); 
    $('#blackout').hide(); 
    $("html,body").css("overflow","auto");
    $('html').scrollTop(scrollPos);
  });
  $('.close').click(function() { 
    var scrollPos = $(window).scrollTop();
    /* Similarly, hide the popup and blackout when the user clicks close */
    $('[id^=popup4-box-]').hide(); 
    $('#blackout').hide(); 
    $("html,body").css("overflow","auto");
    $('html').scrollTop(scrollPos);
  });
  }


  $(document).ready(function() {


  $('body').append('<div class="popup4-box" id="popup4-box-1"><div class="close">X</div><div class="top"><h2>Hi, it is demo window!</h2></div><div class="bottom">Sample content!</div></div>');
  $('body').append('<div id="blackout"></div>');
  
  var boxWidth = 400;
  

  
    function centerBox() {
    
    /* Preliminary information */
    var winWidth = $(window).width();
    var winHeight = $(document).height();
    var scrollPos = $(window).scrollTop();
    /* auto scroll bug */
    
    /* Calculate positions */
    
    var disWidth = (winWidth - boxWidth) / 2
    var disHeight = scrollPos + 150;
    
    /* Move stuff about */
    $('.popup4-box').css({'width' : boxWidth+'px', 'left' : disWidth+'px', 'top' : disHeight+'px'});
    $('#blackout').css({'width' : winWidth+'px', 'height' : winHeight+'px'});
  
    return false;
  }
  
  
  $(window).resize(centerBox);
  $(window).scroll(centerBox);
  centerBox();   

  popUp4();
});

function popUp5(){

  $('[class*=popup5-link]').click(function(e) {
  
    /* Prevent default actions */
    e.preventDefault();
    e.stopPropagation();
    
    /* Get the id (the number appended to the end of the classes) */
    var name = $(this).attr('class');
    var id = name[name.length - 1];
    var scrollPos = $(window).scrollTop();
    
    /* Show the correct popup box, show the blackout and disable scrolling */
    $('#popup5-box-'+id).show();
    $('#blackout').show();
    $('html,body').css('overflow', 'hidden');
    
    /* Fixes a bug in Firefox */
    $('html').scrollTop(scrollPos);
  });
  $('[class*=popup5-box]').click(function(e) { 
    /* Stop the link working normally on click if it's linked to a popup */
    e.stopPropagation(); 
  });
  $('html').click(function() { 
    var scrollPos = $(window).scrollTop();
    /* Hide the popup and blackout when clicking outside the popup */
    $('[id^=popup5-box-]').hide(); 
    $('#blackout').hide(); 
    $("html,body").css("overflow","auto");
    $('html').scrollTop(scrollPos);
  });
  $('.close').click(function() { 
    var scrollPos = $(window).scrollTop();
    /* Similarly, hide the popup and blackout when the user clicks close */
    $('[id^=popup5-box-]').hide(); 
    $('#blackout').hide(); 
    $("html,body").css("overflow","auto");
    $('html').scrollTop(scrollPos);
  });
  }


  $(document).ready(function() {


  $('body').append('<div class="popup5-box" id="popup5-box-1"><div class="close">X</div><div class="top"><h2>Hi, it is demo window!</h2></div><div class="bottom">Sample content!</div></div>');
  $('body').append('<div id="blackout"></div>');
  
  var boxWidth = 400;
  

  
    function centerBox() {
    
    /* Preliminary information */
    var winWidth = $(window).width();
    var winHeight = $(document).height();
    var scrollPos = $(window).scrollTop();
    /* auto scroll bug */
    
    /* Calculate positions */
    
    var disWidth = (winWidth - boxWidth) / 2
    var disHeight = scrollPos + 150;
    
    /* Move stuff about */
    $('.popup5-box').css({'width' : boxWidth+'px', 'left' : disWidth+'px', 'top' : disHeight+'px'});
    $('#blackout').css({'width' : winWidth+'px', 'height' : winHeight+'px'});
  
    return false;
  }
  
  
  $(window).resize(centerBox);
  $(window).scroll(centerBox);
  centerBox();   

  popUp5();
});


  $(document).ready(function() {
    var start = {
      operators: {
        Start: {
          top: 0,
          left: 0,
          properties: {
            title: 'Start',            
            outputs: {
              output_1: {
                label: '',}
            }
          },
        },
      }
    };

    // Apply the plugin on a standard, empty div...
    var $flowchart = $('#start');
    $flowchart.flowchart({
      data: start
    });
    
    var differ_precheck = 0;
    $flowchart.siblings('.differ_precheck').click(function() {
      var operatorId = 'created_operator_' + differ_precheck;
      var operatorData = {
        top: 60,
        left: 500,
        properties: {
          title: '<a href=""  class="popup-link-1">differ precheck</a>' ,
          inputs: {
            input_1: {
              label: ' ',},
            input_2: {
              label: ' ',}
          },
          outputs: {
            output_1: {
              label: ' succeed ',},
            output_2: {
              label: 'failed',
            }

          }
        }
      };

      differ_precheck++;

      $('#start').flowchart('createOperator', operatorId, operatorData);
      popUp();  
    });
    
    $flowchart.siblings('.delete_selected_button').click(function() {
      $flowchart.flowchart('deleteSelected');
    });
    
    $flowchart.siblings('.get_data').click(function() {
      var data = $flowchart.flowchart('getData');
      $('#flowchart_data').val(JSON.stringify(data, null, 2));
    });
    
    var differ_postcheck = 0;
    $flowchart.siblings('.differ_postcheck').click(function() {
      var operatorId = 'created_operator_' + differ_postcheck;
      var operatorData = {
        top: 60,
        left: 500,
        properties: {
          title: '<a href=""  class="popup1-link-1">differ postcheck</a>' ,
          inputs: {
            input_1: {
              label: ' ',},
            input_2: {
              label: ' ',}
          },
          outputs: {
            output_1: {
              label: ' succeed ',},
            output_2: {
              label: 'failed',
            }

          }
        }
      };

      differ_postcheck--;

      $('#start').flowchart('createOperator', operatorId, operatorData);
      popUp1();  
    });
    
    $flowchart.siblings('.delete_selected_button').click(function() {
      $flowchart.flowchart('deleteSelected');
    });
    
    $flowchart.siblings('.get_data').click(function() {
      var data = $flowchart.flowchart('getData');
      $('#flowchart_data').val(JSON.stringify(data, null, 2));
    });
    var configuration_parser = 0;
    $flowchart.siblings('.configuration_parser').click(function() {
      var operatorId = 'created_operator_' + configuration_parser;
      var operatorData = {
        top: 60,
        left: 500,
        properties: {
          title: '<a href=""  class="popup2-link-1">configuration parser</a>' ,
          inputs: {
            input_1: {
              label: ' ',},
            input_2: {
              label: ' ',}
          },
          outputs: {
            output_1: {
              label: ' succeed ',},
            output_2: {
              label: 'failed',
            }

          }
        }
      };

      configuration_parser++;

      $('#start').flowchart('createOperator', operatorId, operatorData);
      popUp2();  
    });
    
    $flowchart.siblings('.delete_selected_button').click(function() {
      $flowchart.flowchart('deleteSelected');
    });
    
    $flowchart.siblings('.get_data').click(function() {
      var data = $flowchart.flowchart('getData');
      $('#flowchart_data').val(JSON.stringify(data, null, 2));
    });
var configuration_sender = 0;
    $flowchart.siblings('.configuration_sender').click(function() {
      var operatorId = 'created_operator_' + configuration_sender;
      var operatorData = {
        top: 60,
        left: 500,
        properties: {
          title: '<a href=""  class="popup3-link-1">configuration sender</a>' ,
          inputs: {
            input_1: {
              label: ' ',},
            input_2: {
              label: ' ',}
          },
          outputs: {
            output_1: {
              label: ' succeed ',},
            output_2: {
              label: 'failed',
            }

          }
        }
      };

      configuration_sender++;

      $('#start').flowchart('createOperator', operatorId, operatorData);
      popUp3();  
    });
    
    $flowchart.siblings('.delete_selected_button').click(function() {
      $flowchart.flowchart('deleteSelected');
    });
    
    $flowchart.siblings('.get_data').click(function() {
      var data = $flowchart.flowchart('getData');
      $('#flowchart_data').val(JSON.stringify(data, null, 2));
    });

var image_loader = 0;
    $flowchart.siblings('.image_loader').click(function() {
      var operatorId = 'created_operator_' + image_loader;
      var operatorData = {
        top: 60,
        left: 500,
        properties: {
          title: '<a href=""  class="popup4-link-1">image loader</a>' ,
          inputs: {
            input_1: {
              label: ' ',},
            input_2: {
              label: ' ',}
          },
          outputs: {
            output_1: {
              label: ' succeed ',},
            output_2: {
              label: 'failed',
            }

          }
        }
      };

      image_loader++;

      $('#start').flowchart('createOperator', operatorId, operatorData);
      popUp4();  
    });
    
    $flowchart.siblings('.delete_selected_button').click(function() {
      $flowchart.flowchart('deleteSelected');
    });
    
    $flowchart.siblings('.get_data').click(function() {
      var data = $flowchart.flowchart('getData');
      $('#flowchart_data').val(JSON.stringify(data, null, 2));
    });

    var Evaluation = 0;
    $flowchart.siblings('.Evaluation').click(function() {
      var operatorId = 'created_operator_' + Evaluation;
      var operatorData = {
        top: 200,
        left: 500,
        properties: 
          title: '<a href=""  class="popup6-link-1">Evaluation</a>' ,
          inputs: {
            input_1: {
              label: ' ',},
            input_2: {
              label: ' ',}
          },
          outputs: {
            output_1: {
              label: ' succeed ',},
            output_2: {
              label: 'failed',
            }

          }
        }
      };

      Evaluation++;

      $('#start').flowchart('createOperator', operatorId, operatorData);
      popUp6();  
    });
    
    $flowchart.siblings('.delete_selected_button').click(function() {
      $flowchart.flowchart('deleteSelected');
    });
    
    $flowchart.siblings('.get_data').click(function() {
      var data = $flowchart.flowchart('getData');
      $('#flowchart_data').val(JSON.stringify(data, null, 2));
    });

var credentials = 0;
    $flowchart.siblings('.credentials').click(function() {
      var operatorId = 'created_operator_' + credentials;
      var operatorData = {
        top: 60,
        left: 500,
        properties: {
          title: '<a href=""  class="popup5-link-1">credentials</a>' ,
          inputs: {
            input_1: {
              label: ' ',},
            input_2: {
              label: ' ',}
          },
          outputs: {
            output_1: {
              label: ' succeed ',},
            output_2: {
              label: 'failed',
            }

          }
        }
      };

      credentials++;

      $('#start').flowchart('createOperator', operatorId, operatorData);
      popUp5();  
    });
    
    $flowchart.siblings('.delete_selected_button').click(function() {
      $flowchart.flowchart('deleteSelected');
    });
    
    $flowchart.siblings('.get_data').click(function() {
      var data = $flowchart.flowchart('getData');
      $('#flowchart_data').val(JSON.stringify(data, null, 2));
    });
  });